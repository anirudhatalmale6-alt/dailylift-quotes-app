#!/usr/bin/env python3
"""
Create Play Store screenshots for DailyLift app
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Phone frame dimensions (1080x1920 - standard phone)
WIDTH = 1080
HEIGHT = 1920

# Colors
colors = [
    ('#667eea', '#764ba2'),  # Purple to violet
    ('#f093fb', '#f5576c'),  # Pink
    ('#4facfe', '#00f2fe'),  # Blue
    ('#43e97b', '#38f9d7'),  # Green
]

quotes = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The mind is everything. What you think you become.", "Buddha"),
    ("Success is walking from failure to failure with no loss of enthusiasm.", "Winston Churchill"),
]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient(width, height, color1, color2):
    """Create a vertical gradient"""
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)

    base = Image.new('RGB', (width, height))

    for y in range(height):
        ratio = y / height
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)

        for x in range(width):
            base.putpixel((x, y), (r, g, b))

    return base

def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width"""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def create_screenshot(index, quote_text, author, color_pair):
    """Create a single screenshot"""
    img = create_gradient(WIDTH, HEIGHT, color_pair[0], color_pair[1])
    draw = ImageDraw.Draw(img)

    # Try to load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        quote_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
        author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", 36)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        quote_font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    white = (255, 255, 255)
    white_80 = (255, 255, 255)

    # App title
    title = "DailyLift"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((title_x, 200), title, fill=white, font=title_font)

    # Subtitle
    subtitle = "Your Daily Dose of Motivation"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((sub_x, 280), subtitle, fill=white_80, font=subtitle_font)

    # Quote mark
    quote_mark = '"'
    try:
        big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 200)
    except:
        big_font = quote_font
    bbox = draw.textbbox((0, 0), quote_mark, font=big_font)
    qm_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((qm_x, 500), quote_mark, fill=(255, 255, 255, 80), font=big_font)

    # Quote text (wrapped)
    lines = wrap_text(quote_text, quote_font, WIDTH - 120, draw)
    y_offset = 750
    line_height = 70

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        line_x = (WIDTH - (bbox[2] - bbox[0])) // 2
        draw.text((line_x, y_offset), line, fill=white, font=quote_font)
        y_offset += line_height

    # Author
    author_text = f"— {author}"
    bbox = draw.textbbox((0, 0), author_text, font=author_font)
    author_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((author_x, y_offset + 40), author_text, fill=white_80, font=author_font)

    # Buttons at bottom
    button_y = 1500

    # New Quote button
    btn_width = 280
    btn_height = 80
    btn_x1 = WIDTH // 2 - btn_width - 20
    draw.rounded_rectangle(
        [btn_x1, button_y, btn_x1 + btn_width, button_y + btn_height],
        radius=40,
        fill=(255, 255, 255, 60),
        outline=(255, 255, 255, 80),
        width=2
    )
    btn_text = "New Quote"
    bbox = draw.textbbox((0, 0), btn_text, font=subtitle_font)
    text_x = btn_x1 + (btn_width - (bbox[2] - bbox[0])) // 2
    text_y = button_y + (btn_height - (bbox[3] - bbox[1])) // 2
    draw.text((text_x, text_y), btn_text, fill=white, font=subtitle_font)

    # Share button
    btn_x2 = WIDTH // 2 + 20
    draw.rounded_rectangle(
        [btn_x2, button_y, btn_x2 + btn_width, button_y + btn_height],
        radius=40,
        fill=(0, 0, 0, 50),
        outline=(255, 255, 255, 80),
        width=2
    )
    share_text = "Share"
    bbox = draw.textbbox((0, 0), share_text, font=subtitle_font)
    text_x = btn_x2 + (btn_width - (bbox[2] - bbox[0])) // 2
    text_y = button_y + (btn_height - (bbox[3] - bbox[1])) // 2
    draw.text((text_x, text_y), share_text, fill=white, font=subtitle_font)

    # Footer text
    footer = "Tap for inspiration ✨"
    bbox = draw.textbbox((0, 0), footer, font=subtitle_font)
    footer_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((footer_x, 1700), footer, fill=white_80, font=subtitle_font)

    return img

# Create output directory
os.makedirs('/var/lib/freelancer/projects/40169610/DailyLift/store-listing/screenshots', exist_ok=True)

# Generate screenshots
for i, (quote, author) in enumerate(quotes):
    color_pair = colors[i % len(colors)]
    screenshot = create_screenshot(i + 1, quote, author, color_pair)
    screenshot.save(f'/var/lib/freelancer/projects/40169610/DailyLift/store-listing/screenshots/screenshot_{i+1}.png', 'PNG')
    print(f"Created screenshot_{i+1}.png")

# Create feature graphic (1024x500)
feature = create_gradient(1024, 500, '#667eea', '#764ba2')
draw = ImageDraw.Draw(feature)

try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

# App name
title = "DailyLift"
bbox = draw.textbbox((0, 0), title, font=title_font)
title_x = (1024 - (bbox[2] - bbox[0])) // 2
draw.text((title_x, 160), title, fill=(255, 255, 255), font=title_font)

# Tagline
tagline = "Your Daily Dose of Motivation"
bbox = draw.textbbox((0, 0), tagline, font=subtitle_font)
tag_x = (1024 - (bbox[2] - bbox[0])) // 2
draw.text((tag_x, 260), tagline, fill=(255, 255, 255), font=subtitle_font)

# Decorative quotes
try:
    quote_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 120)
except:
    quote_font = title_font

draw.text((100, 100), '"', fill=(255, 255, 255, 50), font=quote_font)
draw.text((824, 250), '"', fill=(255, 255, 255, 50), font=quote_font)

feature.save('/var/lib/freelancer/projects/40169610/DailyLift/store-listing/feature_graphic.png', 'PNG')
print("Created feature_graphic.png")

print("\nAll store listing assets created!")
