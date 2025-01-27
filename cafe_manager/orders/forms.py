from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'status']
        widgets = {
            'table_number': forms.NumberInput(attrs={'min': 1, 'max': 50}),
                }

class EditForm(OrderForm):
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            'table_number': forms.NumberInput(attrs={'min': 1, 'max': 50}),
            'items': forms.Textarea(attrs={'rows': 5, 'readonly': 'readonly'}),
            "total_price":forms.NumberInput(attrs={'readonly': 'readonly'})
                }

# class ShowOrder(OrderForm):
#     class Meta:
#         model = Order
#         fields = "__all__"