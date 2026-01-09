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

from config import WHITE, BLUE, ORANGE, MIN_WIDTH, MIN_HEIGHT, FPS, HEIGHT, WIDTH 
print(MIN_WIDTH, MIN_HEIGHT,  HEIGHT, WIDTH)
pygame.display.set_caption("Finance Investement Tracker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

START_COLOR = (25, 45, 100)   # Deep Blue (Corner 1)
MID_COLOR = (50, 150, 180)    # Vibrant Teal (Middle)
END_COLOR = (120, 230, 230)   # Bright Cyan/Aqua (Corner 2 - The Glow)

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

def get_instant_bg(width, height):
    # This uses Pygame's built-in C-engine to stretch the image
    return pygame.transform.smoothscale(SMALL_GRADIENT, (width, height))

def tint_icon(icon, color):
    tinted = icon.copy()
    tinted.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted   

def load_icon(path, size):
    icon = pygame.image.load(path).convert_alpha() 
    return pygame.transform.smoothscale(icon, size)

class icon:
    def __init__(self,  size, pos=(0,0)):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        
        self.rect = self.surface.get_rect(topleft=pos)
    
    def add_image(self, icon, pos):
        self.surface.blit(icon, pos)
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def set_pos(self, x, y):
        self.rect.topleft = (x, y)

    def tint(self, color):
        self.surface = tint_icon(self.surface, color)


def main():
    Options = ["Stocks", "Bonds", "Mutual Funds", "ETFs", "Cryptocurrency"]
    screen  = pygame.display.set_mode(
                (800, 700),
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
    share_icon = load_icon("assests/stock_icon.png", (70, 70))
    stock_bar_icon = icon((120, 100) ,pos=(220, 250))
    stock_bar_icon.add_image(share_icon, (0, 0))
    stock_bar_icon.tint(WHITE)

    # report combine icon
    pie_chart_icon = load_icon("assests/stock_pies.png",(48, 48) )
    bar_icon = load_icon("assests/stock_icon.png", (60,60))
    stock_report_icon = icon((120,120), pos=(300, 250))
    stock_report_icon.add_image(pie_chart_icon, (0, 0))
    stock_report_icon.add_image(bar_icon, (50, 0))
    stock_report_icon.tint(WHITE)

    
    
    # Draw once (important!)
    width, height = screen.get_size()
    background = get_instant_bg(width, height)

    

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
        
        screen.blit(background, (0, 0))
        bank_icons.draw(screen)
        stock_bar_icon.draw(screen)
        stock_report_icon.draw(screen)
        
        
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
