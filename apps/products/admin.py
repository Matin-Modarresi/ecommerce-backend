from django.contrib import admin
from .models import Category, Product, ProductImage, Tag
from django.utils.translation import gettext_lazy as _


class CategoryTreeFilter(admin.SimpleListFilter):
    title = _('Category (Deep Search)')
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        categories = Category.objects.all()
        return [(c.id, c.name) for c in categories]

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            def get_subcategories(category):
                all_subs = [category.id]
                for child in category.children.all():
                    all_subs.extend(get_subcategories(child))
                return all_subs

            try:
                selected_category = Category.objects.get(id=category_id)
                all_ids = get_subcategories(selected_category)
                return queryset.filter(category_id__in=all_ids)
            except Category.DoesNotExist:
                return queryset

        return queryset


class RatingFilter(admin.SimpleListFilter):
    title = 'محدوده امتیاز'
    parameter_name = 'rating_range'

    def lookups(self, request, model_admin):
        return (
            ('excellent', 'عالی(بالای ۴.۵)'),
            ('good', 'خوب (۳ تا ۴.۵)'),
            ('poor', 'ضعیف (زیر ۳)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'excellent':
            return queryset.filter(average_rating__gte=4.5)
        if self.value() == 'good':
            return queryset.filter(average_rating__gte=3, average_rating__lt=4.5)
        if self.value() == 'poor':
            return queryset.filter(average_rating__lt=3)

        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock", "is_active")

    list_filter = ("is_active", CategoryTreeFilter, RatingFilter)

    search_fields = ("name", "sku")

    prepopulated_fields = {"slug": ("name",)}

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)

        return queryset, may_have_duplicates


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "is_primary")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
