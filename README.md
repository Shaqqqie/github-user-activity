# GitHub User Activity CLI

A Python command-line application that fetches and displays a user's recent public GitHub activity.

## Features

- Fetch recent public events from the GitHub API.
- Display events in a human-readable format.
- Handle HTTP errors, network failures, and invalid API responses.
- Handle users with no recent public activity.
- Provide a command-line interface.

## Requirements

- Python 3.11 or newer
- Internet connection for fetching GitHub activity

## Installation

Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/Shaqqqie/github-user-activity.git
cd github-user-activity
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the application:

```bash
python -m pip install -e .
```

## Usage

Run the application with a GitHub username:

```bash
github-activity alice
```

Example output:

```text
Fetching activity for user: alice
Starred alice/project
```

The example illustrates the output format; actual activity depends on the user's public GitHub events.

## Development

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the tests:

```bash
python -m pytest
```

Run linting and formatting checks:

```bash
python -m ruff check .
python -m ruff format --check .
```

## Technologies

- Python
- GitHub REST API
- pytest
- Ruff
- setuptools

## License

No license has been selected yet.