from django.urls import path
from . import views

urlpatterns = [
    # path('created-card-info', CreditCardInfoList.as_view()),
    # path('payment', PaymentList.as_view()),
    path('stores', views.store_list, name="list stores"),
    path('store', views.store_create, name="add stores"),
    path('store/<int:pk>', views.store_GPD, name="get, update, delete store ")
]
