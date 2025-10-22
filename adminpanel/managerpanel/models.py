from django.db import models

class Banner(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home'),
        ('about', 'About'),
        ('contact', 'Contact'),
        ('package','Package'),
        ('franchise','Franchise'),
        
    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    banner_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    image = models.ImageField(upload_to='banners/images/', blank=True, null=True)
    video = models.FileField(upload_to='banners/videos/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.page.capitalize()} Banner"
