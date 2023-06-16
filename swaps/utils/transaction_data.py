from swaps.utils.config import tokens


async def setup_tokens_addresses(from_token: str, to_token: str) -> tuple[str, str]:
    to_token_address, from_token_address = tokens[to_token.upper()], tokens[from_token.upper()]
    return to_token_address, from_token_address


async def setup_for_liq(token: str) -> tuple[str, str]:
    if token.lower() == 'usdc':
        from_token_address = tokens[token.upper()]
        to_token_address = tokens['ETH']
    else:
        from_token_address = tokens[token.upper()]
        to_token_address = tokens['USDC']

    return to_token_address, from_token_address
