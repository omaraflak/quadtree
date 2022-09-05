from abc import ABC


class Locatable(ABC):
    def get_x(self) -> float:
        raise NotImplementedError()

    def get_y(self) -> float:
        raise NotImplementedError()
