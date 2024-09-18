# Generate a view for the products endpoint that inherits from the Django REST Framework ViewSet class.
# Start with a list and retrieve method

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sharkapi.models import Product, OrderItem, Order, Category

class CartViewSet(viewsets.ViewSet):
    def delete(self, request, pk=None):
        product_to_remove_from_cart = request.data.get("product_id", None)

        try:
            product = Product.objects.get(pk=product_to_remove_from_cart)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            lineitem = OrderItem.objects.get(
                product=product,
                order__user=request.user,
                order__status="Pending"
            )

        except OrderItem.DoesNotExist:
            return Response({"message": "Product not in user's shopping cart"}, status=status.HTTP_400_BAD_REQUEST)

        lineitem.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        order = Order.objects.filter(user=request.user, status="Pending").first()

        if order is None:
            return Response({"message": "No order found"}, status=status.HTTP_404_NOT_FOUND)

        serialized = CartSerializer(order.products, many=True, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Get the product id from the request body
        product_id = request.data.get("product_id", None)

        try:
            product = Product.objects.get(pk=product_id, stock__gt=0)
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
            if OrderItem.objects.filter(order=order, product=product).exists():
                lineitem = OrderItem.objects.get(order=order, product=product)
                lineitem.quantity += 1
                lineitem.save()
            else:
                lineitem = OrderItem()
                lineitem.product = product
                lineitem.quantity = 1
                lineitem.order = order
                lineitem.price_at_time = product.price
                lineitem.save()

            serialized = CartSerializer(order.products, many=True, context={"request": request})
            return Response(serialized.data, status=status.HTTP_201_CREATED)





# Generate a product serializer class that inherits from the Django REST Framework ModelSerializer class.
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', )

class CartSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=False)
    quantity = serializers.SerializerMethodField()

    def get_quantity(self, obj):
        lineitem = OrderItem.objects.get(
            order__user=self.context['request'].auth.user,
            order__status="Pending",
            product=obj
        )
        return lineitem.quantity

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'category', 'quantity', )
