import ctypes
import random
import threading
import os
import sys
import time
import mutagen
from mutagen.mp3 import MP3
sys.stdout = open('nul', 'w')
import pygame
import pygame.gfxdraw
sys.stdout.close()
sys.stdout = sys.__stdout__
from PIL import Image
from math import floor
import io

def parse_file(path):
    '''This function parses the ID3 information from the song, encompassing details such as the title, artist, album, and image.
    It returns a tuple in the following format: ('mp3 file name', 'music title', 'artist', 'album', music length(float), [binary image data]).
    NOTE: If there isn't information in the file, it returns None instead of string.'''
    audiofile = None
    title = None
    artist = None
    album = None
    length = 0.6
    picture = None

    audiofile = mutagen.File(path)
    if audiofile and 'TIT2' in audiofile:    title  = audiofile.tags['TIT2'].text[0] # try to get music title
    if audiofile and 'TPE1' in audiofile:    artist = audiofile.tags['TPE1'].text[0] # try to get music artist
    if audiofile and 'TALB' in audiofile:    album  = audiofile.tags['TALB'].text[0] # try to get music album
    try:
        length = MP3(path).info.length # will raise error when music length is 0
    except: # im too lazy to explain the error type :\
        pass # length defaults to 0.6
    if audiofile and 'APIC:' in audiofile: picture = audiofile.tags['APIC:'].data # try to get music album picture

    if title == '':
        title = None
    if artist == '':
        artist = None
    if album == '':
        album = None

    return os.path.basename(path), title, artist, album, length, picture

def get_background():
    '''This function returns a path randomly. Like: ./Resources/backgrounds/snow/day.png'''
    path = './Resources/backgrounds'
    dirs = os.listdir(path)
    # 0:00 ~ 10:00 day.png
    # 10:00 ~ 17:00 noon.png
    # 17:00 ~ 23:59 night.png
    hour = time.localtime().tm_hour
    min = time.localtime().tm_min

    is_day = 0 <= hour <= 9 and 0 <= min <= 59
    is_noon = 10 <= hour <= 16 and 0 <= min <= 59
    is_night = 17 <= hour <= 23

    if is_day:
        # DAY
        return './Resources/backgrounds/{}/day.png'.format(random.choice(dirs))
    elif is_noon:
        # NOON
        return './Resources/backgrounds/{}/noon.png'.format(random.choice(dirs))
    elif is_night:
        # NIGHT
        return './Resources/backgrounds/{}/night.png'.format(random.choice(dirs))

def get_note():
    '''This function returns a path randomly. Like: ./Resources/particles/note_blue.png'''
    path = './Resources/particles'
    dirs = os.listdir(path)
    return './Resources/particles/{}'.format(random.choices(dirs)[0])

def fade_in(surf: pygame.Surface, speed: int = 10, max_alpha: int = 255):
    if surf.get_alpha() < max_alpha: # fade in animation
        surf.set_alpha(surf.get_alpha() + speed)

def fade_out(surf: pygame.Surface, speed: int = 10, min_alpha: int = 0):
    if surf.get_alpha() > min_alpha: # fade out animation
        surf.set_alpha(surf.get_alpha() - speed)

def blur_in(speed: int = 1, max_blur_radius=10):
    global background_blur_radius, blurred_background
    if background_blur_radius < max_blur_radius: # blur in animation
            background_blur_radius += speed
            blurred_background = pygame.transform.box_blur(background, background_blur_radius)

def blur_out(speed: int = 1, min_blur_radius=0):
    global blurred_background, background_blur_radius
    if background_blur_radius > min_blur_radius: # blur animation
        background_blur_radius -= speed
        blurred_background = pygame.transform.box_blur(background, background_blur_radius)       

def enter_animation():
    global total_progress_bar_width
    blur_in(speed=1, max_blur_radius=10)
            
    fade_in(info_background, speed=10, max_alpha=180)
    
    fade_in(album_cover, speed=30, max_alpha=255)

    fade_in(music_title_text, speed=10, max_alpha=255)
    
    fade_in(music_artist_text, speed=10, max_alpha=255)

    fade_in(music_pos_text, speed=10, max_alpha=255)

    fade_in(reversed_music_pos_text, speed=10, max_alpha=255)
    
    if total_progress_bar_width < album_cover.get_width(): # animation
        total_progress_bar_width += (album_cover.get_width() - total_progress_bar_width) / 5

