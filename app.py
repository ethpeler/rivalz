import random
import time
import eth_account.signers.local
import web3
from web3 import Web3, Account
from config import RPC_URL, CONTRACT_ADDRESS, CONTRACT_METHOD, CHAIN_ID
def menu() -> int:
    x = None
    while not x:
        print("""
1) You need to do the same
2) Customize and Activate New Collectors
        """)
        x = input("-> ")
    return int(x)


def get_account_from_seed(w3: web3.Web3) -> eth_account.signers.local.LocalAccount:
    w3.eth.account.enable_unaudited_hdwallet_features()
    print("Enter your seed phrase")
    phrase = input("-> ")
    try:
        account = w3.eth.account.from_mnemonic(phrase)
        print(f"Your wallet address: {account.address}")
        return account
    except Exception as e:
        print(e)
        main()


def generate_account(w3: web3.Web3) -> eth_account.signers.local.LocalAccount:
    w3.eth.account.enable_unaudited_hdwallet_features()
    print("New wallet generated...")
    account, mnemonic = w3.eth.account.create_with_mnemonic()
    print(f"Your wallet address: {account.address}")
    print(f"Seed phrase of your wallet: {mnemonic}")
    print(f"Your wallet's private key: {account.key.hex()}")
    return account


def check_eth_balance(w3: web3.Web3, account: eth_account.signers.local.LocalAccount):
    balance = w3.from_wei(w3.eth.get_balance(account.address), "ether")
    print(f"Your wallet balance: {balance} ETH")
    if balance < 0.00001:
        print("Request funds for your wallet using the link:")
        print("https://rivalz2.hub.caldera.xyz/")
        print("")
        input("Then click Enter")
    else:
        input("Click Enter To launch auto-stamping")


def claim_nft(w3: web3.Web3, account: eth_account.signers.local.LocalAccount):
    nonce = w3.eth.get_transaction_count(account.address)
    transaction = {
        'to': CONTRACT_ADDRESS,
        'value': 0,
        'gas': 300000,
        'gasPrice': w3.to_wei('0.02', 'gwei'),
        'nonce': nonce,
        'data': CONTRACT_METHOD,
        'chainId': CHAIN_ID
    }
    try:
        signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"NFT claim hash: {tx_hash.hex()}")
    except Exception as e:
        print(e)


def main() -> None:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if w3.is_connected():
        if (choice := menu()) == 1:
            account = get_account_from_seed(w3)
            check_eth_balance(w3, account)
        elif choice == 2:
            account = generate_account(w3)
            check_eth_balance(w3, account)
        while True:
            print("Let's start branding")
            for i in range(20):
                claim_nft(w3, account)
                print(f"{i + 1}th stamp request sent successfully")
                time.sleep(random.randint(5, 15))
            print("Waiting for 12 hours cooldown")
            time.sleep(43260)
    else:
        print("Web3 connection failed!")
        print("Check your internet connection")


if __name__ == "__main__":
    get_logo()
    main()
