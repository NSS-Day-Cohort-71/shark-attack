# Generate a view for the products endpoint that inherits from the Django REST Framework ViewSet class.
# Start with a list and retrieve method

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sharkapi.models import Product, Category

class CategoriesViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name',)
