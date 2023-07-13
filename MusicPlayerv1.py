import eyed3
import pylrc
from playsound import playsound


audiofile = eyed3.load('大海.mp3')
lyrics = audiofile.tag.lyrics

lrc_string = lyrics[0].text

subs = pylrc.parse(lrc_string)

# playsound('大海.mp3', block = True)
for sub in subs:
    min = sub.minutes
    sec = sub.seconds
    ms = sub.milliseconds
    text = sub.text

    total_ms = ms + sec * 1000 + min * 60 * 1000
    total_sec = total_ms / 1000

    print('时间：{}s 歌词：{}'.format(total_sec, text))

