from utils.chains import ERA
from loguru import logger
from web3 import Web3
import random

from swaps.utils.transaction_data import (
    setup_tokens_addresses,
    setup_for_liq,
)

from utils.transaction_data import (
    create_amount,
    get_wallet_balance,
    load_abi,
    approve_token,
)


class SpaceFiSwap:
    def __init__(self,
                 private_key: str,
                 from_token: str,
                 to_token: str,
                 amount_from: float,
                 amount_to: float
                 ) -> None:
        self.private_key = private_key
        self.from_token = from_token
        self.to_token = to_token
        self.amount_to_swap = random.uniform(amount_from, amount_to)
        self.swap_router_address = '0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d'
        self.web3 = Web3(Web3.HTTPProvider(ERA.rpc))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address
        self.nonce = self.web3.eth.get_transaction_count(self.address_wallet)

    async def swap(self) -> None:
        to_token_address, from_token_address = await setup_tokens_addresses(from_token=self.from_token,
                                                                            to_token=self.to_token)

        value, token_contract = await create_amount(self.from_token, self.web3, from_token_address, self.amount_to_swap)
        value = int(value)
        balance = await get_wallet_balance(self.from_token, self.web3, self.address_wallet, token_contract, 'ERA')

        if value > balance:
            logger.error(f'Not enough money for wallet {self.address_wallet}')
            return

        contract = self.web3.eth.contract(address=Web3.to_checksum_address(self.swap_router_address),
                                          abi=await load_abi('spacefi_swap_router'))

        if self.from_token.lower() != 'eth':
            await approve_token(amount=value,
                                private_key=self.private_key,
                                chain='ERA',
                                from_token_address=from_token_address,
                                spender=self.swap_router_address,
                                address_wallet=self.address_wallet,
                                web3=self.web3)

        deadline = int(self.web3.eth.get_block('latest').timestamp) + 1200

        if self.from_token.lower() == 'eth':

            tx = contract.functions.swapExactETHForTokens(
                0,
                [Web3.to_checksum_address(from_token_address), Web3.to_checksum_address(to_token_address)],
                self.address_wallet,
                deadline
            ).build_transaction({
                'from': self.address_wallet,
                'value': value if self.from_token.lower() == 'eth' else 0,
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
                'maxFeePerGas': 0,
                'maxPriorityFeePerGas': 0,
                'gas': 0
            })

            tx.update({'maxFeePerGas': self.web3.eth.gas_price})
            tx.update({'maxPriorityFeePerGas': self.web3.eth.gas_price})

            gasLimit = self.web3.eth.estimate_gas(tx)
            tx.update({'gas': gasLimit})

        else:
            tx = contract.functions.swapExactTokensForETH(
                value,
                0,
                [Web3.to_checksum_address(from_token_address), Web3.to_checksum_address(to_token_address)],
                self.address_wallet,
                deadline
            ).build_transaction({
                'from': self.address_wallet,
                'value': value if self.from_token.lower() == 'eth' else 0,
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
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


class SpaceFiLiquidity:
    def __init__(self,
                 private_key: str,
                 token: str,
                 amount_from: float,
                 amount_to: float
                 ) -> None:
        self.private_key = private_key
        self.token = token
        self.amount = random.uniform(amount_from, amount_to)
        self.swap_router_address = '0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d'
        self.web3 = Web3(Web3.HTTPProvider(ERA.rpc))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    async def add_liquidity(self) -> None:
        to_token_address, from_token_address = await setup_for_liq(self.token)

        value, token_contract = await create_amount(self.token, self.web3, from_token_address, self.amount)
        value = int(value)
        balance = await get_wallet_balance(self.token, self.web3, self.address_wallet, token_contract, 'ERA')

        if value > balance:
            logger.error(f'Not enough money for wallet {self.address_wallet}')
            return

        contract = self.web3.eth.contract(address=Web3.to_checksum_address(self.swap_router_address),
                                          abi=await load_abi('spacefi_swap_router'))

        await approve_token(amount=value,
                            private_key=self.private_key,
                            chain='ERA',
                            from_token_address='0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4',
                            spender=self.swap_router_address,
                            address_wallet=self.address_wallet,
                            web3=self.web3)

        deadline = int(self.web3.eth.get_block('latest').timestamp) + 1200

        tx = contract.functions.addLiquidityETH(
            Web3.to_checksum_address('0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4'),
            value,
            0,
            0,
            self.address_wallet,
            int(deadline),
        ).build_transaction({
            'from': self.address_wallet,
            'value': value if self.token.lower() == 'eth' else 0,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
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
            f'Added {self.amount} {self.token} tokens to liquidity pool on SpaceFI | TX: https://explorer.zksync.io/tx/{tx_hash}')
