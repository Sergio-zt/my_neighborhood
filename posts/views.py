from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from posts.models import Post
from posts.forms import(
    PostSearchForm,
    PostCreationForm,    
)


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 10
    ordering = ["-id"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        text = self.request.GET.get("text", "")
        context["search_form"] = PostSearchForm(
            initial={
                "text": text
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related("user").prefetch_related("districts")
        form = PostSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(text__icontains=form.cleaned_data["text"])
        return queryset


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post

    def get_queryset(self):
        return super().get_queryset().select_related("user").prefetch_related("districts")


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostCreationForm
    success_url = reverse_lazy("posts:post-list")

    def form_valid(self, form):
        form.instance.user = self.request.user        
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("posts:post-list")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostCreationForm
    success_url = reverse_lazy("posts:post-list")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
