import datetime

from src.market.observer.offer_state.Expired import Expired
from src.market.observer.offer_state.IState import IState


class Valid(IState):
    def __init__(self, valid_until):
        self._valid_until = valid_until

    def date(self):
        return self._valid_until

    def handle(self):
        if datetime.datetime.now() > self._valid_until:
            return Expired()
        else:
            return self
