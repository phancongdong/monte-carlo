from montecarlo.strategies import Strategy
import montecarlo.helpers as jh
from montecarlo import utils


class TestCapitalPropertyRaisesNotImplementedError(Strategy):
    def should_long(self) -> bool:
        self.capital
        return False

    def go_long(self) -> None:
        pass

    def should_cancel_entry(self):
        return False
