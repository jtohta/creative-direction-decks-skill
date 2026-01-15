from color_utils import hex_to_cmyk, hex_to_rgb, is_light_color

# Test hex_to_cmyk
cmyk = hex_to_cmyk("#0A1F44")
print(f"hex_to_cmyk('#0A1F44'): {cmyk}")
assert cmyk == {'c': 85, 'm': 54, 'y': 0, 'k': 73}, f"CMYK test failed: {cmyk}"

# Test hex_to_rgb
rgb = hex_to_rgb("#0A1F44")
print(f"hex_to_rgb('#0A1F44'): {rgb}")
assert rgb == (10, 31, 68), f"RGB test failed: {rgb}"

# Test is_light_color
assert is_light_color("#FFFFFF") == True, "White should be light"
assert is_light_color("#000000") == False, "Black should be dark"
print("is_light_color('#FFFFFF'): True")
print("is_light_color('#000000'): False")

print("\n✓ All color utility tests passed!")
