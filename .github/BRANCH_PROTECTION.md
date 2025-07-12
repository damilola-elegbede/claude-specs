# Branch Protection Setup Guide

This guide explains how to set up branch protection rules to ensure all specifications meet the 90% compliance requirement before merging.

## Prerequisites

- Repository admin access
- GitHub Actions enabled

## Setting Up Branch Protection

1. **Navigate to Settings**
   - Go to your repository on GitHub
   - Click on "Settings" tab
   - Select "Branches" from the left sidebar

2. **Add Branch Protection Rule**
   - Click "Add rule" button
   - Enter branch name pattern: `main` (or `master`)

3. **Configure Protection Rules**

   Check the following options:

   ### ✅ Require a pull request before merging
   - Require approvals: 1 (minimum)
   - Dismiss stale pull request approvals when new commits are pushed
   - Require review from CODEOWNERS (optional)

   ### ✅ Require status checks to pass before merging
   - Require branches to be up to date before merging
   - **Required status checks:**
     - `compliance-test`
     - `markdown-lint`
     - `directory-structure`

   ### ✅ Require conversation resolution before merging
   - Ensures all review comments are addressed

   ### ✅ Include administrators (recommended)
   - Applies rules even to repository admins

4. **Save Changes**
   - Click "Create" or "Save changes"

## Status Checks Explained

### compliance-test
- Runs Python script to check all specifications
- Ensures minimum 90% compliance with template
- Validates required sections and content
- Posts results as PR comment

### markdown-lint
- Checks markdown syntax and formatting
- Ensures consistent style across all files
- Uses `.markdownlint.json` configuration

### directory-structure
- Verifies files are in correct category folders
- Checks for required directories
- Prevents misplaced specification files

## Testing Your Setup

1. Create a new branch
2. Add or modify a specification
3. Create a pull request
4. Verify all status checks run
5. Confirm merge is blocked if any check fails

## Troubleshooting

### "Required status check is expected"
- Push a commit to trigger the workflows
- Wait for workflows to complete at least once
- The status checks will then appear in the dropdown

### Checks not running
- Verify `.github/workflows/compliance-check.yml` exists
- Check Actions tab for any workflow errors
- Ensure GitHub Actions is enabled for the repository

### Compliance test failing
- Review the PR comment for specific issues
- Run `python tests/test_compliance.py` locally
- Fix missing sections or content issues
- Push fixes to trigger re-check

## Local Testing

Before pushing changes, test locally:

```bash
# Run compliance tests
python tests/test_compliance.py

# Check specific file
python -c "
from pathlib import Path
from tests.test_compliance import SpecificationTester
tester = SpecificationTester(Path('.'))
result = tester.test_specification(Path('productivity/gtd-expert-system.md'))
"
```

## Bypass Protection (Emergency Only)

Admins can bypass protection if absolutely necessary:
1. Go to PR page
2. Click "Merge pull request" dropdown
3. Select "Merge without waiting for requirements"
4. Provide justification in merge commit message

⚠️ **Use sparingly and document why protection was bypassed**