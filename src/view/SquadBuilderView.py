class SquadBuilderView:
    def __init__(self, user):
        self.user = user

    def menu(self):
        print(f"\n\n~~SquadBuilder~~")
        choice = input("1. Show squad \n2. Replace player \n3. Release player from squad\n")
        if choice == "1":
            self.squad()
        elif choice == "2":
            self.replace_players()
        elif choice == "3":
            self.remove_player()

    def squad(self):
        print(self.user.squad_builder)

    def replace_players(self):
        print(f"Positions: {list(self.user.squad_builder.formation.get_formation_dict().keys())}")
        pos = input("\nEnter position to be replaced: ")
        print("Unassigned players: \n")
        self.enum_players(self.user.club_players)
        name = input("\nEnter name of player: ")
        self.user.replace_player(pos, name)

    def remove_player(self):
        self.squad()
        pos = input("\nEnter position to be released: ")
        self.user.release_player(pos)

    def enum_players(self, players):
        for i, pl in enumerate(players):
            print(f"{i}. OVR: {pl.overall} \tNAME:  {pl.name}")
