import json
import sys
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from github_activity.__main__ import main


def test_cli_user_not_found(capsys) -> None:
    error = HTTPError(
        url="https://api.github.com", code=404, msg="Not Found", hdrs=None, fp=None
    )

    with (
        patch.object(sys, "argv", ["github_activity", "nonexistent-user"]),
        patch("github_activity.__main__.fetch_user_activity") as mock_fetch,
    ):
        mock_fetch.side_effect = error

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: GitHub user not found." in captured.err
    mock_fetch.assert_called_once_with("nonexistent-user")


def test_cli_http_403(capsys) -> None:
    error = HTTPError(
        url="https://api.github.com", code=403, msg="Forbidden", hdrs=None, fp=None
    )

    with (
        patch.object(sys, "argv", ["github_activity", "alice"]),
        patch("github_activity.__main__.fetch_user_activity") as mock_fetch,
    ):
        mock_fetch.side_effect = error

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: GitHub API request failed (HTTP 403)." in captured.err
    mock_fetch.assert_called_once_with("alice")


def test_cli_network_error(capsys) -> None:
    error = URLError("Name or service not known")

    with (
        patch.object(sys, "argv", ["github_activity", "alice"]),
        patch("github_activity.__main__.fetch_user_activity") as mock_fetch,
    ):
        mock_fetch.side_effect = error

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert (
        "Error: Unable to connect to GitHub. Reason: Name or service not known."
        in captured.err
    )
    mock_fetch.assert_called_once_with("alice")


def test_cli_empty_activity(capsys) -> None:
    with (
        patch.object(sys, "argv", ["github_activity", "alice"]),
        patch("github_activity.__main__.fetch_user_activity") as mock_fetch,
    ):
        mock_fetch.return_value = []

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "No recent public activity found." in captured.out
    mock_fetch.assert_called_once_with("alice")


def test_cli_success(capsys) -> None:
    with (
        patch.object(sys, "argv", ["github_activity", "alice"]),
        patch("github_activity.__main__.fetch_user_activity") as mock_fetch,
    ):
        mock_fetch.return_value = [
            {
                "type": "WatchEvent",
                "repo": {"name": "alice/project"},
                "payload": {"action": "started"},
            }
        ]

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Starred alice/project" in captured.out
    assert captured.err == ""
    mock_fetch.assert_called_once_with("alice")


def test_cli_invalid_json(capsys) -> None:
    error = json.JSONDecodeError(
        msg="Expecting value",
        doc="not valid json",
        pos=0,
    )

    with (
        patch.object(sys, "argv", ["github_activity", "alice"]),
        patch("github_activity.__main__.fetch_user_activity") as mock_fetch,
    ):
        mock_fetch.side_effect = error

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: GitHub returned an invalid JSON response." in captured.err
    assert "Traceback" not in captured.err
    mock_fetch.assert_called_once_with("alice")


def test_cli_invalid_api_response(capsys) -> None:
    with (
        patch.object(sys, "argv", ["github_activity", "testuser"]),
        patch("github_activity.__main__.fetch_user_activity") as mock_fetch,
    ):
        mock_fetch.side_effect = ValueError("Expected event data to be of type dict")

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert (
        "Error: Invalid GitHub API response: Expected event data to be of type dict"
        in captured.err
    )
    assert "Traceback" not in captured.err
    mock_fetch.assert_called_once_with("testuser")


def test_cli_missing_username(capsys) -> None:
    with (
        patch.object(sys, "argv", ["github_activity"]),
        patch("github_activity.__main__.fetch_user_activity") as mock_fetch,
    ):
        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Please provide a GitHub username." in captured.err
    mock_fetch.assert_not_called()
