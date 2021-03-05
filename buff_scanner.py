import argparse
import codecs
import csv
import datetime
import json

import trio

from buff2steam.provider.buff import Buff

header = [
    'market_hash_name', 'buff_says_ratio', 'buff_sell_num', 'buff_min_price', 'buff_says_steam_price',
    'buff_market_url', 'steam_market_url'
]


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config path', default='./config.json')
    args = parser.parse_args()
    with open(args.config) as fp:
        config = json.load(fp)

    filename = 'buff_scanner_result_' + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '.csv'

    with open(filename, 'wb') as fp:
        fp.write(codecs.BOM_UTF8)

    with open(filename, 'a', newline='') as fp:
        csv.writer(fp).writerow(header)

    buff = Buff(
        config['main']['game'],
        config['main']['game_appid'],
        config['buff']['requests_kwargs']
    )

    total_page = await buff.get_total_page()
    visited = set()
    for each_page in range(1, total_page + 1):
        try:
            items = await buff.get_items(each_page)
        except ValueError:
            continue

        for item in items:
            if item['id'] in visited:
                continue

            market_hash_name = item['market_hash_name']
            buff_sell_num = item['sell_num']
            steam_market_url = item['steam_market_url']
            buff_min_price = int(float(item['sell_min_price']) * 100)
            buff_says_steam_price = int(float(item['goods_info']['steam_price_cny']) * 100)

            if not config['main']['max_price'] > buff_min_price > config['main']['min_price']:
                continue

            buff_says_ratio = round(buff_min_price / buff_says_steam_price if buff_says_steam_price else 1, 4)
            if buff_says_ratio > config['main']['accept_buff_threshold']:
                continue

            with open(filename, 'a', newline='', encoding='utf-8') as fp:
                row = [
                    market_hash_name, buff_says_ratio, buff_sell_num,
                    buff_min_price / 100, buff_says_steam_price / 100,
                    'https://buff.163.com/market/goods?goods_id=' + str(item['id']), steam_market_url
                ]
                print(row)
                csv.writer(fp).writerow(row)


if __name__ == '__main__':
    trio.run(main)
