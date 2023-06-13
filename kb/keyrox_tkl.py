import time

from exception.KeyBufferException import KeyBufferException
from kb.keyboard import Keyboard
from mode.keyrox_tkl import ModeList
from mode.mode import Mode, ModeFlags, get_r_value, get_g_value, get_b_value, get_direction_lr_ud, get_direction_ud, \
    ModeColors

PACKET_LENGTH = 520


class KeyroxTKL(Keyboard):
    def __init__(self, path):
        super().__init__(path, PACKET_LENGTH)
    
    def send(self, data: bytearray):
        buffer = bytearray([0x00] + list(data))
        self.device.send_feature_report(buffer)
        time.sleep(0.01)
    
    def _set_mode_value(self, mode: Mode) -> None:
        buffer = self.get_buffer()
        buffer[4] = 0x01
        buffer[6] = 0x04
        buffer[8] = mode.value
        self.send(buffer)
    
    def _set_mode_data(self, mode: Mode) -> None:
        if mode.value == ModeList.CUSTOM_MODE_VALUE:
            return
        
        buffer = self.get_buffer()
        buffer[4] = 0x09
        buffer[6] = 0x05
        buffer[7] = mode.value
        buffer[8] = mode.brightness
        buffer[9] = 0xFF
        
        if mode.flags & ModeFlags.MODE_FLAG_HAS_SPEED:
            buffer[10] = mode.speed
            buffer[11] = 0xFF
            
            if mode.value == ModeList.SPECTRUM_MODE_VALUE:
                buffer[10] += 0x80
        
        if mode.flags & ModeFlags.MODE_FLAG_HAS_MODE_SPECIFIC_COLOR:
            if mode.flags & ModeFlags.MODE_FLAG_HAS_RANDOM_COLOR and mode.color_mode == ModeColors.MODE_COLORS_RANDOM:
                buffer[10] += 0x80
            else:
                buffer[11] = get_r_value(mode.colors[0])
                buffer[12] = get_g_value(mode.colors[0])
                buffer[13] = get_b_value(mode.colors[0])
        
        if (mode.flags & ModeFlags.MODE_FLAG_HAS_DIRECTION_LR) and (mode.flags & ModeFlags.MODE_FLAG_HAS_DIRECTION_UD):
            buffer[10] += get_direction_lr_ud(mode.direction)
        elif (mode.flags & ModeFlags.MODE_FLAG_HAS_DIRECTION_UD) and not (
                mode.flags & ModeFlags.MODE_FLAG_HAS_DIRECTION_LR):
            buffer[10] += get_direction_ud(mode.direction)
        
        self.send(buffer)
    
    def release_key_buffer(self) -> None:
        if self.mode.value != ModeList.CUSTOM_MODE_VALUE:
            raise KeyBufferException()
        
        buffer = self.get_buffer()
        buffer[4] = 0xB0
        buffer[5] = 0x01
        buffer[6] = 0x07
        
        for i in self.key_buffer.buffer:
            offset = 7 + i.key * 4
            buffer[offset + 1] = get_r_value(i.color)
            buffer[offset + 2] = get_g_value(i.color)
            buffer[offset + 3] = get_b_value(i.color)
            buffer[offset + 4] = self.mode.brightness
        
        self.send(buffer)
