import pytest
import allure


@allure.epic("API тестирование")
@allure.feature("Поиск API")
class TestSearchAPI:
    """API тесты для поиска книг"""

    @allure.story("GET /search")
    @allure.title("Поиск книг по запросу '{query}'")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "smoke")
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.parametrize("query", [
        "детективы",
        "Python",
        "Толстой"
    ])
    def test_search_books(self, litres_client, query):
        """Тест: Поиск книг по различным запросам"""
        with allure.step(f"Поиск книг по запросу: {query}"):
            response = litres_client.search_books(query)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверка что есть результаты"):
            data = response.json()
            # Проверяем структуру ответа
            assert 'payload' in data or 'data' in data or isinstance(data, list), \
                "Неожиданная структура ответа"

    @allure.story("GET /search")
    @allure.title("Поиск с лимитом результатов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize("limit", [5, 10, 24])
    def test_search_with_limit(self, litres_client, limit):
        """Тест: Поиск с ограничением количества результатов"""
        with allure.step(f"Поиск с лимитом {limit}"):
            response = litres_client.search_books("книга", limit=limit)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"

    @allure.story("GET /search")
    @allure.title("Поиск с пагинацией")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "regression")
    @pytest.mark.api
    @pytest.mark.regression
    def test_search_with_pagination(self, litres_client):
        """Тест: Поиск с offset для пагинации"""
        with allure.step("Поиск первой страницы"):
            response_page1 = litres_client.search_books("роман", limit=10, offset=0)
            assert response_page1.status_code == 200

        with allure.step("Поиск второй страницы"):
            response_page2 = litres_client.search_books("роман", limit=10, offset=10)
            assert response_page2.status_code == 200