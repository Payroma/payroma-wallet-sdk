from web3 import Web3
from typing import Union
import hashlib
import webbrowser


class Network(object):
    RPC = 1
    NAME = 2
    CHAIN_ID = 3
    SYMBOL = 4
    EXPLORER = 5

    def __init__(
            self, rpc: str, name: str, chain_id: int, symbol: str, explorer: str
    ):
        self.rpc = rpc
        self.name = name
        self.chainID = chain_id
        self.symbol = symbol
        self.explorer = explorer


class Address(object):
    def __init__(
            self, value: str
    ):
        self.__value = Web3.toChecksumAddress(value)

        sha256 = hashlib.sha256(self.__value.encode()).hexdigest()
        self.__int = int(sha256, 16) % (10 ** 8)

    def value(self) -> str:
        return self.__value

    def to_integer(self) -> int:
        return self.__int

    def explorer_view(self, network_interface: Network, browse: bool = True) -> str:
        url = '{}/address/{}'.format(network_interface.explorer, self.__value)
        if browse:
            webbrowser.open_new(url)

        return url


class WeiAmount(object):
    def __init__(
            self, value: int, decimals: int
    ):
        self.__value = value
        self.__ether = float(Web3.fromWei(self.__value, str(decimals)))
        self.__int, self.__decimals = self.__display_float(self.__ether).split('.')

    def value(self) -> int:
        return self.__value

    def to_string(self) -> str:
        return str(self.__value)

    def to_ether(self) -> float:
        return self.__ether

    def to_ether_string(self, currency_format: bool = True) -> str:
        if self.__ether > 999 and currency_format:
            return '{:,}.{}'.format(int(self.__int), self.__decimals)
        elif self.__ether > 0 or not currency_format:
            return '{}.{}'.format(self.__int, self.__decimals)

        # in case integer = 0
        return self.__int

    @staticmethod
    def __display_float(value: float) -> str:
        # format numbers > 1.
        if str(value).find('+') > -1:
            return '{:.1f}'.format(value)

        # format numbers > 1e-05
        e_idx = str(value).find('e')
        if e_idx == -1:
            return str(value)

        # format numbers < 1e-05
        shift = e_idx
        if str(value).find('.') > -1:
            shift -= 1

        decimal_points = -int(str(value)[str(value).find('-'):]) - 1 + shift
        float_format = '{:.' + str(decimal_points) + 'f}'

        return float_format.format(value)


class EtherAmount(object):
    def __init__(
            self, value: Union[str, int, float], decimals: int
    ):
        self.__value = value

        if isinstance(value, str):
            value = value.replace(',', '')
        self.__wei = int(Web3.toWei(value, str(decimals)))

    def value(self) -> Union[str, int, float]:
        return self.__value

    def to_wei(self) -> float:
        return self.__wei


class Wallet(object):
    USERNAME = 1
    ADDRESS = 2
    PIN_CODE = 3
    DATE_CREATED = 4
    IS_FAVORITE = 5

    def __init__(
            self, address_id: int, username: str, address: str,
            pin_code: bytes, date_created: str, is_favorite: bool
    ):
        self.addressID = address_id
        self.username = username
        self.address = Address(address)
        self.pinCode = pin_code
        self.dateCreated = date_created
        self.isFavorite = is_favorite


class Token(object):
    SYMBOL = 1
    DECIMALS = 2

    def __init__(
            self, contract: str, symbol: str, decimals: int
    ):
        self.contract = Address(contract)
        self.symbol = symbol
        self.decimals = decimals


class Transaction(object):
    FUNCTION = 1
    FROM = 2
    TO = 3
    AMOUNT = 4
    SYMBOL = 5
    DECIMALS = 6
    DATE = 7
    STATUS = 8

    class Status:
        FAILED = 0
        SUCCESS = 1
        PENDING = 2

    def __init__(
            self, tx_hash: str, function: str,
            from_address: str, to_address: str, amount: int,
            symbol: str, decimals: int, date_created: str, status: int
    ):
        self.txHash = tx_hash
        self.function = function
        self.fromAddress = Address(from_address)
        self.toAddress = Address(to_address)
        self.amount = WeiAmount(amount, decimals)
        self.symbol = symbol
        self.decimals = decimals
        self.dateCreated = date_created
        self.status = status


class AddressBook(object):
    USERNAME = 1
    ADDRESS = 2

    def __init__(
            self, address_id: int, username: str, address: str
    ):
        self.addressID = address_id
        self.username = username
        self.address = Address(address)


class Stake(object):
    END_BLOCK = 1
    DURATION = 2
    STAKE_TOKEN_CONTRACT = 3
    REWARD_TOKEN_CONTRACT = 4
    STAKE_TOKEN_SYMBOL = 5
    REWARD_TOKEN_SYMBOL = 6
    STAKE_TOKEN_DECIMALS = 7
    REWARD_TOKEN_DECIMALS = 8

    def __init__(
            self, contract: str, end_block: int, duration: str,
            stake_token_contract: str, reward_token_contract: str,
            stake_token_symbol: str, reward_token_symbol: str,
            stake_token_decimals: int, reward_token_decimals: int
    ):
        self.contract = Address(contract)
        self.endBlock = end_block
        self.duration = duration
        self.stakeTokenContract = stake_token_contract
        self.rewardTokenContract = reward_token_contract
        self.stakeTokenSymbol = stake_token_symbol
        self.rewardTokenSymbol = reward_token_symbol
        self.stakeTokenDecimals = stake_token_decimals
        self.rewardTokenDecimals = reward_token_decimals
