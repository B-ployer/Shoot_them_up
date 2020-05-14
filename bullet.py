from parameters import *
from images import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, belonging="enemy"):
        pygame.sprite.Sprite.__init__(self)
        self.belonging = belonging
        if self.belonging == "player":
            self.image = bullet_img
        else:
            self.image = enemy_bullet_img
            self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        if self.belonging == "player":
            self.rect.bottom = y
            self.speedy = -10
        else:
            self.rect.top = y
            self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.belonging == "player" and self.rect.bottom < 0 or self.belonging != "player" and self.rect.top > HEIGHT:
            self.kill()
