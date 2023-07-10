from zksync2.manage_contracts.zksync_contract import ZkSyncContract
from zksync2.transaction.transaction_builders import TxWithdraw
from zksync2.provider.eth_provider import EthereumProvider
from zksync2.module.module_builder import ZkSyncBuilder
from eth_account.signers.local import LocalAccount
from zksync2.core.types import Token
from eth_account import Account
from loguru import logger
from web3 import Web3
import random

from src.utils.chains import (
    ETH,
    ERA,
)


class MainBridge:
    def __init__(self,
                 private_key: str,
                 amount_from: float,
                 amount_to: float,
                 ) -> None:
        self.amount = round(random.uniform(amount_from, amount_to), 8)
        self.zk_web3 = ZkSyncBuilder.build(ERA.rpc)
        self.eth_web3 = Web3(Web3.HTTPProvider(ETH.rpc))
        self.account: LocalAccount = Account.from_key(private_key)
        self.address_wallet = self.account.address

    async def deposit(self) -> None:
        eth_provider = EthereumProvider(self.zk_web3, self.eth_web3, self.account)
        l1_tx_receipt = eth_provider.deposit(token=Token.create_eth(),
                                             amount=Web3.to_wei(self.amount, 'ether'),
                                             gas_price=self.eth_web3.eth.gas_price)

        if not l1_tx_receipt["status"]:
            logger.error("Deposit transaction on L1 network failed")
            return

        zksync_contract = ZkSyncContract(self.zk_web3.zksync.main_contract_address, self.eth_web3, self.account)

        l2_hash = self.zk_web3.zksync.get_l2_hash_from_priority_op(l1_tx_receipt, zksync_contract)

        logger.info("Waiting for deposit transaction on L2 network to be finalized (5-7 minutes)")
        self.zk_web3.zksync.wait_for_transaction_receipt(transaction_hash=l2_hash,
                                                         timeout=360,
                                                         poll_latency=10)

        logger.success(
            f"Bridged {self.amount} ETH tokens | TX: https://etherscan.io/tx/{l1_tx_receipt['transactionHash'].hex()}")

    async def withdraw(self) -> None:
        withdrawal_tx = TxWithdraw(web3=self.zk_web3,
                                   token=Token.create_eth(),
                                   amount=Web3.to_wei(self.amount, "ether"),
                                   gas_limit=0,
                                   account=self.account)

        estimated_gas = self.zk_web3.zksync.eth_estimate_gas(withdrawal_tx.tx)

        tx = withdrawal_tx.estimated_gas(estimated_gas)
        signed = self.account.sign_transaction(tx)
        raw_tx_hash = self.zk_web3.zksync.send_raw_transaction(signed.rawTransaction)
        tx_hash = self.zk_web3.to_hex(raw_tx_hash)
        logger.success(
            f'Bridged {self.amount} ETH tokens from ZkSync ERA => to ETH mainnet | TX: https://explorer.zksync.io/tx/{tx_hash}')
