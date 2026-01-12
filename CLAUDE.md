# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Python-based Anthropic Skill** for generating DJ brand guide PowerPoint presentations. The skill is invoked by the FastAPI backend (`creative-direction-decks-api`) and creates professional 2-slide presentations.

## Architecture

This skill is deployed to Anthropic's Skills API and invoked via the FastAPI backend:

```
FastAPI Backend → Claude API (with skill) → PowerPoint Generation → Files API
```

### Key Files

| File | Purpose |
|------|---------|
| `pptx_generator.py` | Main PowerPoint generation logic |
| `color_utils.py` | Hex to CMYK/RGB conversion utilities |
| `narrative_generator.py` | Brand narrative text generation |
| `SKILL.md` | Skill documentation (shown to Claude) |
| `requirements.txt` | Python dependencies |
| `upload_skill.py` | Script to upload skill to Anthropic |

### Skill Capabilities

**Slide 1: Brand Moodboard**
- 2x2 grid of AI-generated images (downloaded from Files API via `file_id`)
- Auto-generated brand narrative (2 paragraphs)
- Falls back to text prompts if images unavailable

**Slide 2: Color Palette**
- Primary color block with hex + CMYK values
- Supporting color bars with automatic text contrast
- Color palette description

## Commands

### Upload Skill to Anthropic

```bash
cd /Users/jtohta/projects/creative-direction-decks-app/creative-direction-decks-skill
ANTHROPIC_API_KEY=your_key python3 upload_skill.py
```

After upload, copy the `SKILL_ID` to the API's `.env` file.

### Local Testing

```bash
# Create virtual environment (if needed)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
python test_skill.py
```

## Dependencies

- `python-pptx>=0.6.21` - PowerPoint generation
- `anthropic>=0.30.0` - Files API access for image download

## Integration with FastAPI Backend

The skill is invoked by `creative-direction-decks-api/app/claude_client.py`:

1. Backend generates images via Fal.ai
2. Images uploaded to Anthropic Files API (returns `file_id`)
3. Backend invokes this skill with `file_id` references
4. Skill downloads images and creates PowerPoint
5. PowerPoint returned via Files API

## Design System

- **Typography**: Fjalla One (headers), Helvetica Neue (body)
- **Layout**: 16:9 slides (10" × 5.625")
- **Image aspect ratio**: 16:9 (1920×1080)
