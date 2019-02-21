from buff2steam import *


class C5(BaseProvider):
    # keyword=%E6%9C%88%E7%A5%9E%E9%A3%9E%E9%AA%91
    api_search = 'https://open.c5game.com/v1/store'

    def query_by_name(self, name: str) -> typing.Union[dict, bool]:
        res = self.opener.get(self.api_search, params={
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
