from payromasdk import MainProvider, PNSProvider, engine, tools


# Create a network interface
defaultNetwork = tools.interface.Network(
    rpc='https://data-seed-prebsc-1-s1.binance.org:8545',
    name='Binance Smart Chain (TestNet)',
    chain_id=97,
    symbol='BNB',
    explorer='https://testnet.bscscan.com'
)


devAddress = tools.interface.Address('0x149A03EBA3c0786581ad4b2cEC8082ef9e9425Bb')
# -> devAddress.explorer_view(network_interface=defaultNetwork)


tokenAddress = tools.interface.Address('0xfCF2F96ab285eFfd3E37848f86a4b08969A397Ef')
# -> tokenAddress.explorer_view(network_interface=defaultNetwork)


stakeAddress = tools.interface.Address('0x0b36A0A12a97fAA918DD274eE66A35e61355e507')
# -> stakeAddress.explorer_view(network_interface=defaultNetwork)


pnsAddress = tools.interface.Address('0x6575E25763BCd9fDb0c663984c4122D1fFc447e9')
# -> pnsAddress.explorer_view(network_interface=defaultNetwork)


# Network engine
allNetworks = engine.network.get_all()
engine.network.add_new(network_interface=defaultNetwork)
engine.network.remove(network_interface=defaultNetwork)


# Connect with a network
MainProvider.connect(network_interface=defaultNetwork)
PNSProvider.connect(network_interface=defaultNetwork)
PNSProvider.set_contract(address=pnsAddress)


# Create a wallet interface
defaultAddressBook = tools.interface.AddressBook(
    address_id=devAddress.to_integer(),
    username='test',
    address=devAddress.value()
)


# Addresses book engine
allAddressesBook = engine.addressbook.get_all()
engine.addressbook.add_new(address_book_interface=defaultAddressBook)
engine.addressbook.remove(address_book_interface=defaultAddressBook)


# Create a wallet interface
createNewWallet = engine.wallet.create(
    username='username_test',
    password='password_test',
    pin_code='pin_test',
    private_key='private_key_test'
)

defaultWallet = tools.interface.Wallet(
    address_id=devAddress.to_integer(),
    username='test',
    address=devAddress.value(),
    pin_code=b'pin_test',
    private_key=b'private_key_test',
    date_created='Thu Nov 25 15:24:24 2021',
    is_favorite=False
)


# Wallet engine
allWallets = engine.wallet.get_all()
engine.wallet.add_new(wallet_interface=defaultWallet)
engine.wallet.remove(wallet_interface=defaultWallet)

walletEngine = engine.wallet.WalletEngine(wallet_interface=defaultWallet)
walletEngine.username()
walletEngine.address()
walletEngine.pin_code()
walletEngine.private_key()
walletEngine.date_created()
walletEngine.login(password='')
walletEngine.tokens()
walletEngine.transactions()


# Create token interface
tokenInterface = tools.interface.Token(
    contract=tokenAddress.value(),
    symbol='PYA',
    decimals=18
)


# Token engine
tokenEngine = engine.token.TokenEngine(token_interface=tokenInterface)
tokenEngine.name()
tokenEngine.symbol()
tokenEngine.decimals()
tokenEngine.total_supply()
tokenEngine.balance_of(address=devAddress)


# Create stake pair interface
stakeInterface = tools.interface.Stake(
    contract=stakeAddress.value(),
    end_block=0,
    duration='locked',
    stake_token_contract=tokenEngine.interface.contract.value(),
    reward_token_contract=tokenEngine.interface.contract.value(),
    stake_token_symbol=tokenEngine.symbol(),
    reward_token_symbol=tokenEngine.symbol(),
    stake_token_decimals=tokenEngine.decimals(),
    reward_token_decimals=tokenEngine.decimals()
)


# Stake engine
stakeEngine = engine.stake.StakeEngine(stake_interface=stakeInterface)
stakeEngine.owner()
stakeEngine.is_initialized()
stakeEngine.start_block()
stakeEngine.total_supply()
stakeEngine.deposit(amount=tools.interface.EtherAmount(1, 18))
stakeEngine.balance_of(address=devAddress)
stakeEngine.pending_reward(address=devAddress)
stakeEngine.withdraw(amount=tools.interface.EtherAmount(0.5, 18))


# PNS engine
pnsEngine = engine.pns.PNSEngine()
pnsEngine.owner()
pnsEngine.new_record(name='dev')
pnsEngine.is_recorded(name='dev')
pnsEngine.get_by_name(name='dev')
pnsEngine.get_by_address(address=devAddress)
