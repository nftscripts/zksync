class Chain:
    def __init__(self, chain_id: int, rpc: str, scan: str, token: str, code: int) -> None:
        self.chain_id = chain_id
        self.rpc = rpc
        self.scan = scan
        self.token = token
        self.code = code


ETH = Chain(
    chain_id=1,
    rpc='http://rpc.ankr.com/eth',
    scan='https://etherscan.io/tx',
    token='ETH',
    code=9001
)

OP = Chain(
    chain_id=10,
    rpc='https://rpc.ankr.com/optimism',
    scan='https://optimistic.etherscan.io/tx',
    token='ETH',
    code=9007
)

BSC = Chain(
    chain_id=56,
    rpc='https://bsc-dataseed.binance.org',
    scan='https://bscscan.com/tx',
    token='BNB',
    code=9015
)

POLYGON = Chain(
    chain_id=137,
    rpc='https://polygon-rpc.com',
    scan='https://polygonscan.com/tx',
    token='MATIC',
    code=9006
)

ARB = Chain(
    chain_id=42161,
    rpc='https://arb1.arbitrum.io/rpc',
    scan='https://arbiscan.io/tx',
    token='ETH',
    code=9002
)

NOVA = Chain(
    chain_id=42170,
    rpc='https://nova.arbitrum.io/rpc',
    scan='https://nova.arbiscan.io/tx',
    token='ETH',
    code=9016
)

ERA = Chain(
    chain_id=324,
    rpc='https://mainnet.era.zksync.io',
    scan='https://explorer.zksync.io/tx',
    token='ETH',
    code=9014
)

LITE = Chain(
    chain_id=...,
    rpc='https://mainnet.era.zksync.io',
    scan='https://explorer.zksync.io/tx',
    token='ETH',
    code=9003
)

chain_mapping = {
    'matic': POLYGON,
    'eth': ETH,
    'op': OP,
    'bsc': BSC,
    'arb': ARB,
    'nova': NOVA,
    'era': ERA,
    'lite': LITE
}
