from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def open(self, url):
        """Открытие страницы по URL"""
        self.browser.get(url)

    def find_element(self, locator):
        """Поиск элемента на странице"""
        return self.browser.find_element(*locator)

    def find_elements(self, locator):
        """Поиск всех элементов по локатору"""
        return self.browser.find_elements(*locator)

    def is_element_visible(self, locator, timeout=10):
        """Проверка видимости элемента"""
        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except:
            return False

    def is_element_present(self, locator, timeout=10):
        """Проверка наличия элемента в DOM"""
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False

    def wait_for_element(self, locator):
        """Ожидание появления элемента"""
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        """Кликнуть на элемент"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def input_text(self, locator, text: str):
        """Ввести текст"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        """Получить текст элемента"""
        return self.find_element(locator).text
