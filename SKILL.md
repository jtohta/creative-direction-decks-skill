---
name: dj-brand-moodboard
description: "Generates a professional 2-slide brand guide for DJs from structured questionnaire data. Creates brand moodboard with image prompts and color palette with hex codes."
version: 2.0.0
---

# DJ Brand Guide Generator

## Overview

This skill generates a professional 2-slide brand guide for DJs based on structured input:
- **Slide 1**: Brand moodboard with 4 AI image generation prompts and brand narrative
- **Slide 2**: Color palette with primary color, supporting colors (hex + CMYK), and description

**Images are now generated automatically** via Fal.ai's Nano Banana Pro API integration. FAL_KEY environment variable is required.

## Input Format

The skill expects a JSON file with this structure:

```json
{
  "dj_name": "Aqua Voyager",
  "music_style": "Deep house, progressive, techno - journey sets",
  "core_descriptors": ["oceanic", "mysterious", "hypnotic", "building", "immersive"],
  "emotional_target": "Like they're exploring an alien underwater world, discovering something ancient and beautiful",
  "physical_place": "Deep ocean, but not Earth's ocean - somewhere more mysterious",
  "color_preferences": {
    "primary": ["deep blue", "teal", "midnight blue"],
    "accents": ["cyan", "purple", "bioluminescent"],
    "mood": "dark with glowing highlights"
  },
  "visual_references": [
    "bioluminescent creatures",
    "deep sea scenes", 
    "abstract fluid art",
    "octopus/jellyfish energy"
  ],
  "forms_and_textures": ["organic flowing forms", "liquid", "ethereal"],
  "existing_visuals": "octopus and jellyfish visuals",
  "brand_positioning": "otherworldly explorer, ancient mystery meets futuristic sound"
}
```

## Complete Workflow

### Step 1: Generate Image Prompts Meta-Prompt

```bash
node generate_moodboard.js input.json
```

Creates a meta-prompt that an LLM uses to generate 4 distinct image prompts.

**Output:** `input_meta_prompt.txt`

**Next:** Copy meta-prompt → paste into Claude/GPT-4 → save JSON response as `prompts.json`

### Step 2: Generate Images with Fal.ai (MANDATORY)

```bash
FAL_KEY=your_api_key node generate_images.js prompts.json input.json
```

Generates actual images from the prompts using Fal.ai's Nano Banana Pro API.

**Output:** `dj_name_label.png` files (one per prompt) + updated `prompts.json` with image paths

**Requirements:**
- FAL_KEY environment variable must be set
- Images are cached - will skip if already generated
- Retries 3 times on API failures

### Step 3: Generate Color Palette Meta-Prompt

```bash
node generate_color_palette.js input.json
```

Creates a meta-prompt that an LLM uses to generate a color palette with hex codes and description.

**Output:** `input_color_palette_meta_prompt.txt`

**Next:** Copy meta-prompt → paste into Claude/GPT-4 → save JSON response as `colors.json`

Expected JSON format:
```json
{
  "primary": {"name": "Deep Ocean Blue", "hex": "#0A1F44"},
  "palette": [
    {"name": "Electric Cyan", "hex": "#00D9FF"},
    {"name": "Black", "hex": "#000000"},
    {"name": "White", "hex": "#FFFFFF"}
  ],
  "description": "Two paragraph description (max 620 chars)"
}
```

### Step 4: Generate PowerPoint

```bash
node create_moodboard_pptx.js prompts.json input.json colors.json
```

Creates a 2-slide PowerPoint presentation with embedded generated images.

**Output:** `dj_name_brand_guide.pptx`

## Output Structure

### Slide 1: Brand Moodboard
- Title: "[DJ NAME] - OVERALL BRAND MOODBOARD"
- 4 generated images (2x2 grid) with labels, displayed with 16:9 aspect ratio
- Each image generated from AI prompts via Fal.ai
- Brand narrative paragraph
- Typography: Fjalla One (headers), Helvetica Neue (body)
- Supports arbitrary number of prompts (grid expands dynamically)

### Slide 2: Color Palette
- Title: "BRAND COLOR PALETTE"
- Large primary color block (rounded rectangle):
  - Label: "[ PRIMARY POP COLOR]"
  - Hex code and CMYK values overlaid in white
- 6-8 supporting color bars (stacked rounded rectangles):
  - Each with hex code and CMYK values
  - White text on dark colors, black on light
- 2-paragraph color description (max 620 chars)
- Slide border and page number "05"
- Footer: "ART DIRECTION GUIDE"
- Typography: Fjalla One (headers), Helvetica Neue (body)

## Design Features

- **Typography**: Fjalla One for headers, Helvetica Neue for body text
- **Color swatches**: Rounded rectangles with automatic hex to CMYK conversion
- **Layout**: Professional design matching Cult Creatives template style
- **Spacing**: All content stays within slide borders (620 char limit enforced)
- **Dynamic**: Everything generated from DJ's unique input data (no templates)

## Technical Notes

- **All JavaScript:** Fully Node.js-based workflow (no Python dependencies)
- **Fal.ai Integration:** Uses Nano Banana Pro API for 16:9 image generation
- **Caching:** Generated images are cached to avoid re-generation
- **Retry Logic:** 3 retries with exponential backoff for API failures
- Automatic hex to CMYK conversion for print specifications
- Character limit (620) enforced by LLM via meta-prompt
- Slide dimensions: 16:9 (10" × 5.625")
- Requires: Node.js with pptxgenjs, @fal-ai/client, node-fetch

## Environment Variables

- `FAL_KEY` (REQUIRED): Your Fal.ai API key
  - Get an API key from: https://fal.ai
  - Set with: `export FAL_KEY=your_api_key`
  - Or pass inline: `FAL_KEY=your_key node generate_images.js ...`

## Scripts

- `generate_moodboard.js` - Creates meta-prompt for image prompts
- `generate_images.js` - Generates actual images via Fal.ai API (mandatory step)
- `generate_color_palette.js` - Creates meta-prompt for color palette + description
- `create_moodboard_pptx.js` - Generates 2-slide PowerPoint with embedded images

## Future Enhancements

- Additional slides (Visual Pillars, Photography Style, Typography)
- Full multi-slide brand deck
- Automated end-to-end workflow (form → email)
- Support for other image generation APIs
