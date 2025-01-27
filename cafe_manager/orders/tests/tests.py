import json

from django.test import TestCase, Client
from django.urls import reverse
from cafe_manager.orders.models import Order, Dish
from cafe_manager.orders.forms import OrderForm, EditForm


class OrderViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        Order.objects.create(table_number=1,
                             items={"Pizza": 10},
                             total_price=10.00,
                             status='pending')
        Order.objects.create(table_number=2,
                             items={"Sushi": 15},
                             total_price=15.00,
                             status='completed')

    def test_order_list(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertEqual(len(response.context['orders']), 2)
        self.assertEqual(response.context['orders'][1].table_number,
                     2)
        self.assertEqual(response.context['orders'][1].total_price,
                     15.00)
        self.assertEqual(response.context['orders'][1].status,
                     'completed')


    def test_order_create_get(self):
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_form.html')

    def test_order_create_post(self):
        response = self.client.post(reverse('order_create'), {
           "items": '[{"name":"Суп","price":12}]', 'table_number':'1', 'status':"pending"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('order_list'))
        self.assertEqual(Order.objects.count(), 3)
        order = Order.objects.first()
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.items, {"Pizza": 10})
        self.assertEqual(order.total_price, 10.00)

    def test_order_search(self):
        response = self.client.get(reverse('order_search'))
        self.assertEqual(response.status_code, 200)

    def test_revenue_report(self):
        response = self.client.get(reverse('revenue_report'))
        self.assertEqual(response.status_code, 200)

    # def test_order_update(self):
    #     response = self.client.get(reverse('order_update'))
    #     self.assertEqual(response.status_code, 200)
