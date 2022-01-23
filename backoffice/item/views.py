from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers

from .models import Category, Item, StoreItem, Discount
from .serializers import CategorySerializer, AddCategorySerializer, ItemSerializer, StoreItemSerializer, \
    StoreWithItemSerializer, DiscountSerializer, AddDiscountSerializer
from settings.models import Store
from django.http import JsonResponse
from common.permissions import IsOwnerShopOnlyOrGetOnly, IsOnlySuperUser
from rest_framework.parsers import MultiPartParser, FormParser


# api item
@api_view(['GET'])
def item_list(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
# @user_passes_test(lambda u: u.is_superuser)
@permission_classes([IsOnlySuperUser])
def item_GPD(request, pk):
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        return Response("Item not found !", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:
            serializer = ItemSerializer(item, data=request.data, read_only=False)
            if serializer.is_valid():
                data = request.data
                item.category_id = data['category_id']
                item.name = data['name']
                item.price = data['price']
                item.cost = data['cost']
                if 'image' in data:
                    item.image = data['image']
                item.display = data['display']
                item.save()
                created_serializer = ItemSerializer(item)
                return Response(created_serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response("Item successfully delete")

    elif request.method == 'GET':
        serializer = ItemSerializer(item, many=False)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsOnlySuperUser])
def item_create(request):
    # parser_classes = [MultiPartParser, FormParser]
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        # item = request.data
        # Item.objects.create(**item)
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api category
@api_view(['POST'])
@permission_classes([IsOnlySuperUser])
def category_create(request):
    serializer = ADDCategorySerializer(data=request.data)
    if serializer.is_valid():
        try:
            category = request.data
            Category.objects.create(**category)
            return Response(serializer.data)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOnlySuperUser])
def category_GPD(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response("Category not found !", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:
            serializer = CategorySerializer(category, data=request.data, read_only=False)
            if serializer.is_valid():
                data = request.data
                category.name = data['name']
                category.description = data['description']
                category.save()
                created_serializer = CategorySerializer(category)
                return Response(created_serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response("Category successfully delete")

    elif request.method == 'GET':
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsOnlySuperUser])
class CategoryList(APIView):
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


# api store item
@api_view(['GET'])
@permission_classes([IsOwnerShopOnlyOrGetOnly, IsOnlySuperUser])
def store_items_list(request):
    store_items = StoreItem.objects.all()
    serializer = StoreItemSerializer(store_items, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOwnerShopOnlyOrGetOnly])
def store_item_update_or_delete(request, pk):
    method = request.method
    try:
        store_item = StoreItem.objects.get(id=pk)
    except StoreItem.DoesNotExist:
        return Response("Item not found !", status=status.HTTP_404_NOT_FOUND)

    if method == 'PUT':
        serializer = StoreItemSerializer(store_item, data=request.data)
        if serializer.is_valid():
            data = request.data
            store_item.store_id = data['store_id']
            store_item.item_id = data['item_id']
            store_item.price = data['price']
            store_item.in_stock = data['in_stock']
            store_item.low_stock = data['low_stock']
            store_item.save()
            updated_serializer = StoreItemSerializer(store_item)
            return Response(updated_serializer.data)

    elif method == 'DELETE':
        store_item.delete()
        return Response("Item successfully delete")

    elif method == 'GET':
        serializer = StoreItemSerializer(store_item)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsOwnerShopOnlyOrGetOnly, IsOnlySuperUser])
def store_with_item_list(request):
    if request.user.is_superuser:
        stores = Store.objects.all()
    else:
        stores = Store.objects.filter(store=request.user.store_id)
    serializer = StoreWithItemSerializer(stores, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsOwnerShopOnlyOrGetOnly])
def create_store_items(request):
    store_serializer = StoreWithItemSerializer(data=request.data, read_only=False)
    if store_serializer.is_valid():
        try:
            store_items = request.data["store_items"]
            for store_item in store_items:
                StoreItem.objects.create(**store_item)
            return Response(request.data, status.HTTP_201_CREATED)
        except Exception:
            return Response(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsOwnerShopOnlyOrGetOnly])
