from django.contrib import admin

from bookmarks.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('favourite',)}
