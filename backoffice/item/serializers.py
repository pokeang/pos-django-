import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Category, Item, StoreItem, Discount
from settings.models import Store


# Custom image field - handles base 64 encoded images
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,') # format ~= data:image/X,
            ext = format.split('/')[-1] # guess file extension
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'category_name', 'category', 'price', 'cost', 'display', 'image', 'image_url')  # '__all__'

        read_only_fields = ('id', 'category_name', 'image_url')


class StoreItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreItem
        fields = ('id', 'store_id', 'item_id', 'item_name', 'price', 'in_stock', 'low_stock', 'date_created')


class StoreWithItemSerializer(serializers.ModelSerializer):
    store_items = StoreItemSerializer(many=True)

    class Meta:
        model = Store
        fields = ('id', 'name', 'store_items')  # '__all__'


class AddCategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    def validate_name(self, name):
        if(Category.objects.filter(name=name).exists()):
            raise serializers.ValidationError('Category name is already exist')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryWithItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'items')  # '__all__'


class AddDiscountSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    def validate_name(self, name):
        if(Discount.objects.filter(name=name).exists()):
            raise serializers.ValidationError('Discount name is already exist')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'name', 'store', 'store_name', 'item', 'item_name', 'value', 'type', 'type_str',
                  'date_start', 'date_end')
        read_only_fields = ('store_name', 'type_str', 'item_name')
