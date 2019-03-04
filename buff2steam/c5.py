from buff2steam import *


class C5:
    base_url = 'https://open.c5game.com'

    api_search = base_url + '/v1/store'
    api_inventory = base_url + '/v4/user/inventory/index'
    api_withdraw = base_url + '/v4/user/inventory/withdraw'
    api_history = base_url + '/v1/user/sell/trade-history'
    api_batch_pre = base_url + '/v4/trade/order/batch-pre'
    api_batch_payment = base_url + '/v4/trade/order/batch-payment'
    api_cancel = base_url + '/v3/user/sell/cancel-self-order'
    api_login = base_url + '/passport/login'

    common_params = {}

    def __init__(self, username, password, device_id, game_appid='570'):
        self.username = username
        self.password = password
        self.device_id = device_id
        self.game_appid = game_appid

        self.login()

    def login(self):
        res = requests.post(self.api_login, {
            'username': self.username,
            'password': self.password,
            'device_id': self.device_id,
        }).json()

        if res['status'] != 200:
            print('C5: Login:', res, flush=True)
            exit(1)

        self.common_params = {
            'access-token': res['data']['access-token']
        }

    def query_by_name(self, name: str) -> typing.Union[dict, bool]:
        res = requests.get(self.api_search, params={
            'keyword': name
        }).json()

        if 'data' not in res:
            return False

        data = res['data']
        if data['total'] == 1:
            return data['list'][0]

        for each in data['list']:
            if each['name'] == name:
                return each

    def buy(self, max_price: float, item_id: str, auto_buy_qty: int = 1):
        res = requests.post(self.api_batch_pre, {
            'max_price': max_price,
            'item_id': item_id,
            'num': auto_buy_qty
        }, params=self.common_params).json()

        if res['status'] == 401:
            self.login()
            return self.buy(max_price, item_id, auto_buy_qty)

        # may be sold out?
        if res['status'] == 500:
            return False

        id_list = []
        for item_id in res['data']['list'][0]:
            id_list.append(item_id)

        requests.post(self.api_batch_payment, {
            'noPwd': 1,
            'id[]': id_list
        }, params=self.common_params)

        return True

    def withdraw(self):
        params = {
            'appid': self.game_appid,
        }
        params.update(self.common_params)
        res = requests.get(self.api_inventory, params=params).json()

        if res['status'] == 401:
            self.login()
            return self.withdraw()

        id_list = []
        for item in res['data']['list']:
            id_list.append(item['id'])

        if not id_list:
            return False

        requests.post(self.api_withdraw, {
            'appid': self.game_appid,
            'id[]': id_list,
        }, params=self.common_params)

        return True

    def cancel(self):
        params = {
            'type': 1,
            'appid': self.game_appid,
            'status': 1
        }
        params.update(self.common_params)

        res = requests.get(self.api_history, params=params).json()

        if res['status'] == 401:
            self.login()
            return self.cancel()

        for order in res['data']['list']:
            requests.post(self.api_cancel, {
                'order_id': order['order_id']
            }, params=params)

        return True


if __name__ == '__main__':
    with open('../config.json') as fp:
        config = json.load(fp)

    c5 = C5(
        config['c5']['auto_buy']['username'],
        config['c5']['auto_buy']['password'],
        config['c5']['auto_buy']['device_id']
    )
    c5.buy(0.01, '18806')
    # c5.withdraw()
    # c5.cancel()
