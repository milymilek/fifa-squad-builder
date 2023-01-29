from datetime import datetime

from src.db_handler.DBHandler import DBHandler
from src.market.observer.PlayerOffer import PlayerOffer
from src.market.observer.offer_state.Valid import Valid
from src.models.Player import Player


class MarketHandler(DBHandler):
    def fetch_offers(self):
        cursor = self.db.cursor()
        cursor.execute(
            f"""SELECT MO.offer_id, P.player_name, U.username, MO.valid_until, MO.price
                FROM MarketOffers MO
                INNER JOIN players P
                ON MO.player_id = P.player_id
                INNER JOIN Users U
                ON MO.user_id = U.user_id
                WHERE MO.status = 'Valid'
                """
        )
        result = cursor.fetchall()
        valid_offers = [PlayerOffer(*r) for r in result]
        return valid_offers

    def get_player_from_offer(self, offer):
        player_id = self.query_return(f"SELECT player_id FROM players where player_name='{offer.get_player()}'")
        result = self.query_return(f"""SELECT P.player_name,
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
                                FROM players P
                                INNER JOIN nationality N
                                ON N.nationality_id = P.nationality_id
                                INNER JOIN clubs C
                                ON C.club_id = P.club_id
                                INNER JOIN leagues L
                                ON L.league_id = P.league_id
                                WHERE P.player_name = '{offer.get_player()}'""")

        player = Player(*result[0], *["x" for i in range(6)], None)
        return player

    def update_offer(self, offer):
        merchant_id = self.query_return(f"SELECT user_id FROM Users where username='{offer.merchant}'")[0][0]

        cursor = self.db.cursor()
        cursor.execute(
            f"""UPDATE MarketOffers
                         SET merchant_id={merchant_id}, status='Sold'
                         WHERE offer_id={offer.get_id()}"""
        )
        self.db.commit()

    def update_state(self, offers):
        for o in offers:
            if not isinstance(o.state, Valid):
                merchant_id = self.query_return(f"SELECT user_id FROM Users where username='{o.merchant}'")

                if not merchant_id:
                    merchant_id = self.query_return(f"SELECT user_id FROM Users where username='{o._owner}'")[0][0]
                else:
                    merchant_id = merchant_id[0][0]

                cursor = self.db.cursor()
                cursor.execute(
                    f"""UPDATE MarketOffers
                     SET merchant_id={merchant_id}, status='{o.get_state_name()}'
                     WHERE offer_id={o._obs_id}"""
                )

                cursor = self.db.cursor()
                cursor.execute(
                    f"""INSERT INTO UserPlayers (user_id, player_id, position)
                        VALUES ({merchant_id},
                                (SELECT player_id FROM players where player_name='{o._player}'),
                                null)"""
                )
                self.db.commit()

    def create_offer(self, player: Player, owner: str, valid_date: datetime, price: int):
        owner_id = self.query_return(f"SELECT user_id FROM Users WHERE username='{owner}'")[0][0]
        player_id = self.query_return(f"SELECT player_id FROM players WHERE player_name='{player.name}'")[0][0]

        cursor = self.db.cursor()
        cursor.execute(
            f"""INSERT INTO MarketOffers (player_id, user_id, merchant_id, listed_at, valid_until, price, status)
                VALUES ({player_id}, {owner_id}, null, '{datetime.now()}', '{valid_date}', {price}, 'Valid')"""
        )
        self.db.commit()

        last_id = self.query_return("SELECT LAST_INSERT_ID()")[0][0]
        print(last_id)
        return PlayerOffer(last_id, player.name, owner, valid_date, price)

