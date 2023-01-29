from typing import List

import config
from src.chemistry.IChemistryComputer import IChemistryComputer
from src.chemistry.NewChemistryComputer import NewChemistryComputer
from src.chemistry.OldChemistryComputer import OldChemistryComputer
from src.models.Formation import Formation
from src.models.Player import Player


class SquadBuilder:
    def __init__(self, formation: Formation, players: List[Player]):
        self.formation = formation
        self._players = self.get_players_list(players)

        if config.CHEMISTRY_VERSION >= 2022:
            self.chemistry_computer: IChemistryComputer = NewChemistryComputer()
        else:
            self.chemistry_computer: IChemistryComputer = OldChemistryComputer()

    def get_players_list(self, players):
        pl = [None] * 11
        for p in players:
            if isinstance(p, Player):
                pl[p.assigned_position] = p
        return pl

    def get_filled(self):
        return [p for p in self._players if p is not None]

    def add_player(self, player: Player):
        self._players.append(player)

    def get_chemistry(self):
        return self.chemistry_computer.compute()

    def get_form(self):
        return self.formation.get_list()

    def get_avg_overall(self):
        return sum([p.overall for p in self._players]) / len(self._players)

    def get_stats(self):
        form = self.get_form()
        chemistry = self.get_chemistry()
        avg_ovr = self.get_avg_overall()
        return {"form": form, "chemistry": chemistry, "avg_ovr": avg_ovr}

    def replace(self, pos, player):
        self._players[pos] = player

    def release(self, pos):
        p = self._players[pos]
        self._players[pos] = None
        print(p)
        return p

    def __str__(self):
        if len(self.get_filled()) == 11:
            stats = self.get_stats()
            squad_info = f"\nFormation: {'-'.join([str(i) for i in stats['form']])} \nChemistry: {stats['chemistry']} " \
                         f"\nAvg Overall: {stats['avg_ovr']:.0f}\n\n"

        else:
            squad_info = "\nTeam incomplete, stats unavailable!\n\n"

        form = iter([1] + self.get_form())
        f = next(form)
        for i, player in enumerate(self._players):
            if player is not None:
                squad_info += f'({player.overall}){player.name}\t\t'
            else:
                squad_info += "(-)[Unfilled]\t\t"
            if i == f-1 and f != 11:
                f += next(form)
                squad_info += "\n"

        return squad_info
