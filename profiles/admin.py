from django.contrib import admin
from .models import Address, Job, UserPicture


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    class Meta:
        model = Address

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    class Meta:
        model = Job 


@admin.register(UserPicture)
class UserPictureAdmin(admin.ModelAdmin):
    class Meta:
        model = UserPicture
