from enum import IntEnum

from mode.mode import Mode, ModeFlags, ModeColors, to_rgb_color


class ModeList(IntEnum):
    WAVE_MODE_VALUE = 0x00
    CONST_MODE_VALUE = 0x01
    BREATHE_MODE_VALUE = 0x02
    HEARTRATE_MODE_VALUE = 0x03
    POINT_MODE_VALUE = 0x04
    WINNOWER_MODE_VALUE = 0x05
    STARS_MODE_VALUE = 0x06
    SPECTRUM_MODE_VALUE = 0x07
    PLUMFLOWER_MODE_VALUE = 0x08
    SHOOT_MODE_VALUE = 0x09
    AMBILIGHT_ROTATE_MODE_VALUE = 0x0A
    RIPPLE_MODE_VALUE = 0x0B
    CUSTOM_MODE_VALUE = 0x0C


class Settings(IntEnum):
    KEYROX_BRIGHTNESS_MIN = 0x00
    KEYROX_BRIGHTNESS_MAX = 0x7F
    KEYROX_SPEED_MIN = 0x00
    KEYROX_SPEED_MAX = 0x04


modes_data = [
    Mode("Custom",
         ModeList.CUSTOM_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_PER_LED_COLOR
         ),
    Mode("Wave",
         ModeList.WAVE_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_SPEED
         | ModeFlags.MODE_FLAG_HAS_DIRECTION_LR
         | ModeFlags.MODE_FLAG_HAS_DIRECTION_UD
         ),
    Mode("Const",
         ModeList.CONST_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR
         | ModeFlags.MODE_FLAG_HAS_BRIGHTNESS
         ),
    Mode("Breathe",
         ModeList.BREATHE_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_RANDOM_COLOR
         | ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR
         | ModeFlags.MODE_FLAG_HAS_SPEED
         ),
    Mode("Heartrate",
         ModeList.HEARTRATE_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_RANDOM_COLOR
         | ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR
         | ModeFlags.MODE_FLAG_HAS_SPEED
         ),
    Mode("Point",
         ModeList.POINT_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_RANDOM_COLOR
         | ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR
         | ModeFlags.MODE_FLAG_HAS_SPEED
         ),
    Mode("Winnower",
         ModeList.WINNOWER_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_SPEED
         | ModeFlags.MODE_FLAG_HAS_DIRECTION_UD),
    Mode("Stars",
         ModeList.STARS_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_RANDOM_COLOR
         | ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR
         | ModeFlags.MODE_FLAG_HAS_SPEED
         ),
    Mode("Spectrum",
         ModeList.SPECTRUM_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_SPEED
         ),
    Mode("Plumflower", ModeList.PLUMFLOWER_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_RANDOM_COLOR
         | ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR
         | ModeFlags.MODE_FLAG_HAS_SPEED
         ),
    Mode("Shoot", ModeList.SHOOT_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_RANDOM_COLOR
         | ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR
         | ModeFlags.MODE_FLAG_HAS_SPEED
         ),
    Mode("Ambilight Rotate", ModeList.AMBILIGHT_ROTATE_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_SPEED
         | ModeFlags.MODE_FLAG_HAS_DIRECTION_UD
         ),
    Mode("Ripple", ModeList.RIPPLE_MODE_VALUE,
         ModeFlags.MODE_FLAG_HAS_RANDOM_COLOR
         | ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR
         | ModeFlags.MODE_FLAG_HAS_SPEED
         )
]


def get_mode(mode: ModeList):
    for m in modes_data:
        if m.value == mode:
            return m
    return modes_data[0]


for m in modes_data:
    m.flags = m.flags | ModeFlags.MODE_FLAG_HAS_BRIGHTNESS
    
    if m.flags & ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR:
        m.color_mode = ModeColors.MODE_COLORS_MODE_SPECIFIC
        m.colors_min = 1
        m.colors_max = 1
        
        m.colors = [to_rgb_color(255, 255, 255)]
    elif m.flags & ModeFlags.MODE_FLAG_HAS_PER_LED_COLOR:
        m.color_mode = ModeColors.MODE_COLORS_PER_LED
    else:
        m.color_mode = ModeColors.MODE_COLORS_NONE
        m.colors_min = 0
        m.colors_max = 0
        m.colors = []
    
    if m.flags & ModeFlags.MODE_FLAG_HAS_SPEED:
        m.speed_min = Settings.KEYROX_SPEED_MIN
        m.speed_max = Settings.KEYROX_SPEED_MAX
        m.speed = m.speed_max
    
    if m.flags & ModeFlags.MODE_FLAG_HAS_BRIGHTNESS:
        m.brightness_min = Settings.KEYROX_BRIGHTNESS_MIN
        m.brightness_max = 0xFF if m.flags & ModeFlags.MODE_FLAG_HAS_PER_LED_COLOR else Settings.KEYROX_BRIGHTNESS_MAX
        m.brightness = m.brightness_max
