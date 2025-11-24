import pytest
import allure

# Тестовые данные - реальные ID книг с Litres
TEST_BOOK_ID = 72456610  # Пелевин "Левый путь"


@allure.epic("API тестирование")
@allure.feature("Корзина API")
class TestCartAPI:
    """API тесты для корзины"""

    @allure.story("GET /wishlist/arts")
    @allure.title("Получение корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "smoke")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_cart(self, litres_client):
        """Тест: Получение корзины через API"""
        with allure.step("Получение корзины"):
            response = litres_client.get_cart()

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"

    @allure.story("PUT /cart/arts/add")
    @allure.title("Добавление книги в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "smoke")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_add_to_cart(self, litres_client):
        """Тест: Добавление книги в корзину через API"""
        with allure.step(f"Добавление книги {TEST_BOOK_ID} в корзину"):
            response = litres_client.add_to_cart([TEST_BOOK_ID])

        with allure.step("Проверка статус кода"):
            assert response.status_code in [200, 201], \
                f"Ожидался статус 200 или 201, получен {response.status_code}"

    @allure.story("PUT /cart/arts/remove")
    @allure.title("Удаление книги из корзины")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    def test_remove_from_cart(self, litres_client):
        """Тест: Удаление книги из корзины через API"""
        # 1. ARRANGE - сначала добавляем книгу
        with allure.step(f"Добавление книги {TEST_BOOK_ID} в корзину"):
            add_response = litres_client.add_to_cart([TEST_BOOK_ID])
            assert add_response.status_code in [200, 201], \
                f"Не удалось добавить книгу. Статус: {add_response.status_code}"

        # 2. ACT - удаляем книгу
        with allure.step(f"Удаление книги {TEST_BOOK_ID} из корзины"):
            response = litres_client.remove_from_cart([TEST_BOOK_ID])

        # 3. ASSERT - проверяем результат
        with allure.step("Проверка статус кода"):
            assert response.status_code in [200, 204], \
                f"Ожидался статус 200 или 204, получен {response.status_code}"

    @allure.story("Полный цикл")
    @allure.title("Добавление и очистка корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    def test_add_and_clear_cart(self, litres_client):
        """Тест: Полный цикл - добавление и очистка корзины"""
        # 1. ARRANGE - добавляем книгу
        with allure.step(f"Добавление книги {TEST_BOOK_ID} в корзину"):
            add_response = litres_client.add_to_cart([TEST_BOOK_ID])
            assert add_response.status_code in [200, 201], \
                f"Не удалось добавить книгу. Статус: {add_response.status_code}"

        # 2. ACT - очищаем корзину
        with allure.step(f"Очистка корзины"):
            clear_response = litres_client.remove_from_cart([TEST_BOOK_ID])

        # 3. ASSERT
        with allure.step("Проверка статус кода очистки"):
            assert clear_response.status_code in [200, 204], \
                f"Ожидался статус 200 или 204, получен {clear_response.status_code}"

    @allure.story("Параметризация")
    @allure.title("Добавление и удаление книги {art_id}")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize("art_id", [72456610])
    def test_add_and_remove_book(self, litres_client, art_id):
        """Тест: Добавление и удаление книги (параметризация)"""
        # 1. Добавляем
        with allure.step(f"Добавление книги {art_id}"):
            add_response = litres_client.add_to_cart([art_id])
            assert add_response.status_code in [200, 201]

        # 2. Удаляем
        with allure.step(f"Удаление книги {art_id}"):
            remove_response = litres_client.remove_from_cart([art_id])
            assert remove_response.status_code in [200, 204]