from django.urls import path
from users.views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)


app_name = "users"

urlpatterns = [
    path("user/", UserListView.as_view(), name="user-list"),
    path("user/<int:pk>", UserDetailView.as_view(), name="user-detail"),
    path("user/<int:pk>/update", UserUpdateView.as_view(), name="user-update"),
    path("user/<int:pk>/delete", UserDeleteView.as_view(), name="user-delete"),
    path("user/create", UserCreateView.as_view(), name="user-create"),
]
