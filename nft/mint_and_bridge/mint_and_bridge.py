from utils.transaction_data import load_abi
from web3.contract import Contract
from loguru import logger
from web3 import Web3
from hexbytes import HexBytes
from asyncio import sleep
from nft.mint_and_bridge.utils.transaction_data import get_contract, get_nft_id


class MintBridge:
    def __init__(self, private_key: str, bridge_to: str) -> None:
        self.private_key = private_key
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
        self.bridge_to = bridge_to
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address
        self.nonce = self.web3.eth.get_transaction_count(self.address_wallet)

    async def mint(self) -> None:
        contract = await get_contract(self.web3)
        tx = contract.functions.mint().build_transaction({
            'from': self.address_wallet,
            'value': self.web3.to_wei(0.0005, 'ether'),
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
            f'Bought NFT | TX: https://explorer.zksync.io/tx/{tx_hash}')

        self.nonce += 1

        await sleep(5)

        nft_id = await get_nft_id(self.web3, tx_hash)
        await self.bridge(nft_id, contract)

    async def bridge(self, nft_id: int, contract: Contract) -> None:
        while True:
            try:
                if self.bridge_to == 'Polygon':
                    tx = contract.functions.crossChain(158, HexBytes(
                        '0xdc60fd9d2a4ccf97f292969580874de69e6c326ed43a183c97db9174962607a8b6552ce320eac5aa'),
                                                       nft_id).build_transaction({
                        'from': self.address_wallet,
                        'value': self.web3.to_wei(0.0013, 'ether'),
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
                        f'Successfully bridged NFT to Polygon zkEVM| TX: https://explorer.zksync.io/tx/{tx_hash}')
                    break

                elif self.bridge_to == 'Arbitrum':
                    tx = contract.functions.crossChain(175, HexBytes(
                        '0x5b10ae182c297ec76fe6fe0e3da7c4797cede02dd43a183c97db9174962607a8b6552ce320eac5aa'),
                                                       nft_id).build_transaction({
                        'from': self.address_wallet,
                        'value': self.web3.to_wei(0.0013, 'ether'),
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
                        f'Successfully bridged NFT to Arbitrum Nova | TX: https://explorer.zksync.io/tx/{tx_hash}')
                    break
            except Exception as ex:
                if 'nonce too low' in str(ex):
                    self.nonce += 1
                    continue
                else:
                    logger.error(f'Something went wrong | {ex}')
                    break


