from web3.contract import Contract
from eth_typing import Address
from web3 import Web3


async def get_wallet_balance(token: str, w3: Web3, address: Address, stable_contract: Contract | None,
                             from_chain: str) -> float:
    if token.lower() != 'eth':
        balance = stable_contract.functions.balanceOf(address).call()
        return balance
    else:
        if from_chain == 'bsc' or from_chain == 'matic':
            balance = stable_contract.functions.balanceOf(address).call()
        else:
            balance = w3.eth.get_balance(address)

        return balance
