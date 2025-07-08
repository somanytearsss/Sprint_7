import requests
import allure
from help_data import url_create_order


class TestOrdersList:
    @allure.title("Проверяем получение списка заказов")
    def test_get_orders_list(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = requests.get(url_create_order)
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"