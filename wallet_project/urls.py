from django.urls import path, include


urlpatterns = [
    path('api/v1/wallets/', include('wallets.urls')),
]
