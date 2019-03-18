import uuid
from django.conf import settings
from yandex_checkout import Configuration, Payment


def payment_formation(order):
    Configuration.account_id = settings.YANDEX_SHOP_ID
    Configuration.secret_key = settings.YANDEX_SECRET_KEY
    independent_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": order.amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://expertsovet.com"
        },
        "receipt": {
            "email": order.email,
            "payment_subject": order.good.payment_subject,
            "payment_mode": order.good.payment_mode,
            "items": [
                {
                    "description": order.good.subtitle[:128],
                    "quantity": 1,
                    "amount": {
                        "value": order.amount,
                        "currency": "RUB"
                    },
                    "vat_code": "1",
                }
            ]
        },
        "description": f"Заказ №{order.id}"
    }, independent_key)
    return payment
