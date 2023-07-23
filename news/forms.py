from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from allauth.account.forms import SignupForm
from django.core.mail import send_mail



class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=128)
    text = forms.CharField(min_length=20, label='Text', widget=forms.Textarea)
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = {
            'title',
            'text',
            'image',
            'connect_category'
        }
        exclude = ['user']

        def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get('title')
            text = cleaned_data.get("text")
            image = self.cleaden_data.get(image)

            if image:
                w,h = get_image_dimensions('image', False)
                if w > 2000 or h > 2000:
                    raise forms.ValidationError('Пожалуйста, используйте изображения не выше и шире 2000 пикселей')

            if name == description:
                raise ValidationError(
                    "Описание не должно быть идентично названию."
                )
            return cleaned_data


class CommentForm(forms.ModelForm):
    connect_post = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Comments
        fields = {
            'text',
        }
        exclude = ['author', 'connect_post']


class StatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Comments.choice, initial=Comments.wait, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Comments
        fields = {
            'status',
        }


