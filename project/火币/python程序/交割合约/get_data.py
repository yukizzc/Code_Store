#!/usr/bin/env python
import time
import datetime
import uuid
import urllib
import asyncio
import websockets
import json
import hmac
import base64
import hashlib
import gzip
import traceback
import configparser
import mysql.connector


def case1():  # 1分钟
    return 0


def case2():  # 5分钟
    return 1


def case3():  # 日线
    return 5


def default():  # 日线
    return 5


switch = {'1min': case1,
          '5min': case2,
          '1day': case3
          }


def generate_signature(host, method, params, request_path, secret_key):
    """Generate signature of huobi future.

    Args:
        host: api domain url.PS: colo user should set this host as 'api.hbdm.com',not colo domain.
        method: request method.
        params: request params.
        request_path: "/notification"
        secret_key: api secret_key
    Returns:
        singature string.
    """
    host_url = urllib.parse.urlparse(host).hostname.lower()
    sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = "\n".join(payload)
    payload = payload.encode(encoding="UTF8")
    secret_key = secret_key.encode(encoding="utf8")
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature


async def subscribe(url, access_key, secret_key, subs, callback=None, auth=False):
    """ Huobi Future subscribe websockets.
    Args:
        url: the url to be signatured.
        access_key: API access_key.
        secret_key: API secret_key.
        subs: the data list to subscribe.
        callback: the callback function to handle the ws data received.
        auth: True: Need to be signatured. False: No need to be signatured.
    """
    async with websockets.connect(url) as websocket:
        if auth:
            timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            data = {
                "AccessKeyId": access_key,
                "SignatureMethod": "HmacSHA256",
                "SignatureVersion": "2",
                "Timestamp": timestamp
            }
            sign = generate_signature(url, "GET", data, "/notification", secret_key)
            data["op"] = "auth"
            data["type"] = "api"
            data["Signature"] = sign
            msg_str = json.dumps(data)
            await websocket.send(msg_str)
            print(f"send: {msg_str}")
        for sub in subs:
            sub_str = json.dumps(sub)
            await websocket.send(sub_str)
            print(f"send: {sub_str}")
        while True:
            rsp = await websocket.recv()
            data = json.loads(gzip.decompress(rsp).decode())
            # print(f"recevie<--: {data}")
            if "op" in data and data.get("op") == "ping":
                pong_msg = {"op": "pong", "ts": data.get("ts")}
                await websocket.send(json.dumps(pong_msg))
                print(f"send: {pong_msg}")
                continue
            if "ping" in data:
                pong_msg = {"pong": data.get("ping")}
                await websocket.send(json.dumps(pong_msg))
                print(f"send: {pong_msg}")
                continue
            rsp = await callback(data)


async def handle_ws_data(*args, **kwargs):
    """ callback function
    Args:
        args: values
        kwargs: key-values.
    """
    time.sleep(1)
    # print("callback param", *args,**kwargs)
    ######################################################################################################################
    # 时间转换成字符串
    time_to_str = lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x))
    # 判断有行情更新
    if 1 and 'tick' in args[0].keys():
        k_time_orgin = args[0]['tick']['id']
        k_time = k_time_orgin
        k_open = args[0]['tick']['open']
        k_high = args[0]['tick']['high']
        k_low = args[0]['tick']['low']
        k_close = args[0]['tick']['close']
        k_vol = args[0]['tick']['vol']
        k_amount = args[0]['tick']['amount']
        code = args[0]['ch'].split('.')[1]
        typee = args[0]['ch'].split('.')[-1]
        choice = typee
        typee_vb = switch.get(choice, default)()

        # 插入数据
        if code == 'BTC_CW' and typee == '1min':
            print(k_time,typee,code,k_open,k_high,k_low,k_close,'成交量', k_vol, '成交额', k_amount)
        update_data(k_time, code, k_open, k_high, k_low, k_close, k_vol, k_amount, typee)


def insert_data(k_time, code, k_open, k_high, k_low, k_close, k_vol, k_amount, typee):
    temp = ' (date,code,open,high,low,close,vol,amount) values(%s,%s,%s,%s,%s,%s,%s,%s)'
    sql = 'insert into ' + code + '_' + typee + temp
    val = (k_time, code, k_open, k_high, k_low, k_close, k_vol, k_amount)
    cursor.execute(sql, val)
    coon.commit()


def update_data(k_time, code, k_open, k_high, k_low, k_close, k_vol, k_amount, typee):
    temp = " SET date={},code=\'{}\',open={},high={},low={},close={},vol=" \
           "{},amount={}".format(k_time,code,k_open,k_high,k_low,k_close,k_vol,k_amount)
    sql = "UPDATE " + code + '_' + typee + temp
    cursor.execute(sql)
    coon.commit()


def sub(url, subs):
    ####  input your access_key and secret_key below:
    access_key = ""
    secret_key = ""

    market_url = url
    order_url = 'wss://api.hbdm.vn/notification'

    market_subs = subs
    order_subs = [
        {
            "op": "sub",
            "cid": str(uuid.uuid1()),
            "topic": "orders.EOS"
        },
        {
            "op": "sub",
            "cid": str(uuid.uuid1()),
            "topic": "positions.EOS"
        },
        {
            "op": "sub",
            "cid": str(uuid.uuid1()),
            "topic": "accounts.EOS"
        }

    ]

    while True:
        try:
            asyncio.get_event_loop().run_until_complete(
                subscribe(market_url, access_key, secret_key, market_subs, handle_ws_data, auth=False))
            # asyncio.get_event_loop().run_until_complete(subscribe(order_url, access_key,  secret_key, order_subs, handle_ws_data, auth=True))
        # except (websockets.exceptions.ConnectionClosed):
        except Exception as e:
            traceback.print_exc()
            print('websocket connection error. reconnect rightnow')


url = 'wss://api.btcgateway.pro/ws'

if __name__ == "__main__":
    li = []
    code_ = ['BTC', 'ETH', 'LINK', 'DOT']
    code_ = ['BTC']
    date_ = ['_CW', '_NW', '_CQ', '_NQ']
    # date_ = ['_CQ']
    type_ = ['1min', '5min', '1day']
    # type_ = ['1min']
    for i in code_:
        for j in date_:
            for k in type_:
                dic = {"sub": "market." + i + j + ".kline." + k, "id": str(uuid.uuid1())}
                li.append(dic)
    url_market_subs = li

    coon = mysql.connector.connect(host='localhost', user='root', passwd='', database='交割合约')
    cursor = coon.cursor()
    sub(url, url_market_subs)