import asyncio
import decimal
import json

import provider.buff
import provider.steam

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

    steam = provider.steam.Steam(
        game_appid=config['main']['game_appid'],
        request_kwargs=config['steam']['requests_kwargs']
    )

    total_page = await buff.get_total_page()
    # print(await asyncio.gather(buff.get_total_page(), buff.get_total_page(), buff.get_total_page()))
    for each_page in range(1, total_page + 1):
        items = await buff.get_items(each_page)
        for item in items:
            market_hash_name = item['market_hash_name']
            buff_min_price = remove_exponent(decimal.Decimal(item['sell_min_price']) * 100)
            buff_says_steam_price = remove_exponent(decimal.Decimal(item['goods_info']['steam_price_cny']) * 100)

            if not config['main']['max_price'] > buff_min_price > config['main']['min_price']:
                continue

            buff_says_ratio = buff_min_price / buff_says_steam_price if buff_says_steam_price else 1
            if buff_says_ratio > decimal.Decimal(config['main']['accept_buff_threshold']):
                continue

            try:
                steam_max_after_tax_price = await steam.max_after_tax_price(market_hash_name)
            except Exception as exception:
                print(exception)
                await asyncio.sleep(config['steam']['request_interval'])
                continue

            current_ratio = buff_min_price / steam_max_after_tax_price

            print(market_hash_name, '{:.2f}'.format(buff_says_ratio), '{:.2f}'.format(current_ratio))

            await asyncio.sleep(config['steam']['request_interval'])


if __name__ == '__main__':
    while True:
        asyncio.run(main())
