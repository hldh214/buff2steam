import httpx


class C5:
    base_url = 'https://open.c5game.com'

    api_search = '/v1/store'
    api_inventory = '/v4/user/inventory/index'
    api_withdraw = '/v4/user/inventory/withdraw'
    api_history = '/v1/user/sell/trade-history'
    api_batch_pre = '/v4/trade/order/batch-pre'
    api_batch_payment = '/v4/trade/order/batch-payment'
    api_cancel = '/v3/user/sell/cancel-self-order'
    api_login = '/passport/login'

    def __init__(self):
        self.opener = httpx.AsyncClient(base_url=self.base_url)

    async def query_by_name(self, name: str):
        res = await self.opener.get(self.api_search, params={
            'keyword': name
        })

        res = res.json()

        if 'data' not in res:
            return False

        data = res['data']
        if data['total'] == 1:
            return data['list'][0]

        for each in data['list']:
            if each['name'] == name:
                return each
