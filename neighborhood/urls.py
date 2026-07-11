from django.urls import path
from .views import (
    index,
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdeteView,
    UserDeleteView,
    DistrictListView,
    DistrictCreateView,
    DistrictUpdateView,
    DistrictDeleteView,
    PostListView,
    PostListDetailView,
    PostCreateView,
)


urlpatterns = [
    path("", index, name="index"),
    path("user/", UserListView.as_view(), name="user-list"),
    path("user/<int:pk>", UserDetailView.as_view(), name="user-detail"),
    path("user/<int:pk>/update", UserUpdeteView.as_view(), name="user-update"),
    path("user/<int:pk>/delete", UserDeleteView.as_view(), name="user-delete"),
    path("user/create", UserCreateView.as_view(), name="user-create"),
    path("district/", DistrictListView.as_view(), name="district-list"),
    path("district/create", DistrictCreateView.as_view(), name="district-create"),
    path("district/<int:pk>/update", DistrictUpdateView.as_view(), name="district-update"),
    path("district/<int:pk>/delete", DistrictDeleteView.as_view(), name="district-delete"),
    path("districts/<int:pk>/toggle-membership/", DistrictListView.toggle_district_membership, name="toggle-district-membership"),
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostListDetailView.as_view(), name="post-detail"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
]


app_name = "neighborhood"
