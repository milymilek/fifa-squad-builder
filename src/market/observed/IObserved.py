from src.market.observer.IObserver import IObserver


class IObserved:
    def add_observer(self, obs: IObserver):
        ...

    def remove_observer(self, obs: IObserver):
        ...

    def notify_observer(self, obs: IObserver):
        ...

    def notify_observers(self):
        ...

    def get_valid_offers(self):
        ...