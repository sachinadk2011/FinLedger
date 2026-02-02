import pygame
import sys
from pygame_created_remain.config import WHITE, BLUE, ORANGE, MIN_WIDTH, MIN_HEIGHT, FPS, HEIGHT, WIDTH, BASE_H, BASE_W, BASE_CARD_H, BASE_CARD_W, BASE_GAP, BASE_MARGIN
from ui import font, icon, button_card
from utils import text_centered, load_icon, get_instant_bg, get_ui_scale

pygame.init()
info = pygame.display.Info()
WIDTH = int(info.current_w * 0.7)
HEIGHT = int(info.current_h * 0.7)
pygame.display.set_caption("Finance Investement Tracker")
clock = pygame.time.Clock()

def bank_module_main():
    screen  = pygame.display.set_mode(
                (WIDTH, HEIGHT),
                pygame.RESIZABLE
            )
    home_icon = load_icon("assests/earn-icon.png", (90, 90))
    main_icon = icon((120, 100) ,pos=(220, 250))
    main_icon.add_image(home_icon, (0, 0))
    main_icon.set_size(0.5)
    main_icon.tint(ORANGE, mode="outline", thickness=2)
                     
    width, height = screen.get_size()
    background = get_instant_bg(width, height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                new_width = max(event.w, MIN_WIDTH)
                new_height = max(event.h, MIN_HEIGHT)
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                background = get_instant_bg(new_width, new_height)

        
        screen.blit(background, (0, 0))
        main_icon.draw(screen)
        

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    bank_module_main()