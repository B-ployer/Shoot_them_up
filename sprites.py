import pygame

pygame.init()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

def init_sprites(a_s, m, al, b, e_b, p):
    a_s.empty()
    m.empty()
    al.empty()
    b.empty()
    e_b.empty()
    p.empty()
