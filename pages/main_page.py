import allure
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    """Класс для работы с главной страницей Литрес"""

    url = "https://www.litres.ru/"

    # Локаторы
    search_input = (By.CSS_SELECTOR, "[data-testid='search__input']")
    book_cards = (By.CSS_SELECTOR, "[data-testid='art__wrapper']")
    book_cover = (By.CSS_SELECTOR, "[data-testid='art__cover']")
    book_title = (By.CSS_SELECTOR, "[data-testid='art__title']")
    # Альтернативные локаторы для главной страницы
    any_book_image = (By.CSS_SELECTOR, "[data-testid='adaptiveCover__img']")
    logo = (By.CSS_SELECTOR, "[data-testid='header--logo'], a[href='/']")

    @allure.step("Открытие главной страницы Литрес")
    def open_page(self):
        """Открытие главной страницы Литрес"""
        self.open(self.url)
        time.sleep(3)

    @allure.step("Проверка видимости логотипа")
    def is_logo_visible(self):
        """Проверка видимости логотипа"""
        return self.is_element_visible(self.logo)

    @allure.step("Поиск книги по запросу: {query}")
    def search_book(self, query: str):
        """Поиск книги"""
        search = self.wait_for_element(self.search_input)
        search.clear()
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        time.sleep(3)

    @allure.step("Получение количества книг на странице")
    def get_books_count_on_page(self) -> int:
        """Получить количество книг на странице"""
        time.sleep(2)
        # Пробуем найти карточки книг
        books = self.find_elements(self.book_cards)
        if len(books) > 0:
            return len(books)
        # Если карточек нет, ищем обложки книг
        covers = self.find_elements(self.any_book_image)
        return len(covers)