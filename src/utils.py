import os
import json
from pygame import mixer

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def play_music(path, loops=-1, volume=0.6):
    try:
        mixer.music.load(path)
        mixer.music.set_volume(volume)
        mixer.music.play(loops=loops)
    except Exception as e:
        print('Music error:', e)

def load_sfx(path):
    try:
        return mixer.Sound(path)
    except Exception:
        return None

def clamp(v, a, b):
    return max(a, min(b, v))