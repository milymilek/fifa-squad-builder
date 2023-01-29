from asyncio import Protocol


class IMatchSimulator(Protocol):
    def simulate(self, user1, user2):
        ...