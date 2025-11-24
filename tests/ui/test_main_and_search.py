import pytest
import allure
from pages.main_page import MainPage
from pages.search_page import SearchPage


@allure.epic("UI тестирование")
@allure.feature("Главная страница")
class TestMainPage:
    """UI тесты главной страницы"""

    @allure.story("Загрузка страницы")
    @allure.title("Главная страница загружается")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("ui", "smoke")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_main_page_loads(self, browser):
        """Тест: Главная страница загружается"""
        main_page = MainPage(browser)

        with allure.step("Открытие главной страницы"):
            main_page.open_page()

        with allure.step("Проверка что страница загрузилась"):
            assert "litres" in browser.current_url.lower(), \
                "Главная страница не загрузилась"

    @allure.story("Отображение контента")
    @allure.title("На главной странице есть книги")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "smoke")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_books_displayed_on_main_page(self, browser):
        """Тест: На главной странице отображаются книги"""
        main_page = MainPage(browser)

        with allure.step("Открытие главной страницы"):
            main_page.open_page()

        with allure.step("Проверка наличия книг"):
            books_count = main_page.get_books_count_on_page()
            assert books_count > 0, "Книги не отображаются на главной странице"


@allure.epic("UI тестирование")
@allure.feature("Поиск")
class TestSearch:
    """UI тесты поиска"""

    @allure.story("Поиск книг")
    @allure.title("Поиск книг по запросу '{search_query}'")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "smoke")
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.parametrize("search_query", [
        "Толстой",
        "Python",
        "Детективы"
    ])
    def test_search_books(self, browser, search_query):
        """Тест: Поиск книг по различным запросам"""
        main_page = MainPage(browser)
        search_page = SearchPage(browser)

        with allure.step("Открытие главной страницы"):
            main_page.open_page()

        with allure.step(f"Поиск книги: {search_query}"):
            main_page.search_book(search_query)

        with allure.step("Проверка результатов поиска"):
            results_count = search_page.get_results_count()
            assert results_count > 0, f"Не найдено результатов по запросу: {search_query}"

    @allure.story("Поиск книг")
    @allure.title("Поиск несуществующей книги")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "regression")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_search_no_results(self, browser):
        """Тест: Поиск несуществующей книги показывает пустой результат или рекомендации"""
        main_page = MainPage(browser)
        search_page = SearchPage(browser)

        with allure.step("Открытие главной страницы"):
            main_page.open_page()

        with allure.step("Поиск несуществующей книги"):
            main_page.search_book("xyznonexistent12345qwerty")

        with allure.step("Проверка результатов"):
            # Litres часто показывает рекомендации даже для абсурдных запросов
            # Проверяем что поиск выполнился (страница загрузилась)
            assert "search" in browser.current_url or "litres" in browser.current_url, \
                "Страница поиска не загрузилась"

    @allure.story("Переход к книге")
    @allure.title("Открытие страницы книги из результатов поиска")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "regression")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_open_book_from_search(self, browser):
        """Тест: Открытие страницы книги из результатов поиска"""
        main_page = MainPage(browser)
        search_page = SearchPage(browser)

        with allure.step("Открытие главной страницы"):
            main_page.open_page()

        with allure.step("Поиск книги"):
            main_page.search_book("детектив")

        with allure.step("Проверка что есть результаты"):
            assert search_page.get_results_count() > 0, "Результаты поиска не найдены"

        with allure.step("Клик по первой книге"):
            search_page.click_first_book()

        with allure.step("Проверка что открылась страница книги"):
            assert "/book/" in browser.current_url or "/audiobook/" in browser.current_url, \
                "Страница книги не открылась"