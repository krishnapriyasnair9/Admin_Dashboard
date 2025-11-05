from django.db import models
from django.contrib.auth.models import User

class Banner(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home'),
        ('package', 'Package'),
        ('franchise', 'Franchise'),
        ('contact', 'Contact'),
    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    banner_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    banner_file = models.FileField(upload_to='banners/', blank=True, null=True)
    heading = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.page.capitalize()} Banner"


# ✅ Save Profile Photos
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photo/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"
