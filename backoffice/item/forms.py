from django import forms
from .models import Item, StoreItem, Category


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ItemStoreForm(forms.ModelForm):
    class Meta:
        model = StoreItem
        fields = ['store', 'item', 'price', 'in_stock', 'low_stock']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
