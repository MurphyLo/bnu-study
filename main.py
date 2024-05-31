import json
import re
import sys
import time
import warnings
import execjs
import requests
from datetime import datetime, timedelta
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from des import *

warnings.filterwarnings('ignore', category=InsecureRequestWarning)


def login(u, p):
    session = requests.session()
    session.headers.update({'User-Agent': 'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'})
    url = 'http://cas.bnu.edu.cn/cas/login'
    res = session.get(url)

    lt = re.search('name="lt" value="(.+)"', res.text).group(1)
    execution = re.search('name="execution" value="(.+?)"', res.text).group(1)
    payload = {
        'rsa': func_des.call("strEnc", u + p + lt, '1', '2', '3'),
        'ul': len(u),
        'pl': len(p),
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit'
    }
    session.post(res.url, data=payload)
    session.get('https://seat.lib.bnu.edu.cn/', verify=False)
    session.get('http://cas.bnu.edu.cn/cas/login', params={'service': 'http://seat.lib.bnu.edu.cn/cas'})
    return session


def self_res(seat_id, start, end, today=False):
    url = 'http://seat.lib.bnu.edu.cn/selfRes'
    date = datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d') if not today else datetime.strftime(datetime.now(), '%Y-%m-%d')
    payload = {
        'SYNCHRONIZER_TOKEN': _map(),
        'SYNCHRONIZER_URI': '/map',
        'date': date,
        'seat': seat_id,
        'start': start * 60,
        'end': end * 60,
        'authid': '-1'
    }
    res = session.post(url, data=payload)
    return res


def _map():
    url = 'http://seat.lib.bnu.edu.cn/map'
    resp = session.get(url)
    synchronizer_token = re.search('name="SYNCHRONIZER_TOKEN" value="(.+?)"', resp.text).group(1)
    return synchronizer_token


def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        config = json.loads(f.read())
    return config


if __name__ == '__main__':
    
    u = '20yydddddxxx'
    p = 'enjoyoureverie'

    start = 9
    end = 21

    func_des = execjs.compile(open('./des.js', 'r').read())
    session = login(u, p)

    t = datetime.strptime(time.strftime('%Y-%m-%d' + ' 19:30:00'), '%Y-%m-%d %H:%M:%S')
    u_mark = time.mktime(t.timetuple())

    while True:
        if time.time() > u_mark:
            time.sleep(0.200)
            resp = self_res(54850, start, end)
            soup = BeautifulSoup(resp.content, 'lxml')
            info = soup.find('div', attrs={'class': 'layoutSeat'}).get_text(separator='\n', strip=True)
            print(info)
            break
        else:
            time.sleep(0.200)
