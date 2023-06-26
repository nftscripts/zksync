from utils.chains import ERA
from eth_abi import encode
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


class SyncSwapSwap:
    def __init__(self, private_key: str, from_token: str, to_token: str,
                 amount_from: float, amount_to: float) -> None:
        self.private_key = private_key
        self.from_token = from_token
        self.to_token = to_token
        self.amount_to_swap = random.uniform(amount_from, amount_to)
        self.classic_pool_factory_address = '0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb'
        self.router_address = '0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295'
        self.web3 = Web3(Web3.HTTPProvider(ERA.rpc))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    async def swap(self) -> None:
        to_token_address, from_token_address = await setup_tokens_addresses(from_token=self.from_token,
                                                                            to_token=self.to_token)

        classic_pool_factory = self.web3.eth.contract(
            address=Web3.to_checksum_address(self.classic_pool_factory_address),
            abi=await load_abi('classic_pool_factory_address'))
        pool_address = classic_pool_factory.functions.getPool(Web3.to_checksum_address(from_token_address),
                                                              Web3.to_checksum_address(to_token_address)).call()

        value, token_contract = await create_amount(self.from_token, self.web3, from_token_address, self.amount_to_swap)
        value = int(value)
        balance = await get_wallet_balance(self.from_token, self.web3, self.address_wallet, token_contract, 'ERA')

        if value > balance:
            logger.error(f'Not enough money for wallet {self.address_wallet}')
            return

        if pool_address == "0x0000000000000000000000000000000000000000":
            logger.error(f'There is no pool')
            return

        swap_data = encode(
            ["address", "address", "uint8"],
            [Web3.to_checksum_address(from_token_address), self.address_wallet, 1]
        )
        native_eth_address = "0x0000000000000000000000000000000000000000"

        steps = [{
            "pool": pool_address,
            "data": swap_data,
            "callback": native_eth_address,
            "callbackData": '0x'
        }]

        paths = [{
            "steps": steps,
            "tokenIn": Web3.to_checksum_address(
                from_token_address) if self.from_token.lower() != 'eth' else Web3.to_checksum_address(
                native_eth_address),
            "amountIn": value,
        }]

        router = self.web3.eth.contract(address=Web3.to_checksum_address(self.router_address),
                                        abi=await load_abi('sync_swap_router'))

        if self.from_token.lower() != 'eth':
            await approve_token(amount=value,
                                private_key=self.private_key,
                                chain='ERA',
                                from_token_address=from_token_address,
                                spender=self.router_address,
                                address_wallet=self.address_wallet,
                                web3=self.web3)

        tx = router.functions.swap(
            paths,
            0,
            int(self.web3.eth.get_block('latest').timestamp) + 1200
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


class SyncSwapLiq:
    def __init__(self, private_key: str,
                 token: str,
                 amount_from: float,
                 amount_to: float) -> None:
        self.private_key = private_key
        self.token = token
        self.amount = random.uniform(amount_from, amount_to)
        self.classic_pool_factory_address = '0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb'
        self.router_address = '0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295'
        self.web3 = Web3(Web3.HTTPProvider(ERA.rpc))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    async def add_liquidity(self) -> None:
        to_token_address, from_token_address = await setup_for_liq(self.token)

        classicPoolFactory = self.web3.eth.contract(address=Web3.to_checksum_address(self.classic_pool_factory_address),
                                                    abi=await load_abi('classic_pool_factory_address'))
        pool_address = classicPoolFactory.functions.getPool(Web3.to_checksum_address(from_token_address),
                                                            Web3.to_checksum_address(to_token_address)).call()

        value, token_contract = await create_amount(self.token, self.web3, from_token_address, self.amount)
        value = int(value)

        balance = await get_wallet_balance(self.token, self.web3, self.address_wallet, token_contract, 'ERA')

        if pool_address == "0x0000000000000000000000000000000000000000":
            logger.error('Pool does not exist')
            return

        if value > balance:
            logger.error(f'Not enough money for wallet {self.address_wallet}')
            return

        native_eth_address = "0x0000000000000000000000000000000000000000"

        min_liquidity = 0
        callback = native_eth_address

        router = self.web3.eth.contract(address=Web3.to_checksum_address(self.router_address),
                                        abi=await load_abi('sync_swap_router'))

        if self.token.lower() != 'eth':
            await approve_token(amount=value,
                                private_key=self.private_key,
                                chain='ERA',
                                from_token_address=from_token_address,
                                spender=self.router_address,
                                address_wallet=self.address_wallet,
                                web3=self.web3)

        data = encode(
            ["address"],
            [self.address_wallet]
        )

        tx = router.functions.addLiquidity2(
            Web3.to_checksum_address(pool_address),
            [(Web3.to_checksum_address(to_token_address), 0),
             (Web3.to_checksum_address(callback), value)] if self.token.lower() == 'eth' else [
                (Web3.to_checksum_address(from_token_address), value)],
            data,
            min_liquidity,
            callback,
            '0x'
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
            f'Added {self.amount} {self.token} tokens to liquidity pool | TX: https://explorer.zksync.io/tx/{tx_hash}')
