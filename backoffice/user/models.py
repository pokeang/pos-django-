from django.db import models
from django.contrib.auth.models import PermissionsMixin, User
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.safestring import mark_safe
from django.utils import timezone
from settings.models import Store
from simple_history.models import HistoricalRecords
from simple_history import register

# after register user generate token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# register(User, app=__package__)


class UserManager(BaseUserManager):

    def _create_user(self, username, password, email, is_staff, is_superuser, is_shop_manager, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, password=password, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, is_shop_manager=is_shop_manager, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        User.history.all()
        return user

    def create_user(self, username, password=None, email=None,  is_staff=False, is_shop_manager=False, **extra_fields):
        if is_shop_manager is None:
            is_shop_manager = False
        return self._create_user(username, password, email,  is_staff, False, is_shop_manager, **extra_fields)
    #
    # def create_shop_manager_user(self, username, email=None, password=None, store=None, **extra_fields):
    #     return self._create_user(username, email, password, True, False, True, store, **extra_fields)

    def create_superuser(self, username, password, email=None, **extra_fields):
        user = self._create_user(username, password, email, True, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    fb_name = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_shop_manager = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    receive_newsletter = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=300,  blank=True, null=True)
    city = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    salary = models.IntegerField(default=0, null=True)
    about_me = models.TextField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to='user', null=True, blank=True)
    history = HistoricalRecords()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email', ]

    def profile_image_preview(self):
        if self.profile_image:
            return mark_safe('<img src="{}" style="width: 65px; height:65px;" style="object-fit:contain" />'.format(self.profile_image.url))
        return '(No image)'
    profile_image_preview.allow_tags = True
    profile_image_preview.short_description = 'Profile Image'

    class Meta:
        db_table = 'auth_user'

    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def create_auth_token(sender, instance=None, created=False, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)
