from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from users.forms import(
    UserSearchForm,
    UserCreationForm,
    UserUpdateForm
)


class UserListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = UserSearchForm(
            initial={
                "username": username
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("districts")
        form = UserSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related("districts")


class UserUpdeteView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()


class UserCreateView(generic.CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    success_url = reverse_lazy("neighborhood:user-list")
