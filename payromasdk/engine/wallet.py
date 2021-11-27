from ..tools import interface, walletcreator
from ..data import wallets, tokens, transactions
from .provider import MainProvider
from typing import Union


def get_all() -> list:
    pass


def add_new(wallet_interface: interface.Wallet) -> bool:
    pass


def remove(wallet_interface: interface.Wallet) -> bool:
    pass


def create(
        username: str, password: str, pin_code: str, private_key: str = None
) -> interface.Wallet:
    pass


def backup_wallets(
        path: str, wallets_id: list = None, progress_event: callable = None,
        password: Union[str, wallets.SPDatabase.ControlObject] = wallets.SPDatabase.Control.AUTO
) -> bool:
    pass


def import_wallets(
        path: str, wallets_id: list = None, progress_event: callable = None,
        password: Union[str, wallets.SPDatabase.ControlObject] = wallets.SPDatabase.Control.AUTO,
        mode: wallets.SPDatabase.ControlObject = wallets.SPDatabase.Control.UPDATE
) -> bool:
    pass


class WalletEngine(object):
    def __init__(self, wallet_interface: interface.Wallet):
        self.__password = None
        self.__isLogged = None

        self.interface = wallet_interface

    def username(self) -> str:
        pass

    def address(self) -> interface.Address:
        pass

    def pin_code(self) -> str:
        pass

    def private_key(self) -> str:
        pass

    def date_created(self) -> str:
        pass

    def is_favorite(self) -> bool:
        pass

    def is_logged(self) -> bool:
        pass

    def login(self, password: str) -> bool:
        pass

    def logout(self):
        pass

    def tokens(self) -> list:
        pass

    def add_token(self, token: interface.Token) -> bool:
        pass

    def remove_token(self, token: interface.Token) -> bool:
        pass

    def transactions(self) -> list:
        pass

    def add_transaction(self, transaction: interface.Transaction) -> bool:
        pass

    def remove_transaction(self, transaction: interface.Transaction) -> bool:
        pass
