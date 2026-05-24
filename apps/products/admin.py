from django.contrib import admin, messages
from .models import Category, Product, ProductImage, Tag
from django.utils.translation import gettext_lazy as _
from django import forms
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import path
from decimal import Decimal


class DiscountForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    percent = forms.DecimalField(
        label=_("Discount percent"),
        min_value=Decimal("0.0"),
        max_value=Decimal("100.0"),
        decimal_places=2,
    )


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
    actions = ["apply_discount"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("apply-discount/",
                 self.admin_site.admin_view(self.apply_discount_view),
                 name="products_apply_discount")
        ]
        return custom_urls + urls

    @admin.action(description=_("Apply discount to selected products..."))
    def apply_discount(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return redirect(f"apply-discount/?ids={','.join(map(str, selected))}")

    def apply_discount_view(self, request):
        ids = request.GET.get("ids", "")
        id_list = [int(x) for x in ids.split(",") if x.strip().isdigit()]

        if request.method == "POST":
            form = DiscountForm(request.POST)
            if form.is_valid():
                percent = form.cleaned_data["percent"]
                multiplier = (Decimal("100.0") - percent) / Decimal("100.0")

                with transaction.atomic():
                    qs = Product.objects.select_for_update().filter(pk__in=id_list)
                    # bulk update سریع: ولی باید قیمت جدید را محاسبه کنیم
                    for p in qs:
                        p.price = (p.price * multiplier).quantize(Decimal("0.01"))
                        p.save(update_fields=["price"])

                self.message_user(request, _("Discount applied successfully."), messages.SUCCESS)
                return redirect("../")  # برگشت به لیست محصول
        else:
            form = DiscountForm(initial={"_selected_action": id_list})

        context = dict(
            self.admin_site.each_context(request),
            title=_("Apply Discount"),
            form=form,
            ids=ids,
        )
        return render(request, "admin/products/apply_discount.html", context)

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)

        return queryset, may_have_duplicates


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "is_primary")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
