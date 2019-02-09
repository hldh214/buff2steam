# buff2steam

> 其實世界上根本就沒有代购, 也可以說人人都是代购, 不管大妹小妹叔叔阿姨, 只要有心, 人人都可以是代购

![head_image](https://camo.githubusercontent.com/3975b56885321eeafd5e0b8ab6ecde3a803e397c/687474703a2f2f696d677372632e62616964752e636f6d2f666f72756d2f7069632f6974656d2f316533633236663430616431363264396635616663656330316364666139656338623133636435392e6a7067)

## 简介

buff2steam 是一个爬虫脚本, 用于爬取 [网易buff](https://buff.163.com/) 上售价低于 [steam 社区市场](https://steamcommunity.com/market/) 上的饰品
设置差价阈值后, 脚本会自动计算差价并筛选出符合的饰品
手动从 buff 购入并上架到 steam 出售从而赚取 steam 钱包余额

## 先决条件

 - 使用本脚本前**必须**了解科学上网相关知识
 - [Python3 + pip](https://www.python.org/) 环境
 - DIY 能力, 因为脚本的配置是因人而异的

## 依赖

```
pip install -r requirements.txt
```

## 配置

```python
# [必填]填你的 buff 网页 session
buff_session = 'session=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# [可保持默认]buff id 黑名单
buff_id_blacklist = (3986,)

# [可保持默认]buff type 黑名单
buff_type_blacklist = ('tool',)

# [可保持默认]游戏名, 目前仅支持 DotA2
game = 'dota2'

# [可保持默认]游戏 appid, 目前仅支持 DotA2
game_appid = '570'

# [可保持默认]货币 id(23 => CNY)
currency = 23  # CNY

# [可保持默认]buff 上显示的 steam 价格(可能不准确, 设置较低的值比较好)阈值
accept_buff_threshold = Decimal(0.6)

# [可保持默认]立即出售阈值
highest_buy_order_ratio_threshold = Decimal(0.75)

# [可保持默认]buff饰品价格最小与最大值区间(CNY * 100)
min_price = 1000
max_price = 30000

# [可保持默认]steam api 请求间隔, ,秒为单位, 太长降低脚本效率, 太短会被 steam 封 ip
steam_api_sleep = 30
```

## 使用方法

```
python3 main.py
```

## License

buff2steam is open-source software licensed under the Unlicense License. See the LICENSE file for more information.
