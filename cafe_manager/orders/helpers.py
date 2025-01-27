import json
from datetime import datetime
from typing import List, Dict, Tuple, Union, Any

from .config import STATUS

# List of status keys derived from the STATUS configuration
STATUS_KEYS: List[str] = [key for key in STATUS.keys()]

def add_to_db(form: Any, response: str) -> bool:
    """
    Adds an order to the database.

    Parameters:
    - form: The form instance containing order data.
    - response: A JSON string representing the order items.

    Returns:
    - bool: True if the order was successfully saved, False otherwise.
    """
    try:
        order = form.save(commit=False)  # Prepare the order without saving it yet
        order_items: List[Dict[str, Union[str, float]]] = json.loads(response) # Parse JSON response
        if order_items:
            order.items = [{item.get('name'): item.get('price')} for item in order_items]
            order.total_price = sum(item['price'] for item in order_items)
            order.save()  # Save the order to the database
            return True
        else:
            return False
    except (json.JSONDecodeError, KeyError) as e:
        return False  # Return False if there was an error during processing

def create_datetime() -> Tuple[datetime, datetime]:
    """
    Creates start and end datetime objects for the current day.

    Returns:
    - Tuple[datetime, datetime]: A tuple containing the start and end of the current day.
    """
    now: datetime = datetime.today()  # Get the current date and time
    start_of_today: datetime = now.replace(hour=0, minute=0, second=0)  # Start of today
    end_of_today: datetime = now.replace(hour=23, minute=59, second=59)  # End of today
    return start_of_today, end_of_today

def search(criteria: str, Order: Any) -> Any:
    """
    Searches for orders based on given criteria.

    Parameters:
    - criteria: A string representing the search criteria, can be a table number or status.
    - Order: The Order model to query against.

    Returns:
    - QuerySet: A set of orders that match the search criteria.
    """
    if criteria.isdigit():
        # Filter by table number if the criteria is numeric
        search_orders = Order.objects.filter(table_number=criteria)
    else:
        criteria_search: Union[str, None] = None
        match criteria.lower():
            case 'в' | 'd': criteria_search = STATUS_KEYS[0]  # Status key for the status "В ожидании"
            case 'г' | 'u': criteria_search = STATUS_KEYS[1]  # Status key for the status "Готово"
            case 'о' | 'j': criteria_search = STATUS_KEYS[2]  # Status key for the status "Оплачено"
        # Filter by status if criteria matches a known status key
        search_orders = Order.objects.filter(status=criteria_search)
    return search_orders

def create_items_list(items)->str:
    item = [f'{list(item.items())[0][0]}:{list(item.items())[0][1]}' for item in items]
    return " ".join(item)


# List of tuples representing status choices for forms
STATUS_CHOICES: List[Tuple[str, str]] = [(key, value) for key, value in STATUS.items()]

