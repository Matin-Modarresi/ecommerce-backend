from django.contrib import admin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("id", "email", "is_staff", "is_active")
    search_fields = ("email",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "phone_number")
