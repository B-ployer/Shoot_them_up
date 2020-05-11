# Игра Shmup
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import pygame
import random
from os import path
from parameters import *
from sprites import *
from images import *
from sounds import *
from player import *
from mob import *
from bullet import *

# Создаем игру и окно
pygame.init()
pygame.mixer.init()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = alien_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -100
        self.speedx = 4
        self.speedy = 2
        self.lives = 5
        self.shoot_delay = 400
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 0:
            self.rect.y = 0
            self.rect.x += self.speedx
            self.shoot()
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.speedx = -self.speedx

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            alien_bullet = Bullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(alien_bullet)
            enemy_bullets.add(alien_bullet)
            shoot_sound.play()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # Убить, если он заходит за верхнюю часть экрана
        if self.rect.top > HEIGHT:
            self.kill()

font_name = pygame.font.match_font('arial')
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

pygame.mixer.music.play(loops=-1)

# Цикл игры
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    if game_over:
        show_go_screen()
        game_over = False
        refresh_sprites(all_sprites, mobs, aliens, bullets, enemy_bullets, powerups)
        player = init_player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
        level = 0
    # Ввод процесса (события)
    for event in pygame.event.get():
        # Проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    if score >= 400 and level == 0:
        new_alien()
        level += 1

    # Обновление
    all_sprites.update()

    # Проверка, попала ли пуля в моба
    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        hit.lives -= 1
        if hit.lives <= 0:
            hit.kill()
            score += 50 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.8:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob()

    hits = pygame.sprite.groupcollide(aliens, bullets, False, True)
    for hit in hits:
        hit.lives -= 1
        if hit.lives <= 0:
            hit.kill()
            score += 60
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)

    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.shield -= 30
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)

    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()

    if player.shield <= 0:
        death_explosion = Explosion(player.rect.center, 'player')
        all_sprites.add(death_explosion)
        player.hide()
        player.lives -= 1
        player.shield = 100
        death_explosion_snd.play()

    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
            shield_sound.play()
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()

    # Если игрок умер, игра окончена
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Рендеринг
    rel_y = bkgd_y % background_rect.height
    screen.fill(BLACK)
    screen.blit(background, (0, rel_y - background_rect.height))
    if rel_y < HEIGHT:
        screen.blit(background, (0, rel_y))
    bkgd_y += 5
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_text(screen, str(len(all_sprites)), 18, WIDTH - 100, 30) # показывает кол-во спрайтов на экране
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    for i in mobs:
        draw_text(i.image, str(i.lives), 18, i.rect.width / 2, i.rect.height / 2)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
