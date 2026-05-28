from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('apps.products.api.urls')),
    path("api/v1/users/", include("apps.users.api.urls")),
    path("api/v1/cart/", include("apps.cart.api.urls")),
    path("api/v1/payments/", include("apps.payments.api.urls")),
]
