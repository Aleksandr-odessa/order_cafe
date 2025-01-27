from django.db import models

from .config import STATUS
from .helpers import STATUS_CHOICES, create_items_list


class Order(models.Model):

    table_number = models.IntegerField(verbose_name="Номер стола", default=1)
    items = models.JSONField(verbose_name="Список блюд", default=dict) # (список заказанных блюд с ценами)
    total_price = models.DecimalField(
        verbose_name="Общая стоимость", max_digits=10, decimal_places=2, default=0
    )
    status = models.CharField(
        verbose_name="Статус заказа", max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = STATUS.get(self.status)
        return (f"Стол {self.table_number} Заказано: {create_items_list(self.items)}"
                f" Заказано на сумму {self. total_price} руб.  Статус заказа - {status} "
                )

class Dish(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название блюда")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена блюда")

    def __str__(self):
        return self.name
