from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoryList.as_view(), name="list category"),
    path('category', views.category_create, name="create category"),
    path('category/<int:pk>', views.category_GPD, name="category-detail, update, delete"),

    path('items', views.item_list, name="list item"),
    path('item', views.item_create, name="add item"),
    path('item/<int:pk>', views.item_GPD, name="item-detail, update, delete"),
    path('item-sale', views.get_item_sale, name="list item is selling"),

    path('store-item', views.store_items_list, name="store items list"),
    path('store-item/<int:pk>', views.store_item_update_or_delete, name="store item update or delete"),
    path('store-items', views.store_with_item_list, name="store with items count list"),
    path('store-item-multiple-add', views.create_store_items),
    path('store-item-multiple-update', views.update_store_items),
    path('get_store_count_item', views.get_store_count_item),
    path('get_store_item_detail/<int:pk>', views.get_store_item_detail),

    path('discounts', views.discount_list, name="list discount"),
    path('discount', views.discount_create, name="create discount"),
    path('discount/<int:pk>', views.discount_GPD, name="discount detail, update, delete"),

]
#