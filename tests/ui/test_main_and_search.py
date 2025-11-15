import pytest
import allure


@allure.epic("UI тестирование")
@allure.feature("Главная страница")
class TestMainPage:
    """Тесты главной страницы"""

    @allure.story("Открытие главной страницы")
    @allure.title("Проверка загрузки главной страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "ui")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_main_page_loads(self, main_page):
        """Тест: Главная страница загружается корректно"""
        with allure.step("Открытие главной страницы"):
            main_page.open_page()
        
        with allure.step("Проверка видимости логотипа"):
            assert main_page.is_logo_visible(), "Логотип не отображается"

    @allure.story("Главная страница")
    @allure.title("Проверка отображения книг на главной странице")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "ui")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_books_displayed_on_main_page(self, main_page):
        """Тест: На главной странице отображаются книги"""
        with allure.step("Открытие главной страницы"):
            main_page.open_page()
        
        with allure.step("Проверка количества книг"):
            books_count = main_page.get_books_count_on_page()
            assert books_count > 0, "Книги не отображаются на главной странице"


@allure.epic("UI тестирование")
@allure.feature("Поиск")
class TestSearch:
    """Тесты функционала поиска"""

    @allure.story("Поиск книг")
    @allure.title("Поиск книги по запросу '{search_query}'")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "regression", "ui")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.parametrize("search_query", [
        "Толстой",
        "Python",
        "Детективы"
    ])
    def test_search_books(self, main_page, search_page, search_query):
        """Тест: Поиск книг по различным запросам"""
        with allure.step("Открытие главной страницы"):
            main_page.open_page()
        
        with allure.step(f"Поиск книги по запросу: {search_query}"):
            main_page.search_book(search_query)
        
        with allure.step("Проверка результатов поиска"):
            results_count = search_page.get_results_count()
            assert results_count > 0, f"Не найдено результатов по запросу: {search_query}"

    @allure.story("Поиск книг")
    @allure.title("Поиск несуществующей книги")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "ui")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_search_no_results(self, main_page, search_page):
        """Тест: Поиск несуществующей книги возвращает пустой результат"""
        with allure.step("Открытие главной страницы"):
            main_page.open_page()
        
        with allure.step("Поиск несуществующей книги"):
            main_page.search_book("asdfghjklqwertyuiop12345")
        
        with allure.step("Проверка отсутствия результатов"):
            assert not search_page.has_results(), "Найдены результаты для несуществующей книги"

    @allure.story("Поиск книг")
    @allure.title("Открытие книги из результатов поиска")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "ui")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_open_book_from_search(self, main_page, search_page, book_page):
        """Тест: Переход на страницу книги из результатов поиска"""
        with allure.step("Открытие главной страницы"):
            main_page.open_page()
        
        with allure.step("Поиск книги"):
            main_page.search_book("Пушкин")
        
        with allure.step("Проверка наличия результатов"):
            assert search_page.get_results_count() > 0, "Результаты поиска не найдены"
        
        with allure.step("Клик по первой книге"):
            search_page.click_first_book()
        
        with allure.step("Проверка открытия страницы книги"):
            assert book_page.is_book_page_loaded(), "Страница книги не загрузилась"
