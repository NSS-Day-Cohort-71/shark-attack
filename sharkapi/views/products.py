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
        # Get all product details from request body
        name = request.data.get("name", None)
        description = request.data.get("description", None)
        price = request.data.get("price", None)
        stock = request.data.get("stock", None)
        category_id = request.data.get("category_id", None)

        if name is None or description is None or price is None or stock is None or category_id is None:
            return Response({"message": "Please provide all product details"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a category object
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a new product object
        product = Product()
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.category = category
        product.save()

        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        # Get all product details from request body
        name = request.data.get("name", None)
        description = request.data.get("description", None)
        price = request.data.get("price", None)
        stock = request.data.get("stock", None)
        category_id = request.data.get("category_id", None)

        if name is None or description is None or price is None or stock is None or category_id is None:
            return Response({"message": "Please provide all product details"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the category object based on the category_id
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the product object based on the pk
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the product object with the new details
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.category = category
        product.save()

        # Return the updated product object in the response
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
