from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image

# ----- Reaction Model -----
class Reaction(models.Model):
    REACTION_CHOICES = [
        ('love', 'Love'),
        ('clap', 'Clap'),
        ('bookmark', 'Bookmark'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post', 'reaction_type')

    def __str__(self):
        return f"{self.user.username} {self.reaction_type} on {self.post.title}"


# ----- Post Model -----
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='post_images/', default='default_post.jpg', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                img = Image.open(self.image.path)
                max_width = 1024
                max_height = 1024
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.ANTIALIAS)
                    img.save(self.image.path)
            except Exception:
                pass

    # ----- REACTION COUNTERS -----
    @property
    def reactions_count(self):
        result = {'love': 0, 'clap': 0, 'bookmark': 0}
        for r_type in result.keys():
            result[r_type] = self.reactions.filter(reaction_type=r_type).count()
        return result

    @property
    def clap_count(self):
        return self.reactions_count.get('clap', 0)

    @property
    def love_count(self):
        return self.reactions_count.get('love', 0)
