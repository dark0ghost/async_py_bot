# This Python file uses the following encoding: utf-8

from aiogram.types import LabeledPrice, ShippingOption
from typing import List

price: List[LabeledPrice] = [
    LabeledPrice(label="test", amount=100)
]

shipping_options: List[ShippingOption] = [
    ShippingOption(id='instant', title='почта Росси').add(LabeledPrice('3 года', 1000)),
    ShippingOption(id='instant', title='тенькоф').add(LabeledPrice('почта Росси', 1000))
]
