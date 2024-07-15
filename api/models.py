from django.db import models

class Product(models.Model):
    serial_number = models.IntegerField()
    product_name = models.CharField(max_length=100)
    input_image_urls = models.TextField()
    output_image_urls = models.TextField(null=True, blank=True)
    request_id = models.CharField(max_length=100, unique=True)
