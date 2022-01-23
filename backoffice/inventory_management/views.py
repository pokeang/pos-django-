from rest_framework.decorators import api_view
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from settings.models import Store
from .models import DailyReceipt, DailyReceiptDetail
from .serializers import DailyReceiptSerializer, DailyReceiptSerializer, DailyReceiptsDetailSerializer, \
    DailyReceiptDetailSerializer


@api_view(['GET'])
def daily_receipt_list(request):
    data = request.query_params
    if data.get('store_id') and data.get('date'):
        daily_receipt_items = DailyReceipt.objects.filter(store=data.get('store_id'), date_sold__date=data.get('date'))
    elif data.get('store_id'):
        daily_receipt_items = DailyReceipt.objects.filter(store=data.get('store_id'))
    elif data.get('date'):
        daily_receipt_items = DailyReceipt.objects.filter(date_sold__date=data.get('date'))
    else:
        daily_receipt_items = DailyReceipt.objects.all()
    serializer = DailyReceiptsDetailSerializer(daily_receipt_items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_daily_receipt(request):
    daily_receipt_items_serializer = DailyReceiptsDetailSerializer(data=request.data, read_only=False)
    if daily_receipt_items_serializer.is_valid():
        try:
            daily_receipt = DailyReceiptSerializer(data=request.data)
            if daily_receipt.is_valid():

                daily_receipt_saved = DailyReceipt.objects.create(store=daily_receipt.validated_data["store"])
                # daily_receipt_saved.save()
                # daily_receipt_ = DailyReceipt.objects.get(pk=daily_receipt_saved.id)

                daily_receipt_items = daily_receipt_items_serializer.validated_data["daily_receipt_items"]
                for daily_receipt_data in daily_receipt_items:
                    daily_receipt_data["daily_receipt"] = daily_receipt_saved
                    DailyReceiptDetail.objects.create(**daily_receipt_data)
                return Response("saved successful", status.HTTP_201_CREATED)
        except Exception:
            return Response(daily_receipt_items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(daily_receipt_items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def daily_receipt_by_id(request, pk):
    method = request.method
    try:
        daily_receipt_items = DailyReceipt.objects.get(id=pk)
    except DailyReceipt.DoesNotExist:
        return Response("Item not found !", status=status.HTTP_404_NOT_FOUND)

    if method == 'DELETE':
        daily_receipt_items.delete()
        return Response("daily receipt successfully delete")

    elif method == 'GET':
        serializer = DailyReceiptSerializer(daily_receipt_items)
        return Response(serializer.data)


@api_view(['DELETE', 'PUT'])
def daily_receipt_detail_bulk_delete(request, pk_ids):
    ids = [int(pk) for pk in pk_ids.split(',')]
    daily_receipt_items = DailyReceiptDetail.objects.filter(id__in=ids)
    if daily_receipt_items.count() > 0:
        daily_receipt_items.delete()
        return Response("daily receipt detail successfully delete")
    return Response("Item not found !", status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def daily_receipt_detail_bulk_update(request):
    print(request.data)
    for daily_receipt_detail in request.data:
        _daily_receipt_detail = DailyReceiptDetail.objects.get(id=daily_receipt_detail['id'])
        serializer = DailyReceiptDetailSerializer(_daily_receipt_detail, data=daily_receipt_detail)
        if serializer.is_valid:
            _daily_receipt_detail.amount_sold = daily_receipt_detail['amount_sold']
            _daily_receipt_detail.price = daily_receipt_detail['price']
            _daily_receipt_detail.save()
    return Response(request.data)


@api_view(['DELETE', 'PUT'])
def daily_receipt_detail_DP(request, pk):
    method = request.method
    try:
        daily_receipt_detail = DailyReceiptDetail.objects.get(id=pk)

    except DailyReceipt.DoesNotExist:
        return Response("Item not found !", status=status.HTTP_404_NOT_FOUND)

    if method == 'DELETE':
        daily_receipt_detail.delete()
        return Response("daily receipt detail successfully delete")
    elif method == 'PUT':
        serializer = DailyReceiptDetail(daily_receipt_detail, data=request.data)
        if serializer.is_valid():
            data = request.data
            daily_receipt_detail.amount_sold = data['amount_sold']
            daily_receipt_detail.price = data['price']
            updated_serializer = DailyReceiptDetail(daily_receipt_detail)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
