# API Reference

Complete API documentation for the DJ Brand Guide Generator skill.

## Modules

### pptx_generator

Main PowerPoint generation module.

#### `create_brand_guide(dj_input, image_prompts, colors, output_path="brand_guide.pptx")`

Create a complete 2-slide DJ brand guide PowerPoint.

**Parameters:**
- `dj_input` (dict): DJ questionnaire data containing:
  - `dj_name` (str): DJ's name
  - `music_style` (str): Genre/style description
  - `core_descriptors` (list[str]): Brand adjectives (min 3)
  - `emotional_target` (str): Target emotional experience
  - `physical_place` (str): Environmental/spatial description
  - `color_preferences` (dict): With keys `primary`, `accents`, `mood`
  - `visual_references` (list[str]): Visual inspiration references
  - `forms_and_textures` (list[str]): Texture descriptors
  - `brand_positioning` (str, optional): Brand positioning statement
  - `existing_visuals` (str, optional): Existing visual assets
- `image_prompts` (list[dict]): List of image prompt dicts containing:
  - `label` (str): Image label (e.g., "BIOLUMINESCENT JELLYFISH")
  - `prompt` (str): Full image generation prompt
  - `file_id` (str): Anthropic Files API file ID
  - `path` (str, optional): Local file path for testing
