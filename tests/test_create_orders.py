import requests
import allure
import pytest
from help_data import url_create_order


@allure.description('Проверяем создание заказа')
class TestCreateOrders:

    @allure.title("Проверяем создания заказа")
    # вводим параметризацию для цвета: каждый цвет, оба, либо без выбора цвета
    @pytest.mark.parametrize('colors', ['BLACK','GREY', ['BLACK','SILVER'], ''])
    def test_create_order(self, colors):
        payload = {
            "firstName": "Артем",
            "lastName": "Елизаров",
            "address": "Москва, Короленко 23",
            "metroStation": 5,
            "phone": "+7 928 421 76 56",
            "rentTime": 2,
            "deliveryDate": "2025-07-13",
            "comment": "Оставьте у двери, пожалуйста",
            "color": [colors]
        }
        with allure.step(f"Создаём заказ с цветом`: {colors}"):
            response = requests.post(url_create_order, json=payload)
            assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"
            assert 'track' in response.json(), f"Ожидался в ответе 'track', но получен {response.json}"