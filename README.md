## Disclaimer

Recently there are many people told me that buff is banning accounts that use this project.

So be careful and take your own risk to enjoy~

<p align="center">
  <b>Special thanks to the generous sponsorship by:</b>
  <br><br>
  <a target="_blank" href="https://www.jetbrains.com/?from=buff2steam">
    <img src="https://camo.githubusercontent.com/bf70170ad535c1272fa96b10a21325bb42d46a88/68747470733a2f2f692e6c6f6c692e6e65742f323031382f30332f32312f356162323233623735636466612e706e67" width=250 alt="logo">
  </a>
  <br><br>
</p>


# buff2steam

> Find item which cheaper than steamcommunity from buff

[简体中文](.github/README-zh-CN.md)

## Table of Contents

- [Introduction](#introduction)
- [requirements](#requirements)
- [usage](#usage)
- [config](#config)
  * [config.json](#configjson)
  * [buff_session](#buff_session)
- [StarChart](#starchart)
- [license](#license)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Introduction

buff2steam is a script, for crawling items from [buff](https://buff.163.com/) which cheaper than [steamcommunity](https://steamcommunity.com/market/).

![demo](https://user-images.githubusercontent.com/5501843/111403234-9ccaf680-8707-11eb-8f92-6d942e38acf4.png)

After set `threshold` in the `config.json` file, the script will automatically calculate the price difference and filter out matching items, as shown above.

 - `buff_id` means `goods_id` in url: https://buff.163.com/market/goods?goods_id=2334
 - `price` means this item's price on buff
 - `sell/want` means this item's sell/buy order count on steamcommunity market
 - `b_o_ratio` means the ratio obtained by selling this item to the highest buy order in the steamcommunity market **immediately** (after deducting the handling fee)
 - `ratio` means the  **possible** ratio obtained by selling this item with the lowest sell order price in the steamcommunity market (after deducting the handling fee)

The last two ratios are the ratio of the price difference. The lower the value, the better, and it means that you have obtained the discounted steam wallet balance through this transaction. 

Then you can buy items from buff manually and sell them to the steamcommunity.

## requirements

`python >= 3.7`

`pip install -r requirements.txt`

`cp config.sample.json config.json`

## usage

`python -m buff2steam`

## config

### config.json

```json5
{
    "main": {
        "game": "csgo",  // dota2
        "game_appid": "730",  // 570
        "accept_buff_threshold": 0.65,  // acceptable ratio
        "min_price": 500,  // CNY, 500 == 5 yuan
        "max_price": 30000  // CNY, 30000 == 300 yuan
    },
    "buff": {
        "requests_kwargs": {
            "headers": {
                "cookie": "session=1-GyCKVt_sSLoNtu2yeM9hY8FPeWTr8Q6ayOYIifqxKLM82044786689"
            }
        }
    },
    "steam": {
        "request_interval": 20,  // steam api request interval (in seconds)
        "requests_kwargs": {
            // if you dont need proxy then remove it
            "proxies": {
                "https": "http://127.0.0.1:7890"
            }
        }
    }
}
```

### buff_session

![session](https://user-images.githubusercontent.com/5501843/75434392-6ac7e480-598c-11ea-85d4-108ac2972cc1.png)

Chrome -> F12 -> Network Tab -> Refresh webpage -> Doc filter -> Response Headers
find `session` in `Set-Cookie` and paste it into `config.json -> buff.requests_kwargs.headers.cookie`

## StarChart

![starchart](https://starchart.cc/hldh214/buff2steam.svg)

## license

buff2steam is open-source software licensed under the Unlicense License. See the LICENSE file for more information.
