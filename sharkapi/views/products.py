# Generate a view for the products endpoint that inherits from the Django REST Framework ViewSet class.
# Start with a list and retrieve method

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sharkapi.models import Product, Category

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Generate a product serializer class that inherits from the Django REST Framework ModelSerializer class.
class PrductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', )

class ProductSerializer(serializers.ModelSerializer):
    category = PrductCategorySerializer(many=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'category',)
