# Игра Shmup
# 1 часть Спрайт игрока и управление
# 2 часть Создание мобов
# 3 часть Создание пуль и столкновений
# 4 часть Загрузка и обработка графики
# 5 часть Замена столкновения с AABB на столкновения с Circle Bounding Box
# 6 часть Анимация спрайтов
# 7 часть Счёт и рендеринг текста
# 8 часть Подключение звуков и музыки
# 9 часть Добавление шкалы здоровья
# 10 часть Добавление анимации взрыва астероида и авто-огня
# 11 часть Добавление анимации взрыва игрока и жизней игрока
# 12 часть Добавление улучшений (щита)
# 13 часть Добавление улучшения (оружия) и звуков улучшений
# 14 часть Добавление экрана "Игра закончена"
# --------------------Самостоятельная-часть---------------------
# 1 часть Добавление жизней мобам
# 2 часть Устранение бага с выстрелами после смерти
# 3 часть Добавление отображения жизней мобов
# 4 часть Улучшение направления мобов, летят в сторону игрока
# 5 часть Улучшение столкновения мобов с границами
# 6 часть Добавление движения бэкграунда
# 7 часть Добавление наклонов карабля и исправление бага с серыми рамками усилений
# 8 часть Добавление спрайта Alien
# 9 часть Добавление класса вражеских снарядов, добавление выстрелов спрайту Alien и устранение pygame.transform.scale из метода update в классе Player

# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 4000

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shut`em up!")
clock = pygame.time.Clock()
bkgd_y = 0
Level = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)    для тестирования колайд-боксов
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.image = player_img
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            self.image = player_img_left
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
            self.image = player_img_right
        if keystate[pygame.K_SPACE] and self.hidden == False:
            self.shoot()
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        # тайм-аут для бонусов
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
            shoot_sound.play()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_imges)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)    для тестирования колайд-боксов
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        time_to_arriving = 0.125 * (((player.rect.x - self.rect.x) ** 2) + (player.rect.y - self.rect.y) ** 2) ** 0.5
        # self.speedy = random.randrange(1, 8)     простой параметр скорости по Y
        # self.speedx = random.randrange(-3, 3)    простой параметр скорости по X
        self.speedx = (player.rect.x - self.rect.x) / time_to_arriving
        self.speedy = (player.rect.y - self.rect.y) / time_to_arriving
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        if self.image_orig == meteor_imges[0]:
            self.lives = 4
        elif self.image_orig == meteor_imges[1] or self.image_orig == meteor_imges[2]:
            self.lives = 3
        elif self.image_orig == meteor_imges[4] or self.image_orig == meteor_imges[5]:
            self.lives = 2
        else:
            self.lives = 1

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 25 or self.rect.left > WIDTH + 25 or self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

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
            alien_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(alien_bullet)
            enemy_bullets.add(alien_bullet)
            shoot_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

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

# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, 'new_starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_img = pygame.transform.scale(player_img, (50, 38))
player_img_left = pygame.image.load(path.join(img_dir, "playerShip1_orange_left.png"))
player_img_left = pygame.transform.scale(player_img_left, (50, 38))
player_img_right = pygame.image.load(path.join(img_dir, "playerShip1_orange_right.png"))
player_img_right = pygame.transform.scale(player_img_right, (50, 38))
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed07.png")).convert()
meteor_imges = []
meteor_list =['meteorBrown_big1.png','meteorBrown_med1.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_imges.append(pygame.image.load(path.join(img_dir, img)).convert())
alien_img = pygame.image.load(path.join(img_dir, "ufoGreen.png")).convert()
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png'))
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png'))

# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    snd_for_expl = pygame.mixer.Sound(path.join(snd_dir, snd))
    snd_for_expl.set_volume(0.4)
    expl_sounds.append(snd_for_expl)
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.3)
death_explosion_snd = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'PowerupShield.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'PowerupGun.wav'))

# Создание и заполнение групп спрайтов
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()
score = 0
pygame.mixer.music.play(loops=-1)

# Цикл игры
game_over = True
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        aliens = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
        Level = 0
    # Ввод процесса (события)
    for event in pygame.event.get():
        # Проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    if score >= 400 and Level == 0:
        new_alien()
        Level += 1

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
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    for i in mobs:
        draw_text(i.image, str(i.lives), 18, i.rect.width / 2, i.rect.height / 2)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
