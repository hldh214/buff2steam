from buff2steam import *


class Buff(BaseProvider):
    web_withdraw = 'https://buff.163.com/api/market/backpack/withdraw'
    web_backpack = 'https://buff.163.com/api/market/backpack'

    def withdraw(self, backpack_ids: typing.List[str] = None, game: str = 'dota2') -> bool:
        if not backpack_ids:
            backpack_ids = []

            res = self.opener.get(self.web_backpack, params={
                'game': game
            }).json()

            if res['data']['backpack_count'] == 0:
                return False

            for each_item in res['data']['items']:
                backpack_ids.append(each_item['id'])

        self.opener.post(self.web_withdraw, json={
            "game": game,
            "backpack_ids": backpack_ids
        })

        return True
