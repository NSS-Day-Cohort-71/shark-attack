# Create a class for a OrderItem table based on the following DBML schema:
# Table OrderItem {
#   id integer [primary key]
#   order_id integer [ref: > Order.id]
#   product_id integer [ref: > Product.id]
#   quantity integer [not null]
#   price_at_time decimal(10,2) [not null]
# }
from django.db import models

class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)