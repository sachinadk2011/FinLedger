import pygame
from config import WHITE

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