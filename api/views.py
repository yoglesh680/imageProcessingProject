# api/views.py

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Product
from .serializers import ProductSerializer
import csv
import uuid
from .tasks import process_images
import io

class UploadCSVView(APIView):
    def post(self, request):
        file = request.data['file']
        if isinstance(file, InMemoryUploadedFile):
            try:
                data = file.read().decode('utf-8')
                csv_reader = csv.reader(io.StringIO(data))
                request_id = str(uuid.uuid4())

                # Skip the header row
                next(csv_reader)

                for row in csv_reader:
                    if len(row) != 3:
                        return Response({"error": "CSV file must have three columns: serial_number, product_name, input_image_urls"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    serial_number, product_name, input_image_urls = row
                    Product.objects.update_or_create(
                        serial_number=int(serial_number),
                        product_name=product_name,
                        input_image_urls=input_image_urls,
                        defaults={'request_id': request_id}
                    )

                process_images.delay(request_id)
                return Response({"requestId": request_id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid file"}, status=status.HTTP_400_BAD_REQUEST)

class StatusView(APIView):
    def get(self, request, request_id):
        products = Product.objects.filter(request_id=request_id)
        if not products:
            return Response({"status": "Invalid request ID"}, status=status.HTTP_404_NOT_FOUND)

        status = "Completed" if products[0].output_image_urls else "Processing"
        return Response({"status": status})

class ProcessedDataView(APIView):
    def get(self, request):
        request_id = request.query_params.get('requestId')
        products = Product.objects.filter(request_id=request_id)
        if not products:
            return Response({"status": "Invalid request ID"}, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                "serialNumber": p.serial_number,
                "productName": p.product_name,
                "inputImageUrls": p.input_image_urls.split(';'),
                "outputImageUrls": p.output_image_urls.split(';') if p.output_image_urls else []
            }
            for p in products
        ]
        return Response(data)
