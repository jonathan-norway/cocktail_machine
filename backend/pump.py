import logging
import smbus2

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


class Pump:
    ML_P_MS = 0.045

    def __init__(self, pump_code: str, bottle: str, amount: int,
                 internal: bool, tube_volume: int, i2c_addr):
        logger.debug(f"Initiated pump with pump code {pump_code}")
        self.pump_code = pump_code
        self.bottle = bottle
        self.amount = amount
        self.internal = internal
        self.tube_volume = tube_volume
        self.i2c_addr = i2c_addr
        self.confirm_flush_internal = False

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

    def as_dict(self) -> dict:
        return {
            "pump_code": self.pump_code,
            "amount": self.amount
        }

    def send_pump_event(self, amount: int):
        logger.info(f"Sending pump event to {self.pump_logger_format()} for {amount}ml")
        time_bytes = self.__number_to_bytes(self.__calculate_ms(amount))
        # What does the initial write do?
        # arduino_service.write_block_data(arduino_service.i2c_addr_6,
        # [self.pump_started, *time_bytes])
        send = []

    def __number_to_bytes(self, number: int):
        pass

    def __calculate_ms(self, ml):
        return int(ml / self.ML_P_MS)
