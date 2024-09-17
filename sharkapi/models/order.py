# Create a Django model for the Order table based on the following DBML schema:
# Table Order {
#   id integer [primary key]
#   user_id integer [ref: > User.id]
#   status varchar [not null]
#   created_at timestamp [default: `now()`]
#   updated_at timestamp
# }
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    carrier = models.CharField(max_length=100, default="USPS")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    products = models.ManyToManyField("Product", through="OrderItem", related_name="orders")
