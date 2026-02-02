import pygame
from pygame_created_remain.config import WHITE, BLUE, ORANGE, MIN_WIDTH, MIN_HEIGHT, FPS, HEIGHT, WIDTH, BASE_H, BASE_W, BASE_CARD_H, BASE_CARD_W, BASE_GAP, BASE_MARGIN

START_COLOR = (25, 45, 100)   # Deep Blue (Corner 1)
MID_COLOR = (50, 150, 180)    # Vibrant Teal (Middle)
END_COLOR = (120, 230, 230)   # Bright Cyan/Aqua (Corner 2 - The Glow)

# Create a small gradient surface
def create_gradient_surface(width, height, c1, c2, c3):
    surface = pygame.Surface((width, height))

    for y in range(height):
        for x in range(width):
            # diagonal ratio (0 → 1)
            ratio = ((x / width) + (y / height)) / 2

            # curve control (IMPORTANT)
            ratio = ratio * ratio * (3 - 2 * ratio)

            if ratio < 0.5:
                # Blend from c1 to c2
                f = ratio * 2
                r = int(c1[0] + (c2[0] - c1[0]) * f)
                g = int(c1[1] + (c2[1] - c1[1]) * f)
                b = int(c1[2] + (c2[2] - c1[2]) * f)
            else:
                # Blend from c2 to c3
                f = (ratio - 0.5) * 2
                r = int(c2[0] + (c3[0] - c2[0]) * f)
                g = int(c2[1] + (c3[1] - c2[1]) * f)
                b = int(c2[2] + (c3[2] - c2[2]) * f)

            surface.set_at((x, y), (r, g, b))

    return surface

SMALL_GRADIENT = create_gradient_surface(100, 100, START_COLOR, MID_COLOR, END_COLOR)

# Function to get a stretched gradient background
def get_instant_bg(width, height):
    # This uses Pygame's built-in C-engine to stretch the image
    return pygame.transform.smoothscale(SMALL_GRADIENT, (width, height))





def get_ui_scale(screen_w, screen_h):
    scale_x = screen_w / BASE_W
    scale_y = screen_h / BASE_H

    # Use the smaller one to prevent overflow
    layout_scale = min(scale_x, scale_y)
    layout_scale = max(0.85, min(layout_scale, 1.35))
    font_scale = layout_scale * 0.92 if layout_scale != 1 else layout_scale 
    icon_scale = layout_scale * 0.9 if layout_scale != 1 else layout_scale

    return (layout_scale, font_scale, icon_scale)

