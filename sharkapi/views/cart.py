# Generate a view for the products endpoint that inherits from the Django REST Framework ViewSet class.
# Start with a list and retrieve method

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sharkapi.models import Product, OrderItem, Order, Category

class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Get the product id from the request body
        product_id = request.data.get("product_id", None)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Is this a new order, or is customer adding product to existing order?
        # Are there any rows in the Order table for customer with status of "Pending"
        order = Order.objects.filter(user=request.user, status="Pending").first()

        # If new order, create a new order object
        if order is None:
            new_order = Order()
            new_order.user = request.auth.user
            new_order.status = "Pending"
            new_order.save()

            # Create an new_order item instance
            lineitem = OrderItem()
            # Add product and order to orderitem instance
            lineitem.product = product
            lineitem.quantity = 1
            lineitem.order = new_order
            lineitem.price_at_time = product.price
            lineitem.save()
            serialized = CartSerializer(new_order.products, many=True)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            lineitem = OrderItem()
            lineitem.product = product
            lineitem.quantity = 1
            lineitem.order = order
            lineitem.price_at_time = product.price
            lineitem.save()

            serialized = CartSerializer(order.products, many=True)
            return Response(serialized.data, status=status.HTTP_201_CREATED)





# Generate a product serializer class that inherits from the Django REST Framework ModelSerializer class.
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', )

class CartSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=False)


    """
        "lineitems": [
            {
                "id": 1,
                "name": "Product 1",
            }
        ]
    """

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'category',)
