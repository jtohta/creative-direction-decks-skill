# DJ Brand Moodboard Generator Skill

A skill for generating professional brand moodboard and color palette slides for DJs from structured questionnaire data.

## Overview

This skill creates a 2-slide brand guide PowerPoint:
- **Slide 1**: Brand Moodboard (4 image prompts + brand narrative)
- **Slide 2**: Color Palette (primary color + supporting colors with hex/CMYK + description)

## Files

- `SKILL.md` - Skill documentation
- `generate_moodboard.py` - Generates meta-prompt for 4 image prompts
- `generate_color_palette.py` - Generates meta-prompt for color palette + description
- `create_moodboard_pptx.js` - Creates PowerPoint from prompts and colors
- `aqua_voyager_*.json` - Example files for Aqua Voyager DJ

## Prerequisites

```bash
# Install Node.js dependencies
npm install

# Set up Fal.ai API key (REQUIRED for image generation)
export FAL_KEY=your_api_key_here
# Get your API key from: https://fal.ai
```

## Complete Workflow

### Step 1: Create DJ Input JSON

Create a JSON file with the DJ's brand data:

```json
{
  "dj_name": "Your DJ Name",
  "music_style": "Deep house, progressive, techno",
  "core_descriptors": ["oceanic", "mysterious", "hypnotic"],
  "emotional_target": "Like exploring an alien underwater world",
  "physical_place": "Deep ocean, but not Earth's ocean",
  "color_preferences": {
    "primary": ["deep blue", "teal"],
    "accents": ["cyan", "purple"],
    "mood": "dark with glowing highlights"
  },
  "visual_references": ["bioluminescent creatures", "deep sea"],
  "forms_and_textures": ["organic flowing forms", "liquid"],
  "existing_visuals": "optional - any existing visual work",
  "brand_positioning": "otherworldly explorer"
}
```

### Step 2: Generate Image Prompts Meta-Prompt

```bash
node generate_moodboard.js your_dj_input.json
```

This creates `your_dj_input_meta_prompt.txt`

Copy this meta-prompt → paste into Claude/GPT-4 → get back JSON with 4 image prompts

Save as `your_dj_prompts.json`

### Step 3: Generate Images with Fal.ai (MANDATORY)

```bash
FAL_KEY=your_api_key node generate_images.js your_dj_prompts.json your_dj_input.json
```

This generates actual images from the prompts using Fal.ai's Nano Banana Pro API:
- Creates PNG files (e.g., `aqua_voyager_bioluminescent_jellyfish.png`)
- Updates `your_dj_prompts.json` with image paths
- Images are cached (will skip if already exists)
- Retries 3 times on API failures

### Step 4: Generate Color Palette Meta-Prompt

```bash
node generate_color_palette.js your_dj_input.json
```

This creates `your_dj_input_color_palette_meta_prompt.txt`

Copy this meta-prompt → paste into Claude/GPT-4 → get back JSON with colors + description (620 char max)

Save as `your_dj_colors.json`

### Step 5: Generate PowerPoint

```bash
node create_moodboard_pptx.js your_dj_prompts.json your_dj_input.json your_dj_colors.json
```

Output: `your_dj_name_brand_guide.pptx` (2 slides with embedded images)

## Output Slides

### Slide 1: Brand Moodboard
- Title with DJ name
- 4 generated images (2x2 grid) displayed with 16:9 aspect ratio
- Each image labeled above
- Brand narrative paragraph
- Fjalla One font for headers, Helvetica Neue for body
- Supports arbitrary number of prompts (grid expands dynamically)

### Slide 2: Color Palette
- Title "BRAND COLOR PALETTE"
- Large primary color block with label
- 6-8 supporting color bars with hex + CMYK values
- 2-paragraph description (max 620 chars)
- Slide border and page number
- Fjalla One font for headers, Helvetica Neue for body

## Design Features

- **All JavaScript workflow** - no Python dependencies
- **Automatic image generation** via Fal.ai Nano Banana Pro API
- **16:9 aspect ratio** images with proper centering
- **Caching** - generated images are reused to save API calls
- Clean, professional layout matching Cult Creatives template style
- Rounded rectangles for color swatches
- Automatic CMYK conversion from hex codes
- White text on dark colors, black text on light colors
- Proper spacing to stay within slide borders
- Dynamic content generation based on DJ's unique aesthetic

## Environment Setup

Set your Fal.ai API key before using image generation:

```bash
# Option 1: Export (persists for session)
export FAL_KEY=your_fal_api_key_here

# Option 2: Inline (one-time use)
FAL_KEY=your_key node generate_images.js prompts.json input.json
```

Get your API key from: https://fal.ai

## Future Enhancements

- Additional slide types (Visual Brand Pillars, Photography Style, Typography)
- Full multi-slide brand deck generation
- Automated end-to-end workflow
- Support for other image generation APIs

## Example Usage

See the included `aqua_voyager_*.json` files for a complete example of:
- DJ input data
- Generated image prompts
- Generated color palette with description

Run:
```bash
node create_moodboard_pptx.js aqua_voyager_prompts.json aqua_voyager_input.json aqua_voyager_colors.json
```

To see the complete 2-slide brand guide for Aqua Voyager.
