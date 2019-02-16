import json
import os
import re
import time

import requests

from decimal import *

from termcolor import cprint, colored

from buff2steam.c5 import C5

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/config.json') as fp:
    config = json.load(fp)

steam_api = 'https://steamcommunity.com/market/listings/' + str(config['main']['game_appid']) + '/{0}/render'
steam_order_api = 'https://steamcommunity.com/market/itemordershistogram?language=schinese&currency=23&item_nameid={0}'
steam_price_overview_api = 'https://steamcommunity.com/market/priceoverview'
buff_api = 'https://buff.163.com/api/market/goods'

item_nameid_pattern = re.compile(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)')
wanted_cnt_pattern = re.compile(r'<span\s*class="market_commodity_orders_header_promote">(\d+)</span>')

buff_opener = requests.session()
for key, value in config['buff']['requests_kwargs'].items():
    setattr(buff_opener, key, value)

steam_opener = requests.session()
for key, value in config['steam']['requests_kwargs'].items():
    setattr(steam_opener, key, value)

c5 = C5()


def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


try:
    while True:
        total_page = buff_opener.get(buff_api, params={
            'page_num': 1,
            'game': config['main']['game']
        }).json()['data']['total_page']

        for each_page in range(1, total_page + 1):
            res = buff_opener.get(buff_api, params={
                'page_num': each_page,
                'game': config['main']['game']
            }).json()

            if res['code'] != 'OK':
                print(res, flush=True)
                exit(1)

            items = res['data']['items']
            for item in items:
                if item['id'] in config['buff']['blacklist']['id']:
                    continue

                if item['goods_info']['info']['tags']['type']['internal_name'] in config['buff']['blacklist']['type']:
                    continue

                market_hash_name = item['market_hash_name']
                buff_min_price = remove_exponent(Decimal(item['sell_min_price']) * 100)
                buff_says_steam_price = remove_exponent(Decimal(item['goods_info']['steam_price_cny']) * 100)

                if not config['main']['max_price'] > buff_min_price > config['main']['min_price']:
                    continue

                if not buff_says_steam_price:
                    continue

                buff_says_ratio = buff_min_price / buff_says_steam_price
                if buff_says_ratio > Decimal(config['main']['accept_buff_threshold']):
                    continue

                time.sleep(config['steam']['request_interval'])
                res = steam_opener.get(steam_api.format(market_hash_name), params={
                    'count': 1,
                    'currency': 23
                })

                if res.status_code == 429:
                    cprint('steam_api_429', 'magenta', flush=True)
                    continue

                try:
                    res = res.json()
                except json.decoder.JSONDecodeError:
                    continue

                if not res or not res['listinginfo']:
                    continue

                listinginfo = res['listinginfo'][next(iter(res['listinginfo']))]
                steam_price = Decimal(listinginfo['converted_price'])
                steam_tax_ratio = steam_price / (steam_price + Decimal(listinginfo['converted_fee']))

                item_nameid = item_nameid_pattern.findall(
                    steam_opener.get(item['steam_market_url']).text
                )

                if not item_nameid:
                    continue

                item_nameid = item_nameid[0]
                orders_data = steam_opener.get(steam_order_api.format(item_nameid)).json()

                if 'highest_buy_order' not in orders_data or not orders_data['highest_buy_order']:
                    continue

                highest_buy_order = Decimal(orders_data['highest_buy_order'])
                wanted_cnt = wanted_cnt_pattern.findall(orders_data['buy_order_summary'])
                if wanted_cnt:
                    wanted_cnt = wanted_cnt[0]
                else:
                    wanted_cnt = 0

                current_ratio = buff_min_price / steam_price
                highest_buy_order_ratio = buff_min_price / (highest_buy_order * steam_tax_ratio)

                if highest_buy_order_ratio > 1:
                    continue

                # sold in 24h
                steam_price_overview = steam_opener.get(steam_price_overview_api, params={
                    'appid': config['main']['game_appid'],
                    'currency': 23,
                    'market_hash_name': market_hash_name
                }).json()

                if 'volume' not in steam_price_overview:
                    continue

                config['buff']['blacklist']['id'].append(item['id'])

                # C5 price compare
                c5_data = c5.query_by_name(item['name'])

                print(' '.join([
                    colored('buff_id/price: {buff_id}/{buff_price};'.format(
                        buff_id=item['id'], buff_price=buff_min_price / 100
                    ), color='green' if buff_min_price / 100 < c5_data['price'] else None),
                    colored('c5_id/price: {c5_id}/{c5_price};'.format(
                        c5_id=c5_data['item_id'] if c5_data else 0, c5_price=c5_data['price'] if c5_data else 0
                    ), color='green' if c5_data and buff_min_price / 100 > c5_data['price'] else None),
                    colored('sell/want/sold: {sell}/{want}/{sold};'.format(
                        sell=res['total_count'], want=wanted_cnt, sold=steam_price_overview['volume']
                    )),
                    colored(
                        'b_o_ratio: {b_o_ratio:04.2f}; ratio: {ratio:04.2f}'.format(
                            b_o_ratio=highest_buy_order_ratio, ratio=current_ratio
                        ),
                        color='green' if highest_buy_order_ratio < config['main'][
                            'highest_buy_order_ratio_threshold'] else None
                    )
                ]), flush=True)
except KeyboardInterrupt:
    print('Bye~')
    exit(0)
