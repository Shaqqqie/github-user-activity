import json
from urllib.request import urlopen


def fetch_user_activity(username: str) -> list[dict]:
    github_api_url = f"https://api.github.com/users/{username}/events/public"

    with urlopen(github_api_url, timeout=10) as response:
        data = response.read()

    json_data = json.loads(data)

    if not isinstance(json_data, list):
        raise ValueError("Expected a list of GitHub events")

    if not all(isinstance(item, dict) for item in json_data):
        raise ValueError("Expected event data to be of type dict")

    return json_data
