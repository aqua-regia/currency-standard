from abc import abstractmethod


class SymbolProcessor:
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def symbol_to_asset(self, symbol):
        pass

    @abstractmethod
    def can_process_symbol(self, symbol):
        pass
