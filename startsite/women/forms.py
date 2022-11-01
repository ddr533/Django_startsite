from django import forms
from django.core.exceptions import ValidationError

from .models import *


# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), required=False, label="Контент")
#     is_published = forms.BooleanField(label="Публикация", initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Women
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 200:
            raise ValidationError('Длина превышает 200 символов')

        return title
