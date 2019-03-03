# buff2steam

> 其實世界上根本就沒有代购, 也可以說人人都是代购, 不管大妹小妹叔叔阿姨, 只要有心, 人人都可以是代购

![head_image](https://user-images.githubusercontent.com/5501843/53693505-5c2c0900-3ddc-11e9-84c8-67e37e04798d.png)

## 目录

- [简介](#简介)
- [先决条件](#先决条件)
- [依赖](#依赖)
- [配置](#配置)
  * [获取 buff session](#获取-buff-session)
- [使用方法](#使用方法)
- [License](#license)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## 简介

buff2steam 是一个爬虫脚本, 用于爬取 [网易buff](https://buff.163.com/) 上售价低于 [steam 社区市场](https://steamcommunity.com/market/) 上的饰品

设置差价阈值后, 脚本会自动计算差价并筛选出符合的饰品, 如上图

 - id 表示此物品 https://buff.163.com/market/goods?goods_id=2334 里面的 goods_id
 - s_cnt 表示此物品在 steam 社区市场上的出售单数量
 - w_cnt 表示此物品在 steam 社区市场上的订购单数量
 - volume 表示此物品在 steam 社区市场上 24h 内的销量
 - buff_price 表示此物品在 buff 上的最低售价
 - b_o_ratio 表示此物品在 steam 社区市场**立即**出售给最高出价的订购单所获得的余额折扣(扣除手续费后)
 - ratio 表示此物品在 steam 社区市场竞价出售**可能**获得的最低余额折扣(扣除手续费后)

最后面这两个 ratio 就是上述的差价阈值, 这个值越低越好, 越低表示你通过这笔交易获得了这个折扣的 steam 钱包余额

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

### 复制 config.sample.json 为 config.json: `cp config.sample.json config.json`, 以下配置均在 config.json 中进行

### 获取 buff session

![session](https://camo.githubusercontent.com/89f04601687e404b342402eb59ac97b148a91bb8/68747470733a2f2f7773332e73696e61696d672e636e2f6c617267652f30303542597170676c793167303036717933356e616a3331367a3070743432742e6a7067)
如图: Chrome 浏览器 -> F12 -> Network选项卡 -> 刷新网页 -> Doc筛选 -> Response Headers 部分
蓝色框框里面就是我们需要的session

```python
# [必填]填你的 buff 网页 session
buff_session = 'session=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# [必填]代理 ip, 如果使用 SS Windows 客户端并且是默认配置, 则此项可保持默认, 若不需要代理则可去掉
proxies = {
    'https': 'http://127.0.0.1:1080'
}

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
