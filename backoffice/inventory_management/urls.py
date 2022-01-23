from django.urls import path
from . import views

urlpatterns = [
    path('receipts-list', views.daily_receipt_list, name="list daily receipts"),
    path('receipts', views.create_daily_receipt, name="add"),
    path('receipts/<int:pk>', views.daily_receipt_by_id, name="detail, update, delete"),
    path('remove-detail-receipts/<str:pk_ids>', views.daily_receipt_detail_bulk_delete, name="batch delete"),
    path('remove-detail-receipt/<int:pk>', views.daily_receipt_detail_DP, name="delete daily receipts detail one by one"),
    path('update-detail-receipts', views.daily_receipt_detail_bulk_update, name="batch update"),
]
