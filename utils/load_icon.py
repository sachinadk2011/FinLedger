import pygame

# Function to load and scale an icon
def load_icon(path, size):
    icon = pygame.image.load(path).convert_alpha() 
    return pygame.transform.smoothscale(icon, size)