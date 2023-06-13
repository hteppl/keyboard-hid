from abc import ABC, abstractmethod
from typing import List

import hid

from mode.mode import Mode, to_rgb_color


class ColoredKey:
    def __init__(self, key: int, r: int, g: int, b: int):
        self.key = key
        self.color = to_rgb_color(r, g, b)


class KeyBuffer:
    def __init__(self):
        self.buffer: List[ColoredKey] = []
    
    def add(self, key: int, r: int, g: int, b: int) -> None:
        self.buffer.append(ColoredKey(key, r, g, b))
    
    def clear(self):
        self.buffer = []


class Keyboard(ABC):
    def __init__(self, path: bytes, packet_len: int):
        self.device: hid.device = hid.device()
        self.device.open_path(path)
        self.packet_len: int = packet_len
        self.mode: Mode or None = None
        self.key_buffer = KeyBuffer()
        
        print("Manufacturer: %s" % self.device.get_manufacturer_string())
        print("Product: %s" % self.device.get_product_string())
    
    def close(self) -> None:
        self.device.close()
    
    def get_buffer(self) -> bytearray:
        buffer = bytearray(self.packet_len)
        buffer[:] = [0x00] * self.packet_len
        return buffer
    
    @abstractmethod
    def send(self, data) -> None:
        pass
    
    def get_key_buffer(self) -> KeyBuffer:
        return self.key_buffer
    
    def reset_release_buffer(self) -> None:
        self.key_buffer.clear()
    
    def set_mode(self, mode: Mode) -> None:
        self.mode = mode
        self._set_mode_value(mode)
        self._set_mode_data(mode)
    
    @abstractmethod
    def _set_mode_value(self, mode: Mode) -> None:
        pass
    
    @abstractmethod
    def _set_mode_data(self, mode: Mode) -> None:
        pass
    
    @abstractmethod
    def release_key_buffer(self) -> None:
        pass
