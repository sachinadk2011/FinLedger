import pygame
import sys




ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


WIDTH, HEIGHT = 800, 700
MIN_WIDTH, MIN_HEIGHT = 400, 300

pygame.init()
info = pygame.display.Info()
#pygame.display.set_minimum_size(MIN_WIDTH, MIN_HEIGHT)

#pygame.display.iconify()

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


def main():
    Options = ["Stocks", "Bonds", "Mutual Funds", "ETFs", "Cryptocurrency"]
    screen  = pygame.display.set_mode(
                (800, 700),
                pygame.RESIZABLE
            )
    #bank icon combine
    pig_icon = pygame.image.load("assests/pig_icon.png").convert_alpha()
    pig_icon = pygame.transform.smoothscale(pig_icon, (48, 48))
    coin_icon = pygame.image.load("assests/coins.png").convert_alpha()
    coin_icon = pygame.transform.smoothscale(coin_icon, (20, 20))
    credit_icons = pygame.image.load("assests/credi-card.png").convert_alpha()
    credit_icons = pygame.transform.smoothscale(credit_icons, (35, 40))
    bank_icons = pygame.Surface((150, 100), pygame.SRCALPHA)
    bank_icons.blit(credit_icons, (20, 21))
    bank_icons.blit(coin_icon, (18, 5))
    bank_icons.blit(pig_icon, (0, 20))
    white_bank_icon = tint_icon(bank_icons, WHITE)

    #share icon 
    share_icon = pygame.image.load("assests/stock_icon.png").convert_alpha()
    final_share_icon = pygame.transform.smoothscale(share_icon, (70, 70))
    white_share_icon = tint_icon(final_share_icon, WHITE)

    # report combine icon
    pie_chart_icon = pygame.image.load("assests/stock_pies.png").convert_alpha()
    pie_chart_icon = pygame.transform.smoothscale(pie_chart_icon, (48, 48))
    bar_icon = pygame.transform.smoothscale(share_icon, (60, 60))
    stock_report_icon = pygame.Surface((120, 120), pygame.SRCALPHA)
    stock_report_icon.blit(pie_chart_icon, (0, 0))
    stock_report_icon.blit(bar_icon, (50, 0))
    white_report_icon = tint_icon(stock_report_icon, WHITE)

    """ bank_icon = pygame.image.load("assests/pigibank.png").convert_alpha()
    bank_icon = pygame.transform.smoothscale(bank_icon, (48, 48))
    stock_icon = pygame.image.load("assests/stock_icon.png").convert_alpha()
    stock_icon = pygame.transform.smoothscale(stock_icon, (30, 30))
    reporting_icon = pygame.image.load("assests/pie_charts.png").convert_alpha()
    reporting_icon = pygame.transform.smoothscale(reporting_icon, (38, 38))
    combined_icon = pygame.Surface((120, 120), pygame.SRCALPHA)
    combined_icon.blit(stock_icon, (0, 0))
    combined_icon.blit(reporting_icon, (25, 0))
    orange_icon = tint_icon(combined_icon, ORANGE)
    blue_icons = tint_icon(stock_icon, BLUE)
    blue_icon = tint_icon(bank_icon, BLUE) """
    
    # Draw once (important!)
    width, height = screen.get_size()
    background = get_instant_bg(width, height)

    while True:
        clock.tick(60)
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
        screen.blit(white_bank_icon, (120, 250))
        screen.blit(white_share_icon, (220, 250))
        screen.blit(white_report_icon, (350, 250))
        
        
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
