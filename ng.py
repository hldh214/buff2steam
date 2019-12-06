import tornado.ioloop
import tornado.web
import tornado.queues

from producer import Producer
from ws import WebsocketHandler

# 待询价饰品
item_queue = tornado.queues.Queue()
# 全部可交易饰品列表
item_list = [
    # todo: scrape all item_ids
    774681, 774864, 774774, 774712, 774871, 774738
]
# 好价饰品
bid_dict = {}
connection_pool = set()

producer = Producer(item_list, item_queue, bid_dict)
tornado.ioloop.IOLoop.current().add_callback(producer.watch_queue)
tornado.ioloop.IOLoop.current().add_callback(producer.enqueue)

# todo: write_message() on event?
application = tornado.web.Application([
    (r"/ws", WebsocketHandler, {'item_queue': item_queue, 'bid_dict': bid_dict}),
])
application.listen(8888)
tornado.ioloop.IOLoop.current().start()
