import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    """Класс для работы с главной страницей Литрес"""

    url = "https://www.litres.ru/"

    logo = (By.CSS_SELECTOR, "[data-testid='header--logo']")
    search_input = (By.CSS_SELECTOR, "input[type='search'], input[name='q'], .search-input")
    search_button = (By.CSS_SELECTOR, ".search-button, button[type='submit']")
    cart_icon = (By.CSS_SELECTOR, ".cart-icon, [class*='cart'], [href*='basket']")
    catalog_button = (By.CSS_SELECTOR, ".catalog-button, [class*='catalog']")
    favorites_link = (By.CSS_SELECTOR, "[href*='favorite'], .favorites")
    loyalty_link = (By.CSS_SELECTOR, "[href*='bonus'], [href*='loyalty']")
    book_cards = (By.CSS_SELECTOR, ".book-card, .art-item, [class*='Book']")
    add_to_cart_buttons = (By.CSS_SELECTOR, ".add-to-cart, [class*='addToCart'], [class*='buy']")
    book_titles = (By.CSS_SELECTOR, ".book-title, [class*='Title']")
    cart_counter = (By.CSS_SELECTOR, ".cart-count, .basket-count, [class*='count']")

    @allure.step("Открытие главной страницы Литрес")
    def open_page(self):
        """Открытие главной страницы Литрес"""
        self.open(self.url)

    @allure.step("Проверка видимости логотипа")
    def is_logo_visible(self):
        """Проверка видимости логотипа"""
        return self.is_element_visible(self.logo)

    @allure.step("Поиск книги по запросу: {query}")
    def search_book(self, query: str):
        """Поиск книги"""
        self.input_text(self.search_input, query)
        search_input = self.find_element(self.search_input)
        search_input.send_keys(Keys.RETURN)

    @allure.step("Нажатие кнопки поиска")
    def click_search_button(self):
        """Нажать кнопку поиска"""
        self.click(self.search_button)

    @allure.step("Переход в корзину")
    def go_to_cart(self):
        """Перейти в корзину"""
        self.click(self.cart_icon)

    @allure.step("Переход в каталог")
    def go_to_catalog(self):
        """Перейти в каталог"""
        self.click(self.catalog_button)

    @allure.step("Переход в избранное")
    def go_to_favorites(self):
        """Перейти в избранное"""
        self.click(self.favorites_link)

    @allure.step("Переход на страницу лояльности")
    def go_to_loyalty(self):
        """Перейти на страницу лояльности"""
        self.click(self.loyalty_link)

    @allure.step("Получение количества книг на странице")
    def get_books_count_on_page(self) -> int:
        """Получить количество книг на странице"""
        books = self.find_elements(self.book_cards)
        return len(books)
