import asyncio
import decimal

import buff2steam.exceptions
from buff2steam import config, logger
from buff2steam.provider.buff import Buff
from buff2steam.provider.steam import Steam


def remove_exponent(d):
    return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()


async def main_loop(buff, steam):
    total_page = await buff.get_total_page()
    visited = set()
    for each_page in range(1, total_page + 1):
        logger.debug(f'page: {each_page} / {total_page}...')
        items = await buff.get_items(each_page)
        logger.debug(f'items: {items}')
        logger.debug(f'got {len(items)} items')
        for item in items:
            if item['id'] in visited:
                continue

            market_hash_name = item['market_hash_name']
            buff_min_price = remove_exponent(decimal.Decimal(item['sell_min_price']) * 100)
            buff_says_steam_price = remove_exponent(decimal.Decimal(item['goods_info']['steam_price_cny']) * 100)

            if not config['main']['max_price'] > buff_min_price > config['main']['min_price']:
                logger.debug(f'buff_min_price: {buff_min_price} not in range')
                continue

            buff_says_ratio = buff_min_price / buff_says_steam_price if buff_says_steam_price else 1
            if buff_says_ratio > decimal.Decimal(config['main']['accept_buff_threshold']):
                logger.debug(f'buff_says_ratio: {buff_says_ratio} > {config["main"]["accept_buff_threshold"]}')
                continue

            try:
                listings_data = await steam.listings_data(market_hash_name)
            except buff2steam.exceptions.SteamError:
                logger.warning(
                    f'failed to get listings data for ({market_hash_name}), '
                    f'waiting {config["steam"]["request_interval"]} seconds...'
                )
                continue

            current_ratio = buff_min_price / listings_data['converted_price']

            orders_data = await steam.orders_data(market_hash_name)
            highest_buy_order = decimal.Decimal(orders_data['highest_buy_order'])
            wanted_cnt = orders_data['wanted_cnt']
            steam_tax_ratio = decimal.Decimal(listings_data['steam_tax_ratio'])
            highest_buy_order_ratio = buff_min_price / (highest_buy_order * steam_tax_ratio)
            buff_min_price_human = float(buff_min_price / 100)

            visited.add(item['id'])

            logger.info(' '.join([
                'buff_id/price: {buff_id}/{buff_price};'.format(
                    buff_id=item['id'], buff_price=buff_min_price_human
                ),
                'sell/want: {sell}/{want};'.format(
                    sell=listings_data['total_count'], want=wanted_cnt
                ),
                'b_o_ratio: {b_o_ratio:04.2f}; ratio: {ratio:04.2f}'.format(
                    b_o_ratio=highest_buy_order_ratio, ratio=current_ratio
                )
            ]))


async def main():
    try:
        while True:
            async with Buff(
                    game=config['main']['game'],
                    game_appid=config['main']['game_appid'],
                    request_interval=config['buff']['request_interval'],
                    request_kwargs=config['buff']['requests_kwargs'],
            ) as buff, Steam(
                game_appid=config['main']['game_appid'],
                request_interval=config['steam']['request_interval'],
                request_kwargs=config['steam']['requests_kwargs'],
            ) as steam:
                await main_loop(buff, steam)
    except KeyboardInterrupt:
        exit('Bye~')


if __name__ == '__main__':
    asyncio.run(main())
