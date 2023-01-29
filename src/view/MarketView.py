class MarketView:
    def __init__(self, market, user):
        self.market = market
        self.user = user

    def menu(self):
        print(f"\n\n~~~FIFA Marketplace!!!\t~~~ Balance: {self.user.get_balance()}")
        choice = input("1. Show offers \n2. Buy player \n3. Sell player \n4. Your offers\n")
        if choice == "1":
            self.all_offers()
        elif choice == "2":
            self.buy()
        elif choice == "3":
            self.sell()
        elif choice == "4":
            self.all_user_offers()

    def all_offers(self):
        print("\n\nAll market available offers: ")
        for o in self.market.get_valid_offers():
            print(o.get_offer())

    def all_user_offers(self):
        for o in self.market.get_valid_user_offers(self.user.username):
            print(o.get_offer())

    def buy(self):
        self.all_offers()
        buy_nbr = input("\nEnter number of offer to buy: ")
        self.user.buy(buy_nbr)

    def sell(self):
        self.enum_players(self.user.club_players)
        sell_name = input("\nEnter name of player to sell: ")
        price = input("\n Enter price: ")
        valid_until = input("\n Enter date of offer expiration (dd/mm/yyyy): ")
        self.user.sell(sell_name, price, valid_until)
        #self.market.create_observer(sell_name, self.user.username, valid_until, price)

    def enum_players(self, players):
        for i, pl in enumerate(players):
            print(f"{i}. OVR: {pl.overall} \tNAME:  {pl.name}")

