from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from sharkapi.views import ProductViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', ProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls)),
]

