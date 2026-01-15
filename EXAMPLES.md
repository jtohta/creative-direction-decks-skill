# Usage Examples

Practical examples for using the DJ Brand Guide Generator skill.

## Example 1: Basic Usage

Generate a complete brand guide from structured data:

```python
from pptx_generator import create_brand_guide

# DJ input from questionnaire
dj_input = {
    "dj_name": "Aqua Voyager",
    "music_style": "Deep house, progressive, techno - journey sets",
    "core_descriptors": ["oceanic", "mysterious", "hypnotic", "building", "immersive"],
    "emotional_target": "Like they're exploring an alien underwater world",
    "physical_place": "Deep ocean, but not Earth's ocean",
    "color_preferences": {
        "primary": ["deep blue", "teal"],
        "accents": ["cyan", "purple"],
        "mood": "dark with glowing highlights"
    },
    "visual_references": ["bioluminescent creatures", "deep sea scenes", "nebulas"],
    "forms_and_textures": ["organic flowing forms", "liquid", "ethereal", "glowing"],
    "brand_positioning": "otherworldly explorer of sonic depths"
}

# Images (pre-generated via Fal.ai)
images = [
    {
        "label": "BIOLUMINESCENT JELLYFISH",
        "prompt": "Ethereal bioluminescent jellyfish floating in deep dark ocean...",
        "file_id": "file_123"
    },
    {
        "label": "DEEP OCEAN STRUCTURE",
        "prompt": "Abstract underwater architecture with flowing organic forms...",
        "file_id": "file_456"
    },
    {
        "label": "LIQUID FORMS",
        "prompt": "Liquid metal flowing through cosmic underwater environment...",
        "file_id": "file_789"
    },
    {
        "label": "COSMIC UNDERWATER",
        "prompt": "Alien underwater landscape with purple and cyan glowing elements...",
        "file_id": "file_abc"
    }
]

# Colors (pre-generated via Claude API)
colors = {
    "primary": {"name": "Deep Ocean Blue", "hex": "#0A1F44"},
    "palette": [
        {"name": "Electric Cyan", "hex": "#00D9FF"},
        {"name": "Purple Glow", "hex": "#8B00FF"},
        {"name": "Teal Depth", "hex": "#008B8B"},
        {"name": "Dark Blue", "hex": "#001F3F"},
        {"name": "Bright Cyan", "hex": "#00FFFF"},
        {"name": "Black", "hex": "#000000"},
        {"name": "White", "hex": "#FFFFFF"}
    ],
    "description": "This brand embodies oceanic, mysterious, hypnotic energy through its color palette. Deep Ocean Blue serves as the foundational anchor, establishing the core atmosphere of otherworldly exploration. Supporting tones — electric cyan, purple glow — create depth and nuance, evoking the feeling of exploring an alien underwater world. These colors speak to a sonic identity rooted in deep house and progressive techno.\\n\\nWithin this carefully curated world, moments of intensity emerge. Bright cyan and purple glow cut through the atmosphere, adding punctuation and emotional peaks without disrupting the flow."
}

# Generate PowerPoint
output_path = create_brand_guide(dj_input, images, colors)
print(f"Brand guide created: {output_path}")
```

---

## Example 2: Using Individual Utilities

Use color conversion utilities:

```python
from color_utils import hex_to_cmyk, hex_to_rgb, is_light_color

# Convert hex to CMYK
hex_color = "#0A1F44"
cmyk = hex_to_cmyk(hex_color)
print(f"{hex_color} in CMYK: C:{cmyk['c']}% M:{cmyk['m']}% Y:{cmyk['y']}% K:{cmyk['k']}%")
# Output: #0A1F44 in CMYK: C:85% M:54% Y:0% K:73%

# Convert hex to RGB
rgb = hex_to_rgb(hex_color)
print(f"{hex_color} in RGB: {rgb}")
# Output: #0A1F44 in RGB: (10, 31, 68)

# Determine text color
print(f"Use white text? {not is_light_color(hex_color)}")
# Output: Use white text? True
```

---

## Example 3: Generate Narrative Only

Generate just the brand narrative:

```python
from narrative_generator import generate_brand_narrative

dj_data = {
    "dj_name": "Aqua Voyager",
    "music_style": "Deep house, progressive, techno",
    "core_descriptors": ["oceanic", "mysterious", "hypnotic"],
    "emotional_target": "Like exploring an alien underwater world",
    "physical_place": "Deep ocean, but not Earth's ocean",
    "color_preferences": {
        "primary": ["deep blue", "teal"],
        "accents": ["cyan", "purple"],
        "mood": "dark with glowing highlights"
    },
    "forms_and_textures": ["organic flowing forms", "liquid", "ethereal"],
    "brand_positioning": "otherworldly explorer of sonic depths"
}

narrative = generate_brand_narrative(dj_data)
print(narrative)
```

**Output:**
```
Aqua Voyager's world embodies otherworldly explorer of sonic depths. This is Deep ocean, but not Earth's ocean — Like exploring an alien underwater world. The visual language draws from organic flowing forms, liquid, ethereal, creating a sense of oceanic, mysterious, hypnotic that mirrors Deep house, progressive, techno. Deep blue, teal establish the foundational atmosphere, while cyan, purple punctuate key moments of intensity and revelation.

This aesthetic oceanic, inviting deeper exploration rather than demanding immediate attention. Every element flows organically, creating an experience that feels both mysterious and hypnotic. It captures the essence of Deep house, progressive, techno — where like exploring an alien underwater world, and the journey matters more than the destination.
```

