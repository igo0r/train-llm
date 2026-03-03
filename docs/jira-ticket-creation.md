# Jira Ticket Creation - Atlassian CLI

## Overview

Use Atlassian CLI (`acli`) to create Jira tickets programmatically.

## Command

```bash
acli jira workitem create [flags]
```

## Required Flags

- `--summary` or `-s`: Ticket title/summary
- `--project` or `-p`: Jira project key (e.g., "PROJ", "TEAM")
- `--type` or `-t`: Issue type (e.g., "Task", "Bug", "Story", "Epic")

## Common Optional Flags

- `-d, --description`: Issue description (supports ADF format)
- `-a, --assignee`: Assignee email or account ID (use `@me` for self-assign)
- `--priority`: Priority level (e.g., "High", "Medium", "Low")
- `--labels`: Comma-separated labels
- `--from-file`: Read issue data from a file
- `--json`: Output response as JSON

## Examples

### Create a simple task
```bash
acli jira workitem create --summary "Fix login bug" --project "MYPROJ" --type "Bug"
```

### Create with full details
```bash
acli jira workitem create \
  --summary "Add user authentication" \
  --project "MYPROJ" \
  --type "Story" \
  --description "Implement OAuth2 login flow" \
  --assignee "user@example.com" \
  --priority "High" \
  --labels "backend,security"
```

### Create from JSON file
```bash
acli jira workitem create --from-file "issue.json"
```

## Authentication

Before using, authenticate with Jira:
```bash
acli jira auth
```

## Notes

- Project key must exist in your Jira instance
- Issue type must be valid for the project
- Use `--json` flag to parse output programmatically
