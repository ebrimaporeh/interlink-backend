# seeder/__init__.py
import json
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.contrib.auth.hashers import make_password
import requests
from io import BytesIO

class BaseSeeder:
    """Base class for all seeders"""
    
    @staticmethod
    def download_image(url):
        """Download image from URL"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img_name = url.split('/')[-1].split('?')[0]
                if not img_name:
                    img_name = 'image.jpg'
                return ContentFile(response.content, name=img_name)
        except Exception as e:
            print(f"Error downloading image: {e}")
        return None
    
    @staticmethod
    def clear_model(model):
        """Clear all data from a model"""
        count = model.objects.count()
        model.objects.all().delete()
        print(f"  ✓ Cleared {count} records from {model.__name__}")
    
    @staticmethod
    def print_success(message):
        print(f"  ✅ {message}")
    
    @staticmethod
    def print_error(message):
        print(f"  ❌ {message}")
    
    @staticmethod
    def print_info(message):
        print(f"  📌 {message}")