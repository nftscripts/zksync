from nft.domain_serivce_name.nft_domain_service import MintName
from nft.mint_and_bridge.mint_and_bridge import MintBridge
from bridges.orbiter_bridge.orbiter_bridge import Orbiter
from bridges.main_bridge.main_bridge import MainBridge
from bridges.bungee.bungee_bridge import BungeeBridge
from swaps.inch_swap.inch_swap import InchSwap
from utils.chains import *
from loguru import logger
from tqdm import tqdm
from config import *

from swaps.spacefi.spacefi import (
    SpaceFiSwap,
    SpaceFiLiquidity,
)

from swaps.mute.mute_swap import (
    MuteSwap,
    MuteLiq,
)

from bridges.orbiter_bridge.utils.transaction_data import (
    get_router,
    get_contract_stable,
)

from swaps.sync_swap.sync_swap import (
    SyncSwapSwap,
    SyncSwapLiq,
)


async def process_sync_swap_swap(private_key: str, pbar: tqdm) -> None:
    from_token = SyncSwapConfig.from_token
    to_token = SyncSwapConfig.to_token
    amount_from = SyncSwapConfig.amount_from
    amount_to = SyncSwapConfig.amount_to

    sync_swap = SyncSwapSwap(
        private_key=private_key,
        from_token=from_token,
        to_token=to_token,
        amount_from=amount_from,
        amount_to=amount_to
    )
    logger.info('Swapping on SyncSwap...')
    await sync_swap.swap()

    pbar.update()


async def process_sync_swap_liquidity(private_key: str, pbar: tqdm) -> None:
    token = SyncSwapLiquidityConfig.token
    amount_from = SyncSwapLiquidityConfig.amount_from
    amount_to = SyncSwapLiquidityConfig.amount_to

    sync_swap = SyncSwapLiq(
        private_key=private_key,
        token=token,
        amount_from=amount_from,
        amount_to=amount_to
    )
    logger.info('Adding liquidity on SyncSwap...')
    await sync_swap.add_liquidity()

    pbar.update()


async def process_orbiter_bridging(private_key: str, pbar: tqdm) -> None:
    token = OrbiterBridgeConfig.token
    from_chain = OrbiterBridgeConfig.from_chain
    to_chain = OrbiterBridgeConfig.to_chain
    amount_from = OrbiterBridgeConfig.amount_from
    amount_to = OrbiterBridgeConfig.amount_to

    if from_chain.lower() not in chain_mapping:
        raise ValueError(f"Unknown chain: {from_chain}. Use only: ARB/OP/BSC/ETH/NOVA/ERA/LITE/FTM/MATIC")

    contract_router = await get_router(token)
    contract_stable = await get_contract_stable(from_chain, token)

    bridger = Orbiter(
        private_key=private_key,
        rpc_chain=chain_mapping[from_chain.lower()].rpc,
        token_contract=contract_stable,
        bridge_contract=contract_router,
        to_chain=to_chain,
        token=token,
        from_chain=from_chain,
        amount_from=amount_from,
        amount_to=amount_to,
        code=chain_mapping[to_chain.lower()].code
    )
    logger.info('Bridging on orbiter...')
    await bridger.bridge()

    pbar.update()


async def process_inch_swap(private_key: str, pbar: tqdm) -> None:
    chain = InchSwapConfig.from_chain
    amount_from = InchSwapConfig.amount_from
    amount_to = InchSwapConfig.amount_to
    slippage = InchSwapConfig.slippage
    from_token_address = InchSwapConfig.from_token_address
    to_token_address = InchSwapConfig.to_token_address

    inch_swap = InchSwap(
        private_key=private_key,
        rpc_chain=chain_mapping[chain.lower()].rpc,
        from_token_address=from_token_address,
        to_token_address=to_token_address,
        chain=chain,
        amount_from=amount_from,
        amount_to=amount_to,
        slippage=slippage
    )

    logger.info('Swapping on 1inch...')
    await inch_swap.swap()

    pbar.update()


