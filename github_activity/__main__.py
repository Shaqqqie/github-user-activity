import json
import sys
from urllib.error import HTTPError, URLError

from .client import fetch_user_activity
from .formatter import format_event


def main() -> int:
    if len(sys.argv) < 2:
        print("Error: Please provide a GitHub username.", file=sys.stderr)
        return 1

    username = sys.argv[1]
    print(f"Fetching activity for user: {username}")
    try:
        data = fetch_user_activity(username)
    except HTTPError as error:
        if error.code == 404:
            print("Error: GitHub user not found.", file=sys.stderr)
            return 1

        print(f"Error: GitHub API request failed (HTTP {error.code}).", file=sys.stderr)
        return 1
    except URLError as error:
        print(
            f"Error: Unable to connect to GitHub. Reason: {error.reason}.",
            file=sys.stderr,
        )
        return 1
    except json.JSONDecodeError:
        print("Error: GitHub returned an invalid JSON response.", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Error: Invalid GitHub API response: {error}", file=sys.stderr)
        return 1
    if not data:
        print("No recent public activity found.")
        return 0

    for event in data:
        print(format_event(event))
    return 0


if __name__ == "__main__":
    sys.exit(main())
