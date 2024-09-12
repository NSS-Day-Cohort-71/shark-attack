# Build a model for the category table based on the following DBML schema:
# Table Category {
#   id integer [primary key]
#   name varchar [not null]
#   description text
# }
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
