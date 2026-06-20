# import colorsys


# TODO: use when getting rgb colors of media
# def get_vips_palette(vips_image, color_count: int = 8) -> list[tuple[int, int, int]]:
#     h_scale = 3 / vips_image.width
#     v_scale = 3 / vips_image.height

#     tiny_img = vips_image.resize(h_scale, vscale=v_scale)

#     palette = []
#     for y in range(tiny_img.height):
#         for x in range(tiny_img.width):
#             pixel = tiny_img(x, y)
#             if len(pixel) >= 3:
#                 r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
#                 palette.append((r, g, b))

#             if len(palette) == color_count:
#                 return palette
#     return palette

# class ColorCalculation:

#     async def rgb_to_hex(self, rgb: tuple[int, int, int]) -> str:
#         return '#{:02x}{:02x}{:02x}'.format(*rgb)

#     async def average_colors(self, rgb_colors: list[tuple[int, int, int]]) -> str:
#         avg = tuple(round(sum(c[i] for c in rgb_colors) / len(rgb_colors)) for i in range(3))
#         return await self.rgb_to_hex(avg)         # type: ignore[attr-defined]

#     async def average_palettes(self, palettes: list[list[tuple[int, int, int]]]) -> list[tuple[int, int, int]]:
#         return [
#             tuple(round(sum(c[i] for c in slot) / len(slot)) for i in range(3))
#             for slot in zip(*palettes)
#         ]  # type: ignore[return-value]

#     async def palette_to_color_tags(self, palette: list[tuple[int, int, int]]) -> list[str]:
#         tags = list({await self.rgb_to_color_tag(color) for color in palette})
#         return tags             # type: ignore[attr-defined]

#     async def rgb_to_color_tag(self, rgb: tuple[int, int, int]) -> str:
#         r, g, b = [x / 255 for x in rgb]
#         h, l, s = colorsys.rgb_to_hls(r, g, b)
#         h = h * 360

#         if l < 0.10: return 'black'
#         if l > 0.93: return 'white'

#         if s < 0.06:
#             if l > 0.80: return 'light gray'
#             if l < 0.30: return 'dark gray'
#             return 'gray'

#         # low saturation
#         if s < 0.15:
#             if l > 0.88: return 'white'
#             if l > 0.78:
#                 if 0 <= h < 60 or 300 <= h <= 360: return 'blush'
#                 if 200 <= h < 280: return 'lavender gray'
#                 return 'light gray'
#             if l > 0.60:
#                 if 0 <= h < 60 or 300 <= h <= 360: return 'blush'
#                 if 200 <= h < 280: return 'cool gray'
#                 if 60 <= h < 180: return 'sage'
#                 return 'warm gray'
#             if l > 0.40:
#                 if 0 <= h < 60 or 300 <= h <= 360: return 'taupe'
#                 if 200 <= h < 280: return 'cool gray'
#                 return 'taupe'
#             if l > 0.25:
#                 if 0 <= h < 60 or 300 <= h <= 360: return 'dark taupe'
#                 return 'dark gray'
#             return 'dark gray'

#         # medium saturation (0.15-0.30)
#         if s < 0.30:
#             if 0 <= h < 20 or 340 <= h <= 360:
#                 if l > 0.80: return 'blush'
#                 if l > 0.60: return 'dusty rose'
#                 if l > 0.40: return 'dusty rose'
#                 if l > 0.25: return 'wine'
#                 return 'dark brown'
#             if 20 <= h < 50:
#                 if l > 0.80: return 'cream'
#                 if l > 0.65: return 'cream'
#                 if l > 0.55: return 'beige'
#                 if l > 0.35: return 'tan'
#                 if l > 0.20: return 'brown'
#                 return 'dark brown'
#             if 50 <= h < 80:
#                 if l > 0.75: return 'cream'
#                 if l > 0.40: return 'tan'
#                 return 'dark olive'
#             if 80 <= h < 160:
#                 if l > 0.70: return 'light green'
#                 if l > 0.40: return 'sage'
#                 return 'dark green'
#             if 160 <= h < 220:
#                 if l > 0.70: return 'light blue'
#                 if l > 0.40: return 'steel blue'
#                 return 'dark slate'
#             if 220 <= h < 280:
#                 if l > 0.80: return 'lavender'
#                 if l > 0.60: return 'lavender'
#                 if l > 0.40: return 'slate blue'
#                 return 'dark slate'
#             if 280 <= h < 340:
#                 if l > 0.80: return 'blush'
#                 if l > 0.60: return 'dusty rose'
#                 if l > 0.40: return 'dusty rose'
#                 return 'wine'

