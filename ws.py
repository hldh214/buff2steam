from abc import ABC

import tornado.websocket
import tornado.queues


class WebsocketHandler(tornado.websocket.WebSocketHandler, ABC):
    def initialize(self, item_queue: tornado.queues.Queue, bid_dict: dict):
        self.item_queue = item_queue
        self.bid_dict = bid_dict

    def check_origin(self, origin):
        return True

    async def on_message(self, message):
        await self.item_queue.put(message)
