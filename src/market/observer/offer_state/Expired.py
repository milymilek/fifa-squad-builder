from src.market.observer.offer_state.IState import IState


class Expired(IState):
    def date(self):
        return "-"

    def handle(self):
        pass