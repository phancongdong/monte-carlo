from montecarlo.config import config
from montecarlo.exceptions import InvalidConfig
from montecarlo.models import SpotExchange, FuturesExchange, Exchange
from montecarlo.modes.utils import get_simulation_model
from montecarlo.services.simulation_assumptions import SimulationModel
from montecarlo.store import store


def initialize_exchanges_state() -> None:
    for name in config['app']['considering_exchanges']:
        starting_assets = config['env']['exchanges'][name]['balance']
        fee = config['env']['exchanges'][name]['fee']
        simulation_model = get_simulation_model(name)

        if simulation_model is SimulationModel.SPOT:
            store.exchanges.storage[name] = SpotExchange(name, starting_assets, fee)
        elif simulation_model is SimulationModel.PERPETUAL_FUTURES:
            store.exchanges.storage[name] = FuturesExchange(
                name, starting_assets, fee,
                futures_leverage_mode=config['env']['exchanges'][name]['futures_leverage_mode'],
                futures_leverage=config['env']['exchanges'][name]['futures_leverage'],
            )
        else:
            raise InvalidConfig(
                f'Unsupported simulation model: {simulation_model.value}'
            )
