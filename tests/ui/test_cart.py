import pytest
import allure
from pages.main_page import MainPage


@allure.epic("UI тестирование")
@allure.feature("Корзина")
class TestCart:
    """Тесты функционала корзины"""

    @allure.story("Пустая корзина")
    @allure.title("Проверка пустой корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "ui")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_empty_cart(self, cart_page):
        """Тест: Проверка отображения пустой корзины"""
        with allure.step("Открытие страницы корзины"):
            cart_page.open_cart()
        
        with allure.step("Проверка отображения сообщения о пустой корзине"):
            assert cart_page.is_empty_cart_visible(), "Сообщение о пустой корзине не отображается"

    @allure.story("Навигация")
    @allure.title("Переход в корзину с главной страницы")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "regression")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_navigate_to_cart(self, browser):
        """Тест: Переход в корзину с главной страницы"""
        main_page = MainPage(browser)

        with allure.step("Открытие главной страницы"):
            main_page.open_page()

        with allure.step("Переход в корзину"):
            main_page.go_to_cart()

        with allure.step("Проверка что открылась корзина"):
            assert "cart" in browser.current_url or "my-books" in browser.current_url, \
                "Страница корзины не открылась"

    @allure.story("Добавление в корзину")
    @allure.title("Добавление книги в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "regression")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_add_book_to_cart(self, browser, main_page, search_page, book_page, cart_page):
        """Тест: Добавление книги в корзину через UI"""

        with allure.step("Открытие главной страницы"):
            main_page.open_page()
        with allure.step("Поиск книги"):
            main_page.search_book("Python")

        with allure.step("Проверка результатов поиска"):
            results = search_page.get_results_count()
            assert results > 0, "Книги не найдены"

        with allure.step("Открытие первой книги"):
            search_page.click_first_book()

        with allure.step("Проверка что страница книги загрузилась"):
            assert book_page.is_book_page_loaded(), "Страница книги не загрузилась"

        with allure.step("Добавление книги в корзину"):
            book_page.add_to_cart()

        with allure.step("Проверка что книга добавлена (кнопка изменилась на 'В корзине')"):
            assert book_page.is_go_to_cart_button_visible(), \
                "Кнопка 'В корзине' не появилась после добавления"

