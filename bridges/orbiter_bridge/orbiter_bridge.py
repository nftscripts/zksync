from bridges.orbiter_bridge.utils.user_data import get_wallet_balance
from utils.transaction_data import create_amount
from utils.transaction_data import approve_token
from fractions import Fraction
from loguru import logger
from web3 import Web3
import random
from bridges.orbiter_bridge.utils.config import (
    chain_with_native_eth,
    chain_without_eipstandart,
)

from bridges.orbiter_bridge.utils.transaction_data import (
    get_chain_id,
    check_eligibility,
    get_scan_url,
)


class Orbiter:
    def __init__(self,
                 private_key: str,
                 rpc_chain: str,
                 token_contract: str | None,
                 bridge_contract: str,
                 to_chain,
                 token: str,
                 from_chain: str,
                 amount_from: float,
                 amount_to: float,
                 code: int) -> None:
        self.token_contract = token_contract
        self.bridge_contract = bridge_contract
        self.private_key = private_key
        self.token = token
        self.from_chain = from_chain
        self.to_chain = to_chain
        self.amount = round(random.uniform(amount_from, amount_to), 7)
        self.code = code
        self.web3 = Web3(Web3.HTTPProvider(rpc_chain))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address
        self.nonce = self.web3.eth.get_transaction_count(self.address_wallet)

    async def create_tx(self) -> dict:
        amount, stable_contract = await create_amount(self.token, self.web3, self.token_contract,
                                                      self.amount)

        balance = await get_wallet_balance(self.token, self.web3, self.address_wallet, stable_contract, self.from_chain)

        eligibility, min_limit, max_limit = await check_eligibility(self.from_chain, self.to_chain, self.token, amount)

        if not eligibility:
            raise Exception(f'Limits error | Min: {min_limit}, Max: {max_limit}')

        if amount > balance:
            raise Exception(f'Not enough balance for wallet {self.address_wallet}')

        amount = int(str(Fraction(amount))[:-4] + str(self.code))

        if self.from_chain.lower() in chain_with_native_eth:
            if self.token.lower() == 'eth':
                tx = {"chainId": await get_chain_id(self.from_chain),
                      'to': self.web3.to_checksum_address(self.bridge_contract),
                      'value': amount,
                      'nonce': self.nonce
                      }
                if not (self.from_chain.lower() in chain_without_eipstandart):
                    tx.update({'maxFeePerGas': self.web3.eth.gas_price})
                    tx.update({'maxPriorityFeePerGas': self.web3.eth.gas_price})
                else:
                    tx.update({'gasPrice': self.web3.eth.gas_price})

                if self.from_chain.lower() == 'era':
                    tx.update({'from': self.address_wallet})

            else:
                tx = stable_contract.functions.transfer(Web3.to_checksum_address(self.bridge_contract),
                                                        amount).build_transaction({
                    'chainId': self.web3.eth.chain_id,
                    'from': self.address_wallet,
                    'nonce': self.nonce
                })
                if not (self.from_chain.lower() in chain_without_eipstandart):
                    tx.update({'maxFeePerGas': self.web3.eth.gas_price})
                    tx.update({'maxPriorityFeePerGas': self.web3.eth.gas_price})
                else:
                    tx.update({'gasPrice': self.web3.eth.gas_price})

            try:
                gasLimit = self.web3.eth.estimate_gas(tx)
                tx.update({'gas': gasLimit})

            except Exception as ex:
                logger.error(f'impossible calculate to chain | {ex}')
        else:
            tx = stable_contract.functions.transfer(Web3.to_checksum_address(self.bridge_contract),
                                                    amount).build_transaction({
                'chainId': self.web3.eth.chain_id,
                'from': self.address_wallet,
                'nonce': self.nonce
            })
            if not (self.from_chain in chain_without_eipstandart):
                tx.update({'maxFeePerGas': self.web3.eth.gas_price})
                tx.update({'maxPriorityFeePerGas': self.web3.eth.gas_price})
            else:
                tx.update({'gasPrice': self.web3.eth.gas_price})

            gasLimit = self.web3.eth.estimate_gas(tx)
            tx.update({'gas': gasLimit})

        return tx

    async def bridge(self) -> None:
        while True:
            try:
                tx = await self.create_tx()
                scan_url = await get_scan_url(self.from_chain)
                signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
                self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                tx_hash = self.web3.to_hex(self.web3.keccak(signed_tx.rawTransaction))
                logger.info(f'Transaction: {scan_url}/{tx_hash}')
                break
            except Exception as ex:
                if 'nonce too low' in str(ex):
                    self.nonce += 1
                    continue
                logger.error(f'Something went wrong | {ex}')
                break
