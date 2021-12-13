from .provider import MainProvider
from ..abis import tokenABI
from ..tools import interface


class TokenEngine(object):
    def __init__(self, token_interface: interface.Token, sender: interface.Address = None):
        self.interface = token_interface
        self.sender = sender

    def name(self) -> str:
        pass

    def symbol(self) -> str:
        pass

    def decimals(self) -> int:
        pass

    def total_supply(self) -> interface.WeiAmount:
        pass

    def balance_of(self, address: interface.Address) -> interface.WeiAmount:
        pass

    def allowance(self, owner: interface.Address, spender: interface.Address) -> interface.WeiAmount:
        pass

    def approve(self, spender: interface.Address, amount: interface.EtherAmount) -> dict:
        pass

    def transfer(self, recipient: interface.Address, amount: interface.EtherAmount) -> dict:
        pass

    def transfer_from(
            self, sender: interface.Address, recipient: interface.Address, amount: interface.EtherAmount
    ) -> dict:
        pass

    def increase_allowance(self, spender: interface.Address, amount: interface.EtherAmount) -> dict:
        pass

    def decrease_allowance(self, spender: interface.Address, amount: interface.EtherAmount) -> dict:
        pass

    def _build_transaction(self, method) -> dict:
        pass


class PayromaTokenEngine(TokenEngine):
    def __init__(self, token_interface: interface.Token):
        super(PayromaTokenEngine, self).__init__(token_interface)

    def owner(self) -> interface.Address:
        pass

    def inflation_rate_annually(self) -> int:
        pass

    def inflation_duration_end_date(self) -> int:
        pass

    def available_to_mint_current_year(self) -> interface.WeiAmount:
        pass

    def transfer_multiple(self, addresses: list, amounts: list) -> dict:
        pass

    def burn(self, amount: interface.EtherAmount) -> dict:
        pass

    def burn_from(self, spender: interface.Address, amount: interface.EtherAmount) -> dict:
        pass

    # Owner functions
    def mint(self, amount: interface.EtherAmount) -> dict:
        pass

    def recover_token(self, token_address: interface.Address, amount: interface.EtherAmount) -> dict:
        pass

    def renounce_ownership(self) -> dict:
        pass

    def transfer_ownership(self, new_owner: interface.Address) -> dict:
        pass


__all__ = ['TokenEngine', 'PayromaTokenEngine']
