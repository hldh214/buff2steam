# buff2steam

## 目录

- [简介](#简介)
- [先决条件](#先决条件)
- [依赖](#依赖)
- [配置](#配置)
  * [config](#config)
  * [获取 buff session](#获取-buff-session)
- [使用方法](#使用方法)
- [license](#license)

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
# python 版本需要 >= 3.7
pip install -r requirements.txt
```

## 配置

### config

复制 config.sample.json 为 config.json: 

`cp config.sample.json config.json`

以下配置均在 config.json 中进行

```json5
{
    "main": {
        "game": "csgo",  // dota2
        "game_appid": "730",  // 570
        "accept_buff_threshold": 0.65,  // buff 上面展示的`参考价格`和其实际在售最低价所计算出来的比例
        "min_price": 500,  // 单位为分, 500 == 5 元
        "max_price": 30000  // 单位为分, 30000 == 300 元
    },
    "buff": {
        "requests_kwargs": {
            "headers": {
                "cookie": "session=1-GyCKVt_sSLoNtu2yeM9hY8FPeWTr8Q6ayOYIifqxKLM82044786689"
            }
        }
    },
    "steam": {
        "request_interval": 20,  // steam api 请求间隔, 单位为秒
        "requests_kwargs": {
            // 代理设置, 若不需要则可去除
            "proxies": {
                "https": "http://127.0.0.1:7890"
            }
        }
    }
}
```

### 获取 buff session

![session](https://user-images.githubusercontent.com/5501843/75434392-6ac7e480-598c-11ea-85d4-108ac2972cc1.png)

如图: Chrome 浏览器 -> F12 -> Network选项卡 -> 刷新网页 -> Doc筛选 -> Response Headers 部分
蓝色框框里面就是我们需要的session

## 使用方法

```
python -m buff2steam
```

## license

buff2steam is open-source software licensed under the Unlicense License. See the LICENSE file for more information.
