# Example file showing a circle moving on screen
import ctypes
import random
import threading
import os
import sys
import time
import stagger
sys.stdout = open('nul', 'w')
import pygame
import pygame.gfxdraw
sys.stdout.close()
sys.stdout = sys.__stdout__
from PIL import Image
import io

def parse_file(path):
    '''This function parses the ID3 information from the song, encompassing details such as the title, artist, album, and image.
    It returns a tuple in the following format: ('mp3 file name', 'music title', 'artist', 'album', [binary image data]).
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

    return os.path.basename(path), title, artist, album, picture

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
    '''This function returns a path randomly. Like: ./Resources/particles/note_blue.png'''
    path = './Resources/particles'
    dirs = os.listdir(path)
    return './Resources/particles/{}'.format(random.choices(dirs)[0])

# pygame setup

ctypes.windll.shcore.SetProcessDpiAwareness(1)
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 125

WIDTH = int(1600 * scale_factor)
HEIGHT = int(900 * scale_factor)
SUPPORTED_FORMATS = ['mp3', 'ogg', 'wav']

pygame.init() # Pygame，启动！
pygame.mixer.init()
# pygame.mixer.music.load(r'C:\Users\Lenovo\Music\张雨生\口是心非 - 张雨生.mp3')
# pygame.mixer.music.play()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Music Player')
background_path = get_background()
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
blurred_background = pygame.transform.box_blur(background, 0)
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
music_title_text = pygame.font.Font('./Resources/fonts/Bold.OTF').render('', antialias=True, color=(255, 255, 255))
music_title_text.set_alpha(0)
music_artist_text = pygame.font.Font('./Resources/fonts/Bold.OTF').render('', antialias=True, color=(255, 255, 255))
music_artist_text.set_alpha(0)
progress_bar_surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
progress_bar_surface.fill((0, 0, 0, 0)) # idk why add it
progress_bar_surface.set_alpha(100)
total_progress_bar_width = 0
debug_font = pygame.font.SysFont('Cascadia Code', 25)
bold_font = pygame.font.Font('./Resources/fonts/Bold.OTF', 30)
debug_screen = False
clock = pygame.time.Clock()
running = True
dt = 0
background_blur_radius = 0
lock = threading.Lock()

def thread_it(func, *args: tuple):
    # 创建
    t = threading.Thread(target=func, args=args) 
    t.daemon = True
    t.start()

def animations():
    
    global note, note_y, note_path, background, blurred_background, background_blur_radius, total_progress_bar_width
    
    note_path = get_note()
    # note = pygame.image.load(note_path)
    note = pygame.transform.scale(note, (64, 64))
    while running:
        if not pygame.mixer.get_init():
            break
        if pygame.mixer.music.get_busy():
            if round(note_y) - 0.1 <= 450:   
                time.sleep(0.1)
                note_path = get_note()
                note = pygame.image.load(note_path)
                note_y = HEIGHT / 2 + 50
            else:
                note_y += (450 - note_y) * 0.1
                time.sleep(0.01)
            
            if background_blur_radius < 10:
                background_blur_radius += 1
                blurred_background = pygame.transform.box_blur(background, background_blur_radius)
            
            if info_background.get_alpha() < 200:
                info_background.set_alpha(info_background.get_alpha() + 10)
            
            if album_cover.get_alpha() < 255:
                album_cover.set_alpha(album_cover.get_alpha() + 30)

            if music_title_text.get_alpha() < 255:
                music_title_text.set_alpha(music_title_text.get_alpha() + 1)
            
            if music_artist_text.get_alpha() < 255:
                music_artist_text.set_alpha(music_artist_text.get_alpha() + 1)
            
            if total_progress_bar_width < album_cover.get_width():
                total_progress_bar_width += (album_cover.get_width() - total_progress_bar_width) / 5
        else:
            total_progress_bar_width = 0

            if background_blur_radius > 0:
                background_blur_radius -= 1
                blurred_background = pygame.transform.box_blur(background, background_blur_radius)       

            if info_background.get_alpha() > 0:
                info_background.set_alpha(info_background.get_alpha() - 10)

            if album_cover.get_alpha() > 0:
                album_cover.set_alpha(album_cover.get_alpha() - 50)
            
            if music_title_text.get_alpha() > 0:
                music_title_text.set_alpha(music_title_text.get_alpha() - 30)

            if music_artist_text.get_alpha() > 0:
                music_artist_text.set_alpha(music_artist_text.get_alpha() - 30)
            
            # if progress_bar_surface.get_alpha() > 0:
                # progress_bar_surface.set_alpha(progress_bar_surface.get_alpha() - 30)

def draw_window():
    '''Draw the screen.'''
    global background, blurred_background, info_background, background_blur_radius, note, music_title_text, music_artist_text
    debug_screen_text = debug_font.render('', antialias=True, color='white')
    if debug_screen:
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
total progessbar width: {total_prog_bar_width}'''.format(
                fps=round(clock.get_fps()),
                draw_perf_sec=str(draw_window_perf)[:6],
                draw_perf='█' * int(round(draw_window_perf, 2) * 150),
                bg_img=background_path,
                is_playing=pygame.mixer.music.get_busy(),
                python_ver=sys.version,
                mouse_x=pygame.mouse.get_pos()[0],
                mouse_y=pygame.mouse.get_pos()[1],
                note_y=round(note_y, 4),
                screen_width=WIDTH,
                screen_height=HEIGHT,
                info_bg_alpha=info_background.get_alpha(),
                bg_blur_var=background_blur_radius,
                total_prog_bar_width=total_progress_bar_width
                ),

            antialias=True,
            color='white',
            bgcolor=(0, 0, 0, 100)
        )
    if pygame.mixer.music.get_busy(): # when start a sound
        # MUSIC INFO ------------------------------------------------------------------------
        music_title = id3[1]
        if music_title is None:
                music_title = id3[0]
        music_title_text = bold_font.render(music_title, antialias=True, color=(255, 255, 255))
        music_artist = id3[2]
        if music_artist is None:
                music_artist = ''
        music_artist_text = bold_font.render(music_artist, antialias=True, color=(255, 255, 255))
        music_artist_text.set_alpha(200) # must be
        album_name = id3[3]
        # MUSIC ALBUM PICTURE ---------------------------------------------------------------
        if id3[4] is None:
                img = Image.open('./Resources/icons/unknown_album.png')
        else:
                img = Image.open(io.BytesIO(id3[4]))
        for i in ['RGB', 'RGBA', 'RGBX', 'ARGB', 'BGRA', 'P']: # this list include priority (try RGB, RGBA first)
                try:
                    temp_album_cover = pygame.image.frombytes(img.tobytes(), img.size, i).convert_alpha()
                except ValueError:
                    continue # if ValueError, which means the album image is not this format
                else:
                    break
        temp_album_cover = pygame.transform.smoothscale(temp_album_cover, (WIDTH / 3.4, WIDTH / 3.4))

        pygame.draw.rect(album_cover, 'white', temp_album_cover.get_rect(), border_radius=int(10 / scale_factor))
        album_cover.blit(temp_album_cover, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        # MUSIC PROGRESS BAR ----------------------------------------------------------------
        pygame.draw.rect(progress_bar_surface, (150, 150, 150), pygame.Rect(WIDTH / 25, HEIGHT / 2 + 100 + 40 + 60, total_progress_bar_width, 10), border_radius=10)
        
        

    screen.blit(blurred_background, (0, 0))
    if pygame.mixer.music.get_busy():
        note = pygame.transform.scale(note, (64, 64))
        screen.blit(note, (WIDTH / 2 - note.get_width() / 2, note_y))
    screen.blit(info_background, (0, 0))
    screen.blit(album_cover, (WIDTH / 25, WIDTH / 25))
    if pygame.mixer.music.get_busy():
        screen.blit(music_title_text, (WIDTH / 25, HEIGHT / 2 + 100))
        screen.blit(music_artist_text, (WIDTH / 25, HEIGHT / 2 + 100 + 40))
        screen.blit(progress_bar_surface, (0, 0)) # just put at 0, 0
    screen.blit(debug_screen_text, (10, 10))
    pygame.display.flip()

thread_it(animations)
while running:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT: # quit program
            running = False
        elif event.type == pygame.DROPFILE: # catch files
            progress_bar_surface.fill((0, 0, 0))
            if event.dict['file'].split('.')[-1] in SUPPORTED_FORMATS:
                id3 = parse_file(event.dict['file'])
                pygame.mixer.music.load(event.dict['file'])
                pygame.mixer.music.play()
            else:
                print('illegal file format detected:', event.dict['file'].split('.')[-1])
        elif event.type == pygame.KEYDOWN: # toggle debug screen
            if event.key == pygame.K_F3:
                debug_screen = not debug_screen 
        elif event.type == pygame.WINDOWRESIZED:
            WIDTH = event.dict['x']
            HEIGHT = event.dict['y']
            screen.fill((0, 0 ,0))
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            screen.fill((0, 0 ,0))
    perf_start = time.perf_counter()
    draw_window()
    draw_window_perf = time.perf_counter() - perf_start
    clock.tick(60)

pygame.quit()