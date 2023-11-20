import logging

from dataclasses import dataclass, field
import re

# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
#                   filename="pump.log", encoding="utf-8", level=logging.DEBUG)
logger = logging.getLogger(__name__)

from datetime import datetime
from .arduino_service import ArduinoService


@dataclass
class Pump:
    ML_P_MS = 0.0045
    # PUMP_STARTED = 65,

    amount: int = field()
    pump_code: str = field()
    tube_volume: int = field()
    contains: str = field(default="")
    internal: bool = field(default=False)
    date_added: str = field(default=datetime.now().date().strftime("%Y-%m-%d"))

    def __post_init__(self):
        [arduino_id, pump_id] = self.pump_code.split("-")
        self.pump_number: int = int(re.findall(r"(\d+)", pump_id)[0])
        self.i2c_addr: int = ArduinoService.ArduinoToAddressDict[re.findall(
            r"(\d+)", arduino_id)[0]]
        self.confirm_flush_internal: bool = field(default=False)

    def pour_amount(self, amount_to_pour: int):
        assert self.amount >= amount_to_pour
        self.amount -= amount_to_pour
        logger.info(f"Pumping '{amount_to_pour}mL from pump #{self.pump_code}'")
        self._send_pump_event_with_amount(amount_to_pour)

    def _send_pump_event_with_amount(self, amount: int):
        milliseconds = self.__calculate_ms(amount)
        logger.info(f"Sending pump event to {self.pump_logger_format()} for {amount}ml")
        self._send_pump_event_with_milliseconds(milliseconds)

    def assert_enough_amount(self, needed_amount: int) -> None:
        if not int(self.amount) >= int(needed_amount):
            raise ValueError(
                f"Pump #{self.pump_code} does not have enough '{self.contains}'. Needs {needed_amount}ml, but only has {self.amount}mL")

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
        self._send_pump_event_with_amount(self.tube_volume)

    def pump_logger_format(self):
        return f"pump #{self.pump_code} containing '{self.contains}'"

    def _send_pump_event_with_milliseconds(self, milliseconds: int) -> None:
        logger.info(f"Sending pump event to {self.pump_logger_format()} for {milliseconds}ms")
        time_bytes = self.__number_to_bytes(milliseconds)
        self._send_pump_event(time_bytes)

    def _send_pump_event(self, time_bytes: list[int]):

        # What does the initial write do - Maybe lights?
        #  arduino_service.write_block_data(self.i2c_addr, [self.pump_started, *time_bytes])
        # [self.pump_started, *time_bytes])
        send = [self.pump_number, *time_bytes]
        logger.debug(
            f"Sending bytes to arduino on behalf of pump '{self.pump_code}'. Payload: {send}")
        ArduinoService.write_block_data(self.i2c_addr, send)

    def __number_to_bytes(self, number: int):
        MAX_NUMBER_OF_TWO_BYTES = 65535
        if number < 0 or number > MAX_NUMBER_OF_TWO_BYTES:
            raise ValueError(
                f"Invalid value '{number}'. Number must be between 0 and 65535 (16-bit range)")
        # Extract the two bytes using bitwise operations
        high_byte = (number >> 8) & 0xFF  # bitwise shift right by a byte
        low_byte = number & 0xFF
        return [high_byte, low_byte]

    def __calculate_ms(self, ml):
        return int(ml / self.ML_P_MS)
