from django.contrib.auth.models import User
from django.db import models
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(
        default='profile_pics/default.jpg',
        upload_to='profile_pics'
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        """
        Override save() to automatically resize profile images
        and safely handle missing files.
        """
        super().save(*args, **kwargs)

        # Ensure the image file actually exists before resizing
        if self.image and os.path.exists(self.image.path):
            try:
                img = Image.open(self.image.path)

                # Only resize if too large
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path, quality=90, optimize=True)

            except Exception as e:
                # Log or print to terminal for debugging
                print(f"Error processing image for {self.user.username}: {e}")
