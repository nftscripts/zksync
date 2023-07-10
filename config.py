RANDOMIZE = True  # Cделать ли выполнение модулей рандомно, чтобы паттерны на аккаунтах не были схожи
RUN_FOREVER = False

# -------------------------------------Модули--------------------------------#
orbiter_bridging = False
inch_swap = False
bungee_bridge = False
syncswap_swap = False
syncswap_liq = False
spacefi_swap = False
spacefi_liq = False
mute_swap = False
mute_liq = False
main_bridge = False
nft_domain_service = False
nft_mint_and_bridge = False


# ---------- Bridges ---------- #


class BungeeBridgeConfig:
    from_chain = 'OP'
    to_chain = 'ERA'
    amount_from = 0.006
    amount_to = 0.006
    bridge_all_balance = False


class MainBridgeConfig:
    amount_from = 0.01
    amount_to = 0.01
    action_type = 'deposit'  # deposit/withdraw


class OrbiterBridgeConfig:
    from_chain = 'OP'
    to_chain = 'ERA'
    token = 'ETH'
    amount_from = 0.006
    amount_to = 0.006


# ---------- Swaps ---------- #


class MuteSwapConfig:
    from_token = 'ETH'  # ETH/USDC
    to_token = 'USDC'
    amount_from = 0.004
    amount_to = 0.004


class InchSwapConfig:
    from_chain = ''
    amount_from = 0.1
    amount_to = 0.2
    slippage = 3
    from_token_address = '' # Пусто, если ETH
    to_token_address = ''


class SyncSwapConfig:
    from_token = 'ETH'  # ETH/USDC
    to_token = 'USDC'
    amount_from = 0.004
    amount_to = 0.004


class SpaceFiSwapConfig:
    from_token = 'ETH'  # ETH/USDC
    to_token = 'USDC'
    amount_from = 0.001
    amount_to = 0.001


# ---------- Liquidity ---------- #


class MuteLiquidityConfig:
    token = 'ETH'  # ETH only
    amount_from = 0.001
    amount_to = 0.001


class SyncSwapLiquidityConfig:
    token = 'ETH'  # ETH/USDC
    amount_from = 0.004
    amount_to = 0.004


class SpaceFiSwapLiquidityConfig:
    token = 'ETH'  # ETH Only
    amount_from = 0.001
    amount_to = 0.001


# ---------- NFT ---------- #


class NFTDomainService:
    pass


class MintAndBridge:
    bridge_to = 'Arbitrum'  # Arbitrum / Polygon
