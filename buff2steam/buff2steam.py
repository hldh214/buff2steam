import asyncio
import decimal
import json

import provider.buff

with open('../config.json') as fp:
    config = json.load(fp)


def remove_exponent(d):
    return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()


async def main():
    buff = provider.buff.Buff(
        config['main']['game'],
        config['main']['game_appid'],
        config['buff']['requests_kwargs']
    )

    total_page = await buff.get_total_page()
    # print(await asyncio.gather(buff.get_total_page(), buff.get_total_page(), buff.get_total_page()))
    for each_page in range(1, total_page + 1):
        items = await buff.get_items(each_page)
        for item in items:
            if item['id'] in config['buff']['blacklist']['id']:
                continue

            if item['goods_info']['info']['tags']['type']['internal_name'] in config['buff']['blacklist']['type']:
                continue

            market_hash_name = item['market_hash_name']
            buff_min_price = remove_exponent(decimal.Decimal(item['sell_min_price']) * 100)
            buff_says_steam_price = remove_exponent(decimal.Decimal(item['goods_info']['steam_price_cny']) * 100)

            if not config['main']['max_price'] > buff_min_price > config['main']['min_price']:
                continue

            if not buff_says_steam_price:
                continue

            buff_says_ratio = buff_min_price / buff_says_steam_price
            if buff_says_ratio > decimal.Decimal(config['main']['accept_buff_threshold']):
                continue

            print(market_hash_name, buff_says_ratio)
            # todo: steam integration


if __name__ == '__main__':
    while True:
        asyncio.run(main())
