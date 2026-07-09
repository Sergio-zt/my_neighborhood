from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .models import (
    District,
    Post,
    User,
)

from .forms import (
    UserSearchForm,
    DistrictSearchForm,
    PostSearchForm
)


@login_required
def index(request):
    """View function for the home page of the site."""

    num_users = settings.AUTH_USER_MODEL.objects.count()
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
    model = settings.AUTH_USER_MODEL
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
        queryset = super().get_queryset()
        form = UserSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


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
        queryset = District.objects.select_related("manufacturer")
        form = DistrictSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(model__icontains=form.cleaned_data["name"])
        return queryset


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
