from abc import ABC

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.queues

import httpx

q = tornado.queues.Queue()


class Client:
    async def watch_queue(self):
        while True:
            items = await q.get()
            print(items)


class EchoWebSocket(tornado.websocket.WebSocketHandler, ABC):
    def check_origin(self, origin):
        return True

    async def on_message(self, message):
        response = await httpx.get('https://httpbin.org/delay/4')
        await q.put(123123)
        await self.write_message(response.text)
        await self.write_message("You said: " + message)


def enqueue():
    pass


if __name__ == "__main__":
    client = Client()
    tornado.ioloop.IOLoop.current().add_callback(client.watch_queue)

    application = tornado.web.Application([
        (r"/ws", EchoWebSocket),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
