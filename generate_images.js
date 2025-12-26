#!/usr/bin/env node
/**
 * DJ Brand Image Generator using Fal.ai Nano Banana Pro
 * Generates actual images from prompts using Fal.ai API
 */

const fs = require("fs");
const path = require("path");
const https = require("https");
const { fal } = require("@fal-ai/client");

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function downloadImage(url, filepath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(filepath);
    https.get(url, response => {
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', err => {
      fs.unlink(filepath, () => reject(err));
    });
  });
}

async function generateImage(prompt, outputPath, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      console.log(`  Generating image (attempt ${i + 1}/${retries})...`);

      // Set credentials globally
      fal.config({ credentials: process.env.FAL_KEY });

      const result = await fal.subscribe("fal-ai/nano-banana-pro", {
        input: {
          prompt: prompt
        }
      });

      const imageUrl = result.data.images[0].url;
      console.log(`  Downloading from: ${imageUrl}`);

      await downloadImage(imageUrl, outputPath);
      console.log(`  ✓ Saved to: ${outputPath}`);

      return true;
    } catch (error) {
      if (i < retries - 1) {
        const waitTime = Math.pow(2, i) * 1000; // 1s, 2s, 4s
        console.log(`  ✗ Error: ${error.message}`);
        console.log(`  Retrying in ${waitTime/1000}s...`);
        await sleep(waitTime);
      } else {
        console.error(`  ✗ Failed after ${retries} retries: ${error.message}`);
        throw error; // Re-throw on final failure (mandatory generation)
      }
    }
  }
  return false;
}

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '_')
    .replace(/^-+|-+$/g, '');
}

async function main() {
  if (process.argv.length !== 4) {
    console.log("Usage: FAL_KEY=your_key node generate_images.js <prompts.json> <dj_input.json>");
    console.log("\nExample:");
    console.log("  FAL_KEY=abc123 node generate_images.js aqua_voyager_prompts.json aqua_voyager_input.json");
    console.log("\nNote: FAL_KEY environment variable is required.");
    process.exit(1);
  }

  // Check for FAL_KEY
  if (!process.env.FAL_KEY) {
    console.error("✗ Error: FAL_KEY environment variable is not set.");
    console.error("Set it with: export FAL_KEY=your_api_key");
    console.error("Or run: FAL_KEY=your_key node generate_images.js ...");
    process.exit(1);
  }

  const promptsFile = process.argv[2];
  const djInputFile = process.argv[3];

  // Load files
  console.log(`Loading ${promptsFile}...`);
  const promptsData = JSON.parse(fs.readFileSync(promptsFile, "utf8"));
  const prompts = promptsData.prompts;

  console.log(`Loading ${djInputFile}...`);
  const djData = JSON.parse(fs.readFileSync(djInputFile, "utf8"));
  const djName = djData.dj_name.toLowerCase().replace(/\s+/g, "_");

  console.log(`\nGenerating ${prompts.length} images for ${djData.dj_name}...`);
  console.log("This may take a few minutes depending on API response time.\n");

  let successCount = 0;
  let failedPrompts = [];

  // Generate images for each prompt
  for (let i = 0; i < prompts.length; i++) {
    const prompt = prompts[i];
    const labelSlug = slugify(prompt.label);
    const filename = `${djName}_${labelSlug}.png`;
    const filepath = path.join(path.dirname(promptsFile), filename);

    console.log(`[${i + 1}/${prompts.length}] ${prompt.label}`);

    // Check if image already exists (caching)
    if (fs.existsSync(filepath)) {
      console.log(`  ✓ Image already exists (cached): ${filepath}`);
      prompt.image_path = filepath;
      successCount++;
      continue;
    }

    try {
      await generateImage(prompt.prompt, filepath);
      prompt.image_path = filepath;
      successCount++;
    } catch (error) {
      failedPrompts.push({ label: prompt.label, error: error.message });
      console.error(`  ✗ FAILED: Could not generate image for "${prompt.label}"`);
      // Don't add image_path if generation failed
    }

    console.log(""); // Empty line between prompts
  }

  // Update prompts JSON with image paths
  console.log(`Updating ${promptsFile} with image paths...`);
  fs.writeFileSync(promptsFile, JSON.stringify(promptsData, null, 2));

  // Print summary
  console.log("\n" + "=".repeat(60));
  console.log(`✓ ${successCount}/${prompts.length} images generated successfully`);

  if (failedPrompts.length > 0) {
    console.log(`\n✗ ${failedPrompts.length} images failed to generate:`);
    failedPrompts.forEach(({ label, error }) => {
      console.log(`  - ${label}: ${error}`);
    });
    console.log("\nError: Image generation is mandatory. All images must be generated successfully.");
    console.log("Please check your FAL_KEY and try again.");
    process.exit(1);
  }

  console.log("\nNext steps:");
  console.log(`1. Run: node generate_color_palette.js ${djInputFile}`);
  console.log("2. Copy the color palette meta-prompt to an LLM");
  console.log("3. Save the response as <dj_name>_colors.json");
  console.log("4. Run: node create_moodboard_pptx.js <prompts.json> <input.json> <colors.json>");
}

if (require.main === module) {
  main().catch(error => {
    console.error("\n✗ Fatal error:", error.message);
    process.exit(1);
  });
}
