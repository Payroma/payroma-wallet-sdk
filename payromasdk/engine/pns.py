from .provider import PNSProvider
from ..abis import pnsABI
from ..tools import interface


class PNSEngine(object):
    def __init__(self):
        pass

    def owner(self) -> interface.Address:
        pass

    def users_count(self) -> int:
        pass

    def is_reserved(self, name: str) -> bool:
        pass

    def is_recorded(self, name: str) -> bool:
        pass

    def get_by_name(self, name: str) -> tuple[str, bool, bool]:
        pass

    def get_by_address(self, address: interface.Address) -> tuple[str, bool, bool]:
        pass

    def new_record(self, name: str) -> dict:
        pass

    def transfer_name(self, new_owner: interface.Address) -> dict:
        pass

    # Owner functions
    def set_verified(self, name: str, state: bool) -> dict:
        pass

    def set_scammer(self, name: str, address: interface.Address, state: bool) -> dict:
        pass

    def reserve_users(self, users: list, statuses: list) -> dict:
        pass

    def set_multi_verified(self, users: list, statuses: list) -> dict:
        pass

    def set_multi_scammers(self, users: list, addresses: list, statuses: list) -> dict:
        pass

    def renounce_ownership(self) -> dict:
        pass

    def transfer_ownership(self, new_owner: interface.Address) -> dict:
        pass
