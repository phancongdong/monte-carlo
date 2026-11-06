from montecarlo.strategies import Strategy
import montecarlo.indicators as ta
from montecarlo import utils


class ExampleStrategy(Strategy):
    def should_long(self) -> bool:
        return False

    def should_short(self) -> bool:
        # For futures trading only
        return False
        
    def go_long(self):
        pass

    def go_short(self):
        # For futures trading only
        pass
