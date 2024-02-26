import asyncio
import re
import time

import httpx

from buff2steam import logger
from buff2steam.exceptions import BuffError


class Buff:
    base_url = 'https://buff.163.com'

    web_goods = '/api/market/goods'
    web_withdraw = '/api/market/backpack/withdraw'
    web_backpack = '/api/market/backpack'
    web_sell_order = '/api/market/goods/sell_order'
    web_buy = '/api/market/goods/buy'
    web_cancel = '/api/market/bill_order/deliver/cancel'
    web_history = '/api/market/buy_order/history'

    csrf_pattern = re.compile(r'name="csrf_token"\s*content="(.+?)"')

    def __init__(self, game, game_appid, config):
        self.game = game
        self.game_appid = game_appid

        self.request_interval = config.get('request_interval', 4)
        self.request_kwargs = config.get('requests_kwargs', {})
        self.sort_by = config.get('sort_by', None)

        self.request_locks = {}  # {url: [asyncio.Lock, last_request_time]}
        self.opener = httpx.AsyncClient(base_url=self.base_url, **self.request_kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.opener.aclose()

    async def request(self, *args, **kwargs) -> dict:
        url = kwargs.get('url', args[1])
        if url not in self.request_locks:
            self.request_locks[url] = [asyncio.Lock(), 0]

        async with self.request_locks[url][0]:
            elapsed = time.monotonic() - self.request_locks[url][1]
            if elapsed < self.request_interval:
                logger.debug(f'Waiting {self.request_interval - elapsed:.2f} seconds before next request({url})...')
                await asyncio.sleep(self.request_interval - elapsed)
            self.request_locks[url][1] = time.monotonic()

            response = await self.opener.request(*args, **kwargs)
            if response.json()['code'] != 'OK':
                raise BuffError(response.json())

            return response.json()['data']

    def _build_web_goods_params(self, page_num):
        params = {
            'page_num': page_num,
            'game': self.game
        }

        if self.sort_by:
            params['sort_by'] = self.sort_by

        return params

    async def get_total_page(self):
        response = await self.request('get', self.web_goods, params=self._build_web_goods_params(1))

        return response.get('total_page')

    async def get_items(self, page):
        response = await self.request('get', self.web_goods, params=self._build_web_goods_params(page))

        return response.get('items')
