
from buff2steam import logger

class _Item():
    def __init__(self,app_id, market_hash_name, steam_price, buff_id, buff_price, volume, ratio) -> None:
        self.app_id = app_id
        self.steam_link = f'https://steamcommunity.com/market/listings/{app_id}/{market_hash_name}'
        self.market_hash_name = market_hash_name
        self.steam_price = steam_price
        self.buff_link = f'https://buff.163.com/goods/{buff_id}'
        self.buff_price = buff_price
        self.volume = volume
        self.ratio = ratio

class Items():
    def __init__(self) -> None:
        self.list :list[_Item] = []
        self._current_item :_Item = None
        self._steam_increasing :list[_Item]= []
        self._steam_decreasing :list[_Item]= []
        self._buff_increasing :list[_Item]= []
        self._buff_decreasing :list[_Item]= []
        self._ratio_increasing :list[_Item]= []
        self._ratio_decreasing :list[_Item]= []
        self._volume_increasing :list[_Item] = []
        self._volume_decreasing :list[_Item] = []
    
    def add_item(self, app_id, market_hash_name, steam_price, buff_id, buff_price, volume, ratio) -> None:
        if self._check_name_exists(market_hash_name):
            self._current_item.steam_price = steam_price
            self._current_item.buff_price = buff_price
            self._current_item.volume = volume
            self._current_item.ratio = ratio
            logger.debug(f'Updated {market_hash_name} in database list')
            self._wipe_chached_lists()
            return
        new_item = _Item(app_id, market_hash_name, steam_price, buff_id, buff_price, volume, ratio)
        self.list.append(new_item)
        logger.debug(f'Added {market_hash_name} to database list')
        self._wipe_chached_lists()
        return

##Soring data

    def get_steam_increasing(self) -> "list[_Item]":
        if bool(self._steam_increasing):
            return self._steam_increasing
        self._steam_increasing = sorted(self.list, key=lambda item: item.steam_price)
        return self._steam_increasing
    
    def get_steam_decreasing(self) -> "list[_Item]":
        if bool(self._steam_decreasing):
            return self._steam_decreasing
        self._steam_decreasing = self.get_steam_increasing()[::-1]
        return self._steam_decreasing

    def get_buff_increasing(self) -> "list[_Item]":
        if bool(self._buff_increasing):
            return self._buff_increasing
        self._buff_increasing = sorted(self.list, key= lambda item: item.buff_price)
        return self._buff_increasing
    
    def get_buff_decreasing(self) -> "list[_Item]":
        if bool(self._buff_decreasing):
            return self._buff_decreasing
        self._buff_decreasing = self.get_buff_increasing()[::-1]
        return self._buff_decreasing
    
    def get_volume_increasing(self) -> "list[_Item]":
        if bool(self._volume_increasing):
            return self._volume_increasing
        self._volume_increasing = sorted(self.list, key= lambda item: item.volume)
        return self._volume_decreasing
    
    def get_volume_decreasing(self) -> "list[_Item]":
        if bool(self._volume_decreasing):
            return self._volume_decreasing
        self._volume_decreasing = self.get_volume_increasing()[::-1]
        return self._volume_decreasing

    def get_ratio_increasing(self) -> "list[_Item]":
        if bool(self._ratio_increasing):
            return self._ratio_increasing
        self._ratio_increasing = sorted(self.list, key= lambda item: item.ratio)
        return self._ratio_increasing
    
    def get_ratio_decreasing(self) -> "list[_Item]":
        if bool(self._ratio_decreasing):
            return self._ratio_decreasing
        self._ratio_decreasing = self.get_ratio_increasing()[::-1]
        return self._ratio_decreasing

##Done sorting data

    def _check_name_exists(self, market_hash_name):
        for item in self.list:
            if market_hash_name == item.market_hash_name:
                self._current_item = item
                return True
        self._current_item = None
        return False

    def _wipe_chached_lists(self):
        logger.debug(f'Clearing out chached lists')
        self._steam_increasing = []
        self._steam_decreasing = []
        self._buff_increasing = []
        self._buff_decreasing = []
        self._ratio_increasing = []
        self._ratio_decreasing = []
        self._volume_increasing = []
        self._volume_decreasing = []

items = Items()