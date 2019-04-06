import json
import os
import re
import time
import threading

import requests

from decimal import *
from http.cookies import SimpleCookie

from requests.cookies import cookiejar_from_dict
from termcolor import cprint

from buff2steam.c5 import C5
from buff2steam.buff import Buff
from buff2steam.steam import Steam

# todo: rework
# # debugging start
# import requests
# import logging
# import http.client as http_client
#
# http_client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
# # debugging end

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/config.json') as fp:
    config = json.load(fp)

steam_api = 'https://steamcommunity.com/market/listings/' + config['main']['game_appid'] + '/{0}/render'
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

c5 = C5(
    config['c5']['auto_buy']['username'],
    config['c5']['auto_buy']['password'],
    config['c5']['auto_buy']['device_id'],
    config['c5']['auto_buy']['pay_pwd'],
    config['main']['game_appid']
)

s = requests.session()
simple_cookie = SimpleCookie()
simple_cookie.load(config['buff']['requests_kwargs']['headers']['cookie'])
buff_cookies = {}
for key, morsel in simple_cookie.items():
    buff_cookies[key] = morsel.value
s.cookies = cookiejar_from_dict(buff_cookies)
buff = Buff(opener=s)


def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def while_true_sleep(fun_arg_tuples, seconds=5):
    while True:
        for fun, arg in fun_arg_tuples:
            if arg:
                fun(**arg)
            else:
                fun()
            time.sleep(seconds)


# buff auto withdraw && cancel
if config['buff']['auto_buy']['enable']:
    t = threading.Thread(target=while_true_sleep, kwargs={
        'fun_arg_tuples': [(buff.withdraw, None), (buff.cancel, None)]
    })
    t.setDaemon(True)
    t.start()

# c5 auto withdraw && cancel
if config['c5']['auto_buy']['enable']:
    t = threading.Thread(target=while_true_sleep, kwargs={
        'fun_arg_tuples': [(c5.withdraw, None), (c5.cancel, None)]
    })
    t.setDaemon(True)
    t.start()

# steam auto sell
if config['steam']['auto_sell']['enable']:
    steam_conf = config['steam']

    s = requests.session()
    for key, value in steam_conf['requests_kwargs'].items():
        setattr(s, key, value)
    s.cookies = cookiejar_from_dict({
        'sessionid': steam_conf['auto_sell']['session_id'],
        'steamLoginSecure': steam_conf['auto_sell']['steam_login_secure'],
        'browserid': steam_conf['auto_sell']['browser_id']
    })

    steam = Steam(
        s, steam_conf['auto_sell']['asf'],
        steam_conf['auto_sell']['steam_id'], config['main']['game_appid']
    )


    def steam_auto_sell():
        while True:
            inventory = steam.inventory()

            if not inventory:
                time.sleep(steam_conf['request_interval'])
                continue

            for each in inventory:
                after_tax_price = steam.max_after_tax_price(each['market_hash_name'])
                if steam.sell(after_tax_price, each['asset_id']):
                    print('{0} - {1} - Sold'.format(each['market_hash_name'], after_tax_price / 100))
                else:
                    cprint('{0} - Failed'.format(each['market_hash_name']), 'magenta')

            steam.confirm()


    t = threading.Thread(target=steam_auto_sell)
    t.setDaemon(True)
    t.start()

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
                print(res)
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
                    cprint('steam_api_429', 'magenta')
                    continue

                try:
                    res = res.json()
                except json.decoder.JSONDecodeError:
                    continue

                if not res or not res['listinginfo']:
                    continue

                listinginfo = res['listinginfo'][next(iter(res['listinginfo']))]

                if 'converted_price' not in listinginfo:
                    continue

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

                config['buff']['blacklist']['id'].append(item['id'])

                # C5 price compare
                c5_data = c5.query_by_name(item['name'])

                if not c5_data:
                    c5_data = {
                        'item_id': 0,
                        'price': float('+inf')
                    }

                buff_min_price_human = float(buff_min_price / 100)

                if buff_min_price_human <= c5_data['price']:
                    cprint(' '.join([
                        'buff_id/price: {buff_id}/{buff_price};'.format(
                            buff_id=item['id'], buff_price=buff_min_price_human
                        ),
                        'sell/want/sold: {sell}/{want};'.format(
                            sell=res['total_count'], want=wanted_cnt
                        ),
                        'b_o_ratio: {b_o_ratio:04.2f}; ratio: {ratio:04.2f}'.format(
                            b_o_ratio=highest_buy_order_ratio, ratio=current_ratio
                        ),
                    ]), color='green' if highest_buy_order_ratio < config['main'][
                        'highest_buy_order_ratio_threshold'] else None)
                else:
                    highest_buy_order_ratio = Decimal(c5_data['price'] * 100) / (highest_buy_order * steam_tax_ratio)
                    current_ratio = Decimal(c5_data['price'] * 100) / steam_price
                    cprint(' '.join([
                        'c5_id/price: {c5_id}/{c5_price};'.format(
                            c5_id=c5_data['item_id'], c5_price=c5_data['price']
                        ),
                        'sell/want/sold: {sell}/{want};'.format(
                            sell=res['total_count'], want=wanted_cnt
                        ),
                        'b_o_ratio: {b_o_ratio:04.2f}; ratio: {ratio:04.2f}'.format(
                            b_o_ratio=highest_buy_order_ratio, ratio=current_ratio
                        )
                    ]), color='green' if highest_buy_order_ratio < config['main'][
                        'highest_buy_order_ratio_threshold'] else None)

                if not config['buff']['auto_buy']['enable']:
                    continue

                if highest_buy_order_ratio > config['main']['highest_buy_order_ratio_threshold']:
                    continue

                if buff_min_price_human <= c5_data['price']:
                    buff.buy(
                        buff_min_price_human, item['id'],
                        config['buff']['auto_buy']['qty'], config['buff']['auto_buy']['pay_method']
                    )
                else:
                    c5.buy(c5_data['price'], str(c5_data['item_id']), config['c5']['auto_buy']['qty'])

except KeyboardInterrupt:
    print('Bye~')
    exit(0)
