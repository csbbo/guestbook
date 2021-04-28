# aiohttp server framework

requirment
- Python 3.8
- mongodb
- pip3 install -r requirements.txt

run server
```shell script
python3 main.py
```

run test
```shell script
# test all
python3 test.py

# test module
python3 test.py modulename

# test method
python3 test.py modulename.methodname
```

> `python3 test.py`程序会fork一个子进程来运行一个临时server, 临时server监听端口为server(默认端口+1),创建一个临时数据库(server默认数据库+_default)
