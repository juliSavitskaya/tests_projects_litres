import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    @allure.step("Открытие страницы: {url}")
    def open(self, url: str):
        """Открыть страницу"""
        self.browser.get(url)

    def find_element(self, locator):
        """Найти элемент"""
        return self.browser.find_element(*locator)

    def find_elements(self, locator):
        """Найти все элементы"""
        return self.browser.find_elements(*locator)

    def wait_for_element(self, locator, timeout=10):
        """Ожидание элемента"""
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    @allure.step("Клик по элементу")
    def click(self, locator):
        """Кликнуть по элементу"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def is_element_visible(self, locator) -> bool:
        """Проверка видимости элемента"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def get_text(self, locator) -> str:
        """Получить текст элемента"""
        return self.find_element(locator).text