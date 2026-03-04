# GitHub CLI (gh) Commands

## Common Operations

### Push Code
```bash
git push origin <branch-name>
```

### Create Pull Request
```bash
gh pr create --title "PR Title" --body "PR Description"
```

### View PR Status
```bash
gh pr status
```

### List PRs
```bash
gh pr list
```

### Check PR Details
```bash
gh pr view <pr-number>
```

### Merge PR
```bash
gh pr merge <pr-number>
```

### Create Branch and Push
```bash
git checkout -b <branch-name>
git push -u origin <branch-name>
```

## Authentication

Ensure you're authenticated:
```bash
gh auth login
```
