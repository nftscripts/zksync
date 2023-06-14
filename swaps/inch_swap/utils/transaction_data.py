from utils.transaction_data import load_abi
from loguru import logger
from web3 import Web3


async def setup_transaction_data(web3: Web3, from_token_address: str, to_token_address: str) -> tuple[str, int, str]:
    if from_token_address == '':
        from_token_address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
        from_decimals = 18

    else:
        from_decimals = await check_data_token(web3, from_token_address)

    if to_token_address == '':
        to_token_address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

    return from_token_address, from_decimals, to_token_address


async def check_data_token(web3: Web3, from_token_address: str) -> int:
    try:
        token_contract = web3.eth.contract(address=web3.to_checksum_address(from_token_address),
                                           abi=await load_abi('erc20'))
        decimals = token_contract.functions.decimals().call()
        symbol = token_contract.functions.symbol().call()

        return decimals

    except Exception as ex:
        logger.error(f'Something went wrong | {ex}')
