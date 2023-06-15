from utils.transaction_data import load_abi
from web3.contract import Contract
from hexbytes import HexBytes
from web3 import Web3


async def get_contract(web3: Web3) -> Contract:
    return web3.eth.contract(address=Web3.to_checksum_address('0xD43A183C97dB9174962607A8b6552CE320eAc5aA'),
                             abi=await load_abi('mint_and_bridge'))


async def get_nft_id(web3: Web3, tx_hash: str) -> int:
    logs = web3.eth.get_transaction_receipt(HexBytes(tx_hash)).logs

    for log in logs:
        if 'topics' in log and len(log['topics']) > 3:
            topic = log['topics'][3]
            if isinstance(topic, HexBytes):
                nft_id = int(topic.hex(), 16)
                return nft_id
