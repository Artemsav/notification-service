from django.urls import path

from .views import ClientSerializers


app_name = 'mailing'

urlpatterns = [
    path('products/', ClientSerializers),
    path('banners/', ClientSerializers),
    path('order/', ClientSerializers),
]
