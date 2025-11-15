import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Класс для работы со страницей корзины"""

    url = "https://www.litres.ru/basket/"
    
    page_title = (By.CSS_SELECTOR, "h1, .page-title")
    empty_cart_message = (By.CSS_SELECTOR, ".empty-cart, [class*='empty'], [class*='Empty']")
    empty_cart_title = (By.CSS_SELECTOR, ".empty-cart h2, .empty-cart-title")
    cart_items = (By.CSS_SELECTOR, ".cart-item, .basket-item, [class*='CartItem']")
    cart_item_title = (By.CSS_SELECTOR, ".cart-item .title, [class*='Title']")
    cart_item_price = (By.CSS_SELECTOR, ".cart-item .price, [class*='Price']")
    remove_item_button = (By.CSS_SELECTOR, ".remove-item, [class*='remove'], [class*='delete']")
    total_price = (By.CSS_SELECTOR, ".total-price, [class*='total']")
    checkout_button = (By.CSS_SELECTOR, ".checkout, [class*='checkout'], [class*='order']")

    @allure.step("Открытие страницы корзины")
    def open_cart(self):
        """Открыть корзину"""
        self.open(self.url)

    @allure.step("Получение заголовка страницы")
    def get_page_title(self) -> str:
        """Получить заголовок страницы"""
        return self.get_text(self.page_title)

    @allure.step("Проверка видимости пустой корзины")
    def is_empty_cart_visible(self) -> bool:
        """Проверить видимость сообщения о пустой корзине"""
        return self.is_element_visible(self.empty_cart_message)

    @allure.step("Получение текста сообщения о пустой корзине")
    def get_empty_cart_title(self) -> str:
        """Получить текст сообщения о пустой корзине"""
        return self.get_text(self.empty_cart_title)

    @allure.step("Получение количества товаров в корзине")
    def get_cart_items_count(self) -> int:
        """Получить количество товаров в корзине"""
        items = self.find_elements(self.cart_items)
        return len(items)

    @allure.step("Получение общей суммы в корзине")
    def get_total_price(self) -> str:
        """Получить общую сумму"""
        return self.get_text(self.total_price)

    @allure.step("Удаление первого товара из корзины")
    def remove_first_item(self):
        """Удалить первый товар"""
        self.click(self.remove_item_button)

    @allure.step("Проверка что корзина не пустая")
    def is_cart_not_empty(self) -> bool:
        """Проверить что корзина не пустая"""
        return self.get_cart_items_count() > 0
