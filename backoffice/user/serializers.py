
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from backoffice import settings
from .models import User
from allauth.account.utils import setup_user_email


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    username = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=False)
    salary = serializers.CharField(required=False)
    is_shop_manager = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    store = serializers.CharField(required=True, )
    address = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    fb_name = serializers.CharField(required=False)
    profile_image = serializers.ImageField(use_url=True, required=False)

    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_phone(self, phone):
        if(User.objects.filter(phone=phone).exists()):
            raise serializers.ValidationError('Phone number already exists')
        return phone

    def validate_username(self, username):
        if(User.objects.filter(username=username).exists()):
            raise serializers.ValidationError('User already exists')
        return username

    def validate_email(self, email):
        if(User.objects.filter(email=email).exists()):
            raise serializers.ValidationError('Email address already exists')
        return email

    def validate_fb_name(self, fb_name):
        if(User.objects.filter(fb_name=fb_name).exists()):
            raise serializers.ValidationError('Facebook name already exists')
        return fb_name

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            'address': self.validated_data.get('address', ''),
            'user_type': self.validated_data.get('user_type', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'store_id': self.validated_data.get('store_id', ''),
            'phone': self.validated_data.get('phone', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        # setup_user_email(request, user, [])

        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = ('pk', 'store', 'username', 'email', 'salary', 'birth_date', 'address', 'phone', 'fb_name',
                  'is_superuser', 'is_shop_manager', 'is_staff', 'about_me', 'profile_image_preview')
        read_only_fields = ('email', )
