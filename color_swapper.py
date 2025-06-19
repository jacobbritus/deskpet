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
old_palette = ["#1b1b1b", "#131313", "#000000", "#34a641", "#49f75d"]  # old colors
new_palette = ["#e0e0e0", "#c1baba", "#6f6f6f", "#3466f8", "#3493f8"]  # new colors

# 🖼 Replace this with your input and output file names
# palette_swap("sprites/white_cat/Excited.png", "sprites/white_cat/Excited.png", old_palette, new_palette)

##### iterating through a file

import os
folder = "sprites/white_cat"

for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)

    print(f"Processing: {folder}")
    palette_swap(file_path, file_path, old_palette, new_palette)
