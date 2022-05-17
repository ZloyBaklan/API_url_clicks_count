import requests
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
    return response.json()["link"]


def count_clicks(token, bitlink):
    parsed = urlparse(bitlink)
    parsed_summary = parsed.netloc + parsed.path
    url_template = 'https://api-ssl.bitly.com/v4/bitlinks/' \
                   f'{parsed_summary}/clicks/summary'
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
    parsed = urlparse(url)
    parsed_url = parsed.netloc + parsed.path
    url_template = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url_template,  headers=headers)
    if response.status_code == 200:
        counter = count_clicks(bitly_token, parsed_url)
        print('Всего кликов по ссылке:', counter)
    else:
        bitlink = cut_link(token, url)
        print('Битлинк:', bitlink)



if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    url = input('Введите ссылку: ')
    check_bitlink(url, bitly_token)
