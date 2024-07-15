# api/tasks.py

from celery import shared_task
from PIL import Image
import requests
from io import BytesIO
from django.conf import settings
from .models import Product
import uuid

@shared_task
def process_images(request_id):
    products = Product.objects.filter(request_id=request_id)

    for product in products:
        input_urls = product.input_image_urls.split(';')
        output_urls = []

        for url in input_urls:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((img.width // 2, img.height // 2))
            output_url = save_to_storage(img)
            output_urls.append(output_url)

        product.output_image_urls = ';'.join(output_urls)
        product.save()

def save_to_storage(img):
    output_path = f"static/{uuid.uuid4().hex}.jpg"
    img.save(output_path, quality=50)
    return settings.MEDIA_URL + output_path