#         # medium-high sat (0.30-0.55)
#         if s < 0.55:
#             if 0 <= h < 15 or 345 <= h <= 360:
#                 if l < 0.20: return 'dark red'
#                 if l < 0.45: return 'crimson'
#                 if l < 0.65: return 'red'
#                 if l < 0.80: return 'rose'
#                 return 'light pink'
#             if 15 <= h < 40:
#                 if l < 0.20: return 'dark brown'
#                 if l < 0.40: return 'brown'
#                 if l < 0.65: return 'orange'
#                 if l < 0.80: return 'peach'
#                 return 'cream'
#             if 40 <= h < 65:
#                 if l < 0.25: return 'dark olive'
#                 if l < 0.55: return 'yellow'
#                 return 'light yellow'
#             if 65 <= h < 80:
#                 if l < 0.30: return 'dark olive'
#                 return 'yellow green'
#             if 80 <= h < 150:
#                 if l < 0.20: return 'dark green'
#                 if l < 0.50: return 'green'
#                 return 'light green'
#             if 150 <= h < 200:
#                 if l < 0.25: return 'dark teal'
#                 if l < 0.55: return 'teal'
#                 return 'light teal'
#             if 200 <= h < 240:
#                 if l < 0.25: return 'dark blue'
#                 if l < 0.55: return 'blue'
#                 return 'light blue'
#             if 240 <= h < 275:
#                 if l < 0.25: return 'dark blue'
#                 if l < 0.55: return 'indigo'
#                 return 'periwinkle'
#             if 275 <= h < 315:
#                 if l < 0.25: return 'dark purple'
#                 if l < 0.55: return 'purple'
#                 return 'lavender'
#             if 315 <= h < 345:
#                 if l < 0.25: return 'dark pink'
#                 if l < 0.55: return 'pink'
#                 return 'light pink'

#         # high sat (0.55+)
#         if 0 <= h < 15 or 345 <= h <= 360:
#             if l < 0.25: return 'dark red'
#             if l < 0.50: return 'red'
#             if l < 0.70: return 'bright red'
#             return 'light pink'
#         if 15 <= h < 40:
#             if l < 0.30: return 'brown'
#             if l < 0.55: return 'orange'
#             return 'peach'
#         if 40 <= h < 65:
#             if l < 0.35: return 'dark yellow'
#             return 'yellow'
#         if 65 <= h < 80: return 'yellow green'
#         if 80 <= h < 150:
#             if l < 0.25: return 'dark green'
#             if l < 0.55: return 'green'
#             return 'bright green'
#         if 150 <= h < 200:
#             if l < 0.30: return 'dark teal'
#             return 'teal'
#         if 200 <= h < 240:
#             if l < 0.30: return 'dark blue'
#             if l < 0.55: return 'blue'
#             return 'sky blue'
#         if 240 <= h < 275:
#             if l < 0.30: return 'dark blue'
#             return 'indigo'
#         if 275 <= h < 315:
#             if l < 0.30: return 'dark purple'
#             if l < 0.55: return 'purple'
#             return 'violet'
#         if 315 <= h < 345:
#             if l < 0.30: return 'dark pink'
#             if l < 0.55: return 'hot pink'
#             return 'pink'

#         return 'neutral'


# color = ColorCalculation()
