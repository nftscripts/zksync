from utils.transaction_data import load_abi
from string import ascii_lowercase
from web3.contract import Contract
from random import choice
from web3 import Web3


async def generate_name() -> str:
    letters = ascii_lowercase
    random_name = ''.join(choice(letters) for _ in range(4))
    return random_name


async def check_eligibility(contract: Contract, name: str) -> None:
    return contract.functions.tokenAddressandID(name).call()


async def load_contract(web3: Web3) -> Contract:
    return web3.eth.contract(address=Web3.to_checksum_address('0x935442AF47F3dc1c11F006D551E13769F12eab13'),
                             abi=await load_abi('era_name_service'))
