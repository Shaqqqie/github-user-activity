def format_event(event: dict) -> str:
    event_type = event["type"]

    if event_type == "PushEvent":
        return format_push_event(event)
    elif event_type == "IssuesEvent":
        return format_issues_event(event)
    elif event_type == "WatchEvent":
        return format_watch_event(event)
    elif event_type == "ForkEvent":
        return format_fork_event(event)
    elif event_type == "CreateEvent":
        return format_create_event(event)
    elif event_type == "PullRequestEvent":
        return format_pull_request_event(event)
    return f"Unsupported event: {event_type}"


def format_push_event(event: dict) -> str:
    repo_name = event["repo"]["name"]
    commit_count = event["payload"].get("size", 0)

    return f"Pushed {commit_count} commits to {repo_name}"


def format_issues_event(event: dict) -> str:
    repo_name = event["repo"]["name"]
    action = event["payload"]["action"]
    issue_number = event["payload"]["issue"]["number"]

    return f"{action.capitalize()} issue #{issue_number} in {repo_name}"


def format_watch_event(event: dict) -> str:
    repo_name = event["repo"]["name"]

    return f"Starred {repo_name}"


def format_fork_event(event: dict) -> str:
    repo_name = event["repo"]["name"]
    forked_repo_name = event["payload"]["forkee"]["full_name"]

    return f"Forked {repo_name} to {forked_repo_name}"


def format_create_event(event: dict) -> str:
    repo_name = event["repo"]["name"]
    ref_type = event["payload"]["ref_type"]

    if ref_type == "repository":
        return f"Created repository {repo_name}"

    ref = event["payload"]["ref"]
    return f"Created {ref_type} {ref} in {repo_name}"


def format_pull_request_event(event: dict) -> str:
    repo_name = event["repo"]["name"]
    action = event["payload"]["action"]
    number = event["payload"]["number"]

    return f"{action.capitalize()} pull request #{number} in {repo_name}"
