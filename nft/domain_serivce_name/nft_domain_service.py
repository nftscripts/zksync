from loguru import logger
from web3 import Web3
import string
import random

from nft.domain_serivce_name.utils.trasaction_data import (
    generate_name,
    check_eligibility,
    load_contract
)


class MintName:
    def __init__(self, private_key: str) -> None:
        self.private_key = private_key
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address
        self.nonce = self.web3.eth.get_transaction_count(self.address_wallet)

    async def mint_name(self) -> None:
        contract = await load_contract(self.web3)
        while True:
            name = await generate_name()
            is_taken = await check_eligibility(contract, name)
            if is_taken != 0:
                continue
            break

        tx = contract.functions.Register(name).build_transaction({
            'from': self.address_wallet,
            'value': self.web3.to_wei(0.003, 'ether'),
            'nonce': self.nonce,
            'maxFeePerGas': 0,
            'maxPriorityFeePerGas': 0,
            'gas': 0
        })

        tx.update({'maxFeePerGas': self.web3.eth.gas_price})
        tx.update({'maxPriorityFeePerGas': self.web3.eth.gas_price})

        gasLimit = self.web3.eth.estimate_gas(tx)
        tx.update({'gas': gasLimit})

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = self.web3.to_hex(raw_tx_hash)
        logger.success(
            f'Minted {name} name | TX: https://explorer.zksync.io/tx/{tx_hash}')
