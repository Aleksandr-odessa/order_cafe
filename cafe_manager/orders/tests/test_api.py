from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = '/orders/api/order/'
        self.order_data = {
            "items": [{"name": "Суп", "price": 12}],
            "table_number": 10,
            "status": "pending"
        }

    def test_get_orders(self):

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):

        response = self.client.post(self.base_url, self.order_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_order_by_id(self):

        create_response = self.client.post(self.base_url, self.order_data, format='json')
        order_id = create_response.data['id']

        response = self.client.get(f'{self.base_url}{order_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['table_number'], 10)

    def test_update_order(self):
        create_response = self.client.post(self.base_url, self.order_data, format='json')
        order_id = create_response.data['id']

        updated_data = {
            "items": [{"name": "Салат", "price": 8}],
            "table_number": 15,
            "status": "paid"
        }
        response = self.client.put(f'{self.base_url}{order_id}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['table_number'], 15)
        self.assertEqual(response.data['status'], 'paid')

    def test_delete_order(self):
        create_response = self.client.post(self.base_url, self.order_data, format='json')
        order_id = create_response.data['id']

        response = self.client.delete(f'{self.base_url}{order_id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'{self.base_url}{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
