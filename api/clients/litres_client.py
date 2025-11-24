import requests
import logging
import allure
import json
from typing import List

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ==================== API ENDPOINTS ====================
BASE_URL = "https://api.litres.ru/foundation/api"

# Cart endpoints
CART_ADD = "/cart/arts/add"
CART_REMOVE = "/cart/arts/remove"

# Wishlist/Cart view endpoint
WISHLIST_ARTS = "/wishlist/arts"

# Search endpoints
SEARCH = "/search"

# Books endpoints
BOOK_DETAILS = "/arts/{art_id}"


class LitresAPIClient:
    """API клиент для Litres с логированием и Allure attachments"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Version': '2',
            'Content-Type': 'application/json',
            'app-id': '115',
            'client-host': 'www.litres.ru',
            'ui-language-code': 'ru',
            'ui-currency': 'RUB',
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
        if request_data:
            allure.attach(
                json.dumps(request_data, indent=2, ensure_ascii=False),
                name="Request",
                attachment_type=allure.attachment_type.JSON
            )

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

    # ==================== HTTP METHODS ====================

    @allure.step("GET {endpoint}")
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Выполнить GET запрос"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("GET", url, **kwargs)
        response = self.session.get(url, **kwargs)
        self._log_response(response)
        self._attach_to_allure(response, kwargs.get('params'))
        return response

    @allure.step("PUT {endpoint}")
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Выполнить PUT запрос"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("PUT", url, **kwargs)
        response = self.session.put(url, **kwargs)
        self._log_response(response)
        self._attach_to_allure(response, kwargs.get('json'))
        return response

    # ==================== CART METHODS ====================

    @allure.step("Получить корзину")
    def get_cart(self, limit: int = 10) -> requests.Response:
        """Получить содержимое корзины"""
        params = {
            'art_groups': [1, 2, 8],
            'limit': limit
        }
        return self.get(WISHLIST_ARTS, params=params)

    @allure.step("Добавить книги в корзину: {art_ids}")
    def add_to_cart(self, art_ids: List[int]) -> requests.Response:
        """Добавить книги в корзину"""
        return self.put(CART_ADD, json={"art_ids": art_ids})

    @allure.step("Удалить книги из корзины: {art_ids}")
    def remove_from_cart(self, art_ids: List[int]) -> requests.Response:
        """Удалить книги из корзины"""
        return self.put(CART_REMOVE, json={"art_ids": art_ids})

    # ==================== SEARCH METHODS ====================

    @allure.step("Поиск книг по запросу '{query}'")
    def search_books(self, query: str, limit: int = 24, offset: int = 0) -> requests.Response:
        """Поиск книг"""
        params = {
            'q': query,
            'limit': limit,
            'offset': offset,
            'is_for_pda': 'false',
            'show_unavailable': 'false',
            'types': ['text_book', 'audiobook', 'podcast']
        }
        return self.get(SEARCH, params=params)

    # ==================== BOOKS METHODS ====================

    @allure.step("Получить детали книги {art_id}")
    def get_book_details(self, art_id: int) -> requests.Response:
        """Получить детали книги"""
        endpoint = BOOK_DETAILS.format(art_id=art_id)
        return self.get(endpoint)