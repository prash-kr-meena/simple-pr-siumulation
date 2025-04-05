# GitHub MCP Server Implementation

This directory contains a custom implementation of the GitHub MCP server for Claude. The server provides tools to interact with the GitHub API, allowing Claude to search repositories, get file contents, and more.

## Files

- `github_mcp_server.py`: The main MCP server implementation that handles requests from Claude and communicates with the GitHub API.
- `test_github_mcp.py`: A test script that demonstrates the functionality of the GitHub API integration.

## Setup

1. The MCP server has been configured in the Claude settings file at:
   `/Users/apple/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

2. The configuration uses your GitHub Personal Access Token to authenticate with the GitHub API.

## Current Status

The MCP server is configured but not yet connected to Claude. To connect the server:

1. Restart VSCode or reload the window (Cmd+Shift+P and select "Developer: Reload Window")
2. Once VSCode is restarted, Claude should be able to use the GitHub MCP server tools

## Available Tools

The current implementation provides the following tools:

1. `search_repositories`: Search for GitHub repositories based on various criteria
   - Parameters: `query`, `page` (optional), `perPage` (optional)

2. `get_file_contents`: Get the contents of a file or directory from a GitHub repository
   - Parameters: `owner`, `repo`, `path`, `branch` (optional)

3. `create_pull_request`: Create a new pull request
   - Parameters: `owner`, `repo`, `title`, `body` (optional), `head`, `base`

## Testing

You can test the GitHub API integration by running the test script:

```bash
python3 github-mcp-server/test_github_mcp.py
```

This script demonstrates:
- Searching for popular JavaScript repositories
- Retrieving the README.md from the most popular repository

## Next Steps

Once the MCP server is connected, you can ask Claude to use it with commands like:

- "Search for popular Python repositories on GitHub"
- "Get the contents of the README.md file from the tensorflow/tensorflow repository"
- "Create a pull request from my feature branch to main"

## Troubleshooting

If the MCP server is not connecting:

1. Verify that VSCode has been restarted after the configuration was updated
2. Check that the GitHub Personal Access Token is valid and has the necessary permissions
3. Ensure the Python script has execute permissions (`chmod +x github_mcp_server.py`)
4. Check the VSCode logs for any error messages related to MCP servers
