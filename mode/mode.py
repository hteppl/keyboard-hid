from enum import IntEnum


class ModeFlags(IntEnum):
    MODE_FLAG_HAS_SPEED = 1 << 0  # Mode has speed parameter
    MODE_FLAG_HAS_DIRECTION_LR = 1 << 1  # Mode has left/right parameter
    MODE_FLAG_HAS_DIRECTION_UD = 1 << 2  # Mode has up/down parameter
    MODE_FLAG_HAS_DIRECTION_HV = 1 << 3  # Mode has horiz/vert parameter
    MODE_FLAG_HAS_BRIGHTNESS = 1 << 4  # Mode has brightness parameter
    MODE_FLAG_HAS_PER_LED_COLOR = 1 << 5  # Mode has per-LED colors
    MODE_FLAG_HAS_MODE_SPECIFIC_COLOR = 1 << 6  # Mode has mode specific colors
    MODE_FLAG_HAS_RANDOM_COLOR = 1 << 7  # Mode has random color option
    MODE_FLAG_MANUAL_SAVE = 1 << 8  # Mode can manually be saved
    MODE_FLAG_AUTOMATIC_SAVE = 1 << 9  # Mode automatically saves


class ModeDirections(IntEnum):
    MODE_DIRECTION_LEFT = 0
    MODE_DIRECTION_RIGHT = 1
    MODE_DIRECTION_UP = 2
    MODE_DIRECTION_DOWN = 3
    MODE_DIRECTION_HORIZONTAL = 4
    MODE_DIRECTION_VERTICAL = 5


class ModeColors(IntEnum):
    MODE_COLORS_NONE = 0
    MODE_COLORS_PER_LED = 1
    MODE_COLORS_MODE_SPECIFIC = 2
    MODE_COLORS_RANDOM = 3


def get_r_value(rgb):
    return rgb & 0x000000FF


def get_g_value(rgb):
    return (rgb >> 8) & 0x000000FF


def get_b_value(rgb):
    return (rgb >> 16) & 0x000000FF


def to_rgb_color(r, g, b):
    return (b << 16) | (g << 8) | r


def get_direction_lr_ud(d):
    if d == ModeDirections.MODE_DIRECTION_LEFT:
        return 0x10
    elif d == ModeDirections.MODE_DIRECTION_RIGHT:
        return 0x00
    elif d == ModeDirections.MODE_DIRECTION_UP:
        return 0x20
    elif d == ModeDirections.MODE_DIRECTION_DOWN:
        return 0x30
    else:
        return 0x00


def get_direction_ud(d):
    if d == ModeDirections.MODE_DIRECTION_UP:
        return 0xA0
    elif d == ModeDirections.MODE_DIRECTION_DOWN:
        return 0xB0
    else:
        return 0xA0


class Mode:
    def __init__(self, name, value, flags):
        self.name: str = name
        self.value: int = value
        self.flags: int = flags
        self.speed_min = 0
        self.speed_max = 0
        self.brightness_min = 0
        self.brightness_max = 0
        self.colors_min = 0
        self.colors_max = 0
        self.speed = 0
        self.brightness = 0
        self.direction = 0
        self.color_mode = 0
        self.colors = [0]
