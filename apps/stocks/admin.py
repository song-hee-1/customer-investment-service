from django.contrib import admin

from .models import Stock, AssetGroup

admin.site.register(Stock)
admin.site.register(AssetGroup)
