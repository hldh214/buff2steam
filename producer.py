import httpx
import tornado.queues


class Producer:
    def __init__(self, item_list: list, item_queue: tornado.queues.Queue, bid_dict: dict):
        self.item_list = item_list
        self.item_queue = item_queue
        self.bid_dict = bid_dict

    async def watch_queue(self):
        while True:
            item_id = await self.item_queue.get()
            print('queue get {}'.format(item_id))
            result = await self.query_price(item_id)
            self.bid_dict[item_id] = result

    async def enqueue(self):
        for item_id in self.item_list:
            print('enqueue {}'.format(item_id))
            result = await self.query_price(item_id)
            self.bid_dict[item_id] = result

    async def query_price(self, item_id):
        # query price and calculate
        async with httpx.AsyncClient() as client:
            response = await client.get('https://httpbin.org/delay/4')
        return response.text
