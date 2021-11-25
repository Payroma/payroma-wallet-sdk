from ..tools import interface
from web3 import Web3
from typing import Union
import hashlib
import SPCrypto


def generate(username: str, password: str, pin_code: str) -> Union[str, str]:
    pass


def pin_code_encrypt(value: str, password: str) -> bytes:
    pass


def pin_code_decrypt(value: bytes, password: str) -> str:
    pass
