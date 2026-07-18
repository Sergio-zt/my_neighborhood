from django.db import models
from django.contrib.auth.models import AbstractUser
from neighborhood.models import District
from django.urls import reverse


class User(AbstractUser):
    districts = models.ManyToManyField(
        District,
        related_name='users',
        blank=True
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_absolute_url(self):
        return reverse("users:user-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"
