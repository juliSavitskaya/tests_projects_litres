"""JSON схема для валидации ответа API поиска"""

SEARCH_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "books": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "price": {"type": "number"},
                    "rating": {"type": "number"}
                },
                "required": ["id", "title"]
            }
        },
        "total": {"type": "integer", "minimum": 0}
    },
    "required": ["books", "total"]
}

BOOK_DETAILS_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "author": {"type": "string"},
        "description": {"type": "string"},
        "price": {"type": "number"},
        "isbn": {"type": "string"}
    },
    "required": ["id", "title", "author"]
}