- `colors` (dict): Color palette data containing:
  - `primary` (dict): Primary color with `name` and `hex` keys
  - `palette` (list[dict]): 6-8 colors with `name` and `hex` keys (must include #000000 and #FFFFFF)
  - `description` (str): 2-paragraph description (max 620 characters)
- `output_path` (str, optional): Output file path. Default: "brand_guide.pptx"

**Returns:**
- `str`: Path to the created PowerPoint file

**Example:**
```python
output = create_brand_guide(dj_input, images, colors, "my_guide.pptx")
```

---

#### `create_moodboard_slide(prs, layout, dj_input, image_prompts)`

Create Slide 1: Brand Moodboard with 2x2 image grid and narrative.

**Parameters:**
- `prs` (Presentation): python-pptx Presentation object
- `layout` (SlideLayout): Blank slide layout
- `dj_input` (dict): DJ questionnaire data
- `image_prompts` (list[dict]): Image prompt dicts with file_id or path

**Slide Layout:**
- Title at (0.5", 0.3") - 9" × 0.5"
- Images in 2-column grid starting at (0.5", 1.0")
  - Left column: x=0.5"
  - Right column: x=5.25"
  - Each box: 4.25" × 2.0"
  - Gap between rows: 0.3"
- Brand narrative below last row of images

---

#### `create_color_palette_slide(prs, layout, dj_input, colors)`

Create Slide 2: Color Palette with primary block and palette bars.

**Parameters:**
- `prs` (Presentation): python-pptx Presentation object
- `layout` (SlideLayout): Blank slide layout
- `dj_input` (dict): DJ questionnaire data
- `colors` (dict): Color palette data

**Slide Layout:**
- Title at (0.5", 0.35") - 8" × 0.5", centered
- Primary color block at (0.4", 1.15") - 5.2" × 2.3"
- Palette bars at (6.0", 1.15") - 3.6" × 0.42" each
  - Gap between bars: 0.07"
- Color description at (0.4", 3.6") - 5.2" × 1.35"

---

### color_utils

Color conversion and formatting utilities.

#### `hex_to_cmyk(hex_color)`

Convert hex color code to CMYK percentages.

**Parameters:**
- `hex_color` (str): Hex color string (e.g., "#0A1F44" or "0A1F44")

**Returns:**
- `dict`: CMYK values as percentages `{c: int, m: int, y: int, k: int}`

**Example:**
```python
cmyk = hex_to_cmyk("#0A1F44")
# Returns: {'c': 85, 'm': 54, 'y': 0, 'k': 73}
```

**Formula:**
1. Convert hex to RGB (0-1 range)
2. Calculate K = 1 - max(R, G, B)
3. If K == 1: C = M = Y = 0
4. Else: C = (1 - R - K) / (1 - K), etc.
5. Round to integers (0-100)

---

#### `hex_to_rgb(hex_color)`

Convert hex color code to RGB tuple.

**Parameters:**
- `hex_color` (str): Hex color string

**Returns:**
- `tuple`: RGB values (r, g, b) in range 0-255

**Example:**
```python
rgb = hex_to_rgb("#0A1F44")
# Returns: (10, 31, 68)
```

---

#### `is_light_color(hex_color)`

Determine if a color is light (for text color selection).

**Parameters:**
- `hex_color` (str): Hex color string

**Returns:**
- `bool`: True if light color (use black text), False if dark (use white text)

**Formula:**
Uses relative luminance calculation:
```
luminance = (0.299 * R + 0.587 * G + 0.114 * B) / 255
is_light = luminance > 0.5
```

**Example:**
```python
is_light_color("#FFFFFF")  # True (use black text)
is_light_color("#000000")  # False (use white text)
```

---

### narrative_generator

Brand narrative generation utilities.

#### `generate_brand_narrative(dj_data)`

Generate a 2-paragraph brand narrative from DJ input data.

**Parameters:**
- `dj_data` (dict): DJ questionnaire data (see create_brand_guide for structure)

**Returns:**
- `str`: Two-paragraph narrative separated by double newline

**Narrative Structure:**
- **Paragraph 1**: Brand world and visual language
  - References place, emotional target, textures, descriptors
  - Mentions primary and accent colors
  - Connects to music style
- **Paragraph 2**: Aesthetic qualities and journey
  - Uses core descriptors to describe experience
  - Emphasizes exploration and flow
  - Reinforces connection to music style

**Example:**
```python
narrative = generate_brand_narrative(dj_input)
# Returns:
# "Aqua Voyager's world embodies otherworldly explorer of sonic depths.
# This is Deep ocean, but not Earth's ocean — Like they're exploring
# an alien underwater world...
#
# This aesthetic oceanic, inviting deeper exploration rather than
# demanding immediate attention..."
```

---

## Data Structure Schemas

### DJ Input Schema

```python
{
    "dj_name": str,                      # Required
    "music_style": str,                  # Required
    "core_descriptors": [str, ...],      # Required, min 3 items
    "emotional_target": str,             # Required
    "physical_place": str,               # Required
    "color_preferences": {               # Required
        "primary": [str, ...],
        "accents": [str, ...],
        "mood": str
    },
    "visual_references": [str, ...],     # Required
    "forms_and_textures": [str, ...],    # Required
    "brand_positioning": str,            # Optional, default: "a unique sonic journey"
    "existing_visuals": str              # Optional
}
```

### Image Prompts Schema

```python
[
    {
        "label": str,        # Required, 2-4 words, ALL CAPS
        "prompt": str,       # Required, detailed prompt
        "file_id": str,      # Required for skill execution
        "path": str          # Optional, for local testing
    },
    ...  # 4 or more items
]
```

### Colors Schema

```python
{
    "primary": {
        "name": str,         # Color name
        "hex": str           # Hex code with #
    },
    "palette": [
        {
            "name": str,     # Color name
            "hex": str       # Hex code with #
        },
        ...  # 6-8 items, MUST include #000000 and #FFFFFF
    ],
    "description": str       # Max 620 characters, 2 paragraphs
}
```

---

## Design Specifications

### Typography

- **Headers**: Fjalla One, 12-24pt, bold
- **Body Text**: Helvetica Neue, 8.5-10pt
- **Labels**: Fjalla One, 10pt, bold
- **Color Codes**: Helvetica Neue, 10-12pt

### Layout

- **Slide Size**: 10" × 5.625" (16:9 aspect ratio)
- **Margins**: 0.4-0.6" on all sides
- **Grid**: 2-column layout for images
- **Spacing**: 0.3" gaps between elements

### Colors

- **Title Text**: #000000 (black)
- **Body Text**: #333333 (dark gray)
- **Label Text**: #666666 (medium gray)
- **Background Fill**: #F5F5F5 (light gray)
- **Border**: #CCCCCC (border gray), 1pt width

### Shapes

- **Rounded Rectangles**: MSO_SHAPE.ROUNDED_RECTANGLE
- **Image Boxes**: 4.25" × 2.0" (16:9 ratio when possible)
- **Color Bars**: 3.6" × 0.42"
- **Primary Block**: 5.2" × 2.3"

---

## Error Handling

### Missing Images

If an image file_id or path is not available, the skill automatically falls back to displaying the text prompt in a styled text box with:
- Light gray background (#F5F5F5)
- Gray border (#CCCCCC)
- 9pt Helvetica Neue text

### Invalid Colors

If a hex color is malformed:
- Functions will attempt to strip # and process
- Invalid hex strings may raise ValueError
- Ensure colors match pattern: `#[0-9A-Fa-f]{6}`

### Font Fallback

If "Fjalla One" is not available in the environment:
- python-pptx will fall back to system default sans-serif
- For production, ensure fonts are installed or accept fallback

---

## Performance Notes

- **Slide Generation**: ~1-2 seconds per slide
- **Image Processing**: Minimal overhead (file references only)
- **CMYK Conversion**: Negligible (simple math operations)
- **Total Execution**: ~3-5 seconds for 2-slide deck

---

## Limitations

- Network access disabled (images must be pre-uploaded to Files API)
- Python 3.11 only (no Node.js)
- 5GB workspace storage limit
- Font rendering depends on environment
- No animation or transition support (static slides only)
