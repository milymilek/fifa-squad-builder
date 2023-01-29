from src.market.observer.IObserver import IObserver
from src.market.observer.offer_state.IState import IState
from src.market.observer.offer_state.Sold import Sold
from src.market.observer.offer_state.Valid import Valid


class PlayerOffer(IObserver):
    def __init__(self, obs_id, player, owner: str, valid_until, price):
        self._obs_id = obs_id
        self._player = player
        self._owner = owner
        self.state = Valid(valid_until)
        self._price = price
        self.merchant = None

    def get_offer(self):
        return f'ID: {self._obs_id}\tNAME: {self._player}\tPRICE: {self._price}\tVALID UNTIL: {self.state.date()} \
                \tSTATE: {self.get_state_name()} \tOWNER: {self._owner}'

    def get_price(self):
        return self._price

    def get_id(self):
        return self._obs_id

    def get_player(self):
        return self._player

    def get_state_name(self):
        return self.state.__class__.__name__

    def change_state(self, state: IState):
        self.state = state

    # def update(self, merchant=None):
    #     if not merchant:
    #         self.change_state(self.state.handle())
    #     else:
    #         self.change_state(Sold())
    #         self.merchant = merchant

    def update(self):
        self.change_state(self.state.handle())

    def __eq__(self, o):
        return self._obs_id == o.get_id() and self._player == o.get_player()
