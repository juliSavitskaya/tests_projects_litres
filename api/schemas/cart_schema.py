"""JSON схема для валидации ответа API корзины"""

CART_SCHEMA = {
    "type": "object",
    "properties": {
        "payload": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "title": {"type": "string"},
                            "price": {"type": "number"},
                            "quantity": {"type": "integer"}
                        }
                    }
                },
                "total": {"type": "number"}
            }
        }
    }
}

EMPTY_CART_SCHEMA = {
    "type": "object",
    "properties": {
        "payload": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "maxItems": 0
                }
            },
            "required": ["data"]
        }
    },
    "required": ["payload"]
}
