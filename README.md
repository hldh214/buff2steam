<p align="center">
  <b>Special thanks to the generous sponsorship by:</b>
  <br><br>
  <a target="_blank" href="https://jb.gg/OpenSourceSupport">
    <img src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.svg" alt="logo">
  </a>
  <br><br>
</p>

# Buff2steam

Welcome to buff2steam, a Python script for finding items on buff that are cheaper than on Steam Community Market.
This readme provides an overview of the project and instructions on how to use it.

**Disclaimer**: Recently, some users have reported that their accounts were banned by Buff for using this project.
Please be careful and use at your own risk.

[简体中文](.github/README-zh-CN.md)

## Table of Contents

- [Introduction](#Introduction)
- [Requirements](#Requirements)
- [Usage](#Usage)
- [Configuration](#Configuration)
  * [config.json](#configjson)
  * [buff_session](#buff_session)
- [StarChart](#StarChart)
- [License](#License)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with
markdown-toc</a></i></small>

## Introduction

buff2steam is a script, for crawling items from [buff](https://buff.163.com/) which cheaper
than [steamcommunity](https://steamcommunity.com/market/).

With buff2steam, you can crawl items on [buff](https://buff.163.com/) and compare their prices to those
on [steamcommunity](https://steamcommunity.com/market/). After setting the `threshold` in the `config.json` file, the
script will automatically calculate the price difference and filter out matching items.

![demo](https://user-images.githubusercontent.com/5501843/111403234-9ccaf680-8707-11eb-8f92-6d942e38acf4.png)

The output includes:

- `buff_id`: `goods_id` in url: https://buff.163.com/market/goods?goods_id=2334
- `price`: item price on buff
- `sell/want`: item sell/buy order count on steamcommunity market
- `b_o_ratio`: ratio obtained by selling this item to the highest buy order in the steamcommunity market **immediately
  ** (transaction fee included)
- `ratio`: **possible** ratio obtained by selling this item with the lowest sell order price in the steamcommunity
  market (transaction fee included)

The last two ratios are the ratio of the price difference. The lower the value, the better, and it means that you have
obtained the discounted steam wallet balance through this transaction.

Then you can buy items from buff manually and sell them to the steamcommunity.

## Requirements

To use buff2steam, you need to have:

- `python >= 3.7`
- `pip install --user pipenv`
- `pipenv sync`
- `cp config.sample.json config.json`

## Usage

To run buff2steam, execute the following command in the terminal:

`python -m buff2steam`

## Configuration

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
    "request_interval": 4,  // buff api request interval (in seconds)
    "requests_kwargs": {
      "headers": {
        "cookie": "session=1-GyCKVt_sSLoNtu2yeM9hY8FPeWTr8Q6ayOYIifqxKLM82044786689"
      }
    }
  },
  "steam": {
    "request_interval": 20,  // steam api request interval (in seconds)
  }
}
```

### buff_session

![session](https://user-images.githubusercontent.com/5501843/75434392-6ac7e480-598c-11ea-85d4-108ac2972cc1.png)

To set the `buff_session` field in `config.json`, follow these steps:

- Open https://buff.163.com/market/ in Chrome
- Press `F12` to open the developer console
- Go to the `Network` tab and refresh the webpage
- Filter by `Doc` and find `session` in the `Set-Cookie` field under `Response Headers`
- Copy the value of `session` and paste it into `config.json` -> `buff.requests_kwargs.headers.cookie`

## StarChart

![starchart](https://starchart.cc/hldh214/buff2steam.svg)

## License

buff2steam is open-source software licensed under the Unlicense License. See the LICENSE file for more information.
