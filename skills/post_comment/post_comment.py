"""
post_comment — Claude Code agent tool

Posts a comment to a GitHub Issue, or writes it to the local ticket JSON
file if GITHUB_TOKEN is not available.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

OWNER = "vvsevolodovich"
REPO = "agent-one-tool-practice"
API_BASE = "https://api.github.com"
TICKETS_DIR = Path(__file__).parent.parent.parent / "data" / "tickets"


def _post_to_local(ticket_id: str, comment: str) -> dict:
    ticket_path = TICKETS_DIR / f"{ticket_id}.json"
    if not ticket_path.exists():
        raise FileNotFoundError(f"Local ticket file not found: {ticket_path}")

    data = json.loads(ticket_path.read_text())
    posted_at = datetime.now(timezone.utc).isoformat()
    data.setdefault("comments", []).append({"body": comment, "posted_at": posted_at})
    ticket_path.write_text(json.dumps(data, indent=2))

    return {
        "ticket_id": ticket_id,
        "comment": comment,
        "posted_at": posted_at,
        "source": "local",
    }


def post_comment(ticket_id: str, comment: str) -> dict:
    """Post a comment to a GitHub issue, falling back to local JSON if no token.

    Args:
        ticket_id: GitHub issue number (string or int).
        comment: The comment body to post.

    Returns:
        dict with keys: ticket_id, comment, and either GitHub fields or source="local".

    Raises:
        requests.HTTPError: If the GitHub API call fails.
    """
    ticket_id = str(ticket_id).lstrip("#")
    token = os.environ.get("GITHUB_TOKEN")

    if not token:
        print("[post_comment] No GITHUB_TOKEN found — writing comment to local JSON.", file=sys.stderr)
        return _post_to_local(ticket_id, comment)

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }

    url = f"{API_BASE}/repos/{OWNER}/{REPO}/issues/{ticket_id}/comments"
    resp = requests.post(url, headers=headers, json={"body": comment})
    resp.raise_for_status()
    data = resp.json()

    return {
        "ticket_id": ticket_id,
        "comment_id": data["id"],
        "comment": comment,
        "html_url": data["html_url"],
        "source": "github",
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python post_comment.py <ticket_id> <comment>", file=sys.stderr)
        print('Example: python post_comment.py 3 "Test cases look good."', file=sys.stderr)
        sys.exit(1)

    result = post_comment(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
