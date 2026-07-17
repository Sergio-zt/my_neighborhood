from django.db import models
from django.conf import settings
from neighborhood.models import District

class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="posts"
    )
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    districts = models.ManyToManyField(
        District,
        related_name="district_posts"
    )
