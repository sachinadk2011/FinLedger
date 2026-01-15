import pygame
from config import WHITE, BLUE, ORANGE, MIN_WIDTH, MIN_HEIGHT, FPS, HEIGHT, WIDTH, BASE_H, BASE_W, BASE_CARD_H, BASE_CARD_W, BASE_GAP, BASE_MARGIN
from .fontManager import font


# Function to tint an icon with a given color
def tint_icon(icon, color):
    tinted = icon.copy()
    tinted.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted   

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
