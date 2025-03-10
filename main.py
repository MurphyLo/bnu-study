import hmac
import hashlib
import json
import re
import sys
import time
import uuid
import warnings
from datetime import datetime, timedelta
from pprint import pprint
from urllib.parse import urlparse, parse_qs
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings('ignore', category=InsecureRequestWarning)

import requests
from des import strEnc


def login(u, p, redirect_url=None):
    """cas通用登录"""
    session = requests.session()
    session.headers.update({'User-Agent': 'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'})
    url = 'http://cas.bnu.edu.cn/cas/login'
    res = session.get(url, params={'service': redirect_url} if redirect_url else None)


    lt = re.search('name="lt" value="(.+)"', res.text).group(1)
    execution = re.search('name="execution" value="(.+?)"', res.text).group(1)
    payload = {
        'rsa': strEnc(u + p + lt, '1', '2', '3'),
        'ul': len(u),
        'pl': len(p),
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit'
    }
    session.post(res.url, data=payload)
    return session


def get_token(session):
    """两阶段获取jwt_token/token：10分钟同时超时"""
    rem_sso_url = 'https://libseat.bnu.edu.cn/rem/static/sso/login'
    # 多次自动重定向后拿到 jwt_token
    jsq_v_resp = session.get(rem_sso_url, params={'redirectUrl': 'https://libseat.bnu.edu.cn/jsq-v'})
    parsed_url = urlparse(jsq_v_resp.url)
    jwt_token = parse_qs(parsed_url.query)['token'][0]

    libseat_url = 'https://libseat.bnu.edu.cn/jsq/static/public/auth/cas/' + jwt_token
    payload = {
        'token': jwt_token + '#/',
        'loginType': 'PC'
    }
    libseat_resp = session.post(libseat_url, data=payload)
    token = libseat_resp.json()['data']['token']

    return token


def get_hmac_header():
    """获取hmac头：所有非登录的功能接口通用"""
    request_date = str(int(time.time() * 1000))
    request_id = str(uuid.uuid4())
    hmac_key = "bnu2024Lib"
    message = "seat::{}::{}::POST".format(request_id, request_date)

    hmac_request_key = hmac.new(
        key=bytes(hmac_key, 'utf-8'),
        msg=bytes(message, 'utf-8'),
        digestmod=hashlib.sha256
        ).hexdigest()

    return {
        "X-request-id": request_id,
        "X-request-date": request_date,
        "X-hmac-request-key": hmac_request_key
    }


def free_book(seat_id: str, start: int, end: int, today=False):
    """功能接口：预约座位"""
    date = datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d') if not today else datetime.strftime(datetime.now(), '%Y-%m-%d')
    free_book_url = f'https://libseat.bnu.edu.cn/jsq/static/frontApi/make/freeBook/{seat_id}/{date}/{start*60}/{end*60}?capToken=capToken'
    session.headers.update(get_hmac_header())
    session.headers.update({'token': token})

    payload = {}
    free_book_res = session.post(free_book_url, json=payload)
    
    return free_book_res.json()


if __name__ == '__main__':

    u = '20yydddddxxx'
    p = 'enjoyoureverie'

    seat_id: str = '188xxxxxxxxxxxxxxxx'
    start:   int = 9
    end:     int = 22

    redirect_url = 'http://seat.lib.bnu.edu.cn/'

    session = login(u, p, redirect_url)
    token = get_token(session)  # 注意 10 分钟超时

    t = datetime.strptime(time.strftime('%Y-%m-%d' + ' 19:30:00'), '%Y-%m-%d %H:%M:%S')
    u_mark = time.mktime(t.timetuple())

    while True:
        if time.time() > u_mark:
            time.sleep(0.200)
            resp = free_book(seat_id, start, end)
            pprint(resp.json())
            break
        else:
            time.sleep(0.200)