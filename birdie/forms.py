from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', )

        def clean_body(self):
            data = self.cleaned_data.get('title')
            if len(data) < 5:
                raise forms.ValidationError('Please enter at least 10 characters')
            return data