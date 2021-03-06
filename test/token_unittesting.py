from payromasdk import engine, tools
from web3 import datastructures
import time
import pyotp
import unittest


debugging = True


def specific_wallets_details() -> dict:
    return {
        29974936: [
            '0xC94EA8D9694cfe25b94D977eEd4D60d7c0985BD3', 'username1', 'password1', '123456'
        ],
        42980736: [
            '0xB41aD6b3EE5373dbAC2b471E4582A0b50f4bC9DE', 'username2', 'password2', '123457'
        ],
        51329850: [
            '0xB72bEC2cB81F9B61321575D574BAC577BAb99141', 'username3', 'password3', '123458'
        ],
        64695172: [
            '0x45EF6cc9f2aD7A85e282D14fc23C745727e547b6', 'username4', 'password4', '123459'
        ],
        52312503: [
            '0x71471d05114c758eBfC3D3b952a722Ef2d53970b', 'username5', 'password5', '123460'
        ]
    }


def specific_networks_details() -> dict:
    return {
        "Ethereum": tools.interface.Network(
            name="Ethereum",
            rpc="https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            chain_id=1,
            symbol="ETH",
            explorer="https://etherscan.io"
        ),
        "Ethereum Ropsten (Testnet)": tools.interface.Network(
            name="Ethereum Ropsten (Testnet)",
            rpc="https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            chain_id=3,
            symbol="ETH",
            explorer="https://ropsten.etherscan.io"
        ),
        "Ethereum Goerli (Testnet)": tools.interface.Network(
            name="Ethereum Goerli (Testnet)",
            rpc="https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            chain_id=5,
            symbol="ETH",
            explorer="https://goerli.etherscan.io"
        ),
        "Binance Smart Chain": tools.interface.Network(
            name="Binance Smart Chain",
            rpc="https://bsc-dataseed1.binance.org",
            chain_id=56,
            symbol="BNB",
            explorer="https://bscscan.com"
        ),
        "Binance Smart Chain (Testnet)": tools.interface.Network(
            name="Binance Smart Chain (Testnet)",
            rpc="https://data-seed-prebsc-1-s1.binance.org:8545",
            chain_id=97,
            symbol="BNB",
            explorer="https://testnet.bscscan.com"
        ),
        "Matic Mumbai (Testnet)": tools.interface.Network(
            name="Binance Smart Chain (Testnet)",
            rpc="https://rpc-mumbai.maticvigil.com",
            chain_id=80001,
            symbol="MATIC",
            explorer="https://mumbai.polygonscan.com"
        )
    }


def specific_tokens_details() -> dict:
    return {
        "PYA": tools.interface.Token(
            contract=tools.interface.Address("0xfCF2F96ab285eFfd3E37848f86a4b08969A397Ef"),
            symbol="PYA",
            decimals=18
        )
    }


def function_name(text: str):
    print(f"[ + ] Start for: {text}")


# Wallet 1
_, __username, __password, __pin_code = specific_wallets_details()[52312503]
wallet1_otp = pyotp.TOTP(tools.walletcreator.otp_hash(__username, __password, __pin_code))
wallet1_address, wallet1_private_key, _ = tools.walletcreator.access(
    __username, __password, __pin_code, wallet1_otp.now()
)


# Wallet 2
_, __username, __password, __pin_code = specific_wallets_details()[29974936]
wallet2_otp = pyotp.TOTP(tools.walletcreator.otp_hash(__username, __password, __pin_code))
wallet2_address, wallet2_private_key, _ = tools.walletcreator.access(
    __username, __password, __pin_code, wallet2_otp.now()
)


# Network configuration
network = specific_networks_details()["Binance Smart Chain (Testnet)"]
engine.provider.MainProvider.connect(network)


# Token engine
token = specific_tokens_details()["PYA"]
token_engine = engine.token.TokenEngine(token_interface=token)
payroma_token_engine = engine.token.PayromaTokenEngine(token_interface=token, sender=wallet1_address)


