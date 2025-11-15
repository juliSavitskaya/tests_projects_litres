import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class BookPage(BasePage):
    """Класс для работы со страницей книги"""

    book_title = (By.CSS_SELECTOR, "h1, .book-title, [class*='Title']")
    book_author = (By.CSS_SELECTOR, ".author, [class*='Author']")
    book_price = (By.CSS_SELECTOR, ".price, [class*='Price']")
    book_description = (By.CSS_SELECTOR, ".description, [class*='Description']")
    book_rating = (By.CSS_SELECTOR, ".rating, [class*='Rating']")
    add_to_cart_button = (By.CSS_SELECTOR, ".add-to-cart, [class*='addToCart'], [class*='buy']")
    add_to_favorites_button = (By.CSS_SELECTOR, ".add-to-favorites, [class*='favorite']")
    read_sample_button = (By.CSS_SELECTOR, ".read-sample, [class*='sample']")
    book_cover = (By.CSS_SELECTOR, ".book-cover, img[class*='cover']")

    @allure.step("Проверка загрузки страницы книги")
    def is_book_page_loaded(self) -> bool:
        """Проверить что страница книги загрузилась"""
        return self.is_element_visible(self.book_title)

    @allure.step("Получение названия книги")
    def get_book_title(self) -> str:
        """Получить название книги"""
        return self.get_text(self.book_title)

    @allure.step("Получение автора книги")
    def get_book_author(self) -> str:
        """Получить автора книги"""
        return self.get_text(self.book_author)

    @allure.step("Получение цены книги")
    def get_book_price(self) -> str:
        """Получить цену книги"""
        return self.get_text(self.book_price)

    @allure.step("Добавление книги в корзину")
    def add_to_cart(self):
        """Добавить книгу в корзину"""
        self.click(self.add_to_cart_button)

    @allure.step("Добавление книги в избранное")
    def add_to_favorites(self):
        """Добавить в избранное"""
        self.click(self.add_to_favorites_button)

    @allure.step("Открытие образца книги")
    def read_sample(self):
        """Открыть образец"""
        self.click(self.read_sample_button)

    @allure.step("Проверка наличия обложки книги")
    def has_book_cover(self) -> bool:
        """Проверить наличие обложки"""
        return self.is_element_visible(self.book_cover)
