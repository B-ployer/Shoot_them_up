from parameters import *
from images import *
from mob import *
from alien import *
from explosion import *
from powerups import Pow
from bullet import *

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def new_alien():
    a = Alien()
    all_sprites.add(a)
    aliens.add(a)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def g_colliding(score, group1, group2, kill_gr_1 = False, kill_gr_2 = False):
    hits = pygame.sprite.groupcollide(group1, group2, kill_gr_1, kill_gr_2)
    for hit in hits:
        hit.lives -= 1
        if hit.lives <= 0:
            hit.kill()
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if type(hit) == Alien:
                score += 60
            elif type(hit) == Mob:
                score += 50 - hit.radius
                if random.random() > 0.8:
                    pow = Pow(hit.rect.center)
                    all_sprites.add(pow)
                    powerups.add(pow)
                newmob()
    return score

def s_colliding(sprite, group, kill_gr, collided=None):
    hits = pygame.sprite.spritecollide(sprite, group, kill_gr, collided)
    for hit in hits:
        if type(hit) == Pow:
            if hit.type == 'shield':
                sprite.shield += random.randrange(10, 30)
                if sprite.shield >= 100:
                    sprite.shield = 100
                shield_sound.play()
            if hit.type == 'gun':
                sprite.powerup()
                power_sound.play()
        else:
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if type(hit) == Bullet:
                sprite.shield -= 30
            elif type(hit) == Mob:
                sprite.shield -= hit.radius * 2
                newmob()
