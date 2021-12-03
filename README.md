# Payroma Wallet SDK
Software development kit of Payroma Wallet

## Requirements
```py
import os
import json
import time
import web3
import pyotp
import base64
import hashlib
import webbrowser
import SPCrypto
import SPDatabase
import SPSecurity
from typing import Union
```

## SDK Configure
Set the application password for database
```text
data.networks.py
data.wallets.py
data.tokens.py
data.transactions.py
data.addressesbook.py
```
```python
config, SPSecurity.secure_string(
    # Set the application password here
    (116, 101, 115, 116)
).decode()
```
