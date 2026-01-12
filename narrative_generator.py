"""
Brand narrative generation for DJ Brand Guide Generator.
Creates compelling 2-paragraph brand stories from DJ input data.
"""


def generate_brand_narrative(dj_data):
    """
    Generate a 2-paragraph brand narrative from DJ input data.

    Args:
        dj_data: Dict containing DJ brand questionnaire data with keys:
            - dj_name: DJ's name
            - physical_place: Environmental/spatial description
            - emotional_target: Target emotional experience
            - core_descriptors: List of brand adjectives
            - color_preferences: Dict with primary, accents, mood
            - forms_and_textures: List of texture descriptors
            - brand_positioning: Brand positioning statement (optional)
            - music_style: Genre/style description

    Returns:
        str: Two-paragraph brand narrative separated by double newline

    Example:
        >>> data = {
        ...     "dj_name": "Aqua Voyager",
        ...     "music_style": "Deep house",
        ...     "core_descriptors": ["oceanic", "mysterious", "hypnotic"],
        ...     ...
        ... }
        >>> narrative = generate_brand_narrative(data)
    """
    dj_name = dj_data['dj_name']
    place = dj_data['physical_place']
    emotional = dj_data['emotional_target']
    descriptors = dj_data['core_descriptors']
    colors_primary = dj_data['color_preferences']['primary']
    colors_accent = dj_data['color_preferences']['accents']
    textures = dj_data['forms_and_textures']
    positioning = dj_data.get('brand_positioning', 'a unique sonic journey')
    music_style = dj_data['music_style']

    # Paragraph 1: Brand world and visual language
    colors_primary_str = ', '.join(colors_primary)
    colors_accent_str = ', '.join(colors_accent)
    textures_str = ', '.join(textures)
    descriptors_str = ', '.join(descriptors[:3])  # First 3 descriptors

    # Capitalize first letter of colors string
    colors_primary_capitalized = colors_primary_str[0].upper() + colors_primary_str[1:]

    para1 = (
        f"{dj_name}'s world embodies {positioning}. This is {place} — {emotional}. "
        f"The visual language draws from {textures_str}, creating a sense of "
        f"{descriptors_str} that mirrors {music_style}. {colors_primary_capitalized} "
        f"establish the foundational atmosphere, while {colors_accent_str} punctuate "
        f"key moments of intensity and revelation."
    )

    # Paragraph 2: Aesthetic qualities and journey
    descriptor_0 = descriptors[0] if len(descriptors) > 0 else "pulls you in"
    descriptor_1 = descriptors[1] if len(descriptors) > 1 else "intentional"
    descriptor_2 = descriptors[2] if len(descriptors) > 2 else "immersive"

    para2 = (
        f"This aesthetic {descriptor_0}, inviting deeper exploration rather than "
        f"demanding immediate attention. Every element flows organically, creating an "
        f"experience that feels both {descriptor_1} and {descriptor_2}. It captures the "
        f"essence of {music_style} — where {emotional.lower()}, and the journey matters "
        f"more than the destination."
    )

    return f"{para1}\n\n{para2}"