def update_store_items(request):

    store_items = request.data["store_items"]
    updated = []
    for store_item in store_items:
        isEdit = False
        try:
            if 'id' not in store_item:
                StoreItem.objects.create(**store_item)
            else:
                store_item_ = StoreItem.objects.get(id=store_item['id'])
                isEdit = True
        except StoreItem.DoesNotExist:
            return Response("Item not found !", status=status.HTTP_404_NOT_FOUND)
        if isEdit:
            store_serializer = StoreItemSerializer(store_item_, data=store_item)
            try:
                if store_serializer.is_valid():
                    store_item_.store_id = store_item['store_id']
                    store_item_.item_id = store_item['item_id']
                    store_item_.price = store_item['price']
                    store_item_.in_stock = store_item['in_stock']
                    store_item_.low_stock = store_item['low_stock']
                    store_item_.save()
                    updated_data = StoreItemSerializer(store_item_)
                    updated.append(updated_data.data)
                else:
                    return Response("Item not found !", status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(updated)


@api_view(['GET'])
@permission_classes([IsOwnerShopOnlyOrGetOnly])
def get_store_item_detail(request, pk):
    try:
        store = Store.objects.get(pk=pk)
    except StoreItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    date = request.query_params.get('date', None)
    if date is not None:
        queryset = StoreItem.objects.filter(store_id=pk, date_created__date=date)

        serializer = StoreItemSerializer(queryset, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsOwnerShopOnlyOrGetOnly])
def get_store_count_item(request):
    data = []
    for item in StoreItem.objects.raw("SELECT sto.id, sto.name as store_name, count(item_id) as total_item, sto.id, DATE(sti.date_created) as date_created FROM store_item_tbl sti INNER JOIN store_tbl sto on sti.store_id = sto.id GROUP BY store_id, Date(date_created)"):
        data.append({
            'id': item.id,
            'name': item.store_name,
            'total_item': item.total_item,
            'date_created': item.date_created
        })

    return JsonResponse(data=data, safe=False)


@api_view(['GET'])
@permission_classes([IsOwnerShopOnlyOrGetOnly])
def get_item_sale(request):
    data = []
    store_id = request.user.store_id
    super_user = request.user.is_superuser
    if super_user:
        sql = '''SELECT it.*, si.in_stock, si.item_id, DATE(si.date_created) AS date_register, 
        (select SUM(drd.amount_sold) from daily_receipt_detail_tbl drd INNER JOIN daily_receipt_tbl dr ON dr.id = drd.daily_receipt_id WHERE DATE(dr.date_sold) = CURRENT_DATE() and drd.item_id = si.item_id GROUP BY drd.item_id, DATE(dr.date_sold)) AS total_item_sold
         FROM item_tbl it 
         LEFT JOIN store_item_tbl si ON it.id = si.item_id 
         WHERE DATE(si.date_created) = CURRENT_DATE() AND it.display=true'''
        for item in Item.objects.raw(sql):
            data.append({
                'id': item.id,
                'name': item.name,
                'display': item.display,
                'price': item.price,
                'image': item.image.url,
                'in_stock': item.in_stock,
                'date_register': item.date_register,
                'total_item_sold': item.total_item_sold
            })
    else:
        sql = '''SELECT it.*, si.in_stock, si.item_id, DATE(si.date_created) AS date_register, 
        (select SUM(drd.amount_sold) from daily_receipt_detail_tbl drd INNER JOIN daily_receipt_tbl dr ON dr.id = drd.daily_receipt_id WHERE dr.store_id = %s AND DATE(dr.date_sold) = CURRENT_DATE() and drd.item_id = si.item_id GROUP BY drd.item_id, DATE(dr.date_sold)) AS total_item_sold
         FROM item_tbl it 
         LEFT JOIN store_item_tbl si ON it.id = si.item_id 
         WHERE DATE(si.date_created) = CURRENT_DATE() AND it.display=true AND si.store_id= %s'''

        for item in Item.objects.raw(sql, [store_id, store_id]):
            data.append({
                'id': item.id,
                'name': item.name,
                'display': item.display,
                'price': item.price,
                'image': item.image.url,
                'in_stock': item.in_stock,
                'date_register': item.date_register,
                'total_item_sold': item.total_item_sold
            })

    return JsonResponse(data=data, safe=False)


# discount api
@api_view(['GET'])
def discount_list(request):
    discount = Discount.objects.all()
    serializer = DiscountSerializer(discount, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsOnlySuperUser])
def discount_create(request):
    serializer = DiscountSerializer(data=request.data)
    if serializer.is_valid():
        # discount = request.data
        # Discount.objects.create(**discount)
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOnlySuperUser])
def discount_GPD(request, pk):

    try:
        discount = Discount.objects.get(id=pk)
    except Discount.DoesNotExist:
        return Response("Discount not found !", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = DiscountSerializer(discount, data=request.data, read_only=False)
        if serializer.is_valid():
            data = request.data
            discount.name = data['name']
            discount.value = data['value']
            discount.store_id = data['store']
            discount.item_id = data['item']
            discount.type = data['type']
            discount.date_start = data['date_start']
            discount.date_end = data['date_end']
            discount.save()
            created_serializer = DiscountSerializer(discount)
            return Response(created_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        discount.delete()
        return Response("Discount successfully delete")

    elif request.method == 'GET':
        serializer = DiscountSerializer(discount, many=False)
        return Response(serializer.data)
