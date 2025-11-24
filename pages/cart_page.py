import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class CartPage(BasePage):
    """Класс для работы со страницей корзины"""

    url = "https://www.litres.ru/my-books/cart/"

    # Локаторы
    page_title = (By.CSS_SELECTOR, "#pageTitle, h1")
    cart_items = (By.CSS_SELECTOR, "[data-testid='сart__list--wrapper']")
    empty_cart_message = (By.CSS_SELECTOR, "[class*='empty'], [class*='Empty']")
    remove_button = (By.CSS_SELECTOR, "[data-testid*='remove'], button[aria-label*='удалить']")

    @allure.step("Открытие страницы корзины")
    def open_page(self):
        """Открытие страницы корзины"""
        self.open(self.url)

    @allure.step("Открытие страницы корзины")
    def open_cart(self):
        """Открытие страницы корзины (алиас)"""
        self.open_page()

    @allure.step("Получение заголовка страницы")
    def get_page_title(self) -> str:
        """Получить заголовок страницы"""
        try:
            title = self.find_element(self.page_title)
            return title.text
        except TimeoutException:
            return self.browser.title

    @allure.step("Проверка что корзина пустая")
    def is_cart_empty(self) -> bool:
        """Проверить что корзина пустая"""
        items = self.find_elements(self.cart_items)
        return len(items) == 0

    @allure.step("Проверка видимости сообщения о пустой корзине")
    def is_empty_cart_visible(self) -> bool:
        """Проверить что отображается сообщение о пустой корзине"""
        # Корзина пустая если нет товаров или есть сообщение о пустой корзине
        return self.is_cart_empty() or self.is_element_present(self.empty_cart_message, timeout=3)

    @allure.step("Получение количества товаров в корзине")
    def get_items_count(self) -> int:
        """Получить количество товаров в корзине"""
        items = self.find_elements(self.cart_items)
        return len(items)

    @allure.step("Получение количества товаров в корзине")
    def get_cart_items_count(self) -> int:
        """Получить количество товаров в корзине (алиас)"""
        return self.get_items_count()

    @allure.step("Удаление первого товара из корзины")
    def remove_first_item(self):
        """Удалить первый товар из корзины"""
        self.click(self.remove_button)
