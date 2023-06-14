from typing import Awaitable
from utils.runner import *
from colorama import Fore
from loguru import logger
from tqdm import tqdm
from web3 import Web3
from config import *
import random

from asyncio import (
    create_task,
    gather,
    run,
    sleep,
)

module_handlers = {
    'orbiter_bridging': process_orbiter_bridging,
    'inch_swap': process_inch_swap,
    'bungee_bridge': process_bungee_bridge,
    'syncswap_swap': process_sync_swap_swap,
    'syncswap_liq': process_sync_swap_liquidity,
    'mute_swap': process_mute_swap,
    'mute_liq': process_mute_liq,
    'main_bridge': process_main_bridge,
    'nft_domain_service': process_nft_domain_service,
    'nft_mint_and_bridge': process_nft_mint_and_bridge,
    'spacefi_swap': process_spacefi_swap,
    'spacefi_liq': process_spacefi_liq
}

with open('config.py', 'r', encoding='utf-8-sig') as file:
    module_config = file.read()

exec(module_config)

with open('wallets.txt', 'r', encoding='utf-8-sig') as file:
    private_keys = [line.strip() for line in file]

patterns = {}
web3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))

for module in module_handlers:
    if globals().get(module):
        patterns[module] = 'On'
    else:
        patterns[module] = 'Off'

print(Fore.BLUE + f'Loaded {len(private_keys)} wallets:')
print('\033[39m')

for private_key in private_keys:
    print(web3.eth.account.from_key(private_key).address)

print(f'----------------------------------------Modules--------------------------------------------')

for pattern, value in patterns.items():
    if value == 'Off':
        print("\033[31m {}".format(f'{pattern} = {value}'))
    else:
        print("\033[32m {}".format(f'{pattern} = {value}'))
print('\033[39m')

print('Created by | https://t.me/cryptoscripts')
print('Donations (Any EVM) | 0x763cDEa4a54991Cd85bFAd1FD47E9c175f53090B')
active_module = [module for module, value in patterns.items() if value == 'On']


async def main() -> None:
    tasks = []
    if RUN_FOREVER:
        while True:
            for private_key in private_keys:
                if RANDOMIZE is False:
                    for pattern in active_module:
                        task = create_task(module_handlers[pattern](private_key, pbar))
                        tasks.append(task)
                    time_to_sleep = random.randint(60, 120)
                    logger.info(f'Sleeping {time_to_sleep} seconds...')
                    await sleep(time_to_sleep)

                else:
                    random_index = random.randint(0, len(active_module) - 1)
                    random_element = active_module[random_index]
                    task = create_task(module_handlers[random_element](private_key, pbar))
                    tasks.append(task)
                    time_to_sleep = random.randint(60, 120)
                    logger.info(f'Sleeping {time_to_sleep} seconds...')
                    await sleep(time_to_sleep)

    else:
        for private_key in private_keys:
            if RANDOMIZE is False:
                for pattern in active_module:
                    task = create_task(module_handlers[pattern](private_key, pbar))
                    tasks.append(task)
                time_to_sleep = random.randint(60, 120)
                logger.info(f'Sleeping {time_to_sleep} seconds...')
                await sleep(time_to_sleep)

            else:
                random.shuffle(active_module)
                for pattern in active_module:
                    task = create_task(module_handlers[pattern](private_key, pbar))
                    tasks.append(task)
                    time_to_sleep = random.randint(60, 120)
                    logger.info(f'Sleeping {time_to_sleep} seconds...')
                    await sleep(time_to_sleep)

    await gather(*tasks)


def start_event_loop(awaitable: Awaitable[object]) -> None:
    run(awaitable)


if __name__ == '__main__':
    with tqdm(total=len(private_keys)) as pbar:
        async def tracked_main():
            await main()


        start_event_loop(tracked_main())
