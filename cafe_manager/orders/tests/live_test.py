import requests

base_url = 'http://127.0.0.1:8000/orders/api/order'

# 1. Получить список всех заказов
def get_all_orders():
    response = requests.get(f'{base_url}/')
    if response.status_code == 200:
        print('Список всех заказов:', response.json())
    else:
        print('Ошибка при получении заказов:', response.status_code)


# 2. Создать новый заказ
def create_order(order_data):
    response = requests.post(f'{base_url}/', json=order_data)
    if response.status_code == 201:
        print('Заказ создан:', response.json())
    else:
        print('Ошибка при создании заказа:', response.status_code)


# 3. Получить конкретный заказ по ID
def get_order_by_id(order_id):
    response = requests.get(f'{base_url}/{order_id}/')
    if response.status_code == 200:
        print('Заказ:', response.json())
    else:
        print('Ошибка при получении заказа:', response.status_code)


# 4. Обновить конкретный заказ по ID
def update_order(order_id, order_data):
    response = requests.put(f'{base_url}/{order_id}/', json=order_data)  # Убедитесь, что есть / в конце
    if response.status_code == 200:
        print('Заказ обновлен:', response.json())
    else:
        print(f'Ошибка при обновлении заказа: {response.status_code}, текст ошибки: {response.text}')


# 5. Удалить конкретный заказ по ID
def delete_order(order_id):
    response = requests.delete(f'{base_url}/{order_id}/'
                               f'')
    if response.status_code == 204:
        print('Заказ удален')
    else:
        print('Ошибка при удалении заказа:', response.status_code)


new_order = {
    "items": [{"Soup" : 15}, {"Pizza": 24}],
    "table_number": 25,
    "status": "pending"
}

updated_order = {
    "items": [{"Soup": 12}, {"Pizza": 24}],
    "table_number": 25,
    "status": "paid"
}

order_id = 45

get_all_orders()
create_order(new_order)
update_order(order_id, updated_order)
get_order_by_id(order_id)
delete_order(order_id)
