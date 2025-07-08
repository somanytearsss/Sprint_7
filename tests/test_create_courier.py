import allure
import requests

from help_data import generate_random_string, url_create_courier, generate_random_login_password_fname


@allure.description('Тестирование класса создания курьера')
class TestCreateCourier:

    @allure.title('Создаем нового курьера, через рандом')
    def test_create_new_courier(self):
        payload = generate_random_login_password_fname()
        response = requests.post(url_create_courier, data=payload)
        assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"
        assert response.json() == {'ok': True}

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_cant_create_two_identical_couriers(self):
        with allure.step("Создание курьера с уникальными данными"):
            payload = generate_random_login_password_fname()
            response = requests.post(url_create_courier, data=payload)
            assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"

        with allure.step("Запрос на создание курьера с данными ранее зарегистрированного курьера"):
            response2 = requests.post(url_create_courier, data=payload)
            assert response2.status_code == 409, f"Ожидался статус 409, но получен {response.status_code}"
            assert response2.json()['message'] == "Этот логин уже используется. Попробуйте другой.", \
                f"Ожидалось сообщение'Этот логин уже используется', но получен ответ {response.json()['message']}"

    @allure.title('Проверка появления ошибки при регистрации без логина')
    def test_registration_without_a_login_failed(self):
        payload = {
        'login': '',
        'password': generate_random_string(5),
        'firstName': generate_random_string(5)
        }
        response = requests.post(url_create_courier, data=payload)
        assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
        assert response.json()['message'] == "Недостаточно данных для создания учетной записи", \
            f"Ожидалось сообщение 'Недостаточно данных для создания учетной записи', но получен ответ {response.json()['message']}"

    @allure.title('Проверка появления ошибки при регистрации без пароля')
    def test_registration_without_a_password_failed(self):
        payload = {
        'login': generate_random_string(5),
        'password': '',
        'firstName': generate_random_string(5)
        }
        response = requests.post(url_create_courier, data=payload)
        assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
        assert response.json()['message'] == "Недостаточно данных для создания учетной записи", \
            f"Ожидалось сообщение 'Недостаточно данных для создания учетной записи', но получен ответ {response.json()['message']}"

    @allure.title('Проверка успешной регистрации при оставлении пустым поля Имя')
    def test_registration_without_a_first_name(self):
        payload = {
        'login': generate_random_string(5),
        'password': generate_random_string(5),
        'firstName': ''
        }
        response = requests.post(url_create_courier, data=payload)
        assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"
        assert response.json() == {'ok': True}

    @allure.title('Проверка появления ошибки при создании курьера с таким же логином')
    def test_error_when_creating_courier_with_existing_login(self):
        with allure.step("Создание курьера с уникальными данными"):
            login_pass = generate_random_login_password_fname()

            response = requests.post(url_create_courier, data=login_pass)
            assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"

        with allure.step("Создание курьера с существующим логином"):
            payload = {
                "login": login_pass.get('login'),
                "password": generate_random_string(5),
                "firstName": generate_random_string(5)
            }
            response2 = requests.post(url_create_courier, data=payload)
            assert response2.status_code == 409, f"Ожидался статус 409, но получен {response.status_code}"