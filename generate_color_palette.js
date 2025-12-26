#!/usr/bin/env node
/**
 * DJ Brand Color Palette Generator
 * Generates a color palette with hex codes from DJ questionnaire data using meta-prompt approach.
 */

const fs = require("fs");
const path = require("path");

function generateColorPalettePrompt(data) {
  /**
   * Generate a meta-prompt that will be used to create a color palette with hex codes.
   * This returns a single prompt that an LLM can use to generate the brand color palette.
   */

  const dataStr = `
DJ Name: ${data.dj_name}
Music Style: ${data.music_style}
Core Descriptors: ${data.core_descriptors.join(', ')}
Emotional Target: ${data.emotional_target}
Physical Place: ${data.physical_place}
Color Preferences:
  - Primary: ${data.color_preferences.primary.join(', ')}
  - Accents: ${data.color_preferences.accents.join(', ')}
  - Mood: ${data.color_preferences.mood}
Visual References: ${data.visual_references.join(', ')}
Forms & Textures: ${data.forms_and_textures.join(', ')}
`;

  const metaPrompt = `Based on this DJ's brand identity, create a cohesive color palette with exact hex codes:

${dataStr}

Generate a color palette that captures this aesthetic. Choose ONE primary brand color (the most important defining color) and 5-7 supporting colors that work together harmoniously. Always include pure black (#000000) and pure white (#FFFFFF) in the palette.

The colors should reflect the mood, emotional target, and visual references provided. Consider the music style and descriptors when choosing the palette.

Also, generate a 2-paragraph descriptive text about the color palette (MAXIMUM 620 characters total including line breaks). The text should:
- Paragraph 1: Explain how the colors establish the brand's atmosphere and emotional resonance
- Paragraph 2: Highlight how accent colors create dynamic tension or punctuation
- Use specific color names from the palette
- Reference the DJ's descriptors, positioning, and music style
- Match the tone of this example: "This brand is grounded, intentional, and quietly powerful. Its core palette draws from earth tones..."

Return your response in this exact JSON format:
{
  "primary": {"name": "Descriptive Color Name", "hex": "#HEXCODE"},
  "palette": [
    {"name": "Descriptive Color Name", "hex": "#HEXCODE"},
    {"name": "Descriptive Color Name", "hex": "#HEXCODE"},
    {"name": "Descriptive Color Name", "hex": "#HEXCODE"},
    {"name": "Black", "hex": "#000000"},
    {"name": "White", "hex": "#FFFFFF"}
  ],
  "description": "Paragraph 1 text here.\\n\\nParagraph 2 text here."
}

CRITICAL: The "description" field must be exactly 620 characters or less (including the \\n\\n between paragraphs).
Make sure all hex codes are valid 6-character hex colors (e.g., #1A2B3C).
`;

  return metaPrompt;
}

function main() {
  if (process.argv.length !== 3) {
    console.log("Usage: node generate_color_palette.js <input.json>");
    process.exit(1);
  }

  const inputFile = process.argv[2];

  // Load input data
  const data = JSON.parse(fs.readFileSync(inputFile, "utf8"));

  // Generate meta-prompt
  const metaPrompt = generateColorPalettePrompt(data);

  // Output the meta-prompt
  const outputFile = path.basename(inputFile, path.extname(inputFile)) + "_color_palette_meta_prompt.txt";
  fs.writeFileSync(outputFile, metaPrompt);

  console.log(`✓ Color palette meta-prompt generated: ${outputFile}`);
  console.log("\nNext steps:");
  console.log("1. Copy the meta-prompt and paste it into an LLM (Claude, GPT-4, etc.)");
  console.log("2. The LLM will return JSON with the color palette and hex codes");
  console.log("3. Save the JSON as <dj_name>_colors.json");
  console.log("4. Use this in the PowerPoint generation");
}

if (require.main === module) {
  main();
}
