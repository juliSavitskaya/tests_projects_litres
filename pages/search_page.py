import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class SearchPage(BasePage):
    """Класс для работы со страницей поиска"""

    # Локаторы
    search_results = (By.CSS_SELECTOR, "[data-testid='art__wrapper']")
    book_cover = (By.CSS_SELECTOR, "[data-testid='art__cover']")
    book_title = (By.CSS_SELECTOR, "[data-testid='art__title']")
    first_book_link = (By.CSS_SELECTOR, "[data-testid='art__wrapper'] [data-testid='art__title']")
    search_content = (By.CSS_SELECTOR, "[data-testid='search__content--wrapper']")

    @allure.step("Получение количества результатов поиска")
    def get_results_count(self) -> int:
        """Получить количество результатов поиска"""
        # Ждём появления контента поиска
        if self.is_element_present(self.search_content):
            results = self.find_elements(self.search_results)
            return len(results)
        return 0

    @allure.step("Клик по первой книге в результатах")
    def click_first_book(self):
        """Кликнуть на первую книгу"""
        first_book = self.wait_for_element(self.first_book_link)
        href = first_book.get_attribute("href")
        if href:
            current_url = self.browser.current_url
            self.browser.get(href)
            self.wait_for_url_changes(current_url)
        else:
            self.browser.execute_script("arguments[0].click();", first_book)
            self.wait_for_url_contains("/book/")

    @allure.step("Проверка наличия результатов поиска")
    def has_results(self) -> bool:
        """Проверить наличие результатов"""
        return self.get_results_count() > 0

    @allure.step("Получение информации о первой книге")
    def get_first_book_info(self) -> dict:
        """Получить информацию о первой книге"""
        title_element = self.find_element(self.book_title)
        return {
            "title": title_element.text,
            "href": title_element.get_attribute("href")
        }
