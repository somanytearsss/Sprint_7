import string
import random

import requests

base_url = 'https://qa-scooter.praktikum-services.ru'
url_create_courier = f'{base_url}/api/v1/courier'
url_courier_login = f'{base_url}/api/v1/courier/login'
url_create_order = f'{base_url}/api/v1/orders'


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_random_login_password_fname():
    # создаём словарь, чтобы метод мог его вернуть
    login_pass = {}

    # генерируем логин, пароль и имя курьера
    login_pass['login'] = generate_random_string(5)
    login_pass['password'] = generate_random_string(5)
    login_pass['first_name'] = generate_random_string(5)

    return login_pass

def registration_courier():
    login_pass = generate_random_login_password_fname()
    requests.post(url_create_courier, data=login_pass)
    return login_pass