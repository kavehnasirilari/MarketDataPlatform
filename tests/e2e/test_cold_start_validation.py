import subprocess
import time

import pytest
import requests


PROJECT_NAME = "mdp_cold_test"
BASE_URL = "http://localhost:8000"


pytestmark = pytest.mark.skip(
    reason=(
        "Cold start validation is not enabled yet. "
        "It requires isolated Docker project execution, "
        "database bootstrap/migration support, and reliable image availability."
    )
)


def run_command(command: list[str], timeout: int = 180):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    assert result.returncode == 0, (
        f"Command failed: {' '.join(command)}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    return result


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

    raise AssertionError(
        f"Endpoint not ready after {timeout_seconds}s: {url}. Last error: {last_error}"
    )


def test_clean_environment_cold_start():
    run_command(["docker", "compose", "-p", PROJECT_NAME, "down", "-v"], timeout=120)

    run_command(["docker", "compose", "-p", PROJECT_NAME, "up", "-d"], timeout=240)

    response = wait_for_endpoint(f"{BASE_URL}/metadata")

    body = response.json()

    assert body["type"] == "success"
    assert body["data"] is not None
    assert "exchanges" in body["data"]