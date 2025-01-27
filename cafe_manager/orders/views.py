from collections import Counter
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets, status
from typing import Any

from rest_framework.response import Response

from .helpers import add_to_db, create_datetime, search, create_items_list
from .serializers import OrderSerializer
from .models import Order, Dish
from .forms import OrderForm, EditForm


def order_list(request: Any) -> render:
    """Render a list of all orders.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML page displaying all orders.
    """
    orders = Order.objects.all()
    orders_show = [model_to_dict(order) for order in orders]
    for order in orders_show:
        order['items'] = create_items_list(order['items'])
    return render(request, 'orders/order_list.html', {'orders_show': orders_show})


def order_create(request: Any) -> render:
    """Create a new order.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML page for creating a new order or redirect to the order list.
    """
    dishes = Dish.objects.all()
    if request.method == "POST":
        response = request.POST.get('items')
        form = OrderForm(request.POST)
        if form.is_valid():
            if add_to_db(form, response):
                return redirect('order_list')
            else:
                return render(request, 'orders/order_form.html',
                              {'form': form, 'dishes': dishes, 'error': 'Необходимо выбрать блюда.'})
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form, 'dishes': dishes})


def order_update(request: Any, pk: int) -> render:
    """Update an existing order.

    Args:
        request: The HTTP request object.
        pk: Primary key of the order to be updated.

    Returns:
        Rendered HTML page for updating the order or redirect to the order list.
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = EditForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form})


def order_delete(request: Any, pk: int) -> render:
    """Delete an existing order.

    Args:
        request: The HTTP request object.
        pk: Primary key of the order to be deleted.

    Returns:
        Rendered HTML page for confirming the deletion or redirect to the order list.
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})


def revenue_report(request: Any) -> render:
    """Generate a report of total revenue from paid orders within a specific time range.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML page displaying total revenue.
    """
    date_time = create_datetime()
    paid_orders = Order.objects.filter(status='paid').filter(created_at__range=(date_time[0], date_time[1]))
    total_revenue = sum(order.total_price for order in paid_orders)
    return render(request, 'orders/revenue_report.html', {'total_revenue': total_revenue})


def order_search(request: Any) -> render:
    """Search for orders based on user-provided criteria.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML page displaying search results or a search form.
    """
    if request.method == "POST":
        criteria = request.POST.get('search')
        result = search(criteria, Order)
        return render(request, 'orders/order_search.html', {'result': result})
    else:
        form = OrderForm()
        return render(request, 'orders/order_search.html', {'form': form})


class OrderViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing orders."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data["total_price"] = sum(value for item in data["items"] for value in item.values())
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
