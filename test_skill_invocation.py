#!/usr/bin/env python3
"""
Test skill invocation directly via Anthropic API.
Bypasses the full API pipeline for faster testing (~30-60s vs 5+ min).

Usage:
    ANTHROPIC_API_KEY=your_key python3 test_skill_invocation.py
"""
import os
import sys
import json

try:
    from anthropic import Anthropic
except ImportError:
    print("Please install anthropic: pip install anthropic")
    sys.exit(1)

# Configuration
SKILL_ID = "skill_016YNozPyDDJvhJwmzpRfRah"
MODEL = "claude-sonnet-4-20250514"

# Minimal test data with brand_narrative
TEST_DJ_INPUT = {
    "dj_name": "Test Artist",
    "music_style": "Electronic techno",
    "core_descriptors": ["dark", "minimal", "hypnotic"],
    "emotional_target": "a trance-like state of focused intensity",
    "physical_place": "an underground concrete warehouse",
    "color_preferences": {
        "primary": ["black", "charcoal"],
        "accents": ["red", "orange"],
        "mood": "dark industrial with warm accents"
    },
    "visual_references": ["industrial architecture", "brutalist design"],
    "forms_and_textures": ["geometric", "concrete", "metal"],
    "brand_positioning": "underground techno pioneer",
    "brand_narrative": "TEST NARRATIVE PARAGRAPH ONE - This text should appear on the moodboard slide in the right column. The narrative lives at the intersection of industrial aesthetics and hypnotic rhythm.\n\nTEST NARRATIVE PARAGRAPH TWO - This is the second paragraph that continues the brand story. If you see this text, the brand_narrative field is being passed correctly from dj_input to the PowerPoint."
}

TEST_COLORS = {
    "primary": {"name": "Obsidian Black", "hex": "#0A0A0A"},
    "palette": [
        {"name": "Rust Orange", "hex": "#D35400"},
        {"name": "Charcoal", "hex": "#2C2C2C"},
        {"name": "Concrete Gray", "hex": "#7F8C8D"},
        {"name": "Deep Red", "hex": "#C0392B"},
        {"name": "Black", "hex": "#000000"},
        {"name": "White", "hex": "#FFFFFF"}
    ],
    "description": "A dark industrial palette anchored by obsidian black with warm rust accents. This color story speaks to underground techno's raw aesthetic.\n\nThe contrast between cold concrete tones and warm orange creates visual tension that mirrors the music's intensity."
}


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Usage: ANTHROPIC_API_KEY=your_key python3 test_skill_invocation.py")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    print("=" * 60)
    print("Testing Skill Invocation with brand_narrative")
    print("=" * 60)
    print(f"Skill ID: {SKILL_ID}")
    print(f"Model: {MODEL}")
    print(f"DJ Name: {TEST_DJ_INPUT['dj_name']}")
    print(f"Brand Narrative (first 80 chars): {TEST_DJ_INPUT['brand_narrative'][:80]}...")
    print()

    # Build the prompt
    prompt = f"""Create a DJ brand guide PowerPoint using this data:

DJ Input:
{json.dumps(TEST_DJ_INPUT, indent=2)}

Colors:
{json.dumps(TEST_COLORS, indent=2)}

Please use the dj-brand-guide-generator skill to create a professional 2-slide PowerPoint presentation.
IMPORTANT: The dj_input includes a 'brand_narrative' field - make sure to pass this to the create_brand_guide function so it appears on the moodboard slide.
Output the file to "test_invocation_output.pptx".
"""

    print("Invoking skill (this may take 30-60 seconds)...")
    print()

    try:
        # Use streaming to handle long-running operations
        with client.beta.messages.stream(
            model=MODEL,
            max_tokens=8192,
            betas=["code-execution-2025-08-25", "skills-2025-10-02"],
            container={
                "skills": [{
                    "type": "custom",
                    "skill_id": SKILL_ID,
                    "version": "latest"
                }]
            },
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            response = stream.get_final_message()

        print("Response received!")
        print()

        # Check for file output
        file_id = None
        for item in response.content:
            if hasattr(item, 'type'):
                print(f"Content block type: {item.type}")
                if item.type == 'text':
                    print(f"Text: {item.text[:200]}..." if len(item.text) > 200 else f"Text: {item.text}")
                elif 'code_execution_tool_result' in item.type:
                    # Check for file outputs in various result types
                    if hasattr(item, 'content'):
                        for content in item.content:
                            print(f"  - Content type: {getattr(content, 'type', 'unknown')}")
                            if hasattr(content, 'type') and content.type == 'file':
                                file_id = content.file_id
                                print(f"  - Output file_id: {file_id}")
                            elif hasattr(content, 'file_id'):
                                file_id = content.file_id
                                print(f"  - Output file_id (direct): {file_id}")
                # Also check bash_code_execution_tool_result
                elif item.type == 'bash_code_execution_tool_result':
                    if hasattr(item, 'content'):
                        for content in item.content:
                            print(f"  - Bash content type: {getattr(content, 'type', 'unknown')}")
                            if hasattr(content, 'file_id'):
                                file_id = content.file_id
                                print(f"  - Bash file_id: {file_id}")
                # Print any other attributes that might contain file info
                for attr in ['file_id', 'files', 'output_files']:
                    if hasattr(item, attr):
                        print(f"  - {attr}: {getattr(item, attr)}")

        if file_id:
            print()
            print("=" * 60)
            print(f"SUCCESS: PowerPoint generated with file_id: {file_id}")
            print("=" * 60)
            print()
            print("To download and verify:")
            print(f"  1. Download the file using the Files API")
            print(f"  2. Open the PowerPoint and check slide 2 (moodboard)")
            print(f"  3. Verify 'BRAND NARRATIVE' section appears on the right")
            print(f"  4. Verify it contains: 'TEST NARRATIVE PARAGRAPH ONE'")
        else:
            print()
            print("WARNING: No file_id found in response.")
            print("Check the response content above for details.")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
