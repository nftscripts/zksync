from bridges.orbiter_bridge.utils.transaction_data import get_chain_id
from utils.transaction_data import decimal_to_int
from aiohttp import ClientSession
from asyncio import sleep
from loguru import logger
from web3 import Web3
import json


async def get_bungee_limits(from_chain: str, to_chain: str) -> tuple[int, int]:
    from_chain_id = await get_chain_id(from_chain)
    to_chain_id = await get_chain_id(to_chain)

    data = await get_bungee_data()

    for i in range(len(data['result'])):
        if data['result'][i]['chainId'] == from_chain_id:
            info = data['result'][i]['limits']

            try:

                if [x for x in info if x['chainId'] == to_chain_id][0] \
                        and [x for x in info if x['chainId'] == to_chain_id][0]['isEnabled'] is True:

                    info = [x for x in info if x['chainId'] == to_chain_id][0]
                    return int(info['minAmount']), int(info['maxAmount'])
                else:
                    logger.error(f'It is not possible to refuel from {from_chain} to {to_chain}')
                    return 0, 0

            except Exception as error:
                logger.error(error)


async def get_bungee_data() -> json:
    url = "https://refuel.socket.tech/chains"
    async with ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            response_text = await response.json()
            return response_text


async def check_balance(web3: Web3, private_key: str):
    try:
        wallet = web3.eth.account.from_key(private_key).address
        balance = web3.eth.get_balance(web3.to_checksum_address(wallet))
        token_decimal = 18
        human_readable = await decimal_to_int(balance, token_decimal)
        return human_readable

    except Exception as error:
        logger.error(error)
        await sleep(1)
        await check_balance(web3, private_key)
