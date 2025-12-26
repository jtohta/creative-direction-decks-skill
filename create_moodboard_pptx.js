#!/usr/bin/env node
/**
 * DJ Brand Moodboard PowerPoint Generator
 * Creates a single-slide moodboard presentation with 4 image prompt boxes and brand narrative
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");

function generateBrandNarrative(data) {
  const dj_name = data.dj_name;
  const place = data.physical_place;
  const emotional = data.emotional_target;
  const descriptors = data.core_descriptors;
  const colors_primary = data.color_preferences.primary;
  const colors_accent = data.color_preferences.accents;
  const textures = data.forms_and_textures;
  const positioning = data.brand_positioning || "a unique sonic journey";
  const music_style = data.music_style;

  // Paragraph 1
  const para1 = `${dj_name}'s world embodies ${positioning}. This is ${place} — ${emotional}. The visual language draws from ${textures.join(", ")}, creating a sense of ${descriptors.slice(0, 3).join(", ")} that mirrors ${music_style}. ${colors_primary.join(", ").charAt(0).toUpperCase() + colors_primary.join(", ").slice(1)} establish the foundational atmosphere, while ${colors_accent.join(", ")} punctuate key moments of intensity and revelation.`;

  // Paragraph 2
  const para2 = `This aesthetic ${descriptors[0] || "pulls you in"}, inviting deeper exploration rather than demanding immediate attention. Every element flows organically, creating an experience that feels both ${descriptors[1] || "intentional"} and ${descriptors[2] || "immersive"}. It captures the essence of ${music_style} — where ${emotional.toLowerCase()}, and the journey matters more than the destination.`;

  return `${para1}\n\n${para2}`;
}

async function createMoodboardSlide(prompts, data, outputFile) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9";
  pptx.author = "DJ Brand Guide Generator";
  pptx.title = `${data.dj_name} - Brand Moodboard`;

  const slide = pptx.addSlide();

  // Title
  slide.addText(`${data.dj_name.toUpperCase()} - OVERALL BRAND MOODBOARD`, {
    x: 0.5,
    y: 0.3,
    w: 9,
    h: 0.5,
    fontSize: 24,
    bold: true,
    color: "000000",
    fontFace: "Arial"
  });

  // Image prompt boxes - 2x2 grid layout
  const boxWidth = 4.25;
  const boxHeight = 2.0;
  const startY = 1.0;
  const leftX = 0.5;
  const rightX = 5.25;
  const gap = 0.3;

  // Top left - Prompt 1
  slide.addText(`[${prompts[0].label}]`, {
    x: leftX,
    y: startY,
    w: boxWidth,
    h: 0.3,
    fontSize: 10,
    bold: true,
    color: "666666",
    fontFace: "Arial"
  });
  slide.addText(prompts[0].prompt, {
    x: leftX,
    y: startY + 0.35,
    w: boxWidth,
    h: boxHeight - 0.35,
    fontSize: 9,
    color: "333333",
    fontFace: "Arial",
    valign: "top",
    fill: { color: "F5F5F5" },
    line: { color: "CCCCCC", width: 1 }
  });

  // Top right - Prompt 2
  slide.addText(`[${prompts[1].label}]`, {
    x: rightX,
    y: startY,
    w: boxWidth,
    h: 0.3,
    fontSize: 10,
    bold: true,
    color: "666666",
    fontFace: "Arial"
  });
  slide.addText(prompts[1].prompt, {
    x: rightX,
    y: startY + 0.35,
    w: boxWidth,
    h: boxHeight - 0.35,
    fontSize: 9,
    color: "333333",
    fontFace: "Arial",
    valign: "top",
    fill: { color: "F5F5F5" },
    line: { color: "CCCCCC", width: 1 }
  });

  // Bottom left - Prompt 3
  const bottomY = startY + boxHeight + gap;
  slide.addText(`[${prompts[2].label}]`, {
    x: leftX,
    y: bottomY,
    w: boxWidth,
    h: 0.3,
    fontSize: 10,
    bold: true,
    color: "666666",
    fontFace: "Arial"
  });
  slide.addText(prompts[2].prompt, {
    x: leftX,
    y: bottomY + 0.35,
    w: boxWidth,
    h: boxHeight - 0.35,
    fontSize: 9,
    color: "333333",
    fontFace: "Arial",
    valign: "top",
    fill: { color: "F5F5F5" },
    line: { color: "CCCCCC", width: 1 }
  });

  // Bottom right - Prompt 4
  slide.addText(`[${prompts[3].label}]`, {
    x: rightX,
    y: bottomY,
    w: boxWidth,
    h: 0.3,
    fontSize: 10,
    bold: true,
    color: "666666",
    fontFace: "Arial"
  });
  slide.addText(prompts[3].prompt, {
    x: rightX,
    y: bottomY + 0.35,
    w: boxWidth,
    h: boxHeight - 0.35,
    fontSize: 9,
    color: "333333",
    fontFace: "Arial",
    valign: "top",
    fill: { color: "F5F5F5" },
    line: { color: "CCCCCC", width: 1 }
  });

  // Brand narrative paragraph on the right side below the grid
  const narrativeY = bottomY + boxHeight + gap + 0.3;
  const narrative = generateBrandNarrative(data);
  
  slide.addText("BRAND NARRATIVE", {
    x: rightX,
    y: narrativeY,
    w: boxWidth,
    h: 0.25,
    fontSize: 12,
    bold: true,
    color: "000000",
    fontFace: "Arial"
  });
  
  slide.addText(narrative, {
    x: rightX,
    y: narrativeY + 0.3,
    w: boxWidth,
    h: 1.2,
    fontSize: 10,
    color: "333333",
    fontFace: "Arial",
    valign: "top"
  });

  await pptx.writeFile({ fileName: outputFile });
  console.log(`✓ PowerPoint created: ${outputFile}`);
}

function hexToCMYK(hex) {
  // Convert hex to RGB
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;

  // Convert RGB to CMYK
  const k = 1 - Math.max(r, g, b);
  const c = k === 1 ? 0 : (1 - r - k) / (1 - k);
  const m = k === 1 ? 0 : (1 - g - k) / (1 - k);
  const y = k === 1 ? 0 : (1 - b - k) / (1 - k);

  return {
    c: Math.round(c * 100),
    m: Math.round(m * 100),
    y: Math.round(y * 100),
    k: Math.round(k * 100)
  };
}

function generateColorPaletteBlurb(colors, data) {
  /**
   * Generate a dynamic color palette description based on the DJ's brand and colors.
   * Should be similar length to template example (~620 characters max to fit in layout).
   */
  
  const primaryColor = colors.primary.name;
  const paletteColorNames = colors.palette.map(c => c.name.toLowerCase()).filter(n => n !== "black" && n !== "white");
  const descriptors = data.core_descriptors;
  const positioning = data.brand_positioning || "sonic journey";
  const emotional = data.emotional_target.toLowerCase();
  const musicStyle = data.music_style;
  
  // Paragraph 1: Establish the palette foundation and emotional resonance
  const para1 = `This brand embodies ${descriptors.slice(0, 3).join(", ")} energy through its color palette. ${primaryColor} serves as the foundational anchor, establishing the core atmosphere of ${positioning}. Supporting tones — ${paletteColorNames.slice(0, 2).join(", ")} — create depth and nuance, evoking ${emotional}. These colors speak to a sonic identity rooted in ${musicStyle}. It's not trying to overwhelm — it invites exploration through carefully balanced contrast and mood.`;
  
  // Paragraph 2: Highlight the dynamic tension or key accent role
  const accentColors = paletteColorNames.slice(-2);
  const accentStr = accentColors.join(" and ").charAt(0).toUpperCase() + accentColors.join(" and ").slice(1);
  const para2 = `Within this carefully curated world, moments of intensity emerge. ${accentStr} cut through the atmosphere, adding punctuation and emotional peaks without disrupting the flow. Used strategically, these accents mark transitions and create visual rhythm that mirrors the ${descriptors[0] || "hypnotic"} quality of the music. In a brand defined by ${descriptors[1] || "depth"} and ${descriptors[2] || "immersion"}, these colors become signatures — symbols of dynamic energy within a landscape of intentional restraint.`;
  
  const fullText = `${para1}\n\n${para2}`;
  
  // Enforce character limit (620 chars max to match template)
  if (fullText.length > 620) {
    return fullText.substring(0, 617) + "...";
  }
  
  return fullText;
}

