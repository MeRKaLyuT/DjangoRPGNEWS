from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=8000)
    data = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    connect_category = models.ForeignKey('Category', on_delete=models.CASCADE)
    connect_comments = models.ForeignKey('Comments', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def save(self):
        super().save()
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                new_img = (500, 600)
                img.thumbnail(new_img)
                img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True, help_text='Название категории')

    def __str__(self):
        return self.title


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=800)
    approved = 'Approved'
    refused = 'Refused'
    wait = 'Waiting'
    choice = (
        (approved, 'Одобрено'),
        (wait, 'Ожидание'),
        (refused, 'Отказано')
    )

    status = models.CharField(max_length=8, choices=choice, default=wait)
    connect_post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])