---

## Example 4: Local Testing with File Paths

Test locally with actual image files before uploading to Files API:

```python
from pptx_generator import create_brand_guide

# For local testing, include both file_id (for production) and path (for local)
images = [
    {
        "label": "BIOLUMINESCENT JELLYFISH",
        "prompt": "...",
        "file_id": None,  # Not yet uploaded
        "path": "./test_images/jellyfish.png"  # Local file
    },
    {
        "label": "DEEP OCEAN STRUCTURE",
        "prompt": "...",
        "file_id": None,
        "path": "./test_images/structure.png"
    },
    {
        "label": "LIQUID FORMS",
        "prompt": "...",
        "file_id": None,
        "path": "./test_images/liquid.png"
    },
    {
        "label": "COSMIC UNDERWATER",
        "prompt": "...",
        "file_id": None,
        "path": "./test_images/cosmic.png"
    }
]

# Generate locally
create_brand_guide(dj_input, images, colors, "test_output.pptx")
```

---

## Example 5: Handling Missing Images

The skill gracefully handles missing images by falling back to text:

```python
# Some images missing
images = [
    {
        "label": "BIOLUMINESCENT JELLYFISH",
        "prompt": "Detailed prompt about jellyfish...",
        "file_id": "file_123"  # Available
    },
    {
        "label": "DEEP OCEAN STRUCTURE",
        "prompt": "Detailed prompt about structures...",
        "file_id": None,  # Missing - will show text fallback
        "path": None
    },
    # ... more images
]

# Skill will:
# - Display image for items with valid file_id/path
# - Display styled text box with prompt for missing images
create_brand_guide(dj_input, images, colors)
```

---

## Example 6: Different DJ Styles

### Techno Producer

```python
dj_input = {
    "dj_name": "Circuit Breaker",
    "music_style": "Industrial techno, hard groove",
    "core_descriptors": ["mechanical", "relentless", "dystopian", "precise"],
    "emotional_target": "Like being inside a massive industrial complex",
    "physical_place": "Post-apocalyptic factory floor",
    "color_preferences": {
        "primary": ["gunmetal gray", "rust orange"],
        "accents": ["electric yellow", "deep red"],
        "mood": "harsh, metallic, with warning signs"
    },
    "visual_references": ["factory machinery", "warning lights", "brutalist architecture"],
    "forms_and_textures": ["angular metal", "riveted steel", "concrete"],
    "brand_positioning": "sonic architect of industrial futures"
}
```

### Ambient/Downtempo Artist

```python
dj_input = {
    "dj_name": "Velvet Dawn",
    "music_style": "Ambient, downtempo, chillout",
    "core_descriptors": ["serene", "ethereal", "meditative", "spacious"],
    "emotional_target": "Like floating in warm, soft clouds at sunrise",
    "physical_place": "Above the clouds at golden hour",
    "color_preferences": {
        "primary": ["soft pink", "warm beige"],
        "accents": ["gold", "lavender"],
        "mood": "gentle, warm, with soft highlights"
    },
    "visual_references": ["sunrise clouds", "soft fabrics", "morning light"],
    "forms_and_textures": ["flowing fabrics", "soft gradients", "gentle curves"],
    "brand_positioning": "curator of peaceful sonic landscapes"
}
```

---

## Example 7: Integration with Claude API

When using this skill via Claude API from FastAPI:

```python
import anthropic
import os
import json

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Prepare data
dj_input = {...}  # Your DJ data
images = [...]    # Images with file_ids
colors = {...}    # Color palette

# Call Claude API with skill
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{
            "type": "custom",
            "skill_id": os.environ["SKILL_ID"],
            "version": "latest"
        }]
    },
    messages=[{
        "role": "user",
        "content": f"""
        Create a DJ brand guide PowerPoint using the dj-brand-guide-generator skill.

        DJ Input:
        {json.dumps(dj_input, indent=2)}

        Image Prompts:
        {json.dumps(images, indent=2)}

        Colors:
        {json.dumps(colors, indent=2)}

        Generate a professional 2-slide PowerPoint.
        """
    }],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
)

# Extract file_id from response
for block in response.content:
    if block.type == "code_execution":
        for output in block.outputs:
            if hasattr(output, "file_id"):
                print(f"PowerPoint created: {output.file_id}")
```

---

## Tips and Best Practices

### Image Prompts
- Use descriptive 2-4 word labels in ALL CAPS
- Ensure prompts are detailed (100-150 words)
- Reference the DJ's visual references and textures
- Specify 16:9 aspect ratio in prompts for best results

### Colors
- Always include #000000 and #FFFFFF in palette
- Primary color should reflect core brand atmosphere
- Use 6-8 total palette colors
- Keep description under 620 characters (enforced)

### DJ Input
- Provide at least 3 core descriptors
- Be specific with emotional target and physical place
- Include brand positioning for better narrative quality
- List multiple visual references for richer context

### Testing
- Test locally with actual image files first
- Verify design fidelity matches JavaScript version
- Check font rendering on different systems
- Validate CMYK conversion for print specs

### Performance
- Pre-upload images to Files API before calling skill
- Use appropriate image resolution (2K recommended)
- Keep color palette to 6-8 colors for optimal layout
- Limit image prompts to 4-6 for best slide composition
