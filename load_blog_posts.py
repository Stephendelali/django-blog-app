import json
import random
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Post   # make sure your app is named 'blog'

# Load JSON file
with open('posts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ensure there are some users to assign posts to
users = list(User.objects.all())
if not users:
    # create 3 test users
    for i in range(1, 4):
        User.objects.create_user(username=f'user{i}', password='password123')
    users = list(User.objects.all())

# Optional: wipe old posts
Post.objects.all().delete()

# Create new posts, randomly assigning an author from the users list
for item in data:
    author = random.choice(users)
    Post.objects.create(
        title=item.get("title", "Untitled"),
        content=item.get("content", ""),
        date_posted=timezone.now(),
        author=author
    )

print("✅ Successfully added posts to the database!")
