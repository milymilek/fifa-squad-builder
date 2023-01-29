from src.db_handler.UserAuthenticator import UserAuthenticator
from src.exceptions.UserNotFoundException import UserNotFoundException
from src.market.observed.IObserved import IObserved
from src.market.observed.Market import Market
from src.view.SquadBuilderView import SquadBuilderView
from src.view.MarketView import MarketView

#todo: handling wiadomości zwrotnych do userów z marketplace, skrzynka odbiorcza z newsami do odebrania, ugułem jakis
#     obiekt do zwrotek
#todo: zwrotki mogą byc zaimplementowane jako obserwator. klienci ktorzy mają wystawionych zawodnikow
# nasłuchują wiadomosci zwrotnych


class ControlCenter:
    def __init__(self):
        self.user_auth = UserAuthenticator()
        self.market = Market()
        self.market_view = None
        self.squad_builder_view = None
        self.user = None

    def init_views(self):
        self.squad_builder_view = SquadBuilderView(self.user)
        self.market_view = MarketView(self.market, self.user)

    def refresh_metadata(self):
        self.market_view.market.update_market()
        self.user.update_user()

    def login(self):
        try:
            username = input("Enter username:\n")
            self.user = self.user_auth.login(username)
            print("Welcome to FIFA Squad Builder!\n\n")
            self.init_views()
            self.display_menu()
        except UserNotFoundException:
            print("User not found, try again...")
            self.login()

    def display_menu(self):
        try:
            self.refresh_metadata()
            choice = input("\n\n1. Squad builder \n2. All players \n3. Market \n4. Simulate match \n")
            if choice == "1":
                self.squad_builder_view.menu()
            elif choice == "2":
                self.display_players()
            elif choice == "3":
                self.market_view.menu()
            elif choice == "4":
                self.display_simulate()
        except Exception:
            print("Error occured...")
        finally:
            self.display_menu()

    def display_simulate(self):
        user2 = input("Enter opponent's nickname: ")
        user2 = self.user_auth.login(user2)
        result = self.user.play_match(user2, simulate=True)
        print(f"RESULT: \n[{self.user.username}] {result[0]} - {result[1]} [{user2.username}]")

    def display_players(self):
        print("\nAll owned players: ")
        for i, pl in enumerate(self.user.get_all_players()):
            print(f"{i}. OVR: {pl.overall} \tNAME:  {pl.name}")
