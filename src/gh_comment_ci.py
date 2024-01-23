# Usage:
# $ python gh_comment_ci.py path/to/report.md

import requests
import os
import sys


token = os.getenv('GITHUB_ACCESS_TOKEN')
repo_slug = os.getenv('SEMAPHORE_GIT_REPO_SLUG')
commit_sha = os.getenv('SEMAPHORE_GIT_SHA')

try:
    report_fn = sys.argv[1]
except:
    print(f"Usage:\n  python {sys.argv[0]} path/to/report.md")
    sys.exit(1)

if repo_slug is None or commit_sha is None:
    print("Missing Semaphore environment variables.")
    sys.exit(1)

if token is None:
    print("GITHUB_ACCESS_TOKEN not set. Silently skipping commit comment.")
    sys.exit(0)

with open(report_fn, 'r') as f:
    comment = f.read()

url = f'https://api.github.com/repos/{repo_slug}/commits/{commit_sha}/comments'
headers = {
    'Authorization': f'Bearer {token}', 
    'X-GitHub-Api-Version': '2022-11-28' 
}
response = requests.post(url, headers=headers, json={'body': comment})

if response.status_code != 201:
    print('Failed to post comment on GitHub.')
    print('Response:', response.content)
    sys.exit(1)
