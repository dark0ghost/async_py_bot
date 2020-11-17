# async_py_bot
[![GitHub watchers](https://img.shields.io/github/watchers/dark0ghost/async_py_bot?style=social&label=Watch&maxAge=2592000)](https://github.com/dark0ghost/async_py_bot/watchers/)
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
# funtions bot:

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

# dependencies
|name|version |
| ------------- | ------------- |
|Python |3.7|
|docker| 19.03.12|
|docker-compose| 1.21.0|
|GCC|9|
|aiogram| 2.5|
|uvloop|0.13.0|
|beautifulsoup4|4.8.0|
|aiofiles|0.4.0|
|aiosmtplib|1.1.0|
|faces|0.1|

# about
```
this repository shows how you can work with aviogram v2, but remember using global variables will lead to UB
```
__project frozen__
