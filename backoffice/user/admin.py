from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class CustomerUserAdmin(UserAdmin):
    search_fields = ('username', 'email', 'first_name')
    list_filter = ('is_active', 'is_staff', 'is_shop_manager')
    ordering = ('-date_joined',)
    list_display = ('profile_image_preview', 'username', 'email', 'date_joined', 'last_login', 'store', 'is_staff', 'is_active')

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Extra User profile',
            {
                'fields': (
                    'is_shop_manager',
                    'fb_name',
                    'phone',
                    'store',
                    'salary',
                    'address',
                    'city',
                    'about_me',
                    'profile_image',
                )
            }
        )
    )
    # fieldsets = ((None, {'fields': ('email', 'username', 'first_name',)}),
    #              ('Permissions', {'fields': ('is_staff', 'is_active')}),
    #              ('Personal', {'fields': ('about_me', 'profile_image')})
    #             )


admin.site.register(User, CustomerUserAdmin)
