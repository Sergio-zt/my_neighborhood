from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import District


class UserCreationForm(UserCreationForm):
    districts = forms.ModelMultipleChoiceField(
        queryset=District.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "districts",
        )


class UserUpdateForm(forms.ModelForm):
    districts = forms.ModelMultipleChoiceField(
        queryset=District.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta():
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "districts"
        ]


class UserSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by user username"
            }
        )
    )

class DistrictSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search district by name"
            }
        )
    )

class PostSearchForm(forms.Form):
    text = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search post by text"
            }
        )
    )


class PostCreateForm(forms.Form):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "title",
            "text",
        )