class TokenUnitTesting(unittest.TestCase):
    # Token engine
    def test_token_engine(self):
        function_name('TokenEngine')

        # Task
        name = token_engine.name()
        symbol = token_engine.symbol()
        decimals = token_engine.decimals()
        total_supply = token_engine.total_supply()

        # Debugging
        if debugging:
            print(f"""
            name: {name}
            symbol: {symbol}
            decimals: {decimals}
            total_supply: {total_supply.to_ether_string()}
            """)

        # Network test
        self.assertEqual(name, "Payroma Wallet")
        self.assertEqual(symbol, token.symbol)
        self.assertEqual(decimals, token.decimals)
        self.assertLessEqual(total_supply.to_ether(), 20000000)

    def test_balance_of(self):
        function_name('balance_of')

        wallets = {
            'wallet 1': wallet1_address,
            'wallet 2': wallet2_address
        }
        for name, address in wallets.items():
            # Task
            result: tools.interface.WeiAmount = token_engine.balance_of(address)

            # Debugging
            if debugging:
                print(f"""
                name: {name}
                address: {address.value()}
                balance: {result.to_ether_string()}
                """)

            # Test
            self.assertIsInstance(result.value(), int)

    def test_allowance(self):
        function_name('allowance')

        # Task
        result: tools.interface.WeiAmount = token_engine.allowance(
            owner=wallet2_address, spender=wallet1_address
        )

        # Debugging
        if debugging:
            print(f"""
            owner: {wallet2_address.value()}
            spender: {wallet1_address.value()}
            balance: {result.to_ether_string()}
            """)

        # Test
        self.assertIsInstance(result.value(), int)

    def test_transfer(self):
        function_name('transfer')

        token_engine.sender = wallet1_address  # Set sender address to token engine
        amount = tools.interface.EtherAmount(10, decimals=token_engine.interface.decimals)
        attempts = 1

        for _ in range(attempts):
            # Task
            sender_balance = token_engine.balance_of(token_engine.sender)
            recipient_balance = token_engine.balance_of(wallet2_address)
            result: dict = token_engine.transfer(recipient=wallet2_address, amount=amount)
            self.__send_transaction(result, wallet1_private_key)

            # Test
            self.assertIsInstance(result, dict)
            self.assertAlmostEqual(
                sender_balance.value() - amount.to_wei(),
                token_engine.balance_of(token_engine.sender).value()
            )
            self.assertAlmostEqual(
                recipient_balance.value() + amount.to_wei(),
                token_engine.balance_of(wallet2_address).value()
            )

    def test_approve(self):
        function_name('approve')

        token_engine.sender = wallet2_address  # Set sender address to token engine
        amount = tools.interface.EtherAmount(100, decimals=token_engine.interface.decimals)
        attempts = 1

        for _ in range(attempts):
            # Task
            result: dict = token_engine.approve(spender=wallet1_address, amount=amount)
            self.__send_transaction(result, wallet2_private_key)

            # Test
            self.assertIsInstance(result, dict)
            self.assertAlmostEqual(
                amount.to_wei(),
                token_engine.allowance(token_engine.sender, wallet1_address).value()
            )

    def test_transfer_from(self):
        function_name('transfer_from')

        token_engine.sender = wallet1_address  # Set sender address to token engine
        amount = tools.interface.EtherAmount(10, decimals=token_engine.interface.decimals)
        attempts = 1

        for _ in range(attempts):
            # Task
            sender_balance = token_engine.balance_of(wallet2_address)
            recipient_balance = token_engine.balance_of(wallet1_address)
            result: dict = token_engine.transfer_from(
                sender=wallet2_address, recipient=wallet1_address, amount=amount
            )
            self.__send_transaction(result, wallet1_private_key)

            # Test
            self.assertIsInstance(result, dict)
            self.assertAlmostEqual(
                sender_balance.value() - amount.to_wei(),
                token_engine.balance_of(wallet2_address).value()
            )
            self.assertAlmostEqual(
                recipient_balance.value() + amount.to_wei(),
                token_engine.balance_of(wallet1_address).value()
            )

    # Payroma token engine
    def test_owner(self):
        function_name('owner')

        # Task
        result: tools.interface.Address = payroma_token_engine.owner()

        # Debugging
        if debugging:
            print(f"""
            owner: {result.value()}
            """)

        # Test
        self.assertEqual(result.value(), '0x149A03EBA3c0786581ad4b2cEC8082ef9e9425Bb')

    def test_inflation_rate_annually(self):
        function_name('inflation_rate_annually')

        # Task
        result: int = payroma_token_engine.inflation_rate_annually()

        # Debugging
        if debugging:
            print(f"""
            inflation_rate_annually: {result}
            """)

        # Test
        self.assertEqual(result, 5)

    def test_inflation_duration_end_date(self):
        function_name('inflation_duration_end_date')

        # Task
        result: int = payroma_token_engine.inflation_duration_end_date()

        # Debugging
        if debugging:
            print(f"""
            inflation_duration_end_date: {result}
            """)

        # Test
        self.assertIsInstance(result, int)

    def test_available_to_mint_current_year(self):
        function_name('available_to_mint_current_year')

        # Task
        result: tools.interface.WeiAmount = payroma_token_engine.available_to_mint_current_year()

        # Debugging
        if debugging:
            print(f"""
            available_to_mint_current_year: {result.to_ether_string()}
            """)

        # Test
        self.assertIsInstance(result.to_ether(), float)

    def test_transfer_multiple(self):
        function_name('transfer_multiple')

        addresses = [
            tools.interface.Address('0xebbdE258abe7c6Ddb5a96971307C753eA66DF563'),
            tools.interface.Address('0x7d33A2566754291411B8d42a240e9019969Bd9aC'),
            tools.interface.Address('0x665c0886ddB1d3A881a7267B4c415e25eDD3a3CD'),
            tools.interface.Address('0x2861AB4072DaC7C861f1b8d23d63e8B1A8d9d3C6')
        ]
        amounts = [
            tools.interface.EtherAmount(10, decimals=payroma_token_engine.interface.decimals),
            tools.interface.EtherAmount(20, decimals=payroma_token_engine.interface.decimals),
            tools.interface.EtherAmount(30, decimals=payroma_token_engine.interface.decimals),
            tools.interface.EtherAmount(40, decimals=payroma_token_engine.interface.decimals)
        ]
        total_amount = tools.interface.EtherAmount(100, decimals=payroma_token_engine.interface.decimals)
        attempts = 1

        for _ in range(attempts):
            # Task
            sender_balance = payroma_token_engine.balance_of(payroma_token_engine.sender)
            recipients_balances = [token_engine.balance_of(address) for address in addresses]
            result: dict = payroma_token_engine.transfer_multiple(addresses=addresses, amounts=amounts)
            self.__send_transaction(result, wallet1_private_key)

            # Test
            self.assertIsInstance(result, dict)
            self.assertAlmostEqual(
                sender_balance.value() - total_amount.to_wei(),
                payroma_token_engine.balance_of(payroma_token_engine.sender).value()
            )
            for index, address in enumerate(addresses):
                self.assertAlmostEqual(
                    recipients_balances[index].value() + amounts[index].to_wei(),
                    payroma_token_engine.balance_of(address).value()
                )

    def test_burn(self):
        function_name('burn')

        amount = tools.interface.EtherAmount(100, decimals=payroma_token_engine.interface.decimals)
        attempts = 1

        for _ in range(attempts):
            # Task
            sender_balance = payroma_token_engine.balance_of(payroma_token_engine.sender)
            total_supply = payroma_token_engine.total_supply()
            result: dict = payroma_token_engine.burn(amount)
            self.__send_transaction(result, wallet1_private_key)

            # Test
            self.assertIsInstance(result, dict)
            self.assertAlmostEqual(
                sender_balance.value() - amount.to_wei(),
                payroma_token_engine.balance_of(payroma_token_engine.sender).value()
            )
            self.assertAlmostEqual(
                total_supply.value() - amount.to_wei(),
                payroma_token_engine.total_supply().value()
            )

    def test_burn_from(self):
        function_name('burn_from')

        amount = tools.interface.EtherAmount(5, decimals=payroma_token_engine.interface.decimals)
        attempts = 1

        for _ in range(attempts):
            # Task
            allowance_balance = payroma_token_engine.allowance(wallet2_address, payroma_token_engine.sender)
            owner_balance = payroma_token_engine.balance_of(wallet2_address)
            total_supply = payroma_token_engine.total_supply()
            result: dict = payroma_token_engine.burn_from(spender=wallet2_address, amount=amount)
            self.__send_transaction(result, wallet1_private_key)

            # Test
            self.assertIsInstance(result, dict)
            self.assertAlmostEqual(
                allowance_balance.value() - amount.to_wei(),
                payroma_token_engine.allowance(wallet2_address, payroma_token_engine.sender).value()
            )
            self.assertAlmostEqual(
                owner_balance.value() - amount.to_wei(),
                payroma_token_engine.balance_of(wallet2_address).value()
            )
            self.assertAlmostEqual(
                total_supply.value() - amount.to_wei(),
                payroma_token_engine.total_supply().value()
            )

    def __send_transaction(self, tx_data: dict, private_key: str):
        tx = engine.provider.MainProvider.build_transaction(
            from_address=tools.interface.Address(tx_data[engine.provider.Metadata.FROM]),
            to_address=tools.interface.Address(tx_data[engine.provider.Metadata.TO]),
            value=tools.interface.EtherAmount(
                value=tx_data[engine.provider.Metadata.VALUE],
                decimals=token_engine.interface.decimals
            ),
            data_bytes=tx_data[engine.provider.Metadata.DATA]
        )
        engine.provider.MainProvider.add_gas(tx)
        tx_hash = engine.provider.MainProvider.send_transaction(tx, private_key)
        time.sleep(10)
        tx_hash.explorer_view()
        transaction = engine.provider.MainProvider.get_transaction(tx_hash)
        transaction_receipt = engine.provider.MainProvider.get_transaction_receipt(tx_hash)

        self.assertIsInstance(tx, dict)
        self.assertIsInstance(tx_hash, tools.interface.TXHash)
        self.assertIsInstance(transaction, datastructures.AttributeDict)
        self.assertIsInstance(transaction_receipt, datastructures.AttributeDict)

        if debugging:
            print(f"""
            tx_hash: {tx_hash.value()}
            transaction: {transaction}
            transaction_receipt: {transaction_receipt}
            """)


if __name__ == '__main__':
    unittest.main()
