import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchPage(BasePage):
    """Класс для работы со страницей поиска"""

    search_results = (By.CSS_SELECTOR, ".search-result, .art-item, [class*='SearchResult']")
    search_results_count = (By.CSS_SELECTOR, ".results-count, [class*='count']")
    first_book = (By.CSS_SELECTOR, ".search-result:first-child, .art-item:first-child")
    first_book_title = (By.CSS_SELECTOR, ".search-result:first-child .title, .art-item:first-child [class*='Title']")
    first_book_author = (By.CSS_SELECTOR, ".search-result:first-child .author, .art-item:first-child [class*='Author']")
    no_results_message = (By.CSS_SELECTOR, ".no-results, [class*='NoResults'], [class*='empty']")
    sort_dropdown = (By.CSS_SELECTOR, ".sort-dropdown, select[name='sort']")
    filter_genre = (By.CSS_SELECTOR, ".filter-genre, [class*='genre']")

    @allure.step("Получение количества результатов поиска")
    def get_results_count(self) -> int:
        """Получить количество результатов поиска"""
        results = self.find_elements(self.search_results)
        return len(results)

    @allure.step("Клик по первой книге в результатах")
    def click_first_book(self):
        """Кликнуть на первую книгу"""
        self.click(self.first_book)

    @allure.step("Получение информации о первой книге")
    def get_first_book_info(self) -> dict:
        """Получить информацию о первой книге"""
        try:
            title = self.get_text(self.first_book_title)
            author = self.get_text(self.first_book_author)
            return {"title": title, "author": author}
        except:
            return {}

    @allure.step("Проверка отображения сообщения 'Нет результатов'")
    def is_no_results_visible(self) -> bool:
        """Проверить видимость сообщения 'Нет результатов'"""
        return self.is_element_visible(self.no_results_message)

    @allure.step("Проверка наличия результатов поиска")
    def has_results(self) -> bool:
        """Проверить наличие результатов"""
        return self.get_results_count() > 0
