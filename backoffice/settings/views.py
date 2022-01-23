from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import CreditCardInfo, Payment, Store
from .serializers import CreditCardInfoSerializer, PaymentSerializer, StoreSerializer
from settings.models import Store
from common.permissions import IsOwnerShopOnlyOrGetOnly, IsOnlySuperUser


@permission_classes([IsOnlySuperUser])
class CreditCardInfoList(generics.ListCreateAPIView):
    queryset = CreditCardInfo.objects.all()
    serializer_class = CreditCardInfoSerializer


@permission_classes([IsOnlySuperUser])
class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# api store
@api_view(['GET'])
def store_list(request):
    if request.user.is_superuser:
        queryset = Store.objects.all()
    else:
        queryset = Store.objects.filter(id=request.user.store_id)
    serializer_class = StoreSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOnlySuperUser])
def store_GPD(request, pk):
    try:
        store = Store.objects.get(id=pk)
    except Store.DoesNotExist:
        return Response("Store not found !", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:
            serializer = StoreSerializer(store, data=request.data, read_only=False)
            if serializer.is_valid():
                data = request.data
                store.name = data['name']
                store.phone_number = data['phone_number']
                store.address = data['address']
                store.description = data['description']
                store.save()
                created_serializer = StoreSerializer(store)
                return Response(created_serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        store.delete()
        return Response("Store successfully delete")

    elif request.method == 'GET':
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsOnlySuperUser])
def store_create(request):
    serializer = StoreSerializer(data=request.data)
    if serializer.is_valid():
        try:
            store = request.data
            Store.objects.create(**store)
            return Response(serializer.data)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


