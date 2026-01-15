#!/usr/bin/env python3
"""
Upload the DJ Brand Guide skill to Anthropic Skills API.
Run this script to get your SKILL_ID for the FastAPI .env file.
"""

from anthropic import Anthropic
from pathlib import Path
import os
import sys

# Directories and files to exclude from upload
EXCLUDE_PATTERNS = {
    'venv', '.venv', 'env', '__pycache__',
    '.git', '.gitignore', '.gitignore_skill', 'node_modules',
    '.DS_Store', '.env', '.claude',
    'upload_skill.py',  # Don't upload the upload script itself
    'README.md', 'CLAUDE.md',  # Project docs, not skill docs
}

# File extensions to exclude (example data)
EXCLUDE_EXTENSIONS = {'.png', '.pptx', '.json'}


SKILL_FOLDER_NAME = "dj-brand-guide-generator"


def collect_skill_files(skill_dir: Path):
    """
    Collect files from skill directory, excluding venv, __pycache__, and example data.

    Returns list of tuples: (filepath, file_content, mime_type)
    Note: filepath must include a directory prefix (e.g., "skill/SKILL.md")
    """
    files = []

    for item in skill_dir.iterdir():
        # Skip excluded directories and files
        if item.name in EXCLUDE_PATTERNS:
            continue

        # Skip directories
        if item.is_dir():
            continue

        # Skip excluded file extensions (example data)
        if item.suffix.lower() in EXCLUDE_EXTENSIONS:
            continue

        # Read file content
        content = item.read_bytes()

        # Determine mime type
        if item.suffix == '.py':
            mime_type = 'text/x-python'
        elif item.suffix == '.md':
            mime_type = 'text/markdown'
        elif item.suffix == '.txt':
            mime_type = 'text/plain'
        elif item.suffix == '.json':
            mime_type = 'application/json'
        else:
            mime_type = 'application/octet-stream'

        # Files must have a directory prefix for the API
        filepath = f"{SKILL_FOLDER_NAME}/{item.name}"
        files.append((filepath, content, mime_type))

    return files


SKILL_TITLE = "DJ Brand Guide Generator"


def find_existing_skill(client, title: str):
    """
    Find an existing skill by display_title.

    Returns skill object if found, None otherwise.
    """
    try:
        skills = client.beta.skills.list(betas=["skills-2025-10-02"])
        for skill in skills.data:
            if skill.display_title == title:
                return skill
    except Exception as e:
        print(f"Warning: Could not list skills: {e}")
    return None


def main():
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Usage: ANTHROPIC_API_KEY=your_key python3 upload_skill.py")
        sys.exit(1)

    # Initialize client
    client = Anthropic(api_key=api_key)

    # Skill directory (current directory where this script lives)
    skill_dir = Path(__file__).parent

    # Collect files (excluding venv, __pycache__, etc.)
    skill_files = collect_skill_files(skill_dir)

    print(f"Uploading skill from: {skill_dir}")
    print("\nFiles to upload:")
    for filepath, content, _ in skill_files:
        print(f"  - {filepath} ({len(content)} bytes)")

    try:
        # Check for existing skill
        print(f"\nChecking for existing skill '{SKILL_TITLE}'...")
        existing_skill = find_existing_skill(client, SKILL_TITLE)

        if existing_skill:
            # Create new version of existing skill
            print(f"Found existing skill: {existing_skill.id}")
            print("Creating new version...")
            new_version = client.beta.skills.versions.create(
                skill_id=existing_skill.id,
                files=skill_files,
                betas=["skills-2025-10-02"]
            )
            # Retrieve updated skill info
            skill = client.beta.skills.retrieve(
                skill_id=existing_skill.id,
                betas=["skills-2025-10-02"]
            )
            action = f"updated (new version: {new_version.version})"
        else:
            # Create new skill
            print("No existing skill found. Creating new skill...")
            skill = client.beta.skills.create(
                display_title=SKILL_TITLE,
                files=skill_files,
                betas=["skills-2025-10-02"]
            )
            action = "created"

        print("\n" + "="*60)
        print(f"✓ Skill {action} successfully!")
        print("="*60)
        print(f"\nSkill ID: {skill.id}")
        print(f"Display Title: {skill.display_title}")
        print(f"\n🔑 Add this to your FastAPI .env file:")
        print(f"SKILL_ID={skill.id}")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error uploading skill: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
