from bridges.orbiter_bridge.utils.transaction_data import get_chain_id
from bridges.bungee.utills.config import BUNGEE_REFUEL_CONTRACTS
from loguru import logger
from web3 import Web3
import random

from bridges.orbiter_bridge.utils.config import (
    chain_without_eipstandart,
)

from bridges.bungee.utills.transaction_data import (
    get_bungee_limits,
    check_balance,
)

from utils.transaction_data import (
    load_abi,
    decimal_to_int,
    round_to,
    int_to_decimal,
)


class BungeeBridge:
    def __init__(self,
                 private_key: str,
                 from_chain: str,
                 to_chain: str,
                 rpc_chain: str,
                 amount_from: float,
                 amount_to: float,
                 bridge_all_balance: bool
                 ) -> None:
        self.private_key = private_key
        self.from_chain = from_chain
        self.to_chain = to_chain
        self.rpc_chain = rpc_chain
        self.amount_to_bridge = random.uniform(amount_from, amount_to)
        self.bridge_all_balance = bridge_all_balance
        self.web3 = Web3(Web3.HTTPProvider(rpc_chain))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address
        self.nonce = self.web3.eth.get_transaction_count(self.address_wallet)

    async def bridge(self) -> None:
        if self.bridge_all_balance is True:
            amount = await check_balance(self.web3, self.private_key) * 0.97
        else:
            amount = self.amount_to_bridge
        value = await int_to_decimal(amount, 18)

        balance = await check_balance(self.web3, self.private_key)
        if self.amount_to_bridge > balance:
            logger.error(f'Not enough balance for wallet {self.address_wallet}')
            return

        limits = await get_bungee_limits(self.from_chain, self.to_chain)
        min_limit = await round_to(await decimal_to_int(limits[0], 18))
        max_limit = await round_to(await decimal_to_int(limits[1], 18))

        if min_limit < self.amount_to_bridge < max_limit:
            pass
        else:
            logger.error(
                f'Amount to bridge ({self.amount_to_bridge}) is out of limits | MIN: {min_limit} MAX: {max_limit}')
            return

        contract = self.web3.eth.contract(
            address=Web3.to_checksum_address(BUNGEE_REFUEL_CONTRACTS[self.from_chain.lower()]),
            abi=await load_abi('bungee_refuel'))

        if not (self.from_chain.lower() in chain_without_eipstandart):
            tx = contract.functions.depositNativeToken(await get_chain_id(self.to_chain),
                                                       self.address_wallet
                                                       ). \
                build_transaction({
                'from': self.address_wallet,
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
                'value': value,
                'maxFeePerGas': 0,
                'maxPriorityFeePerGas': 0,
                'gas': 0
            })
            tx.update({'maxFeePerGas': self.web3.eth.gas_price})
            tx.update({'maxPriorityFeePerGas': self.web3.eth.gas_price})
            gasLimit = self.web3.eth.estimate_gas(tx)
            tx.update({'gas': gasLimit})

        else:
            tx = contract.functions.depositNativeToken(await get_chain_id(self.to_chain),
                                                       self.address_wallet
                                                       ). \
                build_transaction({
                'from': self.address_wallet,
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
                'value': value,
                'gasPrice': self.web3.eth.gas_price,
                'gas': 0
            })
            gasLimit = self.web3.eth.estimate_gas(tx)
            tx.update({'gas': gasLimit})

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = self.web3.to_hex(raw_tx_hash)

        logger.info(f'Swapped {value / 10 ** 18} ETH from {self.from_chain} => {self.to_chain} | Tx hash: {tx_hash}')
                     
