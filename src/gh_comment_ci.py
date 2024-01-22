# Usage:
# gh_comment_cy.py path/to/report.md

import requests
from requests.auth import HTTPBasicAuth
import os
import sys

# Set your credentials and repository details
token = os.getenv('GITHUB_ACCESS_TOKEN')
repo_slug = os.getenv('SEMAPHORE_GIT_REPO_SLUG')
commit_sha = os.getenv('SEMAPHORE_GIT_SHA')

if token is None:
    print("GITHUB_ACCESS_TOKEN not set. Silently skipping commit comment.")
    sys.exit(0)

try:
    report_fn = sys.argv[1]
except:
    print(f"Usage:\n  python {sys.argv[0]} path/to/report.md")
    sys.exit(1)

with open(report_fn, 'r') as f:
    comment = f.read()

url = f'https://api.github.com/repos/{repo_slug}/commits/{commit_sha}/comments'
headers = {
    'Authorization': f'Bearer {token}', 
    'X-GitHub-Api-Version': '2022-11-28' 
}
response = requests.post(url, headers=headers, json={'body': comment})

# Check the response
if response.status_code != 201:
    print('Failed to post comment on GitHub.')
    print('Response:', response.content)
    sys.exit(1)