async function createColorPaletteSlide(colors, data, pptx) {
  const slide = pptx.addSlide();

  // Title (centered)
  slide.addText("BRAND COLOR PALETTE", {
    x: 0.5,
    y: 0.35,
    w: 8,
    h: 0.5,
    fontSize: 24,
    bold: true,
    color: "000000",
    fontFace: "Fjalla One",
    align: "center"
  });

  // Primary color - smaller rounded rectangle on left
  const primaryHex = colors.primary.hex.replace("#", "");
  const primaryCMYK = hexToCMYK(colors.primary.hex);
  
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.4,
    y: 1.15,
    w: 5.2,
    h: 2.3,
    fill: { color: primaryHex },
    line: { type: "none" }
  });

  // Primary color text overlay
  slide.addText(`[ PRIMARY POP COLOR]`, {
    x: 0.6,
    y: 1.45,
    w: 4.8,
    h: 0.35,
    fontSize: 20,
    bold: true,
    color: "FFFFFF",
    fontFace: "Fjalla One"
  });

  slide.addText(`${colors.primary.hex} C: ${primaryCMYK.c}% M: ${primaryCMYK.m}% Y:${primaryCMYK.y}% K:${primaryCMYK.k}%`, {
    x: 0.6,
    y: 1.82,
    w: 4.8,
    h: 0.25,
    fontSize: 12,
    color: "FFFFFF",
    fontFace: "Helvetica Neue"
  });

  // Palette colors - stacked rounded rectangles on right
  const barWidth = 3.6;
  const barHeight = 0.42;
  const barGap = 0.07;
  const startX = 6.0;
  let currentY = 1.15;

  colors.palette.forEach((color, i) => {
    const colorHex = color.hex.replace("#", "");
    const cmyk = hexToCMYK(color.hex);
    const isLight = color.hex.toLowerCase() === "#ffffff" || color.hex.toLowerCase() === "#fff";
    const textColor = isLight ? "000000" : "FFFFFF";

    // Color bar
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: startX,
      y: currentY,
      w: barWidth,
      h: barHeight,
      fill: { color: colorHex },
      line: isLight ? { color: "CCCCCC", width: 1 } : { type: "none" }
    });

    // Text on bar
    slide.addText(`${color.hex} C: ${cmyk.c}% M: ${cmyk.m}% Y:${cmyk.y}% K:${cmyk.k}%`, {
      x: startX + 0.12,
      y: currentY + 0.08,
      w: barWidth - 0.24,
      h: barHeight - 0.16,
      fontSize: 10,
      color: textColor,
      fontFace: "Helvetica Neue",
      valign: "middle"
    });

    currentY += barHeight + barGap;
  });

  // Use description from colors JSON (generated by LLM with character limit)
  const blurb = colors.description || generateColorPaletteBlurb(colors, data);

  slide.addText(blurb, {
    x: 0.4,
    y: 3.6,
    w: 5.2,
    h: 1.35,
    fontSize: 8.5,
    color: "000000",
    fontFace: "Helvetica Neue",
    valign: "top",
    breakLine: true
  });
}

