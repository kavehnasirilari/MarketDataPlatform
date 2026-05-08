from pathlib import Path


def test_required_project_directories_exist():
    root = Path(__file__).resolve().parents[2]

    assert (root / "api_service").exists()
    assert (root / "syncer_service").exists()
    assert (root / "database").exists()
    assert (root / "tests").exists()
    