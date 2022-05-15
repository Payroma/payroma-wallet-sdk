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
data/loader.py
```
```python
SPSecurity.secure_string(
    # Set the application password here, it must be changed in a real environment
    (116, 101, 115, 116)
).decode()
```
```text
data/addressesbook.py
```
```python
# Set the application password here, it must be changed in a real environment
loader.loader(file_name='addressesbook', password='')
```
