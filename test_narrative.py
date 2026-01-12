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
print("Generated Narrative:")
print("=" * 60)
print(narrative)
print("=" * 60)

# Verify structure
assert len(narrative) > 100, "Narrative should be substantial"
assert "Aqua Voyager" in narrative, "Narrative should include DJ name"
assert "\n\n" in narrative, "Narrative should have two paragraphs"

print("\n✓ Narrative generation test passed!")
