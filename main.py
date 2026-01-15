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

# Import custom modules
from ui import font, icon, button_card
from utils import text_centered, load_icon, get_instant_bg, get_ui_scale


pygame.display.set_caption("Finance Investement Tracker")
clock = pygame.time.Clock()


def update_layout(screen, width, height, icons, cards):
    layout_scale, font_scale, icon_scale = get_ui_scale(width, height)
    font.update_scale(font_scale)  

    #update icon sizes
    for icon in icons:
        icon.set_size(icon_scale)
    
    #update button sizes
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

    #update card sizes
    for card in cards:
        card.set_size(size)

    print(f"Resized to: {width}x{height}")

    #update card positions
    card_width = size[0]               
    gap = (width - 2 * margin - 3 * card_width) // 2
    print("Calculated gap: ", gap)
    gap = max(min(gap, 30), min_gap)
    print("Used gap: ", gap, min_gap)

    card_pos_x = (width - (3 * card_width + 2 * gap)) // 2
    print("Card pos x: ", card_pos_x)       
    card_pos_y = height * 0.5
    #update each card position
    for i, card in enumerate(cards):
            card.update_position(card_pos_x + i * (card_width + gap), card_pos_y)

    return font_scale

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

    bank_card = button_card((10,10), bank_icons, caption="Bank Accounts")
    share_card = button_card((10,10), stock_bar_icon, caption="Shares Module")
    stock_report_card = button_card((10,10), stock_report_icon, caption="Overall Summary")
    icons = [bank_icons, stock_bar_icon, stock_report_icon]
    cards = [bank_card, share_card, stock_report_card]

    font_scale = update_layout(screen, width, height, icons, cards)
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
                font_scale = update_layout(screen, width, height, icons, cards)
                
        
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
