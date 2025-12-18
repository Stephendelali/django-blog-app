from django.core.management.base import BaseCommand
from django.db.models import Count
from blog.models import Post, Reaction

class Command(BaseCommand):
    help = 'Update reaction counts for all posts'

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        updated = 0
        
        for post in posts:
            love_count = Reaction.objects.filter(post=post, reaction_type='love').count()
            clap_count = Reaction.objects.filter(post=post, reaction_type='clap').count()
            bookmark_count = Reaction.objects.filter(post=post, reaction_type='bookmark').count()
            
            post.love_count = love_count
            post.clap_count = clap_count
            post.bookmark_count = bookmark_count
            post.save(update_fields=['love_count', 'clap_count', 'bookmark_count'])
            updated += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated} posts')
        )