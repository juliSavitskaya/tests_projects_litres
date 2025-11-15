import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.clients.litres_client import LitresAPIClient
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from pages.book_page import BookPage


@pytest.fixture(scope="function")
def browser():
    """Фикстура для настройки браузера с Allure attachments"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Для запуска в CI/CD раскомментировать:
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Добавляем attachments в Allure
    allure.attach(
        driver.get_screenshot_as_png(),
        name="Screenshot",
        attachment_type=allure.attachment_type.PNG
    )
    
    allure.attach(
        driver.page_source,
        name="HTML Source",
        attachment_type=allure.attachment_type.HTML
    )
    
    try:
        allure.attach(
            str(driver.get_log('browser')),
            name="Browser Logs",
            attachment_type=allure.attachment_type.TEXT
        )
    except:
        pass
    
    driver.quit()


@pytest.fixture(scope="function")
def litres_client():
    """Фикстура для API клиента"""
    return LitresAPIClient()


@pytest.fixture(scope="function")
def main_page(browser):
    """Фикстура для главной страницы"""
    return MainPage(browser)


@pytest.fixture(scope="function")
def search_page(browser):
    """Фикстура для страницы поиска"""
    return SearchPage(browser)


@pytest.fixture(scope="function")
def cart_page(browser):
    """Фикстура для страницы корзины"""
    return CartPage(browser)


@pytest.fixture(scope="function")
def book_page(browser):
    """Фикстура для страницы книги"""
    return BookPage(browser)


def pytest_configure(config):
    """Конфигурация pytest markers"""
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "regression: regression tests")
    config.addinivalue_line("markers", "ui: UI tests")
    config.addinivalue_line("markers", "api: API tests")
