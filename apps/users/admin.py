from django.contrib import admin
from django.db.models import F, Value
from django.db.models.functions import Concat
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_staff", "is_active", "name")
    search_fields = ("email",)

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .annotate(
            name=Concat(F('first_name'), Value(' '), F('last_name'))
        )

    @admin.display(ordering='name', description='custom name')
    def name(self, user):
        return user.name


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone_number")
