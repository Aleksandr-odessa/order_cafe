from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.order_create, name='order_create'),
    path('<int:pk>/edit/', views.order_update, name='order_update'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('revenue/', views.revenue_report, name='revenue_report'),
    path('search/', views.order_search, name='order_search'),
    path('api/', include(router.urls)),
]
