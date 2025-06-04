from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cards.urls')),  # Inclui as URLs da app 'cards'
    path('', include('accounts.urls')), # Inclui as URLs do app 'accounts'
]
