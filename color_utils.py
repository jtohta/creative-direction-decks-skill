"""
Color utility functions for DJ Brand Guide Generator.
Handles color conversions and formatting.
"""


def hex_to_cmyk(hex_color):
    """
    Convert hex color code to CMYK percentages.

    Args:
        hex_color: Hex color string (e.g., "#0A1F44" or "0A1F44")

    Returns:
        dict: CMYK values as percentages {c: int, m: int, y: int, k: int}

    Example:
        >>> hex_to_cmyk("#0A1F44")
        {'c': 85, 'm': 54, 'y': 0, 'k': 73}
    """
    # Strip the hash prefix if present (supports both "#RRGGBB" and "RRGGBB" formats)
    hex_color = hex_color.lstrip('#')

    # Parse hex string into RGB components, normalized to 0-1 range for CMYK math
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    # K (key/black) is derived from the brightest RGB channel
    k = 1 - max(r, g, b)

    if k == 1:
        # Pure black
        c = m = y = 0
    else:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)

    # Return as percentages (0-100)
    return {
        'c': round(c * 100),
        'm': round(m * 100),
        'y': round(y * 100),
        'k': round(k * 100)
    }


def hex_to_rgb(hex_color):
    """Convert hex color code to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )


def rgb_to_hex(r, g, b):
    """Convert RGB values to hex color string."""
    return "#{:02x}{:02x}{:02x}".format(r, g, b).upper()


def is_light_color(hex_color):
    """
    Determine if a color is light (for text color selection).
    Uses luminance calculation to determine if white or black text should be used.

    Args:
        hex_color: Hex color string (e.g., "#FFFFFF")

    Returns:
        bool: True if color is light (use black text), False if dark (use white text)

    Example:
        >>> is_light_color("#FFFFFF")
        True
        >>> is_light_color("#000000")
        False
    """
    r, g, b = hex_to_rgb(hex_color)

    # Calculate relative luminance
    # https://www.w3.org/TR/WCAG20-TECHS/G17.html
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    # Return True if luminance > 0.5 (light color)
    return luminance > 0.5
