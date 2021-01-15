from parameters import *

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
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue07.png")).convert()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "laserRed07.png")).convert()
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
