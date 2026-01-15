import pygame
import sys
import config

pygame.init()
info = pygame.display.Info()

#set config values
config.WIDTH = int(info.current_w * 0.7)
config.HEIGHT = int(info.current_h * 0.7)
config.MIN_WIDTH = int( info.current_w* 0.5)
config.MIN_HEIGHT = int(info.current_h * 0.55)

from config import WHITE, BLUE, ORANGE, MIN_WIDTH, MIN_HEIGHT, FPS, HEIGHT, WIDTH, BASE_H, BASE_W, BASE_CARD_H, BASE_CARD_W, BASE_GAP, BASE_MARGIN
print(MIN_WIDTH, MIN_HEIGHT,  HEIGHT, WIDTH)

pygame.display.set_caption("Finance Investement Tracker")
clock = pygame.time.Clock()


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

# Function to tint an icon with a given color
def tint_icon(icon, color):
    tinted = icon.copy()
    tinted.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted   

# Function to load and scale an icon
def load_icon(path, size):
    icon = pygame.image.load(path).convert_alpha() 
    return pygame.transform.smoothscale(icon, size)

def get_ui_scale(screen_w, screen_h):
    scale_x = screen_w / BASE_W
    scale_y = screen_h / BASE_H

    # Use the smaller one to prevent overflow
    layout_scale = min(scale_x, scale_y)
    layout_scale = max(0.85, min(layout_scale, 1.35))
    font_scale = layout_scale * 0.92 if layout_scale != 1 else layout_scale 
    icon_scale = layout_scale * 0.9 if layout_scale != 1 else layout_scale

    

    return (layout_scale, font_scale, icon_scale)


class FontManager:
    def __init__(self):
        self.scale = 1.0
        self.fonts = {}
        self.size = 24 # default size
        self.font_name = "Arial"

    def update_scale(self, scale):
        if scale != self.scale:
            self.scale = scale
            self.fonts.clear()  # force rebuild

    def get(self, size= 24, bold=False):
        
        key = (size, bold)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.SysFont(
                self.font_name,
                int(size * self.scale),
                bold=bold
            )
        return self.fonts[key]
    
    def set_font_name(self, font_name):
        if font_name != self.font_name:
            self.font_name = font_name
            self.fonts.clear()  # force rebuild
    
    def get_size(self, text, size=24, bold=False):
        font = self.get(size, bold)
        return font.size(text)
    
    def get_height(self, size=24, bold=False):
        font = self.get(size, bold)
        return font.get_height()

    def render(self, text, size=24, color=WHITE, bold=False):
        font = self.get(size, bold)
        return font.render(text, True, color)

# global variable for font
font = FontManager()

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

# Icon class to manage individual icons
class icon:
    def __init__(self,  size, pos=(0,0)):
        self.base_size = size
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        
        self.rel_x, self.rel_y = pos
        self.icons = []
    
    def add_image(self, icon, pos):
        self.icons.append((icon, pos))
        self.surface.blit(icon, pos)

    def set_size(self, scale):
        new_size = (
            int(self.base_size[0] * scale),
            int(self.base_size[1] * scale)
        )
        self.surface = pygame.Surface(new_size, pygame.SRCALPHA)
        for icon, pos in self.icons:
            #scale icon position
            new_pos = (int(pos[0] * scale), int(pos[1] * scale))
            #scale icon size
            icon_size = icon.get_size()
            new_icon_size = (int(icon_size[0] * scale), int(icon_size[1] * scale))
            scaled_icon = pygame.transform.smoothscale(icon, new_icon_size)
            self.surface.blit(scaled_icon, new_pos)

    def get_width(self):
        return self.surface.get_width()
    
    def get_height(self):
        return self.surface.get_height()
    
    def draw(self, target_screen):
        # Draw the icon surface onto the target screen at its relative position
        target_screen.blit(self.surface, (self.rel_x, self.rel_y))

    def set_pos(self, x, y):
        self.rel_x = x
        self.rel_y = y

    def tint(self, color):
        self.surface = tint_icon(self.surface, color)

# Button card class for interactive buttons
class button_card:
    def __init__(self, size, icon, pos=(0,0), caption=""):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=pos)
        self.icon = icon
        self.caption = caption
        self.caption_length = len(caption)
        self.hovered = False
        self.Gray = (60, 60, 60)

    def set_size(self, size):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

    def update_position(self, x, y):
        self.rect.topleft = (x, y)
        x, y = self.surface.get_size() 
        #print(x, y)
        #center icon in button
        icon_x = x // 2 + self.caption_length // 2 - self.icon.get_width() // 3 
        icon_y = y // 2 - self.icon.get_height() // 2 
        self.icon.set_pos(icon_x, icon_y)

    def hovered_check(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            
        else:
            self.hovered = False
            

    def draw(self, screen, color="", alpha=15):
        self.color = color if color else self.Gray
        self.color = ORANGE if self.hovered else self.Gray
        

        #draw card background
        pygame.draw.rect(
            self.surface,
            (*self.color, alpha),
            self.surface.get_rect(),
            border_radius=12
        )

        #drawing border
        pygame.draw.rect(
            self.surface,
            (*self.color, 90),
            self.surface.get_rect(),
            width=3,
            border_radius=12
        )
        #draw icon and caption over button
        self.icon.draw(self.surface)
        if self.caption:
            caption_surf = font.render(self.caption, bold=True)
            caption_rect = caption_surf.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() - 50))
            self.surface.blit(caption_surf, caption_rect)
        screen.blit(self.surface, self.rect.topleft)

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