def update_note():
    global note_y, note_path, note
    if round(note_y) - 0.1 <= 450: # show particle
        time.sleep(0.1)
        note_path = get_note()
        note = pygame.image.load(note_path)
        note_y = HEIGHT / 2 + 50
    else:
        note_y += (450 - note_y) * 0.1
        time.sleep(0.01)

def paste_album_picture():
    global temp_album_cover
    if (id3[5] is None):
        img = Image.open('./Resources/icons/unknown_album.png')
    else:
        img = Image.open(io.BytesIO(id3[5]))
    for img_format in ['RGB', 'RGBA', 'RGBX', 'ARGB', 'BGRA', 'P']: # this list include priority (try RGB, RGBA first)
        try:
            temp_album_cover = pygame.image.frombytes(img.tobytes(), img.size, img_format).convert_alpha()
        except ValueError:
            continue # if ValueError, which means the album image is not this format
        else:
            break
    temp_album_cover = pygame.transform.smoothscale(temp_album_cover, (WIDTH / 3.4, WIDTH / 3.4))

# let program support high-dpi resolution
ctypes.windll.shcore.SetProcessDpiAwareness(1)
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 125

if 1:
    WIDTH = int(1600 * scale_factor)
    HEIGHT = int(900 * scale_factor)
    SUPPORTED_FORMATS = ['mp3', 'ogg', 'wav']

    # pygame setup
    pygame.init() # Pygame, launch!
    pygame.mixer.init() # init pygame mixer
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) # set screen
    pygame.display.set_caption('Music Player') # window title
    music_busy = False # True if there's music playing
    music_pos: float = 0.0 # position of music (seconds)
    music_length: float = 0.0 # total length of music (seconds)
    music_metadata = {} # metadata of music
    background_path = get_background() # path of background
    background = pygame.image.load(background_path) # random background
    background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))
    blurred_background = pygame.transform.box_blur(background, 0) # background but blurry, for play screen
    note_path = get_note() # path of note particle
    note = pygame.image.load(note_path) # draw particle when playing music
    note = pygame.transform.scale(note, (64, 64))
    note_y = HEIGHT / 2 + 25
    info_background = pygame.Surface((WIDTH, HEIGHT)) # a transparent black hover
    info_background.fill((0, 0, 0))
    info_background.set_alpha(0)
    # Music cover - step 1. temporarily load the image
    temp_album_cover = pygame.image.load('./Resources/icons/unknown_album.png').convert_alpha()
    temp_album_cover.set_alpha(0)
    # Music Cover - step 2. ... then create a pygame.Surface ...
    album_cover = pygame.Surface(temp_album_cover.get_size(), flags=pygame.SRCALPHA) #
    album_cover = pygame.transform.smoothscale(album_cover, (WIDTH / 3.4, WIDTH / 3.4))
    # the information of mp3 file
    id3 = ()   # assignment later
    music_title_text = pygame.font.Font('./Resources/fonts/Bold.OTF').render('', antialias=True, color=(255, 255, 255))
    music_title_text.set_alpha(0)
    music_artist_text = pygame.font.Font('./Resources/fonts/Bold.OTF').render('', antialias=True, color=(255, 255, 255))
    music_artist_text.set_alpha(0)
    music_pos_text = pygame.font.Font('./Resources/fonts/Medium.OTF').render('', antialias=True, color=(150, 150, 150))
    music_pos_text.set_alpha(100)
    reversed_music_pos_text = pygame.font.Font('./Resources/fonts/Medium.OTF').render('', antialias=True, color=(150, 150, 150))
    reversed_music_pos_text.set_alpha(100)
    # music progress bar will draw on a surface instead of screen
    progress_bar_surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
    progress_bar_surface.set_alpha(100)
    progress_bar_surface.set_colorkey((0, 0, 0))
    # width of progress bar, make it resizeable
    total_progress_bar_width = 0
    music_progress_width = 0
    # save fonts
    debug_font = pygame.font.SysFont('Cascadia Code', 25)
    bold_font = pygame.font.Font('./Resources/fonts/Bold.OTF', 30)
    medium_font = pygame.font.Font('./Resources/fonts/Medium.OTF', 30)
    small_font = pygame.font.Font('./Resources/fonts/Medium.OTF', 20)
    # True if open debug screen (F3)
    toggle_debug_screen = False
    debug_screen_text = debug_font.render('', antialias=True, color='white')
    clock = pygame.time.Clock()
    # False if click the close button
    running = True
    dt = 0
    # for animation
    background_blur_radius = 0
    lock = threading.Lock() # thread lock

