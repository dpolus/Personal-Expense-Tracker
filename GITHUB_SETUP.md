# GitHub Setup Instructions

This guide will help you upload the Personal Expense Tracker project to GitHub.

## Prerequisites

- GitHub account ([sign up here](https://github.com/join))
- Git installed on your computer ([download here](https://git-scm.com/downloads))

## Step 1: Create a New Repository on GitHub

1. Log in to your GitHub account
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `expense-tracker` (or your preferred name)
   - **Description**: "Personal Expense Tracker - A web application for tracking income and expenses"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Initialize Git in Your Project

Open terminal/command prompt in your project directory and run:

```bash
cd C:\Users\diana\expense_tracker
git init
```

## Step 3: Add Files to Git

```bash
# Add all files
git add .

# Check what will be committed
git status
```

## Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: Personal Expense Tracker application"
```

## Step 5: Connect to GitHub Repository

Replace `<your-username>` and `<repository-name>` with your actual GitHub username and repository name:

```bash
git remote add origin https://github.com/<your-username>/<repository-name>.git
```

For example:
```bash
git remote add origin https://github.com/johndoe/expense-tracker.git
```

## Step 6: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

You'll be prompted for your GitHub username and password (or personal access token).

## Step 7: Verify Upload

1. Go to your GitHub repository page
2. Refresh the page
3. You should see all your project files

## Adding a Repository Description

1. Go to your repository on GitHub
2. Click the gear icon (⚙️) next to "About"
3. Add a description: "A comprehensive web-based application for tracking personal income and expenses"
4. Add topics: `python`, `streamlit`, `expense-tracker`, `finance`, `web-app`
5. Click "Save changes"

## Setting Up GitHub Pages (Optional)

If you want to create a project website:

1. Go to Settings → Pages
2. Under "Source", select "main" branch
3. Click "Save"
4. Your site will be available at `https://<your-username>.github.io/<repository-name>`

## Future Updates

When you make changes to the project:

```bash
# Add changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push origin main
```

## Branching Strategy (Optional)

For team collaboration:

```bash
# Create a new branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push branch to GitHub
git push origin feature/new-feature

# Create Pull Request on GitHub
```

## Troubleshooting

### Issue: Authentication failed

**Solution**: Use a Personal Access Token instead of password
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Issue: Remote already exists

**Solution**: Remove and re-add remote
```bash
git remote remove origin
git remote add origin https://github.com/<username>/<repo>.git
```

### Issue: Files not showing on GitHub

**Solution**: Check .gitignore file - some files may be excluded
```bash
git status  # See what files are tracked
```

## Repository Settings Recommendations

1. **Add Topics**: Go to repository → click gear icon → add relevant topics
2. **Add Description**: Brief description of the project
3. **Enable Issues**: Settings → Features → check "Issues"
4. **Add README badges**: Add status badges to README.md (optional)

## Next Steps

- Share the repository link with your teammates
- They can clone it using: `git clone <repository-url>`
- Follow the SETUP_GUIDE.md for installation instructions

---

**Your project is now on GitHub!** 🎉
