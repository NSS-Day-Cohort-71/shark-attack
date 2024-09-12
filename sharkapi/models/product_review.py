# Create a class for a product review table based on the following DBML schema:
# Table Review {
#   id integer [primary key]
#   product_id integer [ref: > Product.id]
#   user_id integer [ref: > User.id]
#   rating integer [not null]
#   comment text
#   created_at timestamp [default: `now()`]
# }
from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)