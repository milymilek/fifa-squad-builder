from src.db_handler.DBHandler import DBHandler
from src.exceptions import UserNotFoundException
from src.models.Formation import Formation
from src.models.Player import Player
from src.models.PlayerAssigner import PlayerAssigner
from src.models.SquadBuilder import SquadBuilder
from src.models.User import User


class UserAuthenticator(DBHandler):
    def login(self, login):
        cursor = self.db.cursor()
        cursor.execute(f"""
            SELECT *
            FROM Users
            WHERE Users.username = '{login}'
        """)
        result = cursor.fetchall()

        if not result:
            raise UserNotFoundException

        balance = result[0][2]

        return self.get_profile(login, balance)

    def get_profile(self, username, balance):
        cursor = self.db.cursor()
        cursor.execute(f"""
            SELECT U.username,
                   F.n_back,
                   F.n_mid,
                   F.n_front,
                   UP.position,
                   P.player_name,
                   N.nationality_name,
                   C.club_name,
                   L.league_name,
                   P.player_positions,
                   P.overall,
                   P.pace,
                   P.shooting,
                   P.passing,
                   P.dribbling,
                   P.defending,
                   P.physic
            FROM Users U
            INNER JOIN Formations F
            ON U.formation_id = F.formation_id
            INNER JOIN UserPlayers UP
            ON U.user_id = UP.user_id
            INNER JOIN players P
            ON P.player_id = UP.player_id
            INNER JOIN nationality N
            ON N.nationality_id = P.nationality_id
            INNER JOIN clubs C
            ON C.club_id = P.club_id
            INNER JOIN leagues L
            ON L.league_id = P.league_id
            WHERE U.username = '{username}'
        """)
        result = cursor.fetchall()

        if not result:
            formation = [4, 4, 2]
        else:
            formation = result[0][1:4]

        players = [Player(*p[5:], *["x" for i in range(6)], p[4]) for p in result]
        club_players = [p for p in players if p.assigned_position is None]
        squad_players = [p for p in players if p.assigned_position is not None]

        squad_builder = SquadBuilder(Formation(*formation), squad_players)

        return User(username, club_players, squad_builder, balance)
