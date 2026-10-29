import json
from unittest.mock import MagicMock, patch

import pytest

from github_activity.client import fetch_user_activity


def test_fetch_user_activity_success() -> None:
    events = [
        {"type": "PushEvent", "repo": {"name": "alice/project"}, "payload": {"size": 3}}
    ]

    json_data = json.dumps(events).encode("utf-8")

    mock_response = MagicMock()
    mock_response.read.return_value = json_data

    with patch("github_activity.client.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = fetch_user_activity("alice")

    assert result == events

    mock_urlopen.assert_called_once_with(
        "https://api.github.com/users/alice/events/public",
        timeout=10,
    )
    mock_response.read.assert_called_once_with()


def test_fetch_user_activity_empty() -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = b"[]"

    with patch("github_activity.client.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = fetch_user_activity("alice")

    assert result == []

    mock_urlopen.assert_called_once_with(
        "https://api.github.com/users/alice/events/public",
        timeout=10,
    )
    mock_response.read.assert_called_once_with()


def test_fetch_user_activity_invalid_json() -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = b"not valid json"

    with patch("github_activity.client.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with pytest.raises(json.JSONDecodeError):
            fetch_user_activity("alice")


def test_fetch_user_activity_invalid_structure() -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"message": "Unexpected response"}'

    with patch("github_activity.client.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with pytest.raises(ValueError, match="Expected a list of GitHub events"):
            fetch_user_activity("alice")


def test_fetch_user_activity_invalid_event() -> None:
    event = [{"type": "PushEvent"}, "invalid event"]

    json_data = json.dumps(event).encode("utf-8")

    mock_response = MagicMock()
    mock_response.read.return_value = json_data

    with patch("github_activity.client.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with pytest.raises(ValueError, match="Expected event data to be of type dict"):
            fetch_user_activity("testuser")


def test_fetch_user_activity_empty_events() -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = b"[]"

    with patch("github_activity.client.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response

        assert fetch_user_activity("testuser") == []
        mock_urlopen.assert_called_once()
