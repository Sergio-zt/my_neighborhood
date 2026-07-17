from django.urls import path
from posts.views import(
    PostListView,
    PostDetailView,
    PostDeleteView,
    PostUpdateView,
    PostCreateView
)


urlpatterns = [
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="post-update"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
]

app_name = "posts"