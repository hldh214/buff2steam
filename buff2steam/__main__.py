import asyncio
import decimal

from buff2steam import config, logger
from buff2steam.provider.buff import Buff
from buff2steam.provider.steam import Steam


async def main_loop(buff, steam,min_volume):
    total_page = await buff.get_total_page()
    visited = set()
    for each_page in range(1, total_page + 1):
        logger.debug(f'page: {each_page} / {total_page}...')
        items = await buff.get_items(each_page)
        logger.debug(f'got {len(items)} items: {items}')
        for item in items:
            if item['id'] in visited:
                continue

            market_hash_name = item['market_hash_name']
            buff_min_price = int(decimal.Decimal(item['sell_min_price']) * 100)
            buff_says_steam_price = int(decimal.Decimal(item['goods_info']['steam_price_cny']) * 100)

            if not config['main']['max_price'] > buff_min_price > config['main']['min_price']:
                logger.debug(f'{market_hash_name}: buff_min_price({buff_min_price}) not in range, skipping...')
                continue

            buff_says_ratio = buff_min_price / buff_says_steam_price if buff_says_steam_price else 1
            accept_buff_threshold = config['main']['accept_buff_threshold']
            if buff_says_ratio > accept_buff_threshold:
                logger.debug(
                    f'{market_hash_name}: {buff_says_ratio} > {accept_buff_threshold}, skipping...'
                )
                continue

            logger.debug(f'Processing {market_hash_name}...')

            price_overview_data = await steam.price_overview_data(market_hash_name)
            if price_overview_data is None:
                continue

            volume = price_overview_data['volume']
            if min_volume > volume:
                logger.debug(f'{market_hash_name}: volume: {min_volume} > {volume}, skipping.')
                continue

            orders_data = None
            if volume > 0:
                orders_data = await steam.orders_data(market_hash_name)

            current_ratio = buff_min_price / (price_overview_data['price'] / (1 + steam.fee_rate))
            buff_min_price_human = float(buff_min_price / 100)

            result = [
                f'buff_id/price: {item["id"]}/{buff_min_price_human};',
            ]

            if orders_data is None:
                result.append(f'volume: {volume}; ratio: {current_ratio:04.2f}')
            else:
                b_o_ratio = buff_min_price / (orders_data['highest_buy_order'] / (1 + steam.fee_rate))
                result.append(f'sell/want: {orders_data["sell_order_count"]}/{orders_data["buy_order_count"]};')
                result.append(f'volume: {volume}; b_o_ratio: {b_o_ratio:04.2f}; ratio: {current_ratio:04.2f}')

            visited.add(item['id'])

            logger.info(' '.join(result))


async def main():
    try:
        while True:
            min_volume = config['steam']['min_volume']
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
                await main_loop(buff, steam, min_volume)
    except KeyboardInterrupt:
        exit('Bye~')


if __name__ == '__main__':
    asyncio.run(main())
