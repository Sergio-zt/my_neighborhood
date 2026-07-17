from django import forms
from neighborhood.models import District
from posts.models import Post


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


class PostCreationForm(forms.ModelForm):
    districts = forms.ModelMultipleChoiceField(
        queryset=District.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    
    class Meta:
        model = Post
        fields = [
            "districts",
            "title",
            "text"
        ]