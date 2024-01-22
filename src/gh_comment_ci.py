import requests
from requests.auth import HTTPBasicAuth
import os
import sys

# Set your credentials and repository details
token = os.getenv('GITHUB_ACCESS_TOKEN')
repo_slug = os.getenv('SEMAPHORE_GIT_REPO_SLUG')
commit_sha = os.getenv('SEMAPHORE_GIT_SHA')

# Set your comment
report_fn = sys.argv[1]
with open(report_fn, 'r') as f:
    comment = f.read()

# comment = 'This is a comment on a commit.'

# Construct the URL
url = f'https://api.github.com/repos/{repo_slug}/commits/{commit_sha}/comments'
print(url)
print(comment)

# Make a POST request to the GitHub API endpoint
# response = requests.post(url, json={'body': comment}, auth=HTTPBasicAuth(username, token))
headers = {
    'Authorization': f'Bearer {token}', 
    'X-GitHub-Api-Version': '2022-11-28' 
}
print(headers)
response = requests.post(url, headers=headers, json={'body': comment})

# Check the response
if response.status_code == 201:
    print('Comment posted successfully on GitHub.')
else:
    print('Failed to post comment on GitHub.')
    print('Response:', response.content)
