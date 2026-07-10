from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import (
    District,
    Post,
)

from .forms import (
    UserSearchForm,
    UserCreationForm,
    UserUpdateForm,
    DistrictSearchForm,
    PostSearchForm
)


@login_required
def index(request):
    """View function for the home page of the site."""

    num_users = get_user_model().objects.count()
    num_districts = District.objects.count()
    num_posts = Post.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_users": num_users,
        "num_districts": num_districts,
        "num_posts": num_posts,
        "num_visits": num_visits + 1,
    }

    return render(request, "neighborhood/index.html", context=context)

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


class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    success_url = reverse_lazy("neighborhood:user-list")


class DistrictListView(LoginRequiredMixin, generic.ListView):
    model = District
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DistrictListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DistrictSearchForm(
            initial={
                "name": name
            }
        )
        return context

    def get_queryset(self):
        queryset = District.objects.prefetch_related("users").annotate(
            user_count=Count('users')
        )
        form = DistrictSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset
    
    @require_POST
    def toggle_district_membership(request, pk):
        district = get_object_or_404(District, pk=pk)

        if request.user in district.users.all():
            district.users.remove(request.user)
        else:
            district.users.add(request.user)

        return redirect("neighborhood:district-list")


class DistrictCreateView(LoginRequiredMixin, generic.CreateView):
    model = District
    fields = "__all__"
    success_url = reverse_lazy("neighborhood:district-list")


class DistrictUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = District
    fields = "__all__"
    success_url = reverse_lazy("neighborhood:district-list")


class DistrictDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = District
    success_url = reverse_lazy("neighborhood:district-list")


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 10

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
        queryset = super().get_queryset()
        form = PostSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["text"])
        return queryset
