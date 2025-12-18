from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from PIL import Image


# ----- Post Model -----
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        upload_to='post_images/',
        default='default_post.jpg',
        blank=True,
        null=True
    )

    # Reaction counters
    love_count = models.PositiveIntegerField(default=0)
    clap_count = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['-date_posted']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            try:
                img = Image.open(self.image.path)
                max_size = (1024, 1024)
                if img.height > 1024 or img.width > 1024:
                    img.thumbnail(max_size)
                    img.save(self.image.path)
            except Exception:
                pass


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
        indexes = [
            models.Index(fields=['post', 'reaction_type']),
            models.Index(fields=['user', 'post']),
        ]

    def __str__(self):
        return f"{self.user.username} {self.reaction_type} on {self.post.title}"


# ----- Comment Model -----
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    @property
    def is_reply(self):
        return self.parent is not None


# ===== SIGNALS FOR AUTO-UPDATING COUNTERS =====

# @receiver(post_save, sender=Reaction)
# def increment_reaction_count(sender, instance, created, **kwargs):
#     """Increment counter when reaction is created"""
#     if created:
#         post = instance.post
#         field_name = f"{instance.reaction_type}_count"
        
#         # Use F() expression to avoid race conditions
#         from django.db.models import F
#         Post.objects.filter(pk=post.pk).update(**{field_name: F(field_name) + 1})


# @receiver(post_delete, sender=Reaction)
# def decrement_reaction_count(sender, instance, **kwargs):
#     """Decrement counter when reaction is deleted"""
#     post = instance.post
#     field_name = f"{instance.reaction_type}_count"
    
#     # Use F() expression to avoid race conditions
#     from django.db.models import F
#     Post.objects.filter(pk=post.pk).update(**{field_name: F(field_name) - 1})