from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="profile")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100)
    image = models.ImageField(default="profileImages/defaultImg.jpg", upload_to="profileImages")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.width > 200 or img.height > 200:
            new_img = (200, 200)
            img.thumbnail(new_img)
            img.save(self.image.path)

    def __str__(self):
        return f"{self.user}"
