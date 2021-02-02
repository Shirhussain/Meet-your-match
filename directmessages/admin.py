from django.contrib import admin
from .models import DirectMessage


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    class Meta:
        model = DirectMessage
