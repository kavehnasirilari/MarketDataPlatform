import subprocess
import time
import pytest
import requests

BASE_URL = "http://localhost:8000"

def wait_for_endpoint(url: str, timeout_seconds: int = 60):
    started_at = time.time()
    last_error = None

    while time.time() - started_at < timeout_seconds:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return response
        except requests.RequestException as exc:
            last_error = exc

        time.sleep(2)

    raise AssertionError(f"Endpoint not ready after {timeout_seconds}s: {url}. Last error: {last_error}")

def test_docker_compose_starts_successfully():
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0, result.stderr

def test_metadata_endpoint_is_available():
    response = wait_for_endpoint(f"{BASE_URL}/metadata")

    body = response.json()

    assert body["type"] == "success", body
    assert body["message"] is None
    assert body["data"] is not None
    assert "exchanges" in body["data"]
    assert len(body["data"]["exchanges"]) > 0

def test_candles_endpoint_is_available():
    response = wait_for_endpoint(
        f"{BASE_URL}/candles/hyperliquid/futures/ETH-USDC/1m"
    )

    body = response.json()

    assert body["type"] == "success", body
    assert body["data"] is not None
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0

def test_required_containers_are_running():
    result = subprocess.run(
        ["docker", "compose", "ps", "--format", "json"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr

    output = result.stdout

    assert "postgres" in output.lower()
    assert "api" in output.lower()
    assert "syncer" in output.lower()

def test_postgres_container_is_healthy():
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{.State.Health.Status}}", "mdp_postgres"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "healthy"

def test_api_container_is_running():
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{.State.Status}}", "mdp_api"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "running"

def test_syncer_container_completed_successfully_or_is_running():
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{.State.Status}} {{.State.ExitCode}}", "mdp_syncer"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr

    status, exit_code = result.stdout.strip().split()

    assert (
        status == "running"
        or (status == "exited" and exit_code == "0")
    )

def test_api_port_is_exposed():
    result = subprocess.run(
        ["docker", "port", "mdp_api", "8000"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    assert "0.0.0.0" in result.stdout or "127.0.0.1" in result.stdout

def test_postgres_required_tables_exist():
    result = subprocess.run(
        [
            "docker", "exec", "mdp_postgres",
            "psql",
            "-U", "mdp_user",
            "-d", "market_data",
            "-c",
            "\\dt"
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr

    output = result.stdout.lower()

    assert "exchanges" in output
    assert "canonical_symbols" in output
    assert "intervals" in output
    assert "exchange_markets" in output
    assert "supported_markets" in output
    assert "candles" in output

def test_metadata_tables_have_required_seed_data():
    result = subprocess.run(
        [
            "docker", "exec", "mdp_postgres",
            "psql",
            "-U", "mdp_user",
            "-d", "market_data",
            "-t",
            "-c",
            """
            SELECT
                (SELECT COUNT(*) FROM exchanges) AS exchanges_count,
                (SELECT COUNT(*) FROM canonical_symbols) AS symbols_count,
                (SELECT COUNT(*) FROM intervals) AS intervals_count,
                (SELECT COUNT(*) FROM exchange_markets) AS exchange_markets_count,
                (SELECT COUNT(*) FROM supported_markets) AS supported_markets_count;
            """
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr

    counts = [int(value.strip()) for value in result.stdout.strip().split("|")]

    assert counts[0] > 0
    assert counts[1] > 0
    assert counts[2] > 0
    assert counts[3] > 0
    assert counts[4] > 0    

def test_candles_table_contains_data():
    result = subprocess.run(
        [
            "docker",
            "exec",
            "mdp_postgres",
            "psql",
            "-U",
            "mdp_user",
            "-d",
            "market_data",
            "-t",
            "-c",
            "SELECT COUNT(*) FROM candles;"
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr

    candle_count = int(result.stdout.strip())

    assert candle_count > 0

def test_candles_table_contains_data():
    result = subprocess.run(
        [
            "docker",
            "exec",
            "mdp_postgres",
            "psql",
            "-U",
            "mdp_user",
            "-d",
            "market_data",
            "-t",
            "-c",
            "SELECT COUNT(*) FROM candles;"
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr

    candle_count = int(result.stdout.strip())

    assert candle_count > 0

def test_health_endpoint_is_available():
    response = requests.get(f"{BASE_URL}/health", timeout=10)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)



