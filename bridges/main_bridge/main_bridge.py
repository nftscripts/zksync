import random

from bridges.orbiter_bridge.utils.user_data import get_wallet_balance
from swaps.inch_swap.utils.transaction_data import load_abi
from loguru import logger
from web3 import Web3


class MainBridge:
    def __init__(self, private_key: str,
                 amount_from: float,
                 amount_to: float
                 ) -> None:
        self.private_key = private_key
        self.amount = random.uniform(amount_from, amount_to)
        self.web3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address
        self.nonce = self.web3.eth.get_transaction_count(self.address_wallet)

    async def deposit(self) -> None:
        value = self.web3.to_wei(self.amount, 'ether')
        l2_gas_limit = 733664
        balance = await get_wallet_balance('eth', self.web3, self.address_wallet, None, 'eth')

        if value > balance:
            raise Exception(f'Not enough balance for wallet {self.address_wallet}')

        l2_gas_per_pubdata_byte_limit = 800
        contract = self.web3.eth.contract(
            address=Web3.to_checksum_address('0x32400084C286CF3E17e7B677ea9583e60a000324'),
            abi=await load_abi('main_bridge'))

        tx = contract.functions.requestL2Transaction(
            self.address_wallet,
            value,
            b"",
            l2_gas_limit,
            l2_gas_per_pubdata_byte_limit,
            [],
            self.address_wallet
        ).build_transaction({
            'from': self.address_wallet,
            'gas': 150096,
            'gasPrice': self.web3.to_wei(20, 'gwei'),
            'nonce': self.nonce
        })

        # tx.update({'gasPrice': self.web3.eth.gas_price})
        # gasLimit = self.web3.eth.estimate_gas(tx)
        # tx.update({'gas': gasLimit})

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = self.web3.to_hex(raw_tx_hash)
        logger.success(
            f'Bridged {self.amount} ETH tokens | TX: https://etherscan.io/tx/{tx_hash}')
