import logging
import smbus2
from dataclasses import dataclass, field
import re
logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)


class ArduinoService:
    ArduinoToAddressDict = {
        "ar1": "wda",
        "ar2": "wodm"
    }

    def __init__(self):
        pass

    def write_block_data(addr: str, bytes: list) -> None:
        pass


arduino_service = ArduinoService()


@dataclass
class Pump:
    ML_P_MS = 0.045
    PUMP_STARTED = 65,
    pump_code: str = field()
    bottle: str = field(default="")
    amount: int = field
    internal: str = field(default=False)
    tube_volume: int = field()
    confirm_flush_internal: bool = field(default=False)

    def __post_init__(self):
        [arduino_id, pump_id] = self.pump_code.split("-")
        self.pump_number: str = re.findall(r"(\d+)", pump_id)[0]
        self.i2c_addr: bytes = ArduinoService.ArduinoToAddressDict[re.findall(
            r"(\d+)", arduino_id)[0]]

    def pour_amount(self, amount_to_pour: int):
        assert self.amount >= amount_to_pour
        self.amount -= amount_to_pour
        logger.info(f"Pumping '{amount_to_pour}mL from pump #{self.pump_code}'")
        self.send_pump_event(self.pump_code, amount_to_pour)

    def assert_enough_amount(self, needed_amount: int) -> None:
        if not self.amount >= needed_amount:
            raise ValueError(
                f"Pump #{self.pump_code} does not have enough '{self.bottle}'. Needs {needed_amount}ml, but only has {self.amount}mL")

    def set_confirm_flush_internal(self):
        self.confirm_flush_internal = True

    def flush(self) -> None:
        logger.info(f"Starting flushing procedure for {self.pump_logger_format()}'")
        if self.internal:
            self.__flush_internal()
        else:
            self.__flush_tubing()

    def __flush_internal(self):
        logger.info(f"Attempting to flush internal {self.pump_logger_format()}")
        if not self.confirm_flush_internal:
            logger.error(
                f"Internal flushing flag not set yet. Cancelling internal flushing for {self.pump_logger_format()}")
            raise Exception(
                "Internal flushing flag not set. Please confirm flushing before retrying")
        self.__flush_tubing()

    def __flush_tubing(self):
        logger.info(f"Flushing {self.pump_logger_format(())} with {self.tube_volume}mL")
        self.send_pump_event(self.tube_volume)

    def pump_logger_format(self):
        return f"pump #{self.pump_code} containing '{self.bottle}'"

    def send_pump_event(self, amount: int):
        logger.info(f"Sending pump event to {self.pump_logger_format()} for {amount}ml")
        time_bytes = self.__number_to_bytes(self.__calculate_ms(amount))
        # What does the initial write do?
        #  arduino_service.write_block_data(self.i2c_addr, [self.pump_started, *time_bytes])
        # [self.pump_started, *time_bytes])
        send = [self.pump_number, *time_bytes]
        logger.debug(
            f"Sending bytes to arduino on behalf of pump '{self.pump_code}'. Payload: {send}")
        arduino_service.write_block_data(self.i2c_addr, send)

    def __number_to_bytes(self, number: int):
        if number < 0 or number > 65535:
            raise ValueError(
                f"Invalid value '{number}'. Number must be between 0 and 65535 (16-bit range)")
        # Extract the two bytes using bitwise operations
        byte1 = (number >> 8) & 0xFF
        byte2 = number & 0xFF
        return [byte1, byte2]

    def __calculate_ms(self, ml):
        return int(ml / self.ML_P_MS)
