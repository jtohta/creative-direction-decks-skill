# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a DJ brand guide generator that creates professional 2-slide PowerPoint presentations from structured questionnaire data. The system uses a **meta-prompt architecture with automated image generation**:
- **JavaScript scripts** generate meta-prompts that are manually fed to LLMs
- **Fal.ai API integration** automatically generates images from prompts (16:9, 2K resolution)
- **Node.js script** assembles content and embedded images into PowerPoint
- **All JavaScript** - fully Node.js-based workflow (no Python dependencies)

## Commands

### Complete Workflow (5 steps)

1. **Generate image prompts meta-prompt:**
   ```bash
   node generate_moodboard.js <dj_input>.json
   ```
   - Outputs: `<dj_input>_meta_prompt.txt`
   - Next: Copy meta-prompt → paste into LLM → save JSON response as `<dj_name>_prompts.json`

2. **Generate images with Fal.ai (MANDATORY):**
   ```bash
   FAL_KEY=your_key node generate_images.js <prompts>.json <dj_input>.json
   ```
   - Outputs: PNG files (e.g., `aqua_voyager_bioluminescent_jellyfish.png`)
   - Updates `<prompts>.json` with image paths
   - Requires: FAL_KEY environment variable
   - Features: Caching, retry logic (3 attempts), 16:9 aspect ratio

3. **Generate color palette meta-prompt:**
   ```bash
   node generate_color_palette.js <dj_input>.json
   ```
   - Outputs: `<dj_input>_color_palette_meta_prompt.txt`
   - Next: Copy meta-prompt → paste into LLM → save JSON response as `<dj_name>_colors.json`

4. **Generate PowerPoint:**
   ```bash
   node create_moodboard_pptx.js <prompts>.json <dj_input>.json <colors>.json
   ```
   - Outputs: `<dj_name>_brand_guide.pptx` (2 slides with embedded images)

### Quick Test with Example Files

```bash
node create_moodboard_pptx.js aqua_voyager_prompts.json aqua_voyager_input.json aqua_voyager_colors.json
```

## Architecture

### Meta-Prompt + Image Generation Pattern

The system uses a **three-stage generation pattern**:

1. **JavaScript scripts** (`generate_moodboard.js`, `generate_color_palette.js`) create meta-prompts that embed the DJ's input data and instruct an LLM how to generate the final content
2. **Manual LLM step**: User copies meta-prompt to Claude/GPT-4 to generate structured JSON
3. **Automated image generation**: `generate_images.js` calls Fal.ai API to generate actual images
4. **Node.js script** (`create_moodboard_pptx.js`) assembles the LLM-generated content and images into a PowerPoint

This architecture allows dynamic content generation with automated image generation via Fal.ai API.

### Data Flow

```
DJ Input JSON → Node.js (meta-prompt) → LLM (manual) → Prompts JSON →
Fal.ai API (images) → Node.js → PowerPoint with embedded images
```

### Input Data Structure

The DJ input JSON must contain:
- `dj_name`: DJ's name
- `music_style`: Genre/style description
- `core_descriptors`: Array of brand adjectives
- `emotional_target`: Target emotional experience
- `physical_place`: Environmental/spatial description
- `color_preferences`: Object with `primary`, `accents`, `mood`
- `visual_references`: Array of visual inspiration
- `forms_and_textures`: Array of texture descriptors
- `existing_visuals`: Optional existing visual assets
- `brand_positioning`: Brand positioning statement

See `aqua_voyager_input.json` for a complete example.

### Output Slides

**Slide 1: Brand Moodboard**
- 2x2 grid of **actual generated images** (16:9 aspect ratio, properly centered)
- Supports arbitrary number of prompts (grid expands dynamically)
- Auto-generated brand narrative (2 paragraphs)
- Uses `generateBrandNarrative()` function to dynamically create narrative from DJ input
- Falls back to text prompts if images are missing

**Slide 2: Color Palette**
- Primary color block (large rounded rectangle)
- 6-8 supporting color bars with hex and CMYK values
- Auto-conversion from hex to CMYK via `hexToCMYK()` function
- 2-paragraph description (max 620 characters)
- Page number "05" and "ART DIRECTION GUIDE" footer
- Bordered slide layout

### Design System

- **Typography**: Fjalla One (headers), Helvetica Neue (body)
- **Layout**: 16:9 slides (10" × 5.625")
- **Color swatches**: Rounded rectangles with automatic text color (white on dark, black on light)
- **Character limits**: 620 chars for color description (enforced in meta-prompt)

## Technical Notes

### Dependencies

- **Node.js packages**:
  - `pptxgenjs` - PowerPoint generation
  - `@fal-ai/client` - Fal.ai API integration
  - `node-fetch` - HTTP requests
  - Install with: `npm install`
- **Environment variable**: `FAL_KEY` - Fal.ai API key (required)

### Key Functions

- `create_moodboard_pptx.js`:
  - `generateBrandNarrative(data)`: Creates 2-paragraph brand story from DJ input
  - `hexToCMYK(hex)`: Converts hex color codes to CMYK percentages
  - `createMoodboardSlideForDeck(pptx, prompts, data)`: Builds Slide 1
  - `createColorPaletteSlide(colors, data, pptx)`: Builds Slide 2
  - `createFullPresentation(prompts, colors, data, outputFile)`: Orchestrates both slides

### Current Features & Limitations

**Features:**
- ✓ Automated image generation via Fal.ai API
- ✓ 16:9 aspect ratio images with proper centering
- ✓ Image caching to avoid re-generation
- ✓ Retry logic for API failures
- ✓ Fully JavaScript-based workflow

**Limitations:**
- Manual LLM step required for prompt/color generation (by design)
- Requires FAL_KEY environment variable
- No automated end-to-end workflow

### Future Enhancement Plans

- Direct image generation via Fal.ai API integration
- Additional slide types (Visual Brand Pillars, Photography Style, Typography)
- Full multi-slide brand deck generation
- Automated end-to-end workflow (form → email)
