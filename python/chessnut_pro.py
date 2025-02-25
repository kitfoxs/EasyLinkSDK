import ctypes
import logging

# Load the shared library
lib = ctypes.CDLL('path/to/your/library.so')

# Define the function prototypes
lib.cl_version.argtypes = [ctypes.c_char_p]
lib.cl_version.restype = ctypes.c_size_t

lib.cl_connect.argtypes = []
lib.cl_connect.restype = ctypes.c_int

lib.cl_disconnect.argtypes = []
lib.cl_disconnect.restype = None

lib.cl_switch_real_time_mode.argtypes = []
lib.cl_switch_real_time_mode.restype = ctypes.c_int

lib.cl_switch_upload_mode.argtypes = []
lib.cl_switch_upload_mode.restype = ctypes.c_int

lib.cl_set_readtime_callback.argtypes = [ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_size_t)]
lib.cl_set_readtime_callback.restype = None

lib.cl_beep.argtypes = [ctypes.c_ushort, ctypes.c_ushort]
lib.cl_beep.restype = ctypes.c_int

lib.cl_led.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
lib.cl_led.restype = ctypes.c_int

lib.cl_get_mcu_version.argtypes = [ctypes.c_char_p]
lib.cl_get_mcu_version.restype = ctypes.c_size_t

lib.cl_get_ble_version.argtypes = [ctypes.c_char_p]
lib.cl_get_ble_version.restype = ctypes.c_size_t

lib.cl_get_battery.argtypes = []
lib.cl_get_battery.restype = ctypes.c_int

lib.cl_get_file_count.argtypes = []
lib.cl_get_file_count.restype = ctypes.c_int

lib.cl_get_file_and_delete.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
lib.cl_get_file_and_delete.restype = ctypes.c_int

lib.cl_get_file_and_keep.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
lib.cl_get_file_and_keep.restype = ctypes.c_int

# Define the Python functions
def get_version():
    version = ctypes.create_string_buffer(20)
    length = lib.cl_version(version)
    if length > 0:
        return version.value.decode('utf-8')
    else:
        logging.error("Failed to get SDK version")
        return None

def connect():
    result = lib.cl_connect()
    if result == 1:
        logging.info("Successfully connected to chessboard")
    else:
        logging.error("Failed to connect to chessboard")
    return result

def disconnect():
    lib.cl_disconnect()
    logging.info("Disconnected from chessboard")

def switch_real_time_mode():
    result = lib.cl_switch_real_time_mode()
    if result == 1:
        logging.info("Switched to real-time mode")
    else:
        logging.error("Failed to switch to real-time mode")
    return result

def switch_upload_mode():
    result = lib.cl_switch_upload_mode()
    if result == 1:
        logging.info("Switched to upload mode")
    else:
        logging.error("Failed to switch to upload mode")
    return result

def set_readtime_callback(callback):
    CALLBACK_TYPE = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_size_t)
    lib.cl_set_readtime_callback(CALLBACK_TYPE(callback))
    logging.info("Set real-time callback")

def beep(frequency=1000, duration=200):
    result = lib.cl_beep(frequency, duration)
    if result == 1:
        logging.info("Beeped")
    else:
        logging.error("Failed to beep")
    return result

def set_led(leds):
    led_array = (ctypes.c_char_p * 8)(*leds)
    result = lib.cl_led(led_array)
    if result == 1:
        logging.info("Set LED states")
    else:
        logging.error("Failed to set LED states")
    return result

def get_mcu_version():
    version = ctypes.create_string_buffer(100)
    length = lib.cl_get_mcu_version(version)
    if length > 0:
        return version.value.decode('utf-8')
    else:
        logging.error("Failed to get MCU version")
        return None

def get_ble_version():
    version = ctypes.create_string_buffer(100)
    length = lib.cl_get_ble_version(version)
    if length > 0:
        return version.value.decode('utf-8')
    else:
        logging.error("Failed to get BLE version")
        return None

def get_battery():
    level = lib.cl_get_battery()
    if level >= 0:
        return level
    else:
        logging.error("Failed to get battery level")
        return None

def get_file_count():
    count = lib.cl_get_file_count()
    if count >= 0:
        return count
    else:
        logging.error("Failed to get file count")
        return None

def get_file_and_delete(buffer_size=10240):
    buffer = ctypes.create_string_buffer(buffer_size)
    length = lib.cl_get_file_and_delete(buffer, buffer_size)
    if length > 0:
        return buffer.value.decode('utf-8')
    elif length == 0:
        logging.warning("The game file is empty")
        return None
    elif length == -2:
        logging.error("Buffer too small to hold the game file")
        return None
    else:
        logging.error("Failed to retrieve game file")
        return None

def get_file_and_keep(buffer_size=10240):
    buffer = ctypes.create_string_buffer(buffer_size)
    length = lib.cl_get_file_and_keep(buffer, buffer_size)
    if length > 0:
        return buffer.value.decode('utf-8')
    elif length == 0:
        logging.warning("The game file is empty")
        return None
    elif length == -2:
        logging.error("Buffer too small to hold the game file")
        return None
    else:
        logging.error("Failed to retrieve game file")
        return None
