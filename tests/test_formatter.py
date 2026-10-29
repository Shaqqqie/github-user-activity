from github_activity.formatter import format_event


def test_format_push_event() -> None:
    event = {
        "type": "PushEvent",
        "repo": {"name": "alice/project"},
        "payload": {"size": 3},
    }

    result = format_event(event)

    assert result == "Pushed 3 commits to alice/project"


def test_format_issues_event() -> None:
    event = {
        "type": "IssuesEvent",
        "repo": {"name": "alice/project"},
        "payload": {
            "action": "opened",
            "issue": {"number": 42, "title": "Fix login bug"},
        },
    }

    result = format_event(event)

    assert result == "Opened issue #42 in alice/project"


def test_format_watch_event() -> None:
    event = {
        "type": "WatchEvent",
        "repo": {"name": "alice/project"},
        "payload": {"action": "started"},
    }

    result = format_event(event)

    assert result == "Starred alice/project"


def test_format_unsupported_event() -> None:
    event = {"type": "PoopieEvent", "repo": {"name": "Dookie/project"}}

    result = format_event(event)

    assert result == "Unsupported event: PoopieEvent"


def test_format_fork_event() -> None:
    event = {
        "type": "ForkEvent",
        "repo": {"name": "alice/project"},
        "payload": {"forkee": {"full_name": "bob/project"}},
    }

    result = format_event(event)

    assert result == "Forked alice/project to bob/project"


def test_format_create_branch_event() -> None:
    event = {
        "type": "CreateEvent",
        "repo": {"name": "alice/project"},
        "payload": {"ref_type": "branch", "ref": "feature-login"},
    }

    result = format_event(event)

    assert result == "Created branch feature-login in alice/project"


def test_format_create_repository_event() -> None:
    event = {
        "type": "CreateEvent",
        "repo": {"name": "alice/new-project"},
        "payload": {"ref_type": "repository", "ref": None},
    }

    result = format_event(event)

    assert result == "Created repository alice/new-project"


def test_format_pull_request_event() -> None:
    event = {
        "type": "PullRequestEvent",
        "repo": {"name": "alice/project"},
        "payload": {"action": "opened", "number": 27},
    }

    result = format_event(event)

    assert result == "Opened pull request #27 in alice/project"
