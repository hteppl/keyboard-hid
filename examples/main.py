import hid

from kb.keyrox_tkl import KeyroxTKL
from mode.keyrox_tkl import get_mode, ModeList


def list_devices():
    for device_dict in hid.enumerate():
        keys = list(device_dict.keys())
        keys.sort()
        for key in keys:
            print("%s : %s" % (key, device_dict[key]))
        print()


if __name__ == '__main__':
    # use this for detect your keyboard path
    # list_devices()
    
    tkl = KeyroxTKL(b'\\\\?\\HID#VID_1A2C&PID_1511&MI_03#7&1a7ae6a3&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}')
    
    mode = get_mode(ModeList.CUSTOM_MODE_VALUE)
    tkl.set_mode(mode)
    
    tkl.get_key_buffer().add(1, 255, 255, 255)
    tkl.release_key_buffer()
