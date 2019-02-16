from buff2steam import *


class C5:
    # keyword=%E6%9C%88%E7%A5%9E%E9%A3%9E%E9%AA%91
    api_search = 'https://open.c5game.com/v1/store'

    def __init__(self):
        self.opener = requests.session()

    def query_by_name(self, name):
        """
        :param name: str
        :return: dict
        {
            "id": 553453542,
            "item_id": 553468308,
            "appid": 570,
            "appid_icon": "http://c5game.oss-cn-shanghai.aliyuncs.com/app/game/icon/dota2@3x.png@40w.png",
            "num": 58,
            "type": "wearable",
            "update_time": 1550307961,
            "product_type": "S",
            "price": 435,
            "deal": 10203,
            "currency": "￥",
            "name": "月神飞骑",
            "image_url": "https://i.c5game.com/economy/570/2018/08/26/e8e300d988cf79291cb14f30e112a6a6.png",
            "orgi_price": 43500,
            "quality": "unique",
            "rarity": "immortal",
            "quality_name": "标准",
            "rarity_name": "不朽",
            "rarity_color": "#e4ae39",
            "classid": "0",
            "instanceid": 0,
            "tag": "不朽"
        }
        """
        res = self.opener.get(self.api_search, params={
            'keyword': name
        }).json()

        if 'data' not in res:
            return None

        data = res['data']
        if data['total'] == 1:
            return data['list'][0]

        for each in data['list']:
            if each['name'] == name:
                return each
