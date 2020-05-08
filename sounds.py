import pygame
from os import path
from parameters import *

pygame.init()

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
