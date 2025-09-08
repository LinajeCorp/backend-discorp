from django.urls import path
from .views import ProductsAPIView

urlpatterns = [
    # Endpoint para consultar productos desde Strapi
    path('products/', ProductsAPIView.as_view(), name='products-list'),
]
