from django.db import models
from django.contrib.auth.models import User

class PostHashTag(models.Model):
    hashtag = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.hashtag

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(PostHashTag, related_name='blog_posts', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=False , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=False , null=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"    
    
    
class Share_post(models.Model):
    blog = models.ForeignKey(Post, on_delete=models.PROTECT)
    token = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    email = models.EmailField(blank=False , null=True)