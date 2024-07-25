from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.comment_text
    
