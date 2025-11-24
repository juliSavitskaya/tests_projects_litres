import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, browser, timeout=10):
        self.browser = browser
        self.timeout = timeout
        self.wait = WebDriverWait(browser, timeout)

    @allure.step("Открытие страницы: {url}")
    def open(self, url: str):
        """Открыть страницу"""
        self.browser.get(url)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Ожидание загрузки страницы"""
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def find_element(self, locator):
        """Найти элемент с ожиданием"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Найти все элементы"""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return self.browser.find_elements(*locator)
        except TimeoutException:
            return []

    def wait_for_element(self, locator, timeout=None):
        """Ожидание элемента"""
        wait = WebDriverWait(self.browser, timeout or self.timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_element_visible(self, locator, timeout=None):
        """Ожидание видимости элемента"""
        wait = WebDriverWait(self.browser, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=None):
        """Ожидание кликабельности элемента"""
        wait = WebDriverWait(self.browser, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Клик по элементу")
    def click(self, locator):
        """Кликнуть по элементу"""
        element = self.wait_for_element_clickable(locator)
        element.click()

    def is_element_visible(self, locator, timeout=5) -> bool:
        """Проверка видимости элемента"""
        try:
            wait = WebDriverWait(self.browser, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=5) -> bool:
        """Проверка наличия элемента"""
        try:
            wait = WebDriverWait(self.browser, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator) -> str:
        """Получить текст элемента"""
        return self.find_element(locator).text

    def wait_for_url_contains(self, text, timeout=None):
        """Ожидание пока URL содержит текст"""
        wait = WebDriverWait(self.browser, timeout or self.timeout)
        return wait.until(EC.url_contains(text))

    def wait_for_url_changes(self, current_url, timeout=None):
        """Ожидание изменения URL"""
        wait = WebDriverWait(self.browser, timeout or self.timeout)
        return wait.until(EC.url_changes(current_url))