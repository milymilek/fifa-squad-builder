from datetime import datetime
from typing import List

from src.db_handler.UserHandler import UserHandler
from src.exceptions.NotEnoughMoneyException import NotEnoughMoneyException
from src.exceptions.PlayerNotFoundException import PlayerNotFoundException
from src.market.observed.Market import Market
from src.models.Player import Player
from src.models.SquadBuilder import SquadBuilder
from src.simulator.IMatchSimulator import IMatchSimulator
from src.simulator.SimpleMatchSimulator import SimpleMatchSimulator

#todo: dorobić klase do walidacji
class User:
    def __init__(self, username: str, players: List[Player], squad_builder: SquadBuilder, balance):
        self.handler = UserHandler()
        self.username = username
        self.club_players = players
        self.squad_builder = squad_builder
        self.market = Market()
        self._balance = balance
        self.match_simulator: IMatchSimulator = SimpleMatchSimulator()

    def get_all_players(self):
        return self.club_players + self.squad_builder.get_filled()

    def get_unassigned_players(self):
        return [p for p in self.club_players if p.assigned_position is None]

    def get_balance(self):
        return self._balance

    def add_player(self, player: Player):
        self.club_players.append(player)

    def remove_player(self, player: Player):
        self.club_players = [p for p in self.club_players if p != player]

    def buy(self, offer_id):
        offer = self.market.get_offer_by_id(offer_id)
        owner = offer._owner
        price = offer.get_price()
        if self._balance < price:
            raise NotEnoughMoneyException()

        player = self.market.acquire_offer(offer, self.username)
        self.add_player(player)
        self._balance -= price

        self.handler.update_user_players(player, self.username)
        self.handler.update_balance(self.username, -1*price)
        self.handler.update_balance(owner, price)

    def sell(self, name, price, valid_until):
        player = [p for p in self.club_players if p.name == name]
        if not player:
            raise PlayerNotFoundException()
        else:
            player = player[0]

        self.remove_player(player)
        valid_date = datetime.strptime(valid_until, "%d/%m/%Y")
        price = int(price)

        self.market.create_offer(player, self.username, valid_date, price)
        self.handler.remove_user_players(player, self.username)

    def replace_player(self, pos, name):
        pos_map = self.squad_builder.formation.get_formation_dict()[pos]
        player = [p for p in self.club_players if p.name == name][0]
        self.squad_builder.replace(pos_map, player)
        self.club_players = [p for p in self.club_players if p.name != name]
        self.handler.update_user_players2(pos_map, player, self.username)

    def release_player(self, pos):
        pos_map = self.squad_builder.formation.get_formation_dict()[pos]
        player = self.squad_builder.release(pos_map)
        self.club_players.append(player)
        self.handler.update_release_player(pos_map, player, self.username)

    def play_match(self, opponent, simulate=True):
        if simulate:
            return self.match_simulator.simulate(self.squad_builder, opponent.squad_builder)
        return '0:0'

    def update_user(self):
        balance, club_players = self.handler.update_user(self.username)
        self._balance = balance
        self.club_players = club_players
