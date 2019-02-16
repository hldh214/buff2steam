import requests


class C5:
    # keyword=%E6%9C%88%E7%A5%9E%E9%A3%9E%E9%AA%91
    api_search = 'https://open.c5game.com/v1/store'

    def __init__(self):
        self.opener = requests.session()

    def query_price(self, name):
        res = self.opener.get(self.api_search, params={
            'keyword': name
        })

        data = res.json()['data']
        if data['total'] == 1:
            return data['list'][0]['orgi_price']

        for each in data['list']:
            if each['name'] == name:
                return each['orgi_price']
