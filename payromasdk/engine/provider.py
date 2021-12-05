from ..tools import interface
from web3 import Web3, exceptions, datastructures


class Metadata:
    FROM = 'from'
    TO = 'to'
    VALUE = 'value'
    GAS = 'gas'
    GAS_PRICE = 'gasPrice'
    MAX_FEE_PER_GAS = 'maxFeePerGas'
    MAX_PRIORITY_FEE_PER_GAS = 'maxPriorityFeePerGas'
    DATA = 'data'
    NONCE = 'nonce'
    CHAIN_ID = 'chainId'


class __Provider(object):
    def __init__(self):
        self.__contract = None

        self.interface = None
        self.web3 = None

    def connect(self, network_interface: interface.Network) -> bool:
        valid = False
        if isinstance(network_interface, interface.Network):
            self.interface = network_interface
            self.web3 = Web3(Web3.HTTPProvider(self.interface.rpc))
            valid = self.web3.isConnected()

        return valid

    def is_connected(self) -> bool:
        return self.web3.isConnected()

    def build_transaction(
            self, from_address: interface.Address, to_address: interface.Address,
            value: interface.EtherAmount, data_bytes: bytes = b''
    ) -> dict:
        return {
            Metadata.FROM: from_address.value(),
            Metadata.TO: to_address.value(),
            Metadata.VALUE: value.to_wei(),
            Metadata.DATA: data_bytes,
            Metadata.NONCE: self.web3.eth.get_transaction_count(from_address.value()),
            Metadata.CHAIN_ID: self.interface.chainID
        }

    def add_gas(self, tx_data: dict, eth_eip1559: bool = False):
        gas_limit = self.web3.eth.estimate_gas(tx_data)

        if eth_eip1559 and 'ethereum' in self.interface.name.lower():
            pass
        else:
            tx_data.update({
                Metadata.GAS_PRICE: self.web3.eth.gas_price
            })

        tx_data.update({
            Metadata.GAS: gas_limit
        })

    def send_transaction(self, tx_data: dict, private_key: str) -> interface.TXHash:
        signed_txn = self.web3.eth.account.sign_transaction(tx_data, private_key=private_key)
        self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return interface.TXHash(self.web3.toHex(signed_txn.hash))

    def get_transaction(self, transaction_hash: interface.TXHash) -> datastructures.AttributeDict:
        try:
            return self.web3.eth.get_transaction(transaction_hash.value())
        except exceptions.TransactionNotFound:
            return datastructures.AttributeDict(dict())

    def get_transaction_receipt(self, transaction_hash: interface.TXHash) -> datastructures.AttributeDict:
        try:
            return self.web3.eth.get_transaction_receipt(transaction_hash.value())
        except exceptions.TransactionNotFound:
            return datastructures.AttributeDict(dict())


class __MainProvider(__Provider):
    def balance_of(self, address: interface.Address) -> interface.WeiAmount:
        return interface.WeiAmount(
            self.web3.eth.get_balance(address.value()), decimals=18
        )

    def block_number(self) -> int:
        return self.web3.eth.block_number


class __PNSProvider(__Provider):
    def contract(self) -> interface.Address:
        return self.__contract

    def set_contract(self, address: interface.Address):
        self. __contract = address


MainProvider = __MainProvider()
PNSProvider = __PNSProvider()
