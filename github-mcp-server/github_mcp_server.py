#!/usr/bin/env python3
import json
import os
import sys
import requests
from typing import Dict, Any, List, Optional

# GitHub API base URL
GITHUB_API_BASE_URL = "https://api.github.com"

# Get the GitHub Personal Access Token from environment variable
GITHUB_TOKEN = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
if not GITHUB_TOKEN:
    print("Error: GITHUB_PERSONAL_ACCESS_TOKEN environment variable is not set", file=sys.stderr)
    sys.exit(1)

# Set up the headers for GitHub API requests
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "GitHub-MCP-Server/1.0"
}

def handle_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle incoming MCP requests
    """
    method = request_data.get("method")
    
    # Handle different MCP methods
    if method == "list_tools":
        return handle_list_tools()
    elif method == "call_tool":
        return handle_call_tool(request_data.get("params", {}))
    elif method == "list_resources":
        return handle_list_resources()
    elif method == "list_resource_templates":
        return handle_list_resource_templates()
    elif method == "read_resource":
        return handle_read_resource(request_data.get("params", {}))
    else:
        return {
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }

def handle_list_tools() -> Dict[str, Any]:
    """
    List available tools
    """
    return {
        "result": {
            "tools": [
                {
                    "name": "search_repositories",
                    "description": "Search for GitHub repositories",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "page": {
                                "type": "number",
                                "description": "Page number for pagination"
                            },
                            "perPage": {
                                "type": "number",
                                "description": "Results per page (max 100)"
                            }
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_file_contents",
                    "description": "Get contents of a file or directory",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "Repository owner"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name"
                            },
                            "path": {
                                "type": "string",
                                "description": "Path to file/directory"
                            },
                            "branch": {
                                "type": "string",
                                "description": "Branch to get contents from"
                            }
                        },
                        "required": ["owner", "repo", "path"]
                    }
                },
                {
                    "name": "create_pull_request",
                    "description": "Create a new pull request",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "Repository owner"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name"
                            },
                            "title": {
                                "type": "string",
                                "description": "Pull request title"
                            },
                            "body": {
                                "type": "string",
                                "description": "Pull request description"
                            },
                            "head": {
                                "type": "string",
                                "description": "The name of the branch where your changes are implemented"
                            },
                            "base": {
                                "type": "string",
                                "description": "The name of the branch you want the changes pulled into"
                            }
                        },
                        "required": ["owner", "repo", "title", "head", "base"]
                    }
                }
            ]
        }
    }

def handle_call_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle tool calls
    """
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    
    if tool_name == "search_repositories":
        return handle_search_repositories(arguments)
    elif tool_name == "get_file_contents":
        return handle_get_file_contents(arguments)
    elif tool_name == "create_pull_request":
        return handle_create_pull_request(arguments)
    else:
        return {
            "error": {
                "code": -32601,
                "message": f"Tool not found: {tool_name}"
            }
        }

def handle_search_repositories(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search for GitHub repositories
    """
    query = args.get("query")
    page = args.get("page", 1)
    per_page = args.get("perPage", 30)
    
    if not query:
        return {
            "error": {
                "code": -32602,
                "message": "Missing required parameter: query"
            }
        }
    
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
        data = response.json()
        
        return {
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(data, indent=2)
                    }
                ]
            }
        }
    except requests.RequestException as e:
        return {
            "error": {
                "code": -32603,
                "message": f"GitHub API error: {str(e)}"
            }
        }

def handle_get_file_contents(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get contents of a file or directory
    """
    owner = args.get("owner")
    repo = args.get("repo")
    path = args.get("path")
    branch = args.get("branch")
    
    if not owner or not repo or not path:
        return {
            "error": {
                "code": -32602,
                "message": "Missing required parameters: owner, repo, path"
            }
        }
    
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
        data = response.json()
        
        return {
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(data, indent=2)
                    }
                ]
            }
        }
    except requests.RequestException as e:
        return {
            "error": {
                "code": -32603,
                "message": f"GitHub API error: {str(e)}"
            }
        }

def handle_create_pull_request(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new pull request
    """
    owner = args.get("owner")
    repo = args.get("repo")
    title = args.get("title")
    body = args.get("body", "")
    head = args.get("head")
    base = args.get("base")
    
    if not owner or not repo or not title or not head or not base:
        return {
            "error": {
                "code": -32602,
                "message": "Missing required parameters: owner, repo, title, head, base"
            }
        }
    
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
        data = response.json()
        
        return {
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(data, indent=2)
                    }
                ]
            }
        }
    except requests.RequestException as e:
        return {
            "error": {
                "code": -32603,
                "message": f"GitHub API error: {str(e)}"
            }
        }

def handle_list_resources() -> Dict[str, Any]:
    """
    List available resources
    """
    return {
        "result": {
            "resources": []
        }
    }

def handle_list_resource_templates() -> Dict[str, Any]:
    """
    List available resource templates
    """
    return {
        "result": {
            "resourceTemplates": []
        }
    }

def handle_read_resource(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read a resource
    """
    return {
        "error": {
            "code": -32601,
            "message": "Resource not found"
        }
    }

def main():
    """
    Main function to handle MCP requests
    """
    # Print server info to stderr
    print("GitHub MCP Server started", file=sys.stderr)
    
    # Read requests from stdin and write responses to stdout
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            print(json.dumps({
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }), flush=True)
        except Exception as e:
            print(json.dumps({
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }), flush=True)

if __name__ == "__main__":
    main()
