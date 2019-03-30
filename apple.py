import pygame
import random

class Apple(pygame.sprite.Sprite):
    def __init__(self , imagename , active_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(imagename).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        # 随机生成位置
        self.rect.left = random.randint(0 , active_size[0] - self.rect.width)
        self.rect.top = random.randint(0 , active_size[1] - self.rect.height)