def main():
    screen  = pygame.display.set_mode(
                (WIDTH, HEIGHT),
                pygame.RESIZABLE
            )
    #bank icon combine
    pig_icon = load_icon("assests/pig_icon.png", (48, 48))
    coin_icon = load_icon("assests/coins.png", (17, 17))
    credit_icons = load_icon("assests/credi-card.png", (35, 40))
    bank_icons = icon((120, 100), pos=(120, 250))
    bank_icons.add_image(credit_icons, (20, 21))
    bank_icons.add_image(coin_icon, (18, 5))
    bank_icons.add_image(pig_icon, (0, 20))
    bank_icons.tint(WHITE)

    #share icon 
    share_icon = load_icon("assests/stock_icon.png", (80, 80))
    stock_bar_icon = icon((120, 100) ,pos=(220, 250))
    stock_bar_icon.add_image(share_icon, (0, 0))
    stock_bar_icon.tint(WHITE)

    # report combine icon
    pie_chart_icon = load_icon("assests/stock_pies.png",(48, 48) )
    bar_icon = load_icon("assests/stock_icon.png", (60,60))
    stock_report_icon = icon((120,100), pos=(300, 250))
    stock_report_icon.add_image(pie_chart_icon, (0, 0))
    stock_report_icon.add_image(bar_icon, (50, 0))
    stock_report_icon.tint(WHITE)
  
    # Draw once (important!)
    width, height = screen.get_size()
    background = get_instant_bg(width, height)
    layout_scale, font_scale, icon_scale = get_ui_scale(width, height)
    font.update_scale(font_scale)

    margin = int(BASE_MARGIN * layout_scale)
    min_gap = int(BASE_GAP * layout_scale)

    available_width = width - 2 * margin - 2 * min_gap
    max_card_width = available_width // 3



    size = (
        min(
            int(BASE_CARD_W * layout_scale),
            max_card_width
            ),
        int(BASE_CARD_H * layout_scale)
    )
    bank_card = button_card(size, bank_icons, caption="Bank Accounts")
    share_card = button_card(size, stock_bar_icon, caption="Shares Module")
    stock_report_card = button_card(size, stock_report_icon, caption="Overall Summary")

    #initial card positions
    card_width, card_height = bank_card.surface.get_size()
    gap = (width - 2 * margin - 3 * card_width) // 2
    gap = max(gap, min_gap)
    card_pos_x = (width - (3 * card_width + 2 * gap)) // 2
    
    card_pos_y = height * 0.5
    bank_card.update_position(card_pos_x, card_pos_y)
    
    share_card.update_position(card_pos_x + card_width + gap, card_pos_y)
    stock_report_card.update_position(card_pos_x + 2*(card_width + gap), card_pos_y)
    print(f"Gap: {gap}, {card_pos_x}")

    heading = "Offline Personal Finance & Investment Tracker"
    subheading = "Your Financial Compass"
 
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            if event.type == pygame.VIDEORESIZE:
                  
                width, height = max(event.w, MIN_WIDTH), max(event.h, MIN_HEIGHT)
                screen = pygame.display.set_mode(
                 (width, height),
                    pygame.RESIZABLE
                    )
                background = get_instant_bg(width, height)
                layout_scale, font_scale, icon_scale = get_ui_scale(width, height)
                font.update_scale(font_scale)
                
                bank_icons.set_size(icon_scale)
                stock_report_icon.set_size(icon_scale)
                stock_bar_icon.set_size(icon_scale)

                margin = int(BASE_MARGIN * layout_scale)
                min_gap = int(BASE_GAP * layout_scale)

                available_width = width - 2 * margin - 2 * min_gap
                max_card_width = available_width // 3



                size = (
                        min(
                            int(BASE_CARD_W * layout_scale),
                            max_card_width
                            ),
                        int(BASE_CARD_H * layout_scale)
                        )
                print("New button size: ", size)
                bank_card.set_size(size)
                share_card.set_size(size)
                stock_report_card.set_size(size)
                print(f"Resized to: {width}x{height}")
                #update card positions
                card_width, card_height = bank_card.surface.get_size()
                
                gap = (width - 2 * margin - 3 * card_width) // 2
                print("Calculated gap: ", gap)
                gap = max(min(gap, 30), min_gap)
                print("Used gap: ", gap, min_gap)
                card_pos_x = (width - (3 * card_width + 2 * gap)) // 2
                print("Card pos x: ", card_pos_x)
                

                card_pos_y = height * 0.5
                bank_card.update_position(card_pos_x, card_pos_y)
                share_card.update_position(card_pos_x + card_width + gap, card_pos_y)
                stock_report_card.update_position(card_pos_x + 2*(card_width + gap), card_pos_y)
        
        screen.blit(background, (0, 0))
        heading_size = text_centered(screen, heading, size=int(min(60,max(50,56 * font_scale))), color=WHITE, center_pos=(width // 2, height // 6), max_width=width*0.6, bold=True, font_name= "Arial")
        text_centered(screen, subheading, size=int(min(32,max(24,28 * font_scale))), color=(210, 210, 210), center_pos=(width // 2, height // 6 + 1.25 * font.get_height(heading_size)), max_width=width*0.6, bold=False, font_name = "Segoe UI")
        
        #hover check for buttons
        mouse_pos = pygame.mouse.get_pos() 
        bank_card.hovered_check(mouse_pos)
        share_card.hovered_check(mouse_pos)
        stock_report_card.hovered_check(mouse_pos)

        #draw buttons
        bank_card.draw(screen)
        share_card.draw(screen)
        stock_report_card.draw(screen)
        
        
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
