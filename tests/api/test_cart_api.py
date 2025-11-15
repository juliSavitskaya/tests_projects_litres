import pytest
import allure
from jsonschema import validate
from api.schemas.cart_schema import CART_SCHEMA, EMPTY_CART_SCHEMA


@allure.epic("API тестирование")
@allure.feature("Корзина API")
class TestCartAPI:
    """API тесты для корзины"""

    @allure.story("GET /cart/arts")
    @allure.title("Получение пустой корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "smoke")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_empty_cart(self, litres_client):
        """Тест: Получение пустой корзины через API"""
        with allure.step("Очистка корзины"):
            litres_client.clear_cart()
        
        with allure.step("Получение корзины"):
            response = litres_client.get_cart()
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверка что корзина пустая"):
            data = response.json()
            cart_data = data.get("payload", {}).get("data", [])
            assert cart_data == [], "Корзина не пустая"
        
        with allure.step("Валидация схемы ответа"):
            validate(instance=data, schema=EMPTY_CART_SCHEMA)

    @allure.story("POST /cart/add")
    @allure.title("Добавление книги в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "smoke", "regression")
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_book_to_cart(self, litres_client):
        """Тест: Добавление книги в корзину через API"""
        book_id = 12345
        
        with allure.step("Очистка корзины"):
            litres_client.clear_cart()
        
        with allure.step(f"Добавление книги {book_id} в корзину"):
            response = litres_client.add_to_cart(book_id)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code in [200, 201], \
                f"Ожидался статус 200 или 201, получен {response.status_code}"
        
        with allure.step("Получение обновленной корзины"):
            cart_response = litres_client.get_cart()
            cart_data = cart_response.json().get("payload", {}).get("data", [])
        
        with allure.step("Проверка что книга добавлена"):
            book_ids = [item.get("id") for item in cart_data]
            assert book_id in book_ids, f"Книга {book_id} не найдена в корзине"

    @allure.story("POST /cart/clear")
    @allure.title("Очистка корзины")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    def test_clear_cart(self, litres_client):
        """Тест: Очистка корзины через API"""
        with allure.step("Добавление книги в корзину"):
            litres_client.add_to_cart(12345)
        
        with allure.step("Очистка корзины"):
            response = litres_client.clear_cart()
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверка что корзина пустая"):
            cart_response = litres_client.get_cart()
            cart_data = cart_response.json().get("payload", {}).get("data", [])
            assert cart_data == [], "Корзина не пустая после очистки"

    @allure.story("DELETE /cart/{book_id}")
    @allure.title("Удаление книги из корзины")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    def test_remove_book_from_cart(self, litres_client):
        """Тест: Удаление книги из корзины через API"""
        book_id = 12345
        
        with allure.step("Очистка корзины"):
            litres_client.clear_cart()
        
        with allure.step(f"Добавление книги {book_id} в корзину"):
            litres_client.add_to_cart(book_id)
        
        with allure.step(f"Удаление книги {book_id} из корзины"):
            response = litres_client.remove_from_cart(book_id)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code in [200, 204], \
                f"Ожидался статус 200 или 204, получен {response.status_code}"
        
        with allure.step("Проверка что книга удалена"):
            cart_response = litres_client.get_cart()
            cart_data = cart_response.json().get("payload", {}).get("data", [])
            book_ids = [item.get("id") for item in cart_data]
            assert book_id not in book_ids, f"Книга {book_id} все еще в корзине"

    @allure.story("Параметризация")
    @allure.title("Добавление нескольких книг в корзину")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize("book_id", [11111, 22222, 33333])
    def test_add_multiple_books(self, litres_client, book_id):
        """Тест: Добавление разных книг в корзину (параметризация)"""
        with allure.step("Очистка корзины"):
            litres_client.clear_cart()
        
        with allure.step(f"Добавление книги {book_id}"):
            response = litres_client.add_to_cart(book_id)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code in [200, 201], \
                f"Не удалось добавить книгу {book_id}"
