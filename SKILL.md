---
name: dj-brand-guide-generator
description: Generates professional 2-slide PowerPoint presentations from DJ brand questionnaire data. Creates brand moodboard slide with 2x2 image grid and narrative, plus color palette slide with hex/CMYK values. Use when generating DJ brand guides or music artist presentation decks.
---

# DJ Brand Guide Generator

Generates professional 2-slide PowerPoint presentations for DJ/artist brands. Creates a brand moodboard with image grid and narrative, plus a color palette slide with hex and CMYK values.

## Quick Start

Generate a complete brand guide PowerPoint:

```python
from pptx_generator import create_brand_guide
import json

# DJ input data (from questionnaire)
dj_input = {
    "dj_name": "Aqua Voyager",
    "music_style": "Deep house, progressive, techno",
    "core_descriptors": ["oceanic", "mysterious", "hypnotic", "building", "immersive"],
    "emotional_target": "Like they're exploring an alien underwater world...",
    "physical_place": "Deep ocean, but not Earth's ocean",
    "color_preferences": {
        "primary": ["deep blue", "teal"],
        "accents": ["cyan", "purple"],
        "mood": "dark with glowing highlights"
    },
    "visual_references": ["bioluminescent creatures", "deep sea scenes"],
    "forms_and_textures": ["organic flowing forms", "liquid", "ethereal"],
    "brand_positioning": "otherworldly explorer of sonic depths"
}

# Image prompts (already generated via Claude API + Fal.ai)
image_prompts = [
    {
        "label": "BIOLUMINESCENT JELLYFISH",
        "prompt": "Ethereal bioluminescent jellyfish floating in deep ocean...",
        "file_id": "file_abc123",
        "path": "jellyfish.png"  # For local testing
    },
    {
        "label": "DEEP OCEAN STRUCTURE",
        "prompt": "Abstract underwater architecture with flowing forms...",
        "file_id": "file_def456",
        "path": "structure.png"
    },
    {
        "label": "LIQUID FORMS",
        "prompt": "Liquid metal flowing through cosmic water...",
        "file_id": "file_ghi789",
        "path": "liquid.png"
    },
    {
        "label": "COSMIC UNDERWATER",
        "prompt": "Alien underwater landscape with glowing elements...",
        "file_id": "file_jkl012",
        "path": "cosmic.png"
    }
]

# Colors (generated via Claude API)
colors = {
    "primary": {
        "name": "Deep Ocean Blue",
        "hex": "#0A1F44"
    },
    "palette": [
        {"name": "Electric Cyan", "hex": "#00D9FF"},
        {"name": "Purple Glow", "hex": "#8B00FF"},
        {"name": "Teal Depth", "hex": "#008B8B"},
        {"name": "Dark Blue", "hex": "#001F3F"},
        {"name": "Bright Accent", "hex": "#00FFFF"},
        {"name": "Black", "hex": "#000000"},
        {"name": "White", "hex": "#FFFFFF"}
    ],
    "description": "This brand embodies oceanic, mysterious, hypnotic energy through its color palette. Deep Ocean Blue serves as the foundational anchor, establishing the core atmosphere of otherworldly explorer of sonic depths. Supporting tones — electric cyan, purple glow — create depth and nuance, evoking like they're exploring an alien underwater world. These colors speak to a sonic identity rooted in deep house, progressive, techno.\\n\\nWithin this carefully curated world, moments of intensity emerge. Bright accent and white cut through the atmosphere, adding punctuation and emotional peaks without disrupting the flow."
}

# Generate PowerPoint
output_file = create_brand_guide(dj_input, image_prompts, colors, output_path="brand_guide.pptx")
print(f"Created: {output_file}")
```

## Capabilities

### Slide 1: Brand Moodboard
- **2x2 Image Grid**: Supports arbitrary number of images in 2-column layout
- **16:9 Aspect Ratio**: Images automatically centered and fitted
- **Image Labels**: Each image labeled above the box
- **Brand Narrative**: Auto-generated 2-paragraph narrative from DJ input
- **Design**: Fjalla One headers, Helvetica Neue body text

### Slide 2: Color Palette
- **Primary Color Block**: Large rounded rectangle with hex + CMYK values
- **Palette Bars**: 6-8 stacked color bars with automatic text contrast
- **CMYK Conversion**: Automatic hex to CMYK percentage conversion
- **Description**: 2-paragraph color palette description (max 620 chars)
- **Smart Formatting**: White text on dark colors, black text on light colors

## Design System

- **Typography**: Fjalla One (headers), Helvetica Neue (body)
- **Layout**: 16:9 slides (10" × 5.625")
- **Color Swatches**: Rounded rectangles with automatic text color selection
- **Positioning**: Precise inch-based positioning for professional layout

## Technical Notes

- Uses python-pptx library (pre-installed in Claude code execution environment)
- Supports file_id references for images uploaded via Files API
- Fallback to text prompts if images unavailable
- Automatic CMYK conversion for print specifications

See [REFERENCE.md](REFERENCE.md) for complete API documentation.

See [EXAMPLES.md](EXAMPLES.md) for additional usage examples.
