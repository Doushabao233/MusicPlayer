# 编前提醒：本脚本即将停止维护，建议维护v2版本！！

import threading
import time
import pygame
import jieba
import eyed3, pylrc
import sys
from mutagen.mp3 import MP3

stop_music = False
found_lyrics = False
cut_words = []
timer = 0

def thread_it(func, *args: tuple):
    '''将函数打包进线程 不会让主界面卡死'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    t.daemon = True
    t.start()

def timer_func():
    global timer
    start_time = time.time()
    while 1:
        timer = time.time() - start_time

def show_lyric_func(text: list, duration):
    # text like: ['如果', '大海', '能够', '唤回', '曾经', '的', '爱']
    for i in text:
        print(i, end='', flush=True)
        time.sleep(duration / len(text))
    # print(f' | dura: {duration} len: {len(text)} ')
    print()

def func():
    global stop_music

    # do stuff

    thread_it(timer_func) # start timer
    i = 0
    while 1:
        try:
            sub = subs[i]

            min = sub.minutes
            sec = sub.seconds
            ms = sub.milliseconds
            text = sub.text
            total_ms = ms + sec * 1000 + min * 60 * 1000
            total_sec = total_ms / 1000

            duration = 0.9
            # print(f'\n{total_sec} - {total_sec_last}, {duration}')
            # print('sub:', total_sec, '|', sub.text, 'timer:',round(timer,2))
            if abs(round(timer, 2) - round(total_sec, 2)) <= 0.1      or      total_sec == 0:
                thread_it(lambda: show_lyric_func(cut_words[i], duration))
                i += 1
            # else:
                # print('not')
        except IndexError as e:
            print('\nindex error', i, len(subs))
            stop_music = True
            break
        else:
            if i >= len(subs):
                break

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = input('path: ')

# init
pygame.mixer.init()
# get lyrics
try:
    audiofile = eyed3.load(path)
    lyrics = audiofile.tag.lyrics
    lrc_string = lyrics[0].text
    subs = pylrc.parse(lrc_string)  # !!!
    # print('successful get lyrics', [i.text for i in subs])
    for i in subs:
        cut_words.append(jieba.lcut(i.text))
except:
    print('未检测到歌词')
    found_lyrics = False
else:
    found_lyrics = True
# get the duration(sec) of mp3 file
try:
    audio = MP3(path)
    track_length = audio.info.length
except:
    print('读取歌曲长度失败')
    sys.exit()
pygame.mixer.music.load(path)
pygame.mixer.music.play()
if found_lyrics:
    thread_it(func)

while 1: # You must use time.sleep or smth else to make the script run, otherwise the music won't play. 
    if stop_music or timer > track_length:
        pygame.mixer.music.stop()
        break