import time
import re
import requests

from decimal import *
from json.decoder import JSONDecodeError

from termcolor import cprint

buff_session = 'YOUR BUFF SESSION HERE'
proxies = {
    'https': 'http://127.0.0.1:1080'
}
visited_ids = set()
buff_id_blacklist = (3986,)
buff_type_blacklist = ('tool',)
game = 'dota2'
game_appid = '570'
currency = 23  # CNY
accept_buff_threshold = Decimal(0.6)
highest_buy_order_ratio_threshold = Decimal(0.75)
# CNY * 100
min_price = 1000
max_price = 30000
# steam api request interval
steam_api_sleep = 30

steam_api = 'https://steamcommunity.com/market/listings/' + game_appid + '/{0}/render'
steam_order_api = 'https://steamcommunity.com/market/itemordershistogram?language=schinese&currency=23&item_nameid={0}'
steam_price_overview_api = 'https://steamcommunity.com/market/priceoverview'
buff_api = 'https://buff.163.com/api/market/goods'

item_nameid_pattern = re.compile(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)')
wanted_cnt_pattern = re.compile(r'<span\s*class="market_commodity_orders_header_promote">(\d+)</span>')


def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


try:
    while True:
        total_page = requests.get(buff_api, params={
            'page_num': 1,
            'game': game
        }).json()['data']['total_page']

        for each_page in range(1, total_page + 1):
            res = requests.get(buff_api, params={
                'page_num': each_page,
                'game': game
            }, headers={
                'cookie': buff_session
            }).json()

            if res['code'] != 'OK':
                print(res)
                exit(1)

            items = res['data']['items']
            for item in items:
                if item['id'] in visited_ids:
                    continue

                if item['goods_info']['info']['tags']['type']['internal_name'] in buff_type_blacklist:
                    continue

                if item['id'] in buff_id_blacklist:
                    continue
                market_hash_name = item['market_hash_name']
                buff_min_price = remove_exponent(Decimal(item['sell_min_price']) * 100)
                buff_says_steam_price = remove_exponent(Decimal(item['goods_info']['steam_price_cny']) * 100)

                if buff_min_price < min_price or buff_min_price > max_price:
                    continue

                if not buff_says_steam_price:
                    continue

                buff_says_ratio = buff_min_price / buff_says_steam_price
                if buff_says_ratio > accept_buff_threshold:
                    continue

                time.sleep(steam_api_sleep)
                res = requests.get(steam_api.format(market_hash_name), params={
                    'count': 1,
                    'currency': currency,
                }, proxies=proxies)

                if res.status_code == 429:
                    cprint('steam_api_429', 'magenta')
                    continue

                try:
                    res = res.json()
                except JSONDecodeError:
                    continue

                if not res or not res['listinginfo']:
                    continue

                listinginfo = res['listinginfo'][next(iter(res['listinginfo']))]
                steam_price = Decimal(listinginfo['converted_price'])
                steam_tax_ratio = steam_price / (steam_price + Decimal(listinginfo['converted_fee']))

                item_nameid = item_nameid_pattern.findall(requests.get(
                    item['steam_market_url'], proxies=proxies
                ).text)

                if not item_nameid:
                    continue

                item_nameid = item_nameid[0]
                orders_data = requests.get(
                    steam_order_api.format(item_nameid), proxies=proxies
                ).json()

                if 'highest_buy_order' not in orders_data:
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
                steam_price_overview = requests.get(steam_price_overview_api, params={
                    'appid': game_appid,
                    'currency': currency,
                    'market_hash_name': market_hash_name
                }, proxies=proxies).json()

                if 'volume' not in steam_price_overview:
                    continue

                visited_ids.add(item['id'])

                if highest_buy_order_ratio < highest_buy_order_ratio_threshold:
                    cprint('id: {}; s_cnt: {}; w_cnt: {}; volume: {}; buff_price: {}; '
                           'b_o_ratio: {:04.2f}; ratio: {:04.2f}'.format(
                        item['id'], res['total_count'], wanted_cnt, steam_price_overview['volume'], buff_min_price,
                        highest_buy_order_ratio, current_ratio
                    ), 'green')
                    continue

                print('id: {}; s_cnt: {}; w_cnt: {}; volume: {}; buff_price: {}; '
                      'b_o_ratio: {:04.2f}; ratio: {:04.2f}'.format(
                    item['id'], res['total_count'], wanted_cnt, steam_price_overview['volume'], buff_min_price,
                    highest_buy_order_ratio, current_ratio
                ))
except KeyboardInterrupt:
    print('Bye~')
    exit(0)
