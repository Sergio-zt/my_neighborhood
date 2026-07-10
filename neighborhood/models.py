from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class District(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    districts = models.ManyToManyField(District, related_name='users', blank=True)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_absolute_url(self):
        return reverse("neighborhood:user-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='posts'
    )
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField()
