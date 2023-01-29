from src.db_handler.DBHandler import DBHandler
from src.models.Player import Player


class UserHandler(DBHandler):

    def update_user_players(self, player, username):
        merchant_id = self.query_return(f"SELECT user_id FROM Users where username='{username}'")[0][0]

        cursor = self.db.cursor()
        cursor.execute(
            f"""INSERT INTO UserPlayers (user_id, player_id, position)
                VALUES ({merchant_id},
                        (SELECT player_id FROM players where player_name='{player.name}'),
                        null)"""
        )
        self.db.commit()

    def remove_user_players(self, player, username):
        owner_id = self.query_return(f"SELECT user_id FROM Users WHERE username='{username}'")[0][0]
        player_id = self.query_return(f"SELECT player_id FROM players WHERE player_name='{player.name}'")[0][0]

        cursor = self.db.cursor()
        cursor.execute(
            f"""DELETE FROM UserPlayers
                WHERE user_id={owner_id}
                AND player_id={player_id}
            """
        )
        self.db.commit()

    def update_user_players2(self, pos, player, username):
        user_id = self.query_return(f"SELECT user_id FROM Users where username='{username}'")[0][0]
        player_id = self.query_return(f"SELECT player_id FROM players where player_name='{player.name}'")[0][0]

        cursor = self.db.cursor()
        cursor.execute(
            f"""UPDATE UserPlayers 
                SET position=null
                WHERE position={pos}
                """
        )

        cursor = self.db.cursor()
        cursor.execute(
            f"""UPDATE UserPlayers 
                SET position={pos}
                WHERE user_id={user_id} AND player_id={player_id}
                """
        )
        self.db.commit()

    def update_release_player(self, pos, player, username):
        user_id = self.query_return(f"SELECT user_id FROM Users where username='{username}'")[0][0]
        player_id = self.query_return(f"SELECT player_id FROM players where player_name='{player.name}'")[0][0]

        cursor = self.db.cursor()
        cursor.execute(
            f"""UPDATE UserPlayers 
                SET position=null
                WHERE user_id={user_id} AND player_id={player_id}
                """
        )
        self.db.commit()

    def update_user(self, username):
        self.db.commit()
        cursor = self.db.cursor()
        cursor.execute(f"""
                    SELECT balance
                    FROM Users
                    WHERE Users.username = '{username}'
                """)
        result = cursor.fetchall()
        cursor.close()
        balance = result[0][0]

        cursor = self.db.cursor()
        cursor.execute(f"""
            SELECT U.username,
                   U.balance,
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

        players = [Player(*p[3:], *["x" for i in range(6)], p[2]) for p in result]
        club_players = [p for p in players if p.assigned_position is None]

        return balance, club_players

    def update_balance(self, username, price):
        cursor = self.db.cursor()
        cursor.execute(f"""
            UPDATE Users
            SET balance=balance+{price}
            WHERE username = '{username}'
        """)
        self.db.commit()




