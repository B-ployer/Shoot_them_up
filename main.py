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
from alien import *
from bullet import *
from explosion import *
from functions import *

pygame.init()
pygame.mixer.music.play(loops=-1)

# Цикл игры
while running:
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
        if event.type == pygame.QUIT:
            running = False

    if score >= 400 and level == 0:
        new_alien()
        level += 1

    # Обновление
    all_sprites.update()

    score = g_colliding(score, mobs, bullets, False, True)
    score = g_colliding(score, aliens, bullets, False, True)

    s_colliding(player, enemy_bullets, True)
    s_colliding(player, mobs, True, pygame.sprite.collide_circle)
    s_colliding(player, powerups, True)

    if player.shield <= 0:
        death_explosion = Explosion(player.rect.center, 'player')
        all_sprites.add(death_explosion)
        player.hide()
        player.lives -= 1
        player.shield = 100
        death_explosion_snd.play()

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