async def process_bungee_bridge(private_key: str, pbar: tqdm) -> None:
    from_chain = BungeeBridgeConfig.from_chain
    to_chain = BungeeBridgeConfig.to_chain
    amount_from = BungeeBridgeConfig.amount_from
    amount_to = BungeeBridgeConfig.amount_to
    bridge_all_balance = BungeeBridgeConfig.bridge_all_balance

    bungee_bridge = BungeeBridge(
        private_key=private_key,
        from_chain=from_chain,
        to_chain=to_chain,
        rpc_chain=chain_mapping[from_chain.lower()].rpc,
        amount_from=amount_from,
        amount_to=amount_to,
        bridge_all_balance=bridge_all_balance
    )

    logger.info('Bridging on Bungee...')
    await bungee_bridge.bridge()

    pbar.update()


async def process_mute_swap(private_key: str, pbar: tqdm) -> None:
    from_token = MuteSwapConfig.from_token
    to_token = MuteSwapConfig.to_token
    amount_from = MuteSwapConfig.amount_from
    amount_to = MuteSwapConfig.amount_to

    bungee_bridge = MuteSwap(
        private_key=private_key,
        from_token=from_token,
        to_token=to_token,
        amount_from=amount_from,
        amount_to=amount_to
    )

    logger.info('Swapping on Mute...')
    await bungee_bridge.swap()

    pbar.update()


async def process_mute_liq(private_key: str, pbar: tqdm) -> None:
    token = MuteLiquidityConfig.token
    amount_from = MuteLiquidityConfig.amount_from
    amount_to = MuteLiquidityConfig.amount_to

    bungee_bridge = MuteLiq(
        private_key=private_key,
        token=token,
        amount_from=amount_from,
        amount_to=amount_to
    )

    logger.info('Adding liquidity on Mute...')
    await bungee_bridge.add_liquidity()

    pbar.update()


async def process_main_bridge(private_key: str, pbar: tqdm) -> None:
    amount_from = MainBridgeConfig.amount_from
    amount_to = MainBridgeConfig.amount_to
    action_type = MainBridgeConfig.action_type
    main_bridge = MainBridge(
        private_key=private_key,
        amount_from=amount_from,
        amount_to=amount_to
    )

    logger.info('Bridging on main bridge...')
    if action_type.lower() == 'deposit':
        await main_bridge.deposit()
    elif action_type.lower() == 'withdraw':
        await main_bridge.withdraw()
    else:
        logger.error('Unknown action type. Use only: deposit/withdraw')

    pbar.update()


async def process_nft_domain_service(private_key: str, pbar: tqdm) -> None:
    nft_domain_service = MintName(private_key=private_key)

    logger.info('Minting NFT name...')
    await nft_domain_service.mint_name()

    pbar.update()


async def process_nft_mint_and_bridge(private_key: str, pbar: tqdm) -> None:
    bridge_to = MintAndBridge.bridge_to
    nft_domain_service = MintBridge(private_key=private_key,
                                    bridge_to=bridge_to)

    logger.info('Minting NFT...')
    await nft_domain_service.mint()

    pbar.update()


async def process_spacefi_swap(private_key: str, pbar: tqdm) -> None:
    from_token = SpaceFiSwapConfig.from_token
    to_token = SpaceFiSwapConfig.to_token
    amount_from = SpaceFiSwapConfig.amount_from
    amount_to = SpaceFiSwapConfig.amount_to

    spacefi_swap = SpaceFiSwap(private_key=private_key,
                               from_token=from_token,
                               to_token=to_token,
                               amount_from=amount_from,
                               amount_to=amount_to)

    logger.info('Swapping on SpaceFi')
    await spacefi_swap.swap()

    pbar.update()


async def process_spacefi_liq(private_key: str, pbar: tqdm) -> None:
    token = SpaceFiSwapLiquidityConfig.token
    amount_from = SpaceFiSwapLiquidityConfig.amount_from
    amount_to = SpaceFiSwapLiquidityConfig.amount_to

    spacefi_swap = SpaceFiLiquidity(private_key=private_key,
                                    token=token,
                                    amount_from=amount_from,
                                    amount_to=amount_to)

    logger.info('Adding liquidity on SpaceFi')
    await spacefi_swap.add_liquidity()

    pbar.update()
