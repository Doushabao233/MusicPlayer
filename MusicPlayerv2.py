# Example file showing a circle moving on screen
import ctypes
import random
import threading
import pygame
import pygame.gfxdraw
import os
import sys
import time
import stagger
from PIL import Image
import io

def parse_file(path):
    '''This function parses the ID3 information from the song, encompassing details such as the title, artist, album, and image.
    It returns a tuple in the following format: ('music title', 'artist', 'album', [binary image data]).
    NOTE: If there isn't information in the file, it returns None instead of string.'''
    audiofile = None
    title = None
    artist = None
    album = None
    picture = None

    try:
        audiofile = stagger.read_tag(path)
        title = audiofile.title
        artist = audiofile.artist
        album = audiofile.album
        picture = audiofile[stagger.id3.APIC][0].data
    except:
        pass

    if title == '':
        title = None
    if artist == '':
        artist = None
    if album == '':
        album = None

    return title, artist, album, picture

def get_background():
    '''This function returns a path. Like: ./Resources/backgrounds/snow/day.png'''
    path = './Resources/backgrounds'
    dirs = os.listdir(path)
    # 0:00 ~ 10:00 day.png
    # 10:00 ~ 17:00 noon.png
    # 17:00 ~ 23:59 night.png

    if (0 <= time.localtime().tm_hour <= 9 and 0 <= time.localtime().tm_min <= 59):
        # DAY
        return './Resources/backgrounds/{}/day.png'.format(random.choice(dirs))
    elif (10 <= time.localtime().tm_hour <= 16 and 0 <= time.localtime().tm_min <= 59):
        # NOON
        return './Resources/backgrounds/{}/noon.png'.format(random.choice(dirs))
    elif (17 <= time.localtime().tm_hour <= 23):
        # NIGHT
        return './Resources/backgrounds/{}/night.png'.format(random.choice(dirs))

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
SUPPORTED_FORMATS = ['mp3', 'ogg', 'wav']

pygame.init() # Pygame，启动！
pygame.mixer.init()
# pygame.mixer.music.load(r'C:\Users\Lenovo\Music\张雨生\口是心非 - 张雨生.mp3')
# pygame.mixer.music.play()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('Music Player')
background_path = get_background()
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# background = pygame.transform.box_blur(background, 0)
note_path = get_note()
note = pygame.image.load(note_path)
note = pygame.transform.scale(note, (64, 64))
note_y = HEIGHT / 2 + 25
info_background = pygame.Surface((WIDTH, HEIGHT))
info_background.fill((0, 0, 0))
info_background.set_alpha(0)
temp_album_cover = pygame.image.load('test.jpg').convert_alpha() # WIP
temp_album_cover.set_alpha(0)
album_cover = pygame.Surface(temp_album_cover.get_size(), flags=pygame.SRCALPHA) # ROUNDED! NICE!
album_cover = pygame.transform.smoothscale(album_cover, (WIDTH / 3.4, WIDTH / 3.4))
id3: tuple   # assignment later
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

def animations():
    global note_y, note_path, background
    background_blur = 0
    while 1:
        if pygame.mixer.music.get_busy():
            # music note
            if round(note_y) - 0.1 <= 450:   
                time.sleep(0.1)
                note_path = get_note()
                note_y = HEIGHT / 2 + 50
            else:
                note_y += (450 - note_y) * 0.1
                time.sleep(0.01)
            
            # background blur
            if background_blur < 10:
                background_blur += 1
                background = pygame.transform.box_blur(background, background_blur)
        else:
            if background_blur > 0:
                background_blur -= 1
                background = pygame.transform.box_blur(background, background_blur)

def draw_window():
    '''Draw the screen.'''
    global background, info_background
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    debug_screen_text = debug_font.render('', antialias=True, color='white')
    if debug_screen:
        debug_screen_text = debug_font.render(
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
            screen_width=WIDTH,
            screen_height=HEIGHT),

            antialias=True,
            color='white'
        )
    
    screen.blit(background, (0, 0))
    if pygame.mixer.music.get_busy():
        note = pygame.image.load(note_path)
        note = pygame.transform.scale(note, (64, 64))
        screen.blit(note, (WIDTH / 2 - note.get_width() / 2, note_y))

        music_title = id3[0]
        music_artist = id3[1]
        album_name = id3[2]
        if id3[3] is None:
            img = Image.open('./Resources/images/unknown_album.png')
        else:
            img = Image.open(io.BytesIO(id3[3]))
        temp_album_cover = pygame.image.frombytes(img.tobytes(), img.size, 'RGB').convert_alpha()
        temp_album_cover = pygame.transform.smoothscale(temp_album_cover, (WIDTH / 3.4, WIDTH / 3.4))
        if info_background.get_alpha() < 200:
            info_background.set_alpha(info_background.get_alpha() + 10)
        if album_cover.get_alpha() < 500:
            album_cover.set_alpha(album_cover.get_alpha() + 30)
        
        screen.blit(info_background, (0, 0))
        pygame.draw.rect(album_cover, 'white', album_cover.get_rect(), border_radius=10)
        album_cover.blit(temp_album_cover, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(album_cover, (WIDTH / 25, WIDTH / 25))
    else:
        if info_background.get_alpha() > 0:
            info_background.set_alpha(info_background.get_alpha() - 10)

        if album_cover.get_alpha() > 0:
            album_cover.set_alpha(album_cover.get_alpha() - 50)

    screen.blit(debug_screen_text, (10, 10))
    pygame.display.flip()

thread_it(animations)
while running:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT: # quit program
            running = False
        elif event.type == pygame.DROPFILE: # catch files
            print('omg', event.dict)
            if event.dict['file'].split('.')[1] in SUPPORTED_FORMATS:
                id3 = parse_file(event.dict['file'])
                pygame.mixer.music.load(event.dict['file'])
                pygame.mixer.music.play()
            else:
                print('illegal file format detected', event.dict['file'].split('.')[1])
        elif event.type == pygame.KEYDOWN: # toggle debug screen
            if event.key == pygame.K_F3:
                debug_screen = not debug_screen 
    draw_window()
    clock.tick(60)

pygame.quit()