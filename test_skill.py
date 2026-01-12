#!/usr/bin/env python3
"""
Test script for DJ Brand Guide Generator skill.
Requires python-pptx to be installed.

Usage:
    python3 test_skill.py
"""

import sys
import os

# Add skill directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pptx_generator import create_brand_guide
    from color_utils import hex_to_cmyk, hex_to_rgb, is_light_color
    from narrative_generator import generate_brand_narrative
    print("✓ All modules imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nPlease install python-pptx:")
    print("  pip3 install python-pptx")
    sys.exit(1)


def test_color_utils():
    """Test color utility functions."""
    print("\n=== Testing Color Utilities ===")

    # Test hex_to_cmyk
    cmyk = hex_to_cmyk("#0A1F44")
    print(f"hex_to_cmyk('#0A1F44'): {cmyk}")
    assert cmyk == {'c': 85, 'm': 54, 'y': 0, 'k': 73}, f"Expected c:85, m:54, y:0, k:73, got {cmyk}"
    print("✓ hex_to_cmyk test passed")

    # Test hex_to_rgb
    rgb = hex_to_rgb("#0A1F44")
    print(f"hex_to_rgb('#0A1F44'): {rgb}")
    assert rgb == (10, 31, 68), f"Expected (10, 31, 68), got {rgb}"
    print("✓ hex_to_rgb test passed")

    # Test is_light_color
    assert is_light_color("#FFFFFF") == True, "White should be light"
    assert is_light_color("#000000") == False, "Black should be dark"
    assert is_light_color("#0A1F44") == False, "Dark blue should be dark"
    print("✓ is_light_color test passed")


def test_narrative_generator():
    """Test brand narrative generation."""
    print("\n=== Testing Narrative Generator ===")

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
    print(f"Generated narrative (first 100 chars): {narrative[:100]}...")
    assert len(narrative) > 100, "Narrative should be substantial"
    assert "Aqua Voyager" in narrative, "Narrative should include DJ name"
    assert "\n\n" in narrative, "Narrative should have two paragraphs"
    print("✓ Narrative generation test passed")


def test_pptx_generator():
    """Test PowerPoint generation with sample data."""
    print("\n=== Testing PowerPoint Generator ===")

    # Sample data from aqua_voyager example
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

    # Image prompts (without actual files - will use text fallback)
    image_prompts = [
        {
            "label": "BIOLUMINESCENT JELLYFISH",
            "prompt": "Ethereal bioluminescent jellyfish floating in deep dark ocean with glowing tendrils.",
            "file_id": None
        },
        {
            "label": "DEEP OCEAN STRUCTURE",
            "prompt": "Abstract underwater architecture with flowing organic forms and teal lighting.",
            "file_id": None
        },
        {
            "label": "LIQUID FORMS",
            "prompt": "Liquid metal flowing through cosmic underwater environment with purple glow.",
            "file_id": None
        },
        {
            "label": "COSMIC UNDERWATER",
            "prompt": "Alien underwater landscape with purple and cyan glowing elements and nebula-like patterns.",
            "file_id": None
        }
    ]

    # Colors
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
        "description": "This brand embodies oceanic, mysterious, hypnotic energy through its color palette. Deep Ocean Blue serves as the foundational anchor, establishing the core atmosphere of otherworldly exploration. Supporting tones — electric cyan, purple glow — create depth and nuance, evoking the feeling of exploring an alien underwater world. These colors speak to a sonic identity rooted in deep house and progressive techno.\n\nWithin this carefully curated world, moments of intensity emerge. Bright cyan and purple glow cut through the atmosphere, adding punctuation and emotional peaks without disrupting the flow."
    }

    # Generate PowerPoint
    output_path = "test_brand_guide.pptx"
    result = create_brand_guide(dj_input, image_prompts, colors, output_path)

    assert os.path.exists(result), f"PowerPoint file should be created at {result}"
    print(f"✓ PowerPoint created successfully: {result}")

    # Check file size (should be > 10KB)
    file_size = os.path.getsize(result)
    print(f"  File size: {file_size:,} bytes")
    assert file_size > 10000, f"File should be > 10KB, got {file_size} bytes"
    print("✓ PowerPoint generation test passed")

    return result


def main():
    """Run all tests."""
    print("=" * 60)
    print("DJ Brand Guide Generator - Test Suite")
    print("=" * 60)

    try:
        test_color_utils()
        test_narrative_generator()
        output_file = test_pptx_generator()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print(f"\nGenerated test file: {output_file}")
        print("Open this file to verify the design fidelity.")

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
