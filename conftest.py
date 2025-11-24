import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from api.clients.litres_client import LitresAPIClient
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from pages.book_page import BookPage
from utils import attach

# Загружаем переменные окружения из .env файла
load_dotenv()


@pytest.fixture(scope='function')
def browser():
    """Фикстура для настройки браузера через Selenoid"""
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "enableLog": True
        },
        "goog:loggingPrefs": {"browser": "ALL"}
    }
    options.capabilities.update(selenoid_capabilities)

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options
    )
    driver.implicitly_wait(10)

    yield driver

    # Добавляем attachments в Allure
    attach.add_screenshot(driver)
    attach.add_logs(driver)
    attach.add_html(driver)
    attach.add_video(driver)

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