import requests
import logging
import allure
import json
from typing import Dict, Any
from datetime import datetime


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class LitresAPIClient:
    """API клиент для Litres с логированием и Allure attachments"""

    def __init__(self, base_url: str = "https://api.litres.ru/foundation/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept': 'application/json',
        })

    def _log_request(self, method: str, url: str, **kwargs):
        """Логирование запроса"""
        logger.info(f"{method} {url}")
        if 'json' in kwargs:
            logger.info(f"Request body: {json.dumps(kwargs['json'], ensure_ascii=False)}")
        if 'params' in kwargs:
            logger.info(f"Request params: {kwargs['params']}")

    def _log_response(self, response: requests.Response):
        """Логирование ответа"""
        logger.info(f"Status code: {response.status_code}")
        logger.info(f"Response time: {response.elapsed.total_seconds()}s")
        try:
            logger.info(f"Response body: {json.dumps(response.json(), ensure_ascii=False)}")
        except:
            logger.info(f"Response body: {response.text}")

    def _attach_to_allure(self, response: requests.Response, request_data: dict = None):
        """Добавление request/response в Allure отчет"""
        # Request
        if request_data:
            allure.attach(
                json.dumps(request_data, indent=2, ensure_ascii=False),
                name="Request",
                attachment_type=allure.attachment_type.JSON
            )
        
        # Response
        try:
            response_json = response.json()
            allure.attach(
                json.dumps(response_json, indent=2, ensure_ascii=False),
                name="Response",
                attachment_type=allure.attachment_type.JSON
            )
        except:
            allure.attach(
                response.text,
                name="Response",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Curl command
        curl_command = f"curl -X {response.request.method} '{response.request.url}'"
        if response.request.body:
            curl_command += f" -d '{response.request.body.decode() if isinstance(response.request.body, bytes) else response.request.body}'"
        allure.attach(
            curl_command,
            name="Curl",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.step("GET {endpoint}")
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Выполнить GET запрос"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("GET", url, **kwargs)
        
        response = self.session.get(url, **kwargs)
        
        self._log_response(response)
        self._attach_to_allure(response, kwargs.get('params'))
        
        return response

    @allure.step("POST {endpoint}")
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Выполнить POST запрос"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("POST", url, **kwargs)
        
        response = self.session.post(url, **kwargs)
        
        self._log_response(response)
        self._attach_to_allure(response, kwargs.get('json'))
        
        return response

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Выполнить DELETE запрос"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("DELETE", url, **kwargs)
        
        response = self.session.delete(url, **kwargs)
        
        self._log_response(response)
        self._attach_to_allure(response)
        
        return response

    @allure.step("Получить корзину")
    def get_cart(self) -> requests.Response:
        """Получить корзину"""
        return self.get("/cart/arts")

    @allure.step("Добавить книгу {book_id} в корзину")
    def add_to_cart(self, book_id: int) -> requests.Response:
        """Добавить книгу в корзину"""
        return self.post("/cart/add/", json={"art_id": book_id})

    @allure.step("Очистить корзину")
    def clear_cart(self) -> requests.Response:
        """Очистить корзину"""
        return self.post("/cart/clear/")

    @allure.step("Удалить книгу {book_id} из корзины")
    def remove_from_cart(self, book_id: int) -> requests.Response:
        """Удалить книгу из корзины"""
        return self.delete(f"/cart/{book_id}/")

    @allure.step("Поиск книг по запросу '{query}'")
    def search_books(self, query: str, limit: int = 10) -> requests.Response:
        """Поиск книг"""
        params = {'q': query, 'limit': limit}
        return self.get("/search/", params=params)

    @allure.step("Получить детали книги {book_id}")
    def get_book_details(self, book_id: int) -> requests.Response:
        """Получить детали книги"""
        return self.get(f"/books/{book_id}/")

    @allure.step("Получить избранное")
    def get_favorites(self) -> requests.Response:
        """Получить избранное"""
        return self.get("/my-books/favorite/")

    @allure.step("Получить категории каталога")
    def get_catalog_categories(self) -> requests.Response:
        """Получить категории каталога"""
        return self.get("/catalog/categories/")

    @allure.step("Получить книги по категории {category_id}")
    def get_books_by_category(self, category_id: int, limit: int = 20) -> requests.Response:
        """Получить книги по категории"""
        params = {'category': category_id, 'limit': limit}
        return self.get("/catalog/books/", params=params)
