from django.urls import path
from .views import (
    index,
    UserListView,
    DistrictListView,
    PostListView
)


urlpatterns = [
    path("", index, name="index"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("districts/", DistrictListView.as_view(), name="district-list"),
    path("posts/", PostListView.as_view(), name="post-list"),
]


app_name = "neighborhood"
