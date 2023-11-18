import platform
if platform.system() != "Windows":
    import smbus2
import logging
from typing import Sequence


logger = logging.getLogger(__name__)


def throw_on_windows(func):
    def wrapper(*args, **kwargs):
        if platform.system() == "Windows":
            logger.error(f"Function '{func.__name__}' does not work on Windows")
            return
            # raise Exception(f"Function cannot be called on {platform.system()}")
        return func(*args, **kwargs)
    return wrapper


class ArduinoServiceSingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if not ArduinoServiceSingleton.__instance:
            ArduinoServiceSingleton.__instance = ArduinoServiceClass()
        return ArduinoServiceSingleton.__instance


class ArduinoServiceClass:
    ArduinoToAddressDict = {
        "0": 0x4,
        "1": 0x5
    }
    MAX_ATTEMPTS = 9

    def __init__(self):
        self.attempt_i2c_connection()

    @throw_on_windows
    def attempt_i2c_connection(self):
        attempt = 0
        while True and attempt <= ArduinoServiceClass.MAX_ATTEMPTS:
            attempt += 1
            try:
                self.bus = smbus2.SMBus(1)  # will throw on connection issues
                break
            except Exception as e:
                if attempt > ArduinoServiceClass.MAX_ATTEMPTS:
                    logging.error(f"Error establishing connection with Arduino {e}")
                    break

    @throw_on_windows
    def write_block_data(self, addr: int, data: Sequence[int]) -> None:
        assert addr in ArduinoService.ArduinoToAddressDict.values()
        attempt = 0
        while True and attempt < ArduinoServiceClass.MAX_ATTEMPTS:
            attempt += 1
            try:
                self.bus.write_block_data(addr, 0, data)
                break
            except Exception as e:
                if attempt >= ArduinoServiceClass.MAX_ATTEMPTS:
                    logging.error(f"Error communicating with Arduino {e}")
                    break


ArduinoService = ArduinoServiceSingleton.get_instance()
