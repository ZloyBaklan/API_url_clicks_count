import requests
import os
from dotenv import load_dotenv
# from urllib.parse import urlparse


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


def check_bitlink(url, token):
    url_template = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    # parsed = urlparse(url)
    '''
    Получается абсолютно нет смысла пользоваться данной библиотекой,
    хотя в задании рекомендуют ее использовать,
    если нам надо опять делать запрос и просто проверять
    существует ли данный битлинк или он еще не создан...
    '''
    response = requests.get(url_template,  headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    url = input('Введите ссылку: ')
    try:
        check_bitlink(url, bitly_token) is True
        counter = count_clicks(bitly_token, url)
        print('Всего кликов по ссылке:', counter)
    except requests.exceptions.HTTPError:
        bitlink = cut_link(bitly_token, url)
        print('Битлинк:', bitlink)
