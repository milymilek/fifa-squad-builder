from typing import List
from collections import OrderedDict

# TODO: mozna tutaj wrzucic dekorator
class PlayerAssigner:
    def __init__(self, players):
        self._owned_players = dict(players)

    def get_positioned_players(self):
        d_assigned = {k: v for k,v in self._owned_players.items() if k is not None}
        d = dict(sorted(d_assigned.items()))
        return list(d.values())

    def get_players(self):
        return list(self._owned_players.values())

