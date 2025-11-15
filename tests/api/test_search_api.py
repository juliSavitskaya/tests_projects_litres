import pytest
import allure
from jsonschema import validate
from api.schemas.search_schema import SEARCH_RESPONSE_SCHEMA, BOOK_DETAILS_SCHEMA


@allure.epic("API тестирование")
@allure.feature("Поиск API")
class TestSearchAPI:
    """API тесты для поиска книг"""

    @allure.story("GET /search")
    @allure.title("Поиск книг по запросу '{query}'")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "smoke", "regression")
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("query,expected_min_results", [
        ("Python", 1),
        ("Толстой", 5),
        ("Детектив", 10)
    ])
    def test_search_books(self, litres_client, query, expected_min_results):
        """Тест: Поиск книг по различным запросам"""
        with allure.step(f"Поиск книг по запросу: {query}"):
            response = litres_client.search_books(query, limit=20)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Парсинг ответа"):
            data = response.json()
        
        with allure.step("Валидация схемы ответа"):
            validate(instance=data, schema=SEARCH_RESPONSE_SCHEMA)
        
        with allure.step(f"Проверка количества результатов (минимум {expected_min_results})"):
            total = data.get("total", 0)
            assert total >= expected_min_results, \
                f"Найдено {total} книг, ожидалось минимум {expected_min_results}"

    @allure.story("GET /search")
    @allure.title("Поиск с пустым запросом")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    def test_search_empty_query(self, litres_client):
        """Тест: Поиск с пустым запросом"""
        with allure.step("Поиск с пустым запросом"):
            response = litres_client.search_books("", limit=10)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code in [200, 400], \
                f"Неожиданный статус код: {response.status_code}"

    @allure.story("GET /books/{id}")
    @allure.title("Получение деталей книги")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "smoke")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_book_details(self, litres_client):
        """Тест: Получение деталей книги по ID"""
        book_id = 12345
        
        with allure.step(f"Получение деталей книги {book_id}"):
            response = litres_client.get_book_details(book_id)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code in [200, 404], \
                f"Неожиданный статус код: {response.status_code}"
        
        if response.status_code == 200:
            with allure.step("Валидация схемы ответа"):
                data = response.json()
                validate(instance=data, schema=BOOK_DETAILS_SCHEMA)
            
            with allure.step("Проверка наличия обязательных полей"):
                assert "id" in data, "Отсутствует поле 'id'"
                assert "title" in data, "Отсутствует поле 'title'"
                assert data["id"] == book_id, "ID книги не совпадает"

    @allure.story("GET /search")
    @allure.title("Поиск с лимитом результатов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize("limit", [5, 10, 20])
    def test_search_with_limit(self, litres_client, limit):
        """Тест: Поиск с ограничением количества результатов"""
        with allure.step(f"Поиск с лимитом {limit}"):
            response = litres_client.search_books("роман", limit=limit)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step(f"Проверка что результатов не больше {limit}"):
            data = response.json()
            books = data.get("books", [])
            assert len(books) <= limit, f"Получено {len(books)} книг, ожидалось максимум {limit}"
