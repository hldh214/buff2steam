# WARNING: may cause VAC ban
# BE CAUTION
from buff2steam import *


class Steam(BaseProvider):
    base_url = 'https://steamcommunity.com'

    web_sell = base_url + '/market/sellitem'
    web_inventory = base_url + '/inventory/{steam_id}/{game_appid}/{context_id}'
    web_listings = base_url + '/market/listings/{game_appid}/{market_hash_name}/render'

    def __init__(self, opener, asf_config, steam_id, game_appid, context_id=2):
        super().__init__(opener)
        self.asf_config = asf_config
        self.game_appid = game_appid
        self.context_id = context_id
        self.web_inventory = self.web_inventory.format(
            steam_id=steam_id,
            game_appid=game_appid,
            context_id=context_id
        )
        self.web_listings = self.web_listings.replace('{game_appid}', game_appid)

    def inventory(self) -> list:
        res = self.opener.get(self.web_inventory).json()

        if 'total_inventory_count' not in res or 'assets' not in res:
            return []

        result = []
        for asset in res['assets']:
            for description in res['descriptions']:
                if description['classid'] == asset['classid']:
                    result.append({
                        'asset_id': asset['assetid'],
                        'market_hash_name': description['market_hash_name']
                    })
                    break

        return result

    def sell(self, after_tax_price, asset_id) -> bool:
        self.opener.headers['referer'] = 'https://steamcommunity.com/id/'

        res = self.opener.post(self.web_sell, {
            'sessionid': self.opener.cookies['sessionid'],
            'appid': self.game_appid,
            'contextid': self.context_id,
            'assetid': asset_id,
            'amount': '1',
            'price': after_tax_price
        })

        res = res.json()

        if not res:
            return False

        return res['success']

    def max_after_tax_price(self, market_hash_name):
        res = self.opener.get(self.web_listings.format(market_hash_name=market_hash_name), params={
            'count': 1,
            'currency': 23
        }).json()

        listinginfo = res['listinginfo'][next(iter(res['listinginfo']))]

        return listinginfo['converted_price']

    def overpriced(self) -> list:
        pass  # todo

    def remove(self) -> bool:
        pass  # todo

    def confirm(self) -> bool:
        return requests.post(self.asf_config['2fa_accept_url'], headers={
            'authentication': self.asf_config['authentication']
        }).json()['Success']


if __name__ == '__main__':
    with open('../config.json') as fp:
        config = json.load(fp)

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
    # response = steam.sell('755', '15581448240')
    # response = steam.inventory()
    # response = steam.confirm()
    response = steam.max_after_tax_price('Genuine Bow of the Howling Wind')
    print(response)
