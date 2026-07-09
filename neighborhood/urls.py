from django.urls import path
from .views import (
    index,
    UserListView,
    UserCreateView,
    DistrictListView,
    PostListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("districts/", DistrictListView.as_view(), name="district-list"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("user/create", UserCreateView.as_view(), name="user-create"),
]


app_name = "neighborhood"
