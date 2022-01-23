# from django.db import models
# from django.contrib.auth.models import User
# from settings.models import Store
#
# # Create your models here.
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     store = models.OneToOneField(Store, on_delete=models.CASCADE, null=True)
#     phone = models.CharField(max_length=50)
#     salary = models.IntegerField(default=0)
#     dob = models.DateField(auto_now_add=False, blank=True, null=True)
#     fb_name = models.CharField(max_length=45, blank=True)
#     address = models.CharField(max_length=200, blank=True)
#     image = models.ImageField(default='default.png', upload_to='profile_images')
#
#     def store_name(self):
#         return self.store
#
#     def __str__(self):
#         return f'{self.user.username}-Profile'
