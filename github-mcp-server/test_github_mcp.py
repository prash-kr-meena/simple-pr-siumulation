#!/usr/bin/env python3
import os
import requests
import json
import sys

# GitHub API base URL
GITHUB_API_BASE_URL = "https://api.github.com"

# Get the GitHub Personal Access Token from environment variable
GITHUB_TOKEN = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
if not GITHUB_TOKEN:
    print("Error: GITHUB_PERSONAL_ACCESS_TOKEN environment variable is not set", file=sys.stderr)
    print("Please set this environment variable with your GitHub token before running this script", file=sys.stderr)
    sys.exit(1)

# Set up the headers for GitHub API requests
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "GitHub-MCP-Server/1.0"
}

def search_repositories(query, page=1, per_page=10):
    """
    Search for GitHub repositories
    """
    try:
        response = requests.get(
            f"{GITHUB_API_BASE_URL}/search/repositories",
            headers=HEADERS,
            params={
                "q": query,
                "page": page,
                "per_page": per_page
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def get_file_contents(owner, repo, path, branch=None):
    """
    Get contents of a file or directory
    """
    try:
        url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        params = {}
        if branch:
            params["ref"] = branch
            
        response = requests.get(
            url,
            headers=HEADERS,
            params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def create_pull_request(owner, repo, title, head, base, body=""):
    """
    Create a new pull request
    """
    try:
        url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/pulls"
        payload = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
            
        response = requests.post(
            url,
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def main():
    """
    Test GitHub API functions
    """
    print("Testing GitHub API functions...")
    
    # Test search_repositories
    print("\n1. Searching for popular JavaScript repositories:")
    repos = search_repositories("stars:>10000 language:javascript", per_page=5)
    print(json.dumps(repos, indent=2))
    
    # Test get_file_contents
    print("\n2. Getting README.md from a popular repository:")
    if "items" in repos and len(repos["items"]) > 0:
        repo = repos["items"][0]
        owner = repo["owner"]["login"]
        repo_name = repo["name"]
        print(f"Getting README.md from {owner}/{repo_name}")
        contents = get_file_contents(owner, repo_name, "README.md")
        if "content" in contents:
            import base64
            readme_content = base64.b64decode(contents["content"]).decode("utf-8")
            print(f"README.md content (first 500 chars):\n{readme_content[:500]}...")
        else:
            print(json.dumps(contents, indent=2))
    else:
        print("No repositories found to test get_file_contents")
    
    # Test create_pull_request
    print("\n3. Creating a pull request:")
    
    owner = "prash-kr-meena"
    repo = "simple-pr-siumulation"
    title = "Add Hello World implementation"
    body = "This PR adds a basic Hello World Python script as described in the README."
    head = "feature/hello-world"  # Your feature branch
    base = "main"                 # Target branch
    
    print(f"Creating PR from {head} to {base} in {owner}/{repo}")
    result = create_pull_request(owner, repo, title, head, base, body)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
