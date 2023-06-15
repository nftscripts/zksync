from swaps.inch_swap.utils.transaction_data import setup_transaction_data
from bridges.orbiter_bridge.utils.transaction_data import get_chain_id
from aiohttp import ClientSession
from loguru import logger
from web3 import Web3
import random
import json

from utils.transaction_data import (
    approve_token,
    load_contract,
)


class InchSwap:
    def __init__(self,
                 private_key: str,
                 rpc_chain: str,
                 from_token_address: str,
                 to_token_address: str,
                 chain: str,
                 amount_from: float,
                 amount_to: float,
                 slippage: int
                 ) -> None:
        self.base_url = 'https://api-defillama.1inch.io'
        self.inch_version = 5
        self.web3 = Web3(Web3.HTTPProvider(rpc_chain))
        self.private_key = private_key
        self.chain = chain
        self.from_token_address = from_token_address
        self.to_token_address = to_token_address
        self.amount_to_swap = random.uniform(amount_from, amount_to)
        self.slippage = slippage
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address
        self.nonce = self.web3.eth.get_transaction_count(self.address_wallet)

    async def send_requests(self, url: str) -> json:
        async with ClientSession() as session:
            response = await session.get(url)
            response_text = await response.json()
        return response_text

    async def swap(self) -> None:
        response = await self.send_requests(
            url=f'{self.base_url}/v{self.inch_version}.0/{await get_chain_id(self.chain)}/approve/spender')
        spender = response['address']
        from_token_address, from_decimals, to_token_address = await setup_transaction_data(self.web3,
                                                                                           self.from_token_address,
                                                                                           self.to_token_address)
        amount = int(self.amount_to_swap * 10 ** from_decimals)
        token_contract = await load_contract(from_token_address, self.web3, 'erc20')

        if from_token_address != '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
            await approve_token(amount, self.private_key, self.chain, from_token_address, spender, self.address_wallet,
                                self.web3)

        response = await self.send_requests(
            url=f'{self.base_url}/v{self.inch_version}.0/{await get_chain_id(self.chain)}/swap?fromTokenAddress={from_token_address}&toTokenAddress={to_token_address}&amount={amount}&fromAddress={self.address_wallet}&slippage={self.slippage}')
        from_token = response['fromToken']['symbol']
        to_token = response['toToken']['symbol']
        to_token_decimals = response['toToken']['decimals']
        to_token_amount = float(response['toTokenAmount']) / 10 ** to_token_decimals
        tx = response['tx']
        tx['chainId'] = await get_chain_id(self.chain)
        tx['nonce'] = self.nonce
        tx['to'] = Web3.to_checksum_address(tx['to'])
        tx['gasPrice'] = int(tx['gasPrice'])
        tx['gas'] = int(int(tx['gas']))
        tx['value'] = int(tx['value'])

        try:
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash = self.web3.to_hex(raw_tx_hash)

            logger.info(
                f'Swapped {amount / 10 ** from_decimals} {from_token} tokens => to {to_token_amount} {to_token} | Tx hash: {tx_hash}')

        except Exception as ex:
            if 'nonce too low' in str(ex):
                tx['nonce'] = self.nonce + 1
                signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
                raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                tx_hash = self.web3.to_hex(raw_tx_hash)

                logger.info(
                    f'Swapped {amount / 10 ** from_decimals} {from_token} tokens => to {to_token_amount} {to_token} | Tx hash: {tx_hash}')
            else:
                logger.error(f'Something went wrong | {ex}')
                return

