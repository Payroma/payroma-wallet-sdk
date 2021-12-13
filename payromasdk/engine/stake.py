from .provider import MainProvider
from ..abis import stakeABI
from ..tools import interface


class StakeEngine(object):
    def __init__(self, stake_interface: interface.Stake, sender: interface.Address = None):
        self.interface = stake_interface
        self.sender = sender

    def owner(self) -> interface.Address:
        pass

    def smart_chef_factory(self) -> interface.Address:
        pass

    def has_user_limit(self) -> bool:
        pass

    def locked_to_end(self) -> bool:
        pass

    def is_initialized(self) -> bool:
        pass

    def is_paused(self) -> bool:
        pass

    def last_pause_time(self) -> int:
        pass

    def acc_token_per_share(self) -> interface.WeiAmount:
        pass

    def bonus_end_block(self) -> int:
        pass

    def start_block(self) -> int:
        pass

    def last_reward_block(self) -> int:
        pass

    def pool_limit_per_user(self) -> int:
        pass

    def reward_per_block(self) -> interface.WeiAmount:
        pass

    def precision_factor(self) -> int:
        pass

    def reward_token(self) -> interface.Address:
        pass

    def staked_token(self) -> interface.Address:
        pass

    def total_supply(self) -> interface.WeiAmount:
        pass

    def balance_of(self, address: interface.Address) -> interface.WeiAmount:
        pass

    def pending_reward(self, address: interface.Address) -> interface.WeiAmount:
        pass

    def initialize(
            self, staked_token: interface.Address, reward_token: interface.Address,
            reward_per_block: interface.EtherAmount, start_block: int, bonus_end_block: int,
            pool_limit_per_user: int, locked_to_end: bool, admin: interface.Address
    ) -> dict:
        pass

    def deposit(self, amount: interface.EtherAmount) -> dict:
        pass

    def withdraw(self, amount: interface.EtherAmount) -> dict:
        pass

    def get_reward(self) -> dict:
        pass

    # Owner functions
    def emergency_reward_withdraw(self, amount: interface.EtherAmount) -> dict:
        pass

    def recover_wrong_tokens(self, token: interface.Address, amount: interface.EtherAmount) -> dict:
        pass

    def stop_reward(self) -> dict:
        pass

    def set_pause(self, paused: bool) -> dict:
        pass

    def update_pool_limit_per_user(self, status: bool, users: int) -> dict:
        pass

    def update_reward_per_block(self, amount: interface.EtherAmount) -> dict:
        pass

    def update_start_and_end_blocks(self, start_block: int, bonus_end_block: int) -> dict:
        pass

    def renounce_ownership(self) -> dict:
        pass

    def transfer_ownership(self, new_owner: interface.Address) -> dict:
        pass

    def _build_transaction(self, method) -> dict:
        pass


__all__ = ['StakeEngine']
