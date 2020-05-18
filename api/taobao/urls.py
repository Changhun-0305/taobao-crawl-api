from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_product_by_id, name='get_product'),
]