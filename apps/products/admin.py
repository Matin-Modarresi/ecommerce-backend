from django.contrib import admin
from .models import Category, Product, ProductImage, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "price", "stock", "is_active")

    list_filter = ("is_active", "category")

    search_fields = ("name", "sku")

    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = ("id", "product", "is_primary")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}