async function createFullPresentation(prompts, colors, data, outputFile) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9";
  pptx.author = "DJ Brand Guide Generator";
  pptx.title = `${data.dj_name} - Brand Guide`;

  // Slide 1: Moodboard
  await createMoodboardSlideForDeck(pptx, prompts, data);

  // Slide 2: Color Palette (if colors provided)
  if (colors) {
    await createColorPaletteSlide(colors, data, pptx);
  }

  await pptx.writeFile({ fileName: outputFile });
  console.log(`✓ PowerPoint created: ${outputFile}`);
}

async function createMoodboardSlideForDeck(pptx, prompts, data) {
  const slide = pptx.addSlide();

  // Title
  slide.addText(`${data.dj_name.toUpperCase()} - OVERALL BRAND MOODBOARD`, {
    x: 0.5,
    y: 0.3,
    w: 9,
    h: 0.5,
    fontSize: 24,
    bold: true,
    color: "000000",
    fontFace: "Fjalla One"
  });

  // Image/prompt boxes - 2-column grid layout (supports arbitrary number of prompts)
  const boxWidth = 4.25;
  const boxHeight = 2.0;
  const startY = 1.0;
  const leftX = 0.5;
  const rightX = 5.25;
  const gap = 0.3;

  // Loop through all prompts dynamically
  prompts.forEach((prompt, i) => {
    const row = Math.floor(i / 2);
    const col = i % 2;
    const x = col === 0 ? leftX : rightX;
    const y = startY + row * (boxHeight + gap);

    // Add label
    slide.addText(`[${prompt.label}]`, {
      x: x,
      y: y,
      w: boxWidth,
      h: 0.3,
      fontSize: 10,
      bold: true,
      color: "666666",
      fontFace: "Fjalla One"
    });

    // Add image or text fallback
    const contentY = y + 0.35;
    const contentHeight = boxHeight - 0.35;

    if (prompt.image_path && fs.existsSync(prompt.image_path)) {
      // Image exists - display with 16:9 aspect ratio
      const imageAspect = 16 / 9;
      const boxAspect = boxWidth / contentHeight;

      let imgW, imgH, imgX, imgY;

      if (boxAspect > imageAspect) {
        // Box is wider than 16:9 - fit to height
        imgH = contentHeight;
        imgW = imgH * imageAspect;
        imgX = x + (boxWidth - imgW) / 2; // Center horizontally
        imgY = contentY;
      } else {
        // Box is taller than 16:9 - fit to width
        imgW = boxWidth;
        imgH = imgW / imageAspect;
        imgX = x;
        imgY = contentY + (contentHeight - imgH) / 2; // Center vertically
      }

      slide.addImage({
        path: prompt.image_path,
        x: imgX,
        y: imgY,
        w: imgW,
        h: imgH
      });
    } else {
      // No image - show text prompt (fallback)
      slide.addText(prompt.prompt, {
        x: x,
        y: contentY,
        w: boxWidth,
        h: contentHeight,
        fontSize: 9,
        color: "333333",
        fontFace: "Helvetica Neue",
        valign: "top",
        fill: { color: "F5F5F5" },
        line: { color: "CCCCCC", width: 1 }
      });
    }
  });

  // Brand narrative paragraph (positioned below the last row of prompts)
  const numRows = Math.ceil(prompts.length / 2);
  const lastRowY = startY + (numRows - 1) * (boxHeight + gap);
  const narrativeY = lastRowY + boxHeight + gap + 0.3;
  const narrative = generateBrandNarrative(data);
  
  slide.addText("BRAND NARRATIVE", {
    x: rightX,
    y: narrativeY,
    w: boxWidth,
    h: 0.25,
    fontSize: 12,
    bold: true,
    color: "000000",
    fontFace: "Fjalla One"
  });
  
  slide.addText(narrative, {
    x: rightX,
    y: narrativeY + 0.3,
    w: boxWidth,
    h: 1.2,
    fontSize: 10,
    color: "333333",
    fontFace: "Helvetica Neue",
    valign: "top"
  });
}

// Main execution
if (process.argv.length < 4 || process.argv.length > 5) {
  console.log("Usage: node create_moodboard_pptx.js <prompts.json> <dj_input.json> [colors.json]");
  console.log("\nExamples:");
  console.log("  node create_moodboard_pptx.js aqua_voyager_prompts.json aqua_voyager_input.json");
  console.log("  node create_moodboard_pptx.js aqua_voyager_prompts.json aqua_voyager_input.json aqua_voyager_colors.json");
  process.exit(1);
}

const promptsFile = process.argv[2];
const djInputFile = process.argv[3];
const colorsFile = process.argv[4];

// Load files
const prompts = JSON.parse(fs.readFileSync(promptsFile, "utf8")).prompts;
const djData = JSON.parse(fs.readFileSync(djInputFile, "utf8"));
const colors = colorsFile ? JSON.parse(fs.readFileSync(colorsFile, "utf8")) : null;

// Generate output filename
const outputFile = djData.dj_name.toLowerCase().replace(/\s+/g, "_") + "_brand_guide.pptx";

// Create the presentation
createFullPresentation(prompts, colors, djData, outputFile);
