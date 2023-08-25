from abc import ABC, abstractclassmethod


class RoutesBase(ABC):
    @abstractclassmethod  # type: ignore
    def bind():
        pass
