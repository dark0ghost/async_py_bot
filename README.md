# async_py_bot
[![GitHub watchers](https://img.shields.io/github/watchers/dark0ghost/async_py_bot?style=social&label=Watch&maxAge=2592000)](https://github.com/dark0ghost/async_py_bot/watchers/)
[![GitHub issues](https://img.shields.io/github/issues/dark0ghost/async_py_bot)](https://github.com/dark0ghost/async_py_bot/issues)
[![GitHub release](https://img.shields.io/github/release/dark0ghost/async_py_bot)](https://github.com/dark0ghost/async_py_bot/releases/)
[![Github all releases](https://img.shields.io/github/downloads/dark0ghost/async_py_bot/total.svg)](https://github.com/dark0ghost/async_py_bot/releases/)
[![GitHub code size](https://img.shields.io/github/languages/code-size/dark0ghost/async_py_bot?style=flat)](https://github.com/dark0ghost/async_py_bot)

# start with docker-compose:
```bash
cd async_py_bot
docker-compose up
```
# bash up: 
linux:
```bash 
python3 async_py_bot/start_poling.py
```
windows:
```bash
python async_py_bot/start_poling.py
```
### Functions bot:

# 1 start
```
/start ->
hello text
```
# 2 re 
```
/re ->
deleted keyboard
```

# 3 log
```text
/log -> send log_base.log
```
# 4 by
```text
/by -> send by obj 
```
# 5 cat
```text
/cat -> send cat file .png or .jpg or .gif
```
# 6 json
```text
/json -> send link on cloud json or sate state and wait u json
```
### About EVN
|name|description|
| ------------- | ------------- |
|STATS_DB|The name of the database in which the metric will be stored|
|STATS_HOST|Database address|
|STATS_USER|The user who will interact with the database|
|STATS_PASS|Password from **STATS_USER**|
|TOKEN|Bot token|
|PAYMENTS_PROVIDER_TOKEN|Token for payments system in bot |
|TOKEN_QIWI| Token from Qiwi |
|POSTGRES|link for postgres; example: postgress://user:password@localhost:port|
|virustotal|Token from virustotal.com|
|etcherscan|Token from etcherscan.io|
|pastebin|Token from pastebin.com|
|cat_api|Token from thecatapi.com|
|MASTER|id admin user|

### Dependencies
|name|version |
| ------------- | ------------- |
|Python |3.7 (support 3.9)|
|docker| 19.03.12|
|docker-compose| 1.21.0|
|GCC|9 (support 10)|
|aiofiles|0.6.0|
|aiogram|2.11.2|
|aiohttp|3.7.3|
|aiohttp-socks|0.5.5|
|aioinflux|0.9.0|
|aioredis|1.3.1|
|aiosmtplib|1.1.4|
|aiosocksy|0.1.2|
|gino|1.0.1|
|ujson|4.0.2|


# About
```
This repository shows how you can work with aviogram v2
```
__project frozen__
