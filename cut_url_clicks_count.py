import requests
import re
from urllib.parse import urlparse

from settings import SECRET_TOKEN


def cutting_link(token, url):
    url_template = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'long_url': url,
    }
    response = requests.post(url_template, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["id"]


def counting_clicks(token, bitlink):
    url_template = 'https://api-ssl.bitly.com/v4/bitlinks/' \
                   f'{bitlink}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        'units': '-1'
    }
    response = requests.get(url_template, params, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def check_bitlink(url):
    parsed = urlparse(url)
    if parsed.netloc != 'bit.ly':
        return True
    return False


if __name__ == '__main__':
    token = SECRET_TOKEN
    url = input('Введите ссылку: ')
    checked_url = check_bitlink(url)
    if checked_url is True:
        bitlink = cutting_link(token, url)
    else:
        bitlink = re.sub(r'(https|http)?:\/\/', '', url)
    try:
        print('Битлинк:', bitlink)
    except requests.exceptions.HTTPError as url_error:
        print('Ошибка ссылки:', url_error)
    counter = counting_clicks(token, bitlink)
    try:
        print('Всего кликов по ссылке:', counter)
    except requests.exceptions.HTTPError as count_error:
        print('Ошибка подсчета кликов:', count_error)
