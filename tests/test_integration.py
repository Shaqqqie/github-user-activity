import json
import sys
from unittest.mock import MagicMock, patch

from github_activity.__main__ import main


def test_integration_success(capsys) -> None:
    event = [
        {
            "type": "WatchEvent",
            "repo": {"name": "alice/project"},
            "payload": {"action": "started"},
        }
    ]

    json_data = json.dumps(event).encode("utf-8")

    mock_response = MagicMock()
    mock_response.read.return_value = json_data

    with (
        patch.object(sys, "argv", ["github_activity", "alice"]),
        patch("github_activity.client.urlopen") as mock_urlopen,
    ):
        mock_urlopen.return_value.__enter__.return_value = mock_response

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Fetching activity for user: alice" in captured.out
    assert "Starred alice/project" in captured.out
    assert captured.err == ""

    mock_urlopen.assert_called_once_with(
        "https://api.github.com/users/alice/events/public", timeout=10
    )


def test_integration_invalid_event(capsys) -> None:
    event = [{"type": "PushEvent"}, "invalid event"]

    json_data = json.dumps(event).encode("utf-8")

    mock_response = MagicMock()
    mock_response.read.return_value = json_data

    with (
        patch.object(sys, "argv", ["github_activity", "alice"]),
        patch("github_activity.client.urlopen") as mock_urlopen,
    ):
        mock_urlopen.return_value.__enter__.return_value = mock_response

        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert (
        "Error: Invalid GitHub API response: Expected event data to be of type dict"
    ) in captured.err

    assert "Traceback" not in captured.err

    mock_urlopen.assert_called_once_with(
        "https://api.github.com/users/alice/events/public", timeout=10
    )
