from swaps.utils.transaction_data import setup_tokens_addresses
from swaps.utils.transaction_data import setup_for_liq
from loguru import logger
from web3 import Web3
import random

from utils.transaction_data import (
    get_wallet_balance,
    approve_token,
    create_amount,
    load_abi,
)


class MuteSwap:
    def __init__(self, private_key: str,
                 from_token: str,
                 to_token: str,
                 amount_from: float,
                 amount_to: float
                 ) -> None:
        self.private_key = private_key
        self.from_token = from_token
        self.to_token = to_token
        self.amount_to_swap = random.uniform(amount_from, amount_to)
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    async def swap(self) -> None:

        to_token_address, from_token_address = await setup_tokens_addresses(from_token=self.from_token,
                                                                            to_token=self.to_token)
        mute_contract = self.web3.eth.contract(
            address=Web3.to_checksum_address('0x8B791913eB07C32779a16750e3868aA8495F5964'),
            abi=await load_abi('mute_abi'))

        value, token_contract = await create_amount(self.from_token, self.web3, from_token_address, self.amount_to_swap)
        value = int(value)

        balance = await get_wallet_balance(self.from_token, self.web3, self.address_wallet, token_contract, 'ERA')

        if value > balance:
            raise Exception(f'Not enough balance for wallet {self.address_wallet}')

        deadline = int(self.web3.eth.get_block('latest').timestamp) + 1200

        if self.from_token.lower() != 'eth':
            await approve_token(amount=value,
                                private_key=self.private_key,
                                chain='ERA',
                                from_token_address=from_token_address,
                                spender='0x8B791913eB07C32779a16750e3868aA8495F5964',
                                address_wallet=self.address_wallet,
                                web3=self.web3)

        if self.from_token.lower() == 'eth':
            tx = mute_contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
                0,
                [Web3.to_checksum_address(from_token_address), Web3.to_checksum_address(to_token_address)],
                self.address_wallet,
                deadline,
                [True, False]
            ).build_transaction({
                'value': value if self.from_token.lower() == 'eth' else 0,
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
                'from': self.address_wallet,
                'maxFeePerGas': 0,
                'maxPriorityFeePerGas': 0,
                'gas': 0
            })

        else:
            tx = mute_contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                value,
                0,
                [Web3.to_checksum_address(from_token_address), Web3.to_checksum_address(to_token_address)],
                self.address_wallet,
                deadline,
                [False, False]
            ).build_transaction({
                'value': value if self.from_token.lower() == 'eth' else 0,
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
                'from': self.address_wallet,
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
            f'Swapped {self.amount_to_swap} {self.from_token} tokens => {self.to_token} | TX: https://explorer.zksync.io/tx/{tx_hash}')


class MuteLiq:
    def __init__(self, private_key: str,
                 token: str,
                 amount_from: float,
                 amount_to: float
                 ) -> None:
        self.private_key = private_key
        self.token = token
        self.amount = random.uniform(amount_from, amount_to)
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    async def add_liquidity(self) -> None:
        to_token_address, from_token_address = await setup_for_liq(self.token)
        mute_contract = self.web3.eth.contract(
            address=Web3.to_checksum_address('0x8B791913eB07C32779a16750e3868aA8495F5964'),
            abi=await load_abi('mute_abi'))

        value, token_contract = await create_amount(self.token, self.web3, from_token_address, self.amount)
        value = int(value)

        balance = await get_wallet_balance(self.token, self.web3, self.address_wallet, token_contract, 'ERA')

        if value > balance:
            raise Exception(f'Not enough balance for wallet {self.address_wallet}')

        deadline = int(self.web3.eth.get_block('latest').timestamp) + 1200
        if self.token.lower() != 'eth':
            await approve_token(amount=value,
                                private_key=self.private_key,
                                chain='ERA',
                                from_token_address=from_token_address,
                                spender='0x8B791913eB07C32779a16750e3868aA8495F5964',
                                address_wallet=self.address_wallet,
                                web3=self.web3)

        tx = mute_contract.functions.addLiquidityETH(
            Web3.to_checksum_address('0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4'),
            value,
            int(0),
            int(0),
            self.address_wallet,
            int(deadline),
            int(50),
            False
        ).build_transaction({
            'value': value if self.token.lower() == 'eth' else 0,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'from': self.address_wallet,
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
            f'Added {self.amount} {self.token} tokens to liquidity pool on Mute | TX: https://explorer.zksync.io/tx/{tx_hash}')
