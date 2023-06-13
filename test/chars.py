import json
import os
import random
import time
from typing import List

from kb.keyboard import Keyboard, ColoredKey

char_zones = [
    [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    [38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
    [59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
    [77, 78, 79, 80, 81, 82, 83, 84, 85, 86]
]

max_length = max(len(zone) for zone in char_zones)
chars = dict()


def parse_chars(directory='lang'):
    global chars
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        
        if file_name.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    json_data = json.load(file)
                    for key, value in json_data.items():
                        chars[key] = value
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON from file '{file_name}': {str(e)}")
                except UnicodeDecodeError as e:
                    print(f"Error parsing Unicode from file '{file_name}': {str(e)}")
                except IOError as e:
                    print(f"Error reading file '{file_name}': {str(e)}")


def add_char(keyboard: Keyboard, index: int, char: List[List[int]], color=(255, 255, 255)) -> None:
    for i in range(len(char)):
        for j in range(len(char[i])):
            if char[i][j]:
                key = index + j
                length = len(char_zones[i])
                if key < 0 or key >= length:
                    continue
                keyboard.get_release_buffer().append(
                    ColoredKey().from_rgb(char_zones[i][key], color[0], color[1], color[2])
                )


def release_text(keyboard: Keyboard, text: str, delay: float = 0.35) -> None:
    global chars
    
    space = 2
    chars_arr = []
    colors_arr = []
    for ch in text:
        chars_arr.append(chars[ch])
        colors_arr.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    start = max_length
    index_arr = []
    for ch in chars_arr:
        char_size = len(ch[0])
        index_arr.append(start + char_size)
        start += (char_size + space)
    
    chars_len = sum(len(ch[0]) for ch in chars_arr)
    for i in range(max_length + chars_len + space * len(text)):
        for j in range(len(chars_arr)):
            add_char(keyboard, index_arr[j], chars_arr[j], colors_arr[j])
        for k in range(len(chars_arr)):
            index_arr[k] -= 1
        keyboard.release_keys()
        time.sleep(delay)
        keyboard.reset_release_buffer()


parse_chars()
