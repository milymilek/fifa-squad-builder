from typing import List

from src.SingletonMeta import SingletonMeta
from src.db_handler.MarketHandler import MarketHandler
from src.exceptions.OfferNotFoundException import OfferNotFoundException
from src.market.observed.IObserved import IObserved
from src.market.observer.PlayerOffer import IObserver, PlayerOffer
from src.market.observer.offer_state.Expired import Expired
from src.market.observer.offer_state.Sold import Sold
from src.market.observer.offer_state.Valid import Valid
from src.models.Player import Player


class Market(IObserved, metaclass=SingletonMeta):
    def __init__(self):
        self.handler = MarketHandler()
        self._offers: List[PlayerOffer] = self.handler.fetch_offers()

    def get_offers(self):
        return self._offers

    def get_offer_by_id(self, obs_id):
        obs = [o for o in self._offers if o.get_id() == int(obs_id)]
        if not obs:
            raise OfferNotFoundException
        return obs[0]

    def remove_offer(self, obs: IObserver):
        self._offers = [o for o in self._offers if o != obs]

    def create_offer(self, player, owner, valid_until, price):
        player_offer = self.handler.create_offer(player, owner, valid_until, price)
        self._offers.append(player_offer)

    def acquire_offer(self, obs: IObserver, username: str) -> Player:
        if isinstance(obs.state, Expired):
            raise OfferNotFoundException("Offer has expired...")

        obs.change_state(Sold())
        obs.merchant = username

        self.remove_offer(obs)
        self.handler.update_offer(obs)

        player = self.handler.get_player_from_offer(obs)
        return player

    def update_market(self):
        self.notify_observers()
        self.handler.update_state(self._offers)
        self._offers = self.handler.fetch_offers()

    def get_valid_offers(self):
        valid_offers = [o for o in self._offers if isinstance(o.state, Valid)]
        return valid_offers

    def get_valid_user_offers(self, username):
        valid_user_offers = [o for o in self._offers if isinstance(o.state, Valid) and o._owner == username]
        return valid_user_offers

    def notify_observers(self):
        for o in self._offers:
            o.update()
