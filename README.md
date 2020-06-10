<p align="center">
  <b>Special thanks to the generous sponsorship by:</b>
  <br><br>
  <a target="_blank" href="https://www.jetbrains.com/?from=buff2steam">
    <img src="https://camo.githubusercontent.com/bf70170ad535c1272fa96b10a21325bb42d46a88/68747470733a2f2f692e6c6f6c692e6e65742f323031382f30332f32312f356162323233623735636466612e706e67" width=250 alt="logo">
  </a>
  <br><br>
</p>

# buff2steam

> make money from buff.163.com

[简体中文](.github/README-zh-CN.md)

## Table of Contents

- [requirements](#requirements)
- [usage](#usage)
- [config](#config)
- [license](#license)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## requirements

`python >= 3.7`

`pip install -r requirements.txt`

`cp config.sample.json config.json`

## usage

`python -m buff2steam`

## config

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

## StarChart

![starchart](https://starchart.cc/hldh214/buff2steam.svg)

## license

buff2steam is open-source software licensed under the Unlicense License. See the LICENSE file for more information.
