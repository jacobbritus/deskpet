from PIL import Image


def extract_palette(image_path):
    img = Image.open(image_path).convert('RGBA')
    pixels = img.getdata()
    unique_colors = sorted(set(pixels))

    print("🎨 Unique Colors in image:")
    for color in unique_colors:
        hex_color = '#{:02X}{:02X}{:02X}'.format(color[0], color[1], color[2])
        print(f"{hex_color}  (RGBA: {color})")


# Replace this with your file name
# extract_palette("sprites/white_cat/Excited.png")


from PIL import Image

def hex_to_rgba(hex_code):
    hex_code = hex_code.lstrip('#')
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return r, g, b, 255  # full opacity

def palette_swap(image_path, output_path, old_hex, new_hex):
    old_colors = [hex_to_rgba(code) for code in old_hex]
    new_colors = [hex_to_rgba(code) for code in new_hex]

    img = Image.open(image_path).convert('RGBA')
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            current = pixels[x, y]
            if current in old_colors:
                index = old_colors.index(current)
                pixels[x, y] = new_colors[index]

    img.save(output_path)
    print(f"✅ Saved new image as {output_path}")


# 🎨 Replace these hex codes with yours

#                base      secondary   outline    eye dark  eye light  <------ grey_cat
# old_palette = ["#55524e", "#3b3a38", "#000000", "#acacfb", "#d7d7ff"]  # old colors grey
# new_palette = ["#7b644d", "#6e593d", "#000000", "#fbe677", "#fff2aa"]  # new colors TEST

old_palette = []
new_palette = []

# 🖼 Replace this with your input and output file names
# palette_swap("sprites/white_cat/Excited.png", "sprites/white_cat/Excited.png", old_palette, new_palette)

##### iterating through a file and changing the color pallete

import os
folder = "sprites/brown_cat"

for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)

    print(f"Processing: {folder}")
    palette_swap(file_path, file_path, old_palette, new_palette)
