#!/usr/bin/env node
/**
 * DJ Brand Moodboard Meta-Prompt Generator
 * Generates a professional brand moodboard slide from structured DJ questionnaire data.
 * Uses a meta-prompt approach to generate 4 distinct image prompts.
 */

const fs = require("fs");
const path = require("path");

function generateMetaPrompt(data) {
  /**
   * Generate a meta-prompt that will be used to create 4 distinct image generation prompts.
   * This returns a single prompt that an LLM can use to generate the 4 moodboard images.
   */

  // Serialize the data in a readable format
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
Brand Positioning: ${data.brand_positioning || 'N/A'}
Existing Visuals: ${data.existing_visuals || 'N/A'}
`;

  const metaPrompt = `You are creating a brand moodboard for a DJ. Based on the information below, generate 4 distinct AI image generation prompts that together tell a cohesive visual story for this artist's brand identity.

${dataStr}

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
{
  "prompts": [
    {"label": "LABEL HERE", "prompt": "detailed prompt here"},
    {"label": "LABEL HERE", "prompt": "detailed prompt here"},
    {"label": "LABEL HERE", "prompt": "detailed prompt here"},
    {"label": "LABEL HERE", "prompt": "detailed prompt here"}
  ]
}`;

  return metaPrompt;
}

function main() {
  if (process.argv.length !== 3) {
    console.log("Usage: node generate_moodboard.js <input.json>");
    process.exit(1);
  }

  const inputFile = process.argv[2];

  // Load input data
  const data = JSON.parse(fs.readFileSync(inputFile, "utf8"));

  // Generate meta-prompt
  const metaPrompt = generateMetaPrompt(data);

  // Output the meta-prompt
  const outputFile = path.basename(inputFile, path.extname(inputFile)) + "_meta_prompt.txt";
  fs.writeFileSync(outputFile, metaPrompt);

  console.log(`✓ Meta-prompt generated: ${outputFile}`);
  console.log("\nNext steps:");
  console.log("1. Copy the meta-prompt and paste it into an LLM (Claude, GPT-4, etc.)");
  console.log("2. The LLM will return JSON with 4 image prompts");
  console.log("3. Save the JSON response as prompts.json");
  console.log("4. Use FAL_KEY=your_key node generate_images.js to generate actual images");
}

if (require.main === module) {
  main();
}
