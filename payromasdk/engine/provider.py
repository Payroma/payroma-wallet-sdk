from ..tools import interface
from web3 import Web3, exceptions


class __Provider(object):
    def __init__(self):
        self.__contract = None

        self.interface = None
        self.web3 = None

    def connect(self, network_interface: interface.Network):
        self.interface = network_interface

    def is_connected(self) -> bool:
        pass

    def build_transaction(
            self, to: interface.Address, value: interface.EtherAmount, data_bytes: bytes = b''
    ) -> dict:
        pass

    def add_gas(self, tx_data: dict, eth_eip1559: bool = False):
        pass

    def send_transaction(self, tx_data: dict, private_key: str) -> interface.Transaction:
        pass

    def get_transaction(self, transaction: interface.Transaction) -> dict:
        pass

    def get_transaction_receipt(self, transaction: interface.Transaction) -> dict:
        pass


class __MainProvider(__Provider):
    def balance_of(self, address: interface.Address) -> interface.WeiAmount:
        pass

    def block_number(self) -> int:
        pass


class __PNSProvider(__Provider):
    def contract(self) -> str:
        pass

    def set_contract(self, address: interface.Address):
        pass


MainProvider = __MainProvider()
PNSProvider = __PNSProvider()
