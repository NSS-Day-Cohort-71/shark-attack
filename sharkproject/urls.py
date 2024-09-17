from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from sharkapi.views import ProductViewSet, CategoriesViewSet, CartViewSet
from sharkapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoriesViewSet, basename='category')
router.register(r'cart', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user), # Enables http://localhost:8000/register
    path('login', login_user), # Enables http://localhost:8000/login
]