def thread_it(func, *args: tuple):
    # pack functions into a thread
    t = threading.Thread(target=func, args=args) 
    t.daemon = True
    t.start()

def animations():
    
    global note, note_y, note_path, background, blurred_background, background_blur_radius, total_progress_bar_width
    
    note_path = get_note() # random note path
    # note = pygame.image.load(note_path)
    note = pygame.transform.scale(note, (64, 64))
    while running:
        if music_busy: # if music playing....
            update_note()
            enter_animation()
        else:
            total_progress_bar_width = 0

            blur_out(speed=1, min_blur_radius=0)

            fade_out(info_background, speed=10, min_alpha=0)

            fade_out(album_cover, speed=50, min_alpha=0)
            
            fade_out(music_title_text, speed=30, min_alpha=0)

            fade_out(music_artist_text, speed=30, min_alpha=0)
            
            # fade_out(progress_bar_surface, speed=30, min_alpha=0)

            fade_out(music_pos_text, speed=30, min_alpha=0)

            fade_out(reversed_music_pos_text, speed=30, min_alpha=0)

def process_music():
    global music_busy, music_pos, music_metadata, id3, music_title_text, music_title, music_artist, music_artist_text, album_name, music_pos_text, reversed_music_pos_text
    while running:
        music_busy = pygame.mixer.music.get_busy()
        if music_busy:
            music_pos = pygame.mixer.music.get_pos() / 1000 # millseconds -> seconds, 1000ms=1s
            music_metadata = pygame.mixer.music.get_metadata()
            paste_album_picture()

            pygame.draw.rect(album_cover, 'white', temp_album_cover.get_rect(), border_radius=int(10 / scale_factor))
            album_cover.blit(temp_album_cover, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            # MUSIC INFO ------------------------------------------------------------------------
            music_title = id3[1]
            if music_title is None:
                music_title = id3[0]
            # i = len(music_title)
            # while music_title_text.get_width() > WIDTH / 3.4:
            #     music_title = music_title[:i+1]
            #     i -= 1
            # else:
            #     music_title = music_title[:-3] + '...'
            music_title_text = bold_font.render(music_title, antialias=True, color=(255, 255, 255))

            music_artist = id3[2]
            if music_artist is None:
                music_artist = ''
            music_artist_text = bold_font.render(music_artist, antialias=True, color=(255, 255, 255))
            album_name = id3[3]
            music_pos_text = small_font.render('{:0=2d}:{:0=2d}'.format(int(music_pos // 60), int(music_pos % 60)),
                                                 antialias=True, color=(150, 150, 150))
            reversed_music_pos_text = small_font.render('{:0=2d}:{:0=2d}'.format(int((id3[4] - music_pos) // 60), int((id3[4] - music_pos) % 60)),
                                                 antialias=True, color=(150, 150, 150))

def draw_window():
    '''Draw the screen.'''
    global background, blurred_background, info_background, background_blur_radius, note, note_y, music_title_text, music_artist_text, debug_screen_text, draw_window_perf
    if toggle_debug_screen:
        debug_screen_text = debug_font.render(
'''Music Player by Doushabao_233
{fps} fps
draw_window function performance: {draw_perf_sec}s, [{draw_perf}]
background: {bg_img}
is playing? {is_playing}
Python version {python_ver}
mouse: {mouse_x} {mouse_y}
note y: {note_y}
中文测试
screen: {screen_width}x{screen_height}
info background alpha: {info_bg_alpha}
background blur variable: {bg_blur_var}
total progessbar width: {total_prog_bar_width}
music metadata: {music_meta}'''.format(
                fps=round(clock.get_fps()),
                draw_perf_sec=floor(draw_window_perf * 100000) / 100000,
                draw_perf='█' * int(round(draw_window_perf, 2) * 150),
                bg_img=background_path,
                is_playing=music_busy,
                python_ver=sys.version,
                mouse_x=pygame.mouse.get_pos()[0],
                mouse_y=pygame.mouse.get_pos()[1],
                note_y=round(note_y, 4),
                screen_width=WIDTH,
                screen_height=HEIGHT,
                info_bg_alpha=info_background.get_alpha(),
                bg_blur_var=background_blur_radius,
                total_prog_bar_width=total_progress_bar_width,
                # music_pos=floor(music_pos * 100) / 100, music_length=floor(id3[4] * 100) / 100, playing_ratio=floor((music_pos/id3[4]) * 100),
                music_meta=music_metadata
                ),

            antialias=True,
            color='white',
            bgcolor=(0, 0, 0, 100)
        )
    if music_busy: # when start a sound
        # MUSIC PROGRESS BAR ----------------------------------------------------------------
        pygame.draw.rect(progress_bar_surface, (150, 150, 150), pygame.Rect(WIDTH / 25, HEIGHT / 2 + 100 + 40 + 60, total_progress_bar_width, 10), border_radius=10)
        pygame.draw.rect(progress_bar_surface, (245, 245, 245), pygame.Rect(WIDTH / 25, HEIGHT / 2 + 100 + 40 + 60, ((total_progress_bar_width * (music_pos / id3[4]))), 10, border_radius=10))
        
        

    screen.blit(blurred_background, (0, 0))
    if music_busy:
        note = pygame.transform.scale(note, (64, 64))
        screen.blit(note, (WIDTH / 2 - note.get_width() / 2, note_y))
    screen.blit(info_background, (0, 0))
    screen.blit(album_cover, (WIDTH / 25, WIDTH / 25))
    if music_busy:
        info_background.fill((0, 0, 0))
        info_background.blit(music_title_text, (WIDTH / 25, HEIGHT / 2 + 100))
        music_artist_text.set_alpha(200) # must be
        info_background.blit(music_artist_text, (WIDTH / 25, HEIGHT / 2 + 100 + 40))
        info_background.blit(music_pos_text, (WIDTH / 25, HEIGHT / 2 + 100 + 40 + 60 + 10 + 5))
        info_background.blit(reversed_music_pos_text, (WIDTH / 25 + total_progress_bar_width - reversed_music_pos_text.get_width(), HEIGHT / 2 + 100 + 40 + 60 + 10 + 5))
        info_background.blit(progress_bar_surface, (0, 0)) # just put at 0, 0
    if toggle_debug_screen: screen.blit(debug_screen_text, (10, 10))
    pygame.display.flip() # refresh screen

thread_it(animations)
thread_it(process_music)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit program
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F3: # toggle debug screen
            toggle_debug_screen = not toggle_debug_screen
        elif event.type == pygame.DROPFILE: # catch files
            if event.dict['file'].split('.')[-1] in SUPPORTED_FORMATS:
                id3 = parse_file(event.dict['file'])
                pygame.mixer.music.load(event.dict['file'])
                pygame.mixer.music.play()
            else:
                print('illegal file format detected:', event.dict['file'].split('.')[-1])
        elif event.type == pygame.WINDOWRESIZED: # WIP
            WIDTH = event.dict['x']
            HEIGHT = event.dict['y']
            screen.fill((0, 0 ,0))
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            screen.fill((0, 0 ,0))
    perf_start = time.perf_counter() # for debug
    draw_window()
    draw_window_perf = time.perf_counter() - perf_start
    clock.tick(60)

pygame.quit()