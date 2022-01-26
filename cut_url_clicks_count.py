import requests
import re
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def cut_link(token, url):
    url_template = 'https://api-ssl.bitly.com/v4/bitlinks/'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'long_url': url,
    }
    response = requests.post(url_template, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(token, bitlink):
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
    return parsed.netloc != 'bit.ly'


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    url = input('Введите ссылку: ')
    try:
        check_bitlink(url) is True
        bitlink = cut_link(bitly_token, url)
    except requests.exceptions.HTTPError:
        bitlink = re.sub(r'(https|http)?:\/\/', '', url)
    print('Битлинк:', bitlink)
    try:
        counter = count_clicks(bitly_token, bitlink)
    except requests.exceptions.HTTPError:
        counter = 'Ошибка подсчета кликов!'
    print('Всего кликов по ссылке:', counter)
