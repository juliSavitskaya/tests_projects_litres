import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class BookPage(BasePage):
    """Класс для работы со страницей книги"""

    # Локаторы страницы книги
    book_title = (By.CSS_SELECTOR, "h1, [data-testid*='title']")
    book_author = (By.CSS_SELECTOR, "[data-testid='art__authorName--link'], [class*='author']")
    book_price = (By.CSS_SELECTOR, "[data-testid='art__finalPrice'], [class*='price']")
    add_to_cart_button = (By.CSS_SELECTOR,
                          "[data-testid*='buyButton'], "
                          "[data-testid*='addToCart'], "
                          "button[class*='buy'], "
                          "button[class*='cart']"
                          )

    # Модалка с акцией
    modal_overlay = (By.CSS_SELECTOR, "[data-testid='modal__overlay--wrapper']")

    # Кнопка "Перейти в корзину" (появляется после добавления)
    go_to_cart_button = (By.CSS_SELECTOR, "[data-testid='book__goToCartButton']")

    @allure.step("Проверка загрузки страницы книги")
    def is_book_page_loaded(self) -> bool:
        """Проверить что страница книги загружена"""
        current_url = self.browser.current_url
        return "/book/" in current_url or "/audiobook/" in current_url

    @allure.step("Получение названия книги")
    def get_book_title(self) -> str:
        """Получить название книги"""
        try:
            title = self.wait_for_element(self.book_title)
            return title.text
        except TimeoutException:
            return self.browser.title

    @allure.step("Получение автора книги")
    def get_book_author(self) -> str:
        """Получить автора книги"""
        try:
            author = self.find_element(self.book_author)
            return author.text
        except TimeoutException:
            return ""

    @allure.step("Получение цены книги")
    def get_book_price(self) -> str:
        """Получить цену книги"""
        try:
            price = self.find_element(self.book_price)
            return price.text
        except TimeoutException:
            return ""

    @allure.step("Добавление книги в корзину")
    def add_to_cart(self):
        """Добавить книгу в корзину"""
        try:
            button = self.wait_for_element_clickable(self.add_to_cart_button)
            button.click()
        except TimeoutException:
            buttons = self.find_elements(self.add_to_cart_button)
            if buttons:
                self.browser.execute_script("arguments[0].click();", buttons[0])
            else:
                raise Exception("Кнопка 'Добавить в корзину' не найдена")

    @allure.step("Проверка появления модалки с акцией")
    def is_modal_visible(self) -> bool:
        """Проверить появилась ли модалка с акцией"""
        return self.is_element_present(self.modal_overlay, timeout=3)

    @allure.step("Проверка появления кнопки 'Перейти в корзину'")
    def is_go_to_cart_button_visible(self) -> bool:
        """Проверить появилась ли кнопка перехода в корзину"""
        return self.is_element_present(self.go_to_cart_button, timeout=5)

    @allure.step("Переход в корзину")
    def go_to_cart(self):
        """Перейти в корзину после добавления книги"""
        # Если есть модалка - переходим напрямую по URL
        if self.is_modal_visible():
            self.browser.get("https://www.litres.ru/my-books/cart/")
            self.wait_for_page_load()
            return

        # Пробуем кликнуть по кнопке "Перейти в корзину"
        try:
            cart_btn = self.wait_for_element_clickable(self.go_to_cart_button, timeout=5)
            cart_btn.click()
            self.wait_for_url_contains("cart")
        except TimeoutException:
            # Если кнопка не найдена, переходим напрямую
            self.browser.get("https://www.litres.ru/my-books/cart/")
            self.wait_for_page_load()

    @allure.step("Добавление книги в корзину и переход в корзину")
    def add_to_cart_and_go_to_cart(self):
        """Добавить книгу и перейти в корзину"""
        self.add_to_cart()
        self.go_to_cart()

    @allure.step("Проверка наличия кнопки покупки")
    def is_buy_button_visible(self) -> bool:
        """Проверить наличие кнопки покупки"""
        return self.is_element_visible(self.add_to_cart_button)