from dataclasses import dataclass
from collections import OrderedDict


@dataclass
class Formation:
    n_back: int
    n_mid: int
    n_front: int

    def get_list(self):
        return [self.n_back, self.n_mid, self.n_front]

    def get_formation_dict(self):
        d_gk = OrderedDict([("GK", 0)])

        if self.n_back == 3:
            d_back = OrderedDict([("CB" + str(i+1), i + 1) for i in range(self.n_back)])
        else:
            cbs = [("CB" + str(i), i + 2) for i in range(self.n_back-2)]
            d_back = OrderedDict([("LB", 1), *cbs, ("RB", self.n_back)])

        if self.n_mid == 3:
            d_mid = OrderedDict([("CM" + str(i), i + 1 + self.n_back) for i in range(self.n_mid)])
        else:
            cms = [("CM" + str(i), i + 1 + self.n_back) for i in range(self.n_mid-2)]
            d_mid = OrderedDict([("LM", self.n_back+1), *cms, ("RM", self.n_mid+1)])

        if self.n_front == 2:
            d_front = OrderedDict([("ST0", 9), ("ST1", 10)])
        elif self.n_front == 3:
            d_front = OrderedDict([("LW", 8), ("ST", 9), ("RW", 10)])

        return OrderedDict(list(d_gk.items()) + list(d_back.items()) + list(d_mid.items()) + list(d_front.items()))
