# Example file showing a circle moving on screen
import random
import pygame
import os
import sys
import time

def get_background():
    '''This function returns a path. Like: ./Resources/background/snow/day.png'''
    path = './Resources/background'
    dirs = os.listdir(path)
    # 0:00 ~ 10:00 day.png
    # 10:00 ~ 17:00 noon.png
    # 17:00 ~ 23:59 night.png

    if (0 <= time.localtime().tm_hour <= 9 and 0 <= time.localtime().tm_min <= 59):
        # DAY
        return './Resources/background/{}/day.png'.format(random.choice(dirs))
    elif (10 <= time.localtime().tm_hour <= 16 and 0 <= time.localtime().tm_min <= 59):
        # NOON
        return './Resources/background/{}/noon.png'.format(random.choice(dirs))
    elif (17 <= time.localtime().tm_hour <= 23):
        # NIGHT
        return './Resources/background/{}/night.png'.format(random.choice(dirs))

def get_note():
    '''This function returns a path. Like: ./Resources/particles/note_blue.png'''
    path = './Resources/particles'
    dirs = os.listdir(path)
    return './Resources/particles/{}'.format(random.choices(dirs)[0])

# pygame setup
pygame.init()
pygame.mixer.init()
# pygame.mixer.music.load(r'C:\Users\Lenovo\Music\张雨生\口是心非 - 张雨生.mp3')
# pygame.mixer.music.play()
screen = pygame.display.set_mode((1280, 720), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('Music Player')
background_path = get_background()
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
note_path = get_note()
note = pygame.image.load(note_path)
note = pygame.transform.scale(note, (64, 64))
note_y = screen.get_height() / 2 + 25
SUPPORTED_FORMATS = ['mp3', 'ogg', 'wav']
debug_font = pygame.font.SysFont('Cascadia Code', 20, bold=True)
debug_screen = False
clock = pygame.time.Clock()
running = True
dt = 0


def draw_window():
    '''Draw the screen.'''
    global background
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    text_surface = debug_font.render('', antialias=True, color='white')
    if debug_screen:
        text_surface = debug_font.render(
'''Music Player by Doushabao_233
{} fps
background: {}
is playing? {}
Python version {}
note y: {}'''.format(clock.get_fps(), background_path, pygame.mixer.music.get_busy(), sys.version, note_y),
            antialias=True,
            color='white'
        )
    
    screen.blit(background, pygame.Vector2(0, 0))
    if pygame.mixer.music.get_busy():
        screen.blit(note, pygame.Vector2(screen.get_width() / 2 - note.get_width() / 2, note_y))
    screen.blit(text_surface, pygame.Vector2(10, 10))
    pygame.display.flip()
    pygame.display.update()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.DROPFILE:
            print('omg', event.dict)
            if event.dict['file'].split('.')[1] in SUPPORTED_FORMATS:
                pygame.mixer.music.load(event.dict['file'])
                pygame.mixer.music.play()
            else:
                print('illegal file format detected', event.dict['file'].split('.')[1])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                debug_screen = not debug_screen 

    if pygame.mixer.music.get_busy():
        if 350 < note_y <= 359:
            note_y -= 0.1
        elif note_y <= 350:   
            note_path = get_note()
            note = pygame.image.load(note_path)
            note = pygame.transform.scale(note, (64, 64))
            note_y = screen.get_height() / 2 + 30
        else:
            note_y -= 3
    draw_window()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000 

pygame.quit()