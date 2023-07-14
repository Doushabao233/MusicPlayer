# Example file showing a circle moving on screen
import ctypes
import random
import threading
import pygame
import pygame.gfxdraw
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

ctypes.windll.shcore.SetProcessDpiAwareness(1)
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

screen_width = 1280
screen_height = 720

WIDTH = int(screen_width * scale_factor)
HEIGHT = int(screen_height * scale_factor)



pygame.init()
pygame.mixer.init()
# pygame.mixer.music.load(r'C:\Users\Lenovo\Music\张雨生\口是心非 - 张雨生.mp3')
# pygame.mixer.music.play()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('Music Player')
background_path = get_background()
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
note_path = get_note()
note = pygame.image.load(note_path)
note = pygame.transform.scale(note, (64, 64))
note_y = screen.get_height() / 2 + 25
info_background = pygame.Surface((screen.get_width(), screen.get_height()))
info_background.fill((0, 0, 0))
info_background.set_alpha(0)
album_cover = pygame.image.load('test.jpg') # WIP
album_cover.set_alpha(0)
album_cover = pygame.transform.scale(album_cover, (screen.get_width() / 3.4, screen.get_width() / 3.4))
SUPPORTED_FORMATS = ['mp3', 'ogg', 'wav']
debug_font = pygame.font.SysFont('Cascadia Code', 25)
debug_screen = False
clock = pygame.time.Clock()
running = True
dt = 0


def thread_it(func, *args: tuple):
    # 创建
    t = threading.Thread(target=func, args=args) 
    t.daemon = True
    t.start()

def note_y_changer():
    global note_y, note_path
    while 1:
        if pygame.mixer.music.get_busy():
            if round(note_y) - 0.1 <= 450:   
                time.sleep(0.1)
                note_path = get_note()
                note_y = screen.get_height() / 2 + 50
            else:
                note_y += (450 - note_y) * 0.1
                time.sleep(0.01)

def draw_window():
    '''Draw the screen.'''
    global background
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    text_surface = debug_font.render('', antialias=True, color='white')
    if debug_screen:
        text_surface = debug_font.render(
'''Music Player by Doushabao_233
{fps} fps
background: {bg_img}
is playing? {is_playing}
Python version {python_ver}
mouse: {mouse_x} {mouse_y}
note y: {note_y}
中文测试
screen: {screen_width}x{screen_height}'''.format(
            fps=clock.get_fps(),
            bg_img=background_path,
            is_playing=pygame.mixer.music.get_busy(),
            python_ver=sys.version,
            mouse_x=pygame.mouse.get_pos()[0],
            mouse_y=pygame.mouse.get_pos()[1],
            note_y=note_y,
            screen_width=screen.get_width(),
            screen_height=screen.get_height()),

            antialias=True,
            color='white'
        )
    
    screen.blit(background, (0, 0))
    if pygame.mixer.music.get_busy():
        note = pygame.image.load(note_path)
        note = pygame.transform.scale(note, (64, 64))
        screen.blit(note, (screen.get_width() / 2 - note.get_width() / 2, note_y))
        
        if info_background.get_alpha() < 200:
            info_background.set_alpha(info_background.get_alpha() + 10)
        if album_cover.get_alpha() < 500:
            album_cover.set_alpha(album_cover.get_alpha() + 50)
        
        screen.blit(info_background, (0, 0))
        r = pygame.Rect(200, 200, 100, 100)
        # screen.blit(album_cover, (screen.get_width() / 20, screen.get_width() / 20))
    else:
        if info_background.get_alpha() > 0:
            info_background.set_alpha(info_background.get_alpha() - 10)

        if album_cover.get_alpha() > 0:
            album_cover.set_alpha(album_cover.get_alpha() - 50)

    screen.blit(text_surface, (10, 10))
    pygame.display.flip()
    pygame.display.update()

thread_it(note_y_changer)
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
    
    draw_window()

    clock.tick(60)

pygame.quit()