from email import header
import requests

proxy = '127.0.0.1:10808'
proxies = {
    'http': 'socks5://' + proxy,
    'https': 'socks5://' + proxy,
}

try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)