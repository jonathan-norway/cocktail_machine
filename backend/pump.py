from ruamel.yaml import YAML
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

class Pump():
  
  def __init__(self, pump_code: str, bottle: str, amount: str ):
    self.pump_code = pump_code
    self.bottle = bottle
    self.amount = amount
  
  def pour_amount(self, amount: int) -> int:
    self.amount -= amount
    send_pump_event(self.pump_code, amount)
    return self.amount

  def assert_enough_amount(self, needed_amount: int) -> None:
    if self.amount >= needed_amount:
      return
    raise ValueError(f"Pump #{self.pump_code} does not have enough '{self.bottle}'. Needs {needed_amount}ml, but only has {self.amount}mL")
  
  def as_dict(self) -> dict:
    return {
      "pump_code": self.pump_code,
      "amount": self.amount
    }
    
def send_pump_event(pump_code: str, amount: int):
  logger.info(f"Sending pump event to pump #{pump_code} for {amount}ml")