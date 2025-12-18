from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Reaction, Post


@receiver(post_save, sender=Reaction)
def increment_reaction_count(sender, instance, created, **kwargs):
    if created:
        field = f"{instance.reaction_type}_count"
        Post.objects.filter(pk=instance.post_id).update(
            **{field: F(field) + 1}
        )


@receiver(post_delete, sender=Reaction)
def decrement_reaction_count(sender, instance, **kwargs):
    field = f"{instance.reaction_type}_count"
    Post.objects.filter(
    pk=instance.post_id,
    **{f"{field}__gt": 0}
).update(**{field: F(field) - 1})

