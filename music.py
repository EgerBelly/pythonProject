import random
import pygame
pygame.init()

music_for_game = [
    "veselaia.wav",
]

music_for_menu = [
    "music_for_menu/Another_Medium.mp3",
]
food_sound = pygame.mixer.Sound("notification.wav")
def play_music(song):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1)
def random_music_for_menu():
    music_number = random.randint(0, len(music_for_menu)-1)
    play_music(music_for_menu[music_number])
    return music_number
def new_sound_volume(sound):
    food_sound.set_volume(sound)
def decrease_volume(volume):
    if volume >= 0.1:
        return volume - 0.1
    else:
        return volume
def increase_volume(volume):
    if volume <= 0.9:
        return volume + 0.1
    else:
        return volume
