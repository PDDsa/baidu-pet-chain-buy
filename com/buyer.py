import requests, threading, time, json

requests.packages.urllib3.disable_warnings()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
refer = 'https://pet-chain.baidu.com/'
Cookie = 'BAIDUID=02214A476E69A3DFB03495F679809152:FG=1; BIDUPSID=02214A476E69A3DFB03495F679809152; PSTM=1498184316; BDUSS=3ZoVnlrMUNGczFuU09tNTQ4MTF6SU9QakoxbG93Y29BfnJ0QmNvMnhybVhZWlZaSVFBQUFBJCQAAAAAAAAAAAEAAADv3f4vwre5~dK7xqy438G7tdgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJfUbVmX1G1ZN'  # 换成你自己的Cookie
headers = {'Cookie': Cookie, 'Referer': refer, 'User-Agent': UA, 'accept': 'application/json',
           'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'content-type': 'application/json'}


def get_all_pets():
    data = {}
    param = json.loads(
        '{"pageNo":1,"pageSize":50,"querySortType":"AMOUNT_ASC","petIds":[],"lastAmount":null,"lastRareDegree":null,"requestId":123,"appId":1,"tpl":""}')
    param['requestId'] = int(time.time() * 1000)
    url = 'https://pet-chain.baidu.com/data/market/queryPetsOnSale'
    try:
        r = requests.post(url, data=json.dumps(param), headers=headers, verify=False)
        pets = r.json()['data']['petsOnSale']
        for pet in pets:
            data[pet['petId']] = float(pet['amount'])
    except Exception:
        pass
    return data


def buy_pet(petId):
    param = json.loads('{"petId": "007", "requestId": 1517726374504, "appId": 1, "tpl": ""}')
    param['petId'] = petId
    param['requestId'] = int(time.time() * 1000)
    url = 'https://pet-chain.baidu.com/data/txn/create'
    r = requests.post(url, data=json.dumps(param), headers=headers, verify=False)
    return r.json()


def buy_all_pets(max_price):
    while True:
        data = get_all_pets()
        for petId in [id for id in data if data[id] <= 800]:
            try:
                msg = buy_pet(petId)['errorMsg']
                print('{0} ----> {1} : {2}'.format(petId, data[petId], msg))
            except Exception as err:
                pass


if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=buy_all_pets, args=(10,))
        t.start()
