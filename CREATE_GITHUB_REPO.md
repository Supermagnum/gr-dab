# Creating GitHub Repository for gr-dab

## Option 1: Using GitHub CLI (gh)

If you have GitHub CLI installed:

```bash
cd /home/haaken/Nedlastinger/gr-dab
gh repo create gr-dab --public --source=. --remote=origin --push
```

Or if you want it private:

```bash
gh repo create gr-dab --private --source=. --remote=origin --push
```

## Option 2: Manual GitHub Web Interface

1. Go to https://github.com/new
2. Repository name: `gr-dab`
3. Description: "GNU Radio Digital Audio Broadcasting module with USRP B210 support"
4. Choose Public or Private
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

Then run these commands:

```bash
cd /home/haaken/Nedlastinger/gr-dab
git remote add origin https://github.com/YOUR_USERNAME/gr-dab.git
git branch -M main
git add .
git commit -m "Initial commit: gr-dab with USRP B210 support and gr-osmosdr rebuild guide"
git push -u origin main
```

## Option 3: Using SSH (if you have SSH keys set up)

```bash
cd /home/haaken/Nedlastinger/gr-dab
git remote add origin git@github.com:YOUR_USERNAME/gr-dab.git
git branch -M main
git add .
git commit -m "Initial commit: gr-dab with USRP B210 support and gr-osmosdr rebuild guide"
git push -u origin main
```

## Before Pushing

Make sure you've configured git user info:

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Files to Include

The repository includes:
- Source code (already in the repo)
- README.md - Project overview
- USAGE_USRP_B210.md - Usage guide for USRP B210
- rebuild_gr_osmosdr.md - Guide for rebuilding gr-osmosdr
- uff_to_gr_complex.py - UFF file converter script

Build artifacts and temporary files are excluded via .gitignore.
