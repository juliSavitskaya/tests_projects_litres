import pytest
import allure


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
        
        with allure.step("Проверка заголовка страницы"):
            assert cart_page.get_page_title() == "Корзина", "Неверный заголовок страницы"
        
        with allure.step("Проверка отображения сообщения о пустой корзине"):
            assert cart_page.is_empty_cart_visible(), "Сообщение о пустой корзине не отображается"
        
        with allure.step("Проверка текста сообщения"):
            assert cart_page.get_empty_cart_title() == "Корзина пуста", "Неверный текст сообщения"

    @allure.story("Добавление в корзину")
    @allure.title("Добавление книги в корзину через UI")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "regression", "ui")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_add_book_to_cart(self, main_page, search_page, book_page, cart_page):
        """Тест: Добавление книги в корзину и проверка"""
        with allure.step("Открытие главной страницы"):
            main_page.open_page()
        
        with allure.step("Поиск книги"):
            search_query = "Детективы"
            main_page.search_book(search_query)
        
        with allure.step("Проверка результатов поиска"):
            results_count = search_page.get_results_count()
            assert results_count > 0, "Результаты поиска не найдены"
        
        with allure.step("Открытие страницы книги"):
            search_page.click_first_book()
            assert book_page.is_book_page_loaded(), "Страница книги не загрузилась"
        
        with allure.step("Добавление книги в корзину"):
            book_page.add_to_cart()
        
        with allure.step("Переход в корзину"):
            cart_page.open_cart()
        
        with allure.step("Проверка что корзина не пустая"):
            items_count = cart_page.get_cart_items_count()
            assert items_count > 0, "Корзина пустая после добавления книги"

    @allure.story("Навигация")
    @allure.title("Переход в корзину с главной страницы")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "regression")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_navigate_to_cart(self, main_page, cart_page):
        """Тест: Переход в корзину через иконку корзины"""
        with allure.step("Открытие главной страницы"):
            main_page.open_page()
        
        with allure.step("Клик по иконке корзины"):
            main_page.go_to_cart()
        
        with allure.step("Проверка открытия страницы корзины"):
            assert "basket" in cart_page.browser.current_url or "cart" in cart_page.browser.current_url, \
                "Страница корзины не открылась"
