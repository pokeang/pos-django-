from rest_framework import generics
from django.shortcuts import render, redirect
from .models import Category, Item, StoreItem
from .serializers import CategorySerializer, ItemSerializer, StoreItemSerializer
from django.contrib.auth.models import User
from .forms import ItemForm, ItemStoreForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from common.decorators import auth_users, allowed_users


# Create your views here.
@login_required(login_url='user-login')
def index(request):
    item = Item.objects.all()
    item_count = item.count()

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee = request.user
            obj.save()
            return redirect('item-index')
    else:
        form = ItemForm()
    context = {
        'form': form,
        'items': item,
        'item_count': item_count
    }
    return render(request, 'item/index.html', context)


@login_required(login_url='user-login')
def detail(request):
    item = Item.objects.all()

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee = request.user
            obj.save()
            return redirect('item-index')
    else:
        form = ItemForm()
    context = {
        'form': form,
        'items': item
    }
    return render(request, 'item/detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def edit(request, pk):
    item = Item.objects.get(id=pk)
    print(request.method)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('item-index')
    else:
        form = ItemForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'item/edit.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def delete(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item-index')
    context = {
        'form': item
    }
    return render(request, 'item/delete.html', context)


@login_required(login_url='user-login')
def item_store(request):
    store_items = StoreItem.objects.all()
    # item = Item.objects.filter(item=store_item)
    # item_count = item.count()
    if request.method == 'POST':
        form = ItemStoreForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee = request.user
            obj.save()
            return redirect('item-store-index')
    else:
        form = ItemStoreForm()
    context = {
        'form': form,
        'store_items': store_items
    }
    return render(request, 'item/item-store.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def item_store_edit(request, pk):
    store_item = StoreItem.objects.get(id=pk)
    if request.method == 'POST':
        form = ItemStoreForm(request.POST, instance=store_item)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('item-store-index')
    else:
        form = ItemStoreForm(instance=store_item)
    context = {
        'form': form
    }
    return render(request, 'item/item-store-edit.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def item_store_delete(request, pk):
    store_item = StoreItem.objects.get(id=pk)
    if request.method == 'POST':
        store_item.delete()
        return redirect('item-store-index')
    context = {
        'form': store_item
    }
    return render(request, 'item/item-store-delete.html', context)


@login_required(login_url='user-login')
def category(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee = request.user
            obj.save()
            return redirect('category-index')
    else:
        form = CategoryForm()
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'item/category.html', context)


# api
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class StoreItemList(generics.ListCreateAPIView):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer


