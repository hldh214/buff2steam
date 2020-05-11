import argparse
import decimal
import json

import trio

from .provider.buff import Buff
from .provider.steam import Steam


def remove_exponent(d):
    return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()


async def _main(config):
    buff = Buff(
        config['main']['game'],
        config['main']['game_appid'],
        config['buff']['requests_kwargs']
    )

    steam = Steam(
        game_appid=config['main']['game_appid'],
        request_kwargs=config['steam']['requests_kwargs']
    )

    total_page = await buff.get_total_page()
    visited = set()
    for each_page in range(1, total_page + 1):
        items = await buff.get_items(each_page)
        for item in items:
            if item['id'] in visited:
                continue

            market_hash_name = item['market_hash_name']
            buff_min_price = remove_exponent(decimal.Decimal(item['sell_min_price']) * 100)
            buff_says_steam_price = remove_exponent(decimal.Decimal(item['goods_info']['steam_price_cny']) * 100)

            if not config['main']['max_price'] > buff_min_price > config['main']['min_price']:
                continue

            buff_says_ratio = buff_min_price / buff_says_steam_price if buff_says_steam_price else 1
            if buff_says_ratio > decimal.Decimal(config['main']['accept_buff_threshold']):
                continue

            try:
                # todo: gather
                listings_data = await steam.listings_data(market_hash_name)
            except Exception as exception:
                print(exception)
                await trio.sleep(config['steam']['request_interval'])
                continue

            current_ratio = buff_min_price / listings_data['converted_price']

            orders_data = await steam.orders_data(market_hash_name)
            highest_buy_order = decimal.Decimal(orders_data['highest_buy_order'])
            wanted_cnt = orders_data['wanted_cnt']
            steam_tax_ratio = decimal.Decimal(listings_data['steam_tax_ratio'])
            highest_buy_order_ratio = buff_min_price / (highest_buy_order * steam_tax_ratio)
            buff_min_price_human = float(buff_min_price / 100)

            visited.add(item['id'])

            print(' '.join([
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

            await trio.sleep(config['steam']['request_interval'])


async def trio_wrapper():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config path', default='./config.json')
    args = parser.parse_args()
    with open(args.config) as fp:
        config = json.load(fp)

    try:
        while True:
            await _main(config)
    except KeyboardInterrupt:
        exit('Bye~')


def main():
    trio.run(trio_wrapper)
