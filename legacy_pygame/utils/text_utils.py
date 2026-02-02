from ui.fontManager import font
from legacy_pygame.config import WHITE


def text_wrapper(text, max_width, size=24, bold=False):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        line_width, _ = font.get_size(test_line, size, bold)
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines


def text_centered(screen, text, size=24, color=WHITE, center_pos=(0,0),max_width=0, bold=False, font_name="Arial"):
    font.set_font_name(font_name)
    lines = text_wrapper(text, max_width, size, bold)
    line_height = font.get_height(size, bold)
    total_height = line_height * (len(lines) - 1)

    start_y = center_pos[1] - total_height // len(lines)
    for i, line in enumerate(lines):
        line_surf = font.render(line, size=size, color=color, bold=bold)
        
        line_rect = line_surf.get_rect(center=(center_pos[0], start_y + i * line_height))
        screen.blit(line_surf, line_rect)
    return size