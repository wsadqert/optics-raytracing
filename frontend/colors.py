from basics import Ray


def hex_to_rgb(hex_color):
	"""Convert hex color to RGB tuple."""
	hex_color = hex_color.lstrip('#')
	return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
	"""Convert RGB tuple to hex color."""
	return '#' + ''.join(f'{c:02x}' for c in rgb_color)

def weighted_mean_color(hex_color1, hex_color2, weight1, weight2):
	"""Calculate the weighted mean of two hex colors."""
	# Convert hex colors to RGB
	rgb1 = hex_to_rgb(hex_color1)
	rgb2 = hex_to_rgb(hex_color2)

	# Calculate the weighted mean for each component
	total_weight = weight1 + weight2
	weighted_rgb = (
		(rgb1[0] * weight1 + rgb2[0] * weight2) / total_weight,
		(rgb1[1] * weight1 + rgb2[1] * weight2) / total_weight,
		(rgb1[2] * weight1 + rgb2[2] * weight2) / total_weight
	)

	# Convert the resulting RGB back to hex
	return rgb_to_hex(tuple(int(c) for c in weighted_rgb))

def get_transparent_color(ray: Ray, main_color: str, bg_color: str):
	return weighted_mean_color(main_color, bg_color, ray.intensity, (1-ray.intensity))

def convert16to8(color: tuple):
	return tuple(int((c-1) / 256) for c in color)
