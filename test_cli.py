import os

from sentinelkit.cli import main

DATA = os.path.join(os.path.dirname(__file__), "..", "sample_data")


def test_logs_command_exit_code_flags_findings(capsys):
    assert main(["logs", os.path.join(DATA, "auth.log")]) == 2
    assert "Brute-force" in capsys.readouterr().out


def test_password_command_weak_returns_1(capsys):
    assert main(["password", "--password", "password"]) == 1


def test_headers_from_file(capsys):
    assert main(["headers", "--file", os.path.join(DATA, "headers.txt")]) == 2
    assert "Grade" in capsys.readouterr().out


def test_baseline_and_verify_roundtrip(tmp_path, capsys):
    (tmp_path / "x.txt").write_text("hello")
    base = str(tmp_path / "b.json")
    assert main(["baseline", str(tmp_path), "--baseline", base]) == 0
    assert main(["verify", str(tmp_path), "--baseline", base]) == 0
    (tmp_path / "x.txt").write_text("changed")
    assert main(["verify", str(tmp_path), "--baseline", base]) == 2


def test_missing_file_returns_error_code(capsys):
    assert main(["logs", "/nonexistent/auth.log"]) == 3
