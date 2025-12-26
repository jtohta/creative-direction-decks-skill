#!/usr/bin/env python3
"""
DJ Brand Color Palette Generator
Generates a color palette with hex codes from DJ questionnaire data using meta-prompt approach.
"""

import json
import sys
from pathlib import Path


def generate_color_palette_prompt(data):
    """
    Generate a meta-prompt that will be used to create a color palette with hex codes.
    This returns a single prompt that an LLM can use to generate the brand color palette.
    """
    
    data_str = f"""
DJ Name: {data['dj_name']}
Music Style: {data['music_style']}
Core Descriptors: {', '.join(data['core_descriptors'])}
Emotional Target: {data['emotional_target']}
Physical Place: {data['physical_place']}
Color Preferences:
  - Primary: {', '.join(data['color_preferences']['primary'])}
  - Accents: {', '.join(data['color_preferences']['accents'])}
  - Mood: {data['color_preferences']['mood']}
Visual References: {', '.join(data['visual_references'])}
Forms & Textures: {', '.join(data['forms_and_textures'])}
"""
    
    meta_prompt = f"""Based on this DJ's brand identity, create a cohesive color palette with exact hex codes:

{data_str}

Generate a color palette that captures this aesthetic. Choose ONE primary brand color (the most important defining color) and 5-7 supporting colors that work together harmoniously. Always include pure black (#000000) and pure white (#FFFFFF) in the palette.

The colors should reflect the mood, emotional target, and visual references provided. Consider the music style and descriptors when choosing the palette.

Also, generate a 2-paragraph descriptive text about the color palette (MAXIMUM 620 characters total including line breaks). The text should:
- Paragraph 1: Explain how the colors establish the brand's atmosphere and emotional resonance
- Paragraph 2: Highlight how accent colors create dynamic tension or punctuation
- Use specific color names from the palette
- Reference the DJ's descriptors, positioning, and music style
- Match the tone of this example: "This brand is grounded, intentional, and quietly powerful. Its core palette draws from earth tones..."

Return your response in this exact JSON format:
{{
  "primary": {{"name": "Descriptive Color Name", "hex": "#HEXCODE"}},
  "palette": [
    {{"name": "Descriptive Color Name", "hex": "#HEXCODE"}},
    {{"name": "Descriptive Color Name", "hex": "#HEXCODE"}},
    {{"name": "Descriptive Color Name", "hex": "#HEXCODE"}},
    {{"name": "Black", "hex": "#000000"}},
    {{"name": "White", "hex": "#FFFFFF"}}
  ],
  "description": "Paragraph 1 text here.\\n\\nParagraph 2 text here."
}}

CRITICAL: The "description" field must be exactly 620 characters or less (including the \\n\\n between paragraphs).
Make sure all hex codes are valid 6-character hex colors (e.g., #1A2B3C).
"""
    
    return meta_prompt


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_color_palette.py <input.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Load input data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Generate meta-prompt
    meta_prompt = generate_color_palette_prompt(data)
    
    # Output the meta-prompt
    output_file = Path(input_file).stem + "_color_palette_meta_prompt.txt"
    with open(output_file, 'w') as f:
        f.write(meta_prompt)
    
    print(f"✓ Color palette meta-prompt generated: {output_file}")
    print("\nNext steps:")
    print("1. Copy the meta-prompt and paste it into an LLM (Claude, GPT-4, etc.)")
    print("2. The LLM will return JSON with the color palette and hex codes")
    print("3. Save the JSON as <dj_name>_colors.json")
    print("4. Use this in the PowerPoint generation")


if __name__ == "__main__":
    main()
