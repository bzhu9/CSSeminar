from django.contrib import admin
from .models import Room


admin.site.register(
    Room,
    list_display=["id", "title"],
    list_display_links=["id", "title"],
)
