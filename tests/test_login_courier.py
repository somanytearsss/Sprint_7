import allure
import requests
from help_data import registration_courier, url_courier_login, generate_random_string

@allure.description('Тестирование класса авторизации курьера')
class TestLoginCourier:

    @allure.title("Проверка авторизации курьера")
    def test_login_courier(self):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()
            # Извлекаем созданные имя пользователя и пароль
            payload = {
                "login": login_pass.get('login'),
                "password": login_pass.get('password')
            }

        with allure.step("Авторизуемся под созданным курьером"):
            response = requests.post(url_courier_login, json=payload)
            # Проверка успешной авторизации = 200
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
            # Проверка наличия 'id' в ответе
            response_data = response.json()
            assert  'id' in response_data, f"Ожидался в ответе 'id' курьера, но получен {response.json()}"
            # Проверка что 'id' целое число
            assert isinstance(response_data['id'], int)

    @allure.title("Проверка появления ошибки при оставлении поля 'login' пустым")
    def test_courier_no_login_where_login_is_empty(self):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()
            # Извлекаем созданный пароль, имя пользователя оставляем пустым
            payload = {
                "login": '',
                "password": login_pass.get('password')

            }
        with allure.step("Авторизуемся с пустым именем пользователя"):
            response = requests.post(url_courier_login, json=payload)
            # Проверка появления ошибки = 400
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
            # Проверка соответствия текста ошибки требованиям
            assert response.json()['message'] == "Недостаточно данных для входа", \
                f"Ожидалось сообщение 'Недостаточно данных для входа', но получен ответ {response.json()['message']}"

    @allure.title("Проверка появления ошибки при оставлении поля 'password' пустым")
    def test_courier_no_login_where_password_is_empty(self):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()
            # Извлекаем созданное имя пользователя, пароль оставляем пустым
            payload = {
                "login": login_pass.get('login'),
                "password": ''
            }
        with allure.step("Авторизуемся с пустым паролем"):
            response = requests.post(url_courier_login, json=payload)
            # Проверка появления ошибки = 400
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
            # Проверка соответствия текста ошибки требованиям
            assert response.json()['message'] == "Недостаточно данных для входа", \
                f"Ожидалось сообщение 'Недостаточно данных для входа', но получен ответ {response.json()['message']}"

    @allure.title("Проверка появления ошибки при передаче запроса без поля 'login'")
    def test_courier_no_login_without_login(self):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()
            # Извлекаем созданный пароль, имя пользователя не передаём
            payload = {
                  "password": login_pass.get('password')
            }
        with allure.step("Авторизуемся без передачи поля 'login'"):
            response = requests.post(url_courier_login, json=payload)
            # Проверка появления ошибки = 400
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
            # Проверка соответствия текста ошибки требованиям
            assert response.json()['message'] == "Недостаточно данных для входа", \
                f"Ожидалось сообщение 'Недостаточно данных для входа', но получен ответ {response.json()['message']}"

    @allure.title("Проверка появления ошибки при авторизации с некорректным логином")
    def test_courier_no_login_where_login_is_incorrect(self):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()
            # Извлекаем созданный пароль, имя пользователя произвольно генерируем
            payload = {
                "login": generate_random_string(5),
                "password": login_pass.get('password')
            }
        with allure.step("Авторизуемся с некорректным именем пользователя"):
            response = requests.post(url_courier_login, json=payload)
            # Проверка появления ошибки = 404
            assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"
            # Проверка соответствия текста ошибки требованиям
            assert response.json()['message'] == "Учетная запись не найдена", \
                f"Ожидалось сообщение 'Учетная запись не найдена', но получен ответ {response.json()['message']}"

    @allure.title("Проверка появления ошибки при авторизации с некорректным паролем")
    def test_courier_no_login_where_password_is_incorrect(self):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()
            # Извлекаем созданное имя пользователя, пароль произвольно генерируем
            payload = {
                "login": login_pass.get('login'),
                "password": generate_random_string(5)
            }
        with allure.step("Авторизуемся с некорректным паролем"):
            response = requests.post(url_courier_login, json=payload)
            # Проверка появления ошибки = 404
            assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"
            # Проверка соответствия текста ошибки требованиям
            assert response.json()['message'] == "Учетная запись не найдена", \
                f"Ожидалось сообщение 'Учетная запись не найдена', но получен ответ {response.json()['message']}"

    @allure.title("Проверка появления ошибки при авторизации с некорректным именем пользователя и паролем")
    def test_courier_no_login_where_invalid_login_and_password(self):
        with allure.step("Имя пользователя, пароль произвольно генерируем"):
            payload = {
                "login": generate_random_string(5),
                "password": generate_random_string(5)
            }
        with allure.step("Авторизуемся с некорректным именем пользователя и паролем"):
            response = requests.post(url_courier_login, json=payload)
            # Проверка появления ошибки = 404
            assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"
            # Проверка соответствия текста ошибки требованиям
            assert response.json()['message'] == "Учетная запись не найдена", \
                f"Ожидалось сообщение 'Учетная запись не найдена', но получен ответ {response.json()['message']}"

    @allure.title("Проверка появления ошибки при передаче запроса без поля 'password'")
    def test_courier_no_login_without_password(self):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()
            # Извлекаем созданное имя пользователя, пароль не передаём
            payload = {
                "login": login_pass.get('login')
            }
        with allure.step("Авторизуемся без передачи поля 'password'"):
            response = requests.post(url_courier_login, json=payload)
            # Проверка появления ошибки = 400
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
            # Проверка соответствия текста ошибки требованиям
            assert response.json()['message'] == "Недостаточно данных для входа", \
                f"Ожидалось сообщение 'Недостаточно данных для входа', но получен ответ {response.json()['message']}"