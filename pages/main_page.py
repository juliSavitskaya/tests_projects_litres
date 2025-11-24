import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class MainPage(BasePage):
    """Класс для работы с главной страницей Литрес"""

    url = "https://www.litres.ru/"

    # Локаторы
    search_input = (By.CSS_SELECTOR, "[data-testid='search__input']")
    book_cards = (By.CSS_SELECTOR, "[data-testid='art__wrapper']")
    book_cover = (By.CSS_SELECTOR, "[data-testid='art__cover']")
    book_title = (By.CSS_SELECTOR, "[data-testid='art__title']")
    any_book_image = (By.CSS_SELECTOR, "[data-testid='adaptiveCover__img']")
    logo = (By.CSS_SELECTOR, "[data-testid='header--logo'], a[href='/']")
    cart_icon = (By.CSS_SELECTOR, "a[href*='/cart'], a[href*='/basket']")

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
        search = self.wait_for_element_clickable(self.search_input)
        search.clear()
        search.send_keys(query)
        current_url = self.browser.current_url
        search.send_keys(Keys.RETURN)
        # Ждём изменения URL или появления результатов
        self.wait_for_url_changes(current_url)

    @allure.step("Получение количества книг на странице")
    def get_books_count_on_page(self) -> int:
        """Получить количество книг на странице"""
        # Ждём загрузки любых книг
        if self.is_element_present(self.book_cards):
            books = self.find_elements(self.book_cards)
            if len(books) > 0:
                return len(books)

        if self.is_element_present(self.any_book_image):
            covers = self.find_elements(self.any_book_image)
            return len(covers)

        return 0

    @allure.step("Переход в корзину")
    def go_to_cart(self):
        """Перейти в корзину"""
        self.browser.get("https://www.litres.ru/my-books/cart/")
        self.wait_for_page_load()