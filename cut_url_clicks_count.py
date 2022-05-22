import argparse
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


def count_clicks(token, parsed_bitlink):
    url_template = 'https://api-ssl.bitly.com/v4/bitlinks/' \
                   f'{parsed_bitlink}/clicks/summary'
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
    response = requests.get(url_template,  headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description='Программа сокращения ссылок')
    parser.add_argument('link', help='Введите вашу ссылку')
    args = parser.parse_args()
    parsed = urlparse(args.link)
    parsed_url = parsed.netloc + parsed.path
    try:
        if check_bitlink(parsed_url, bitly_token):
            counter = count_clicks(bitly_token, parsed_url)
            print('Всего кликов по ссылке:', counter)   
        else:
            bitlink = cut_link(bitly_token, args.link)
            print('Битлинк:', bitlink)

    except requests.exceptions.HTTPError:
        print('Ошибка ответа страницы.')
