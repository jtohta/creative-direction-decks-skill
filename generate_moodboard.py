#!/usr/bin/env python3
"""
DJ Brand Moodboard Generator
Generates a professional brand moodboard slide from structured DJ questionnaire data.
Uses a meta-prompt approach to generate 4 distinct image prompts.
"""

import json
import sys
from pathlib import Path


def generate_meta_prompt(data):
    """
    Generate a meta-prompt that will be used to create 4 distinct image generation prompts.
    This returns a single prompt that an LLM can use to generate the 4 moodboard images.
    """
    
    # Serialize the data in a readable format
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
Brand Positioning: {data.get('brand_positioning', 'N/A')}
Existing Visuals: {data.get('existing_visuals', 'N/A')}
"""
    
    meta_prompt = f"""You are creating a brand moodboard for a DJ. Based on the information below, generate 4 distinct AI image generation prompts that together tell a cohesive visual story for this artist's brand identity.

{data_str}

The 4 prompts should:
- Work together to communicate this DJ's unique aesthetic world
- Each capture a different visual angle or aspect of their brand
- Use the colors, textures, descriptors, and references provided
- Be specific enough for an AI image generator to create compelling visuals
- Together create visual cohesion (they should feel like they belong in the same universe)

For each prompt, provide:
1. A short label (2-4 words, ALL CAPS) that describes what this image represents
2. The full image generation prompt (detailed, specific, incorporating the aesthetic elements)

Return your response in this exact JSON format:
{{
  "prompts": [
    {{"label": "LABEL HERE", "prompt": "detailed prompt here"}},
    {{"label": "LABEL HERE", "prompt": "detailed prompt here"}},
    {{"label": "LABEL HERE", "prompt": "detailed prompt here"}},
    {{"label": "LABEL HERE", "prompt": "detailed prompt here"}}
  ]
}}"""
    
    return meta_prompt


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_moodboard.py <input.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Load input data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Generate meta-prompt
    meta_prompt = generate_meta_prompt(data)
    
    # Output the meta-prompt
    output_file = Path(input_file).stem + "_meta_prompt.txt"
    with open(output_file, 'w') as f:
        f.write(meta_prompt)
    
    print(f"✓ Meta-prompt generated: {output_file}")
    print("\nNext steps:")
    print("1. Copy the meta-prompt and paste it into an LLM (Claude, GPT-4, etc.)")
    print("2. The LLM will return JSON with 4 image prompts")
    print("3. Use those prompts to generate images")
    print("4. Create the PowerPoint slide with the images")


if __name__ == "__main__":
    main()
