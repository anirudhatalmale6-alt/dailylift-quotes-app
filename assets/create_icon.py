#!/usr/bin/env python3
"""
Create app icon for DailyLift - Quotes & Motivation
Following the Luminous Ascent design philosophy
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_gradient(width, height, color1, color2):
    """Create a vertical gradient from color1 to color2"""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))

    for y in range(height):
        # Create smooth gradient
        ratio = y / height
        # Use easing for smoother transition
        eased_ratio = ratio * ratio * (3 - 2 * ratio)  # smoothstep
        mask_value = int(255 * eased_ratio)
        for x in range(width):
            mask.putpixel((x, y), mask_value)

    base.paste(top, mask=mask)
    return base

def draw_rounded_rect(draw, coords, radius, fill):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = coords
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)

def create_icon():
    size = 1024

    # Colors from the Luminous Ascent philosophy
    purple = (102, 126, 234)  # #667eea
    pink = (118, 75, 162)     # #764ba2
    white = (255, 255, 255)

    # Create gradient background
    img = create_gradient(size, size, purple, pink)
    draw = ImageDraw.Draw(img)

    # Add subtle radial glow effect in center
    center_x, center_y = size // 2, size // 2
    for r in range(200, 0, -5):
        alpha = int(20 * (1 - r / 200))
        glow_color = (255, 255, 255, alpha)
        # We'll skip this for simplicity - gradient is enough

    # Draw elegant quotation mark
    # The quote mark will be a stylized, minimal design
    quote_size = 420
    quote_x = (size - quote_size) // 2 + 30
    quote_y = (size - quote_size) // 2 - 20

    # Draw two elegant circles for the quotation mark (stylized approach)
    circle_radius = 90
    spacing = 180

    # First quote circle (left)
    cx1 = size // 2 - spacing // 2
    cy1 = size // 2 - 40

    # Second quote circle (right)
    cx2 = size // 2 + spacing // 2
    cy2 = size // 2 - 40

    # Draw the quotation marks as elegant curved shapes
    # Using a more sophisticated double-quote design

    # Create the quote mark paths
    # Left quote
    draw.ellipse([cx1 - circle_radius, cy1 - circle_radius,
                  cx1 + circle_radius, cy1 + circle_radius],
                 fill=white)
    # Tail for left quote
    points_left = [
        (cx1 - circle_radius * 0.3, cy1 + circle_radius * 0.5),
        (cx1 - circle_radius * 0.8, cy1 + circle_radius * 2.2),
        (cx1 + circle_radius * 0.1, cy1 + circle_radius * 1.2),
    ]
    draw.polygon(points_left, fill=white)

    # Right quote
    draw.ellipse([cx2 - circle_radius, cy2 - circle_radius,
                  cx2 + circle_radius, cy2 + circle_radius],
                 fill=white)
    # Tail for right quote
    points_right = [
        (cx2 - circle_radius * 0.3, cy2 + circle_radius * 0.5),
        (cx2 - circle_radius * 0.8, cy2 + circle_radius * 2.2),
        (cx2 + circle_radius * 0.1, cy2 + circle_radius * 1.2),
    ]
    draw.polygon(points_right, fill=white)

    # Save the icon
    img.save('/var/lib/freelancer/projects/40169610/DailyLift/assets/icon.png', 'PNG')
    print("Icon created: icon.png")

    # Create adaptive icon foreground (with transparency for Android)
    adaptive = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    adaptive_draw = ImageDraw.Draw(adaptive)

    # Draw quotation marks on transparent background
    # Left quote
    adaptive_draw.ellipse([cx1 - circle_radius, cy1 - circle_radius,
                          cx1 + circle_radius, cy1 + circle_radius],
                         fill=(255, 255, 255, 255))
    adaptive_draw.polygon(points_left, fill=(255, 255, 255, 255))

    # Right quote
    adaptive_draw.ellipse([cx2 - circle_radius, cy2 - circle_radius,
                          cx2 + circle_radius, cy2 + circle_radius],
                         fill=(255, 255, 255, 255))
    adaptive_draw.polygon(points_right, fill=(255, 255, 255, 255))

    adaptive.save('/var/lib/freelancer/projects/40169610/DailyLift/assets/adaptive-icon.png', 'PNG')
    print("Adaptive icon created: adaptive-icon.png")

    # Create splash icon
    splash = create_gradient(size, size, purple, pink)
    splash_draw = ImageDraw.Draw(splash)

    # Draw smaller quotes for splash
    scale = 0.6
    scx1 = size // 2 - int(spacing * scale) // 2
    scy1 = size // 2 - 30
    scx2 = size // 2 + int(spacing * scale) // 2
    scy2 = size // 2 - 30
    sr = int(circle_radius * scale)

    splash_draw.ellipse([scx1 - sr, scy1 - sr, scx1 + sr, scy1 + sr], fill=white)
    splash_points_left = [
        (scx1 - sr * 0.3, scy1 + sr * 0.5),
        (scx1 - sr * 0.8, scy1 + sr * 2.2),
        (scx1 + sr * 0.1, scy1 + sr * 1.2),
    ]
    splash_draw.polygon(splash_points_left, fill=white)

    splash_draw.ellipse([scx2 - sr, scy2 - sr, scx2 + sr, scy2 + sr], fill=white)
    splash_points_right = [
        (scx2 - sr * 0.3, scy2 + sr * 0.5),
        (scx2 - sr * 0.8, scy2 + sr * 2.2),
        (scx2 + sr * 0.1, scy2 + sr * 1.2),
    ]
    splash_draw.polygon(splash_points_right, fill=white)

    splash.save('/var/lib/freelancer/projects/40169610/DailyLift/assets/splash-icon.png', 'PNG')
    print("Splash icon created: splash-icon.png")

    # Create favicon (smaller version)
    favicon = img.resize((196, 196), Image.Resampling.LANCZOS)
    favicon.save('/var/lib/freelancer/projects/40169610/DailyLift/assets/favicon.png', 'PNG')
    print("Favicon created: favicon.png")

    print("\nAll icons generated successfully!")

if __name__ == "__main__":
    create_icon()
