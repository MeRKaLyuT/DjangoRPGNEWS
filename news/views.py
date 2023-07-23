from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from .models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from .forms import PostForm, CommentForm, StatusForm
from django.views.generic.edit import FormMixin
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from django.views import View
from django.urls import reverse_lazy
from django.core.mail import EmailMessage


class PostList(ListView):
    model = Post
    ordering ='data'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentForm
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'connect_post': self.object.id})
        context['comments'] = Comments.objects.filter(connect_post=self.object.id)
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    raise_exception = True

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    raise_exception = True


def Profile(request):
    user = request.user
    username = user.username
    return render(request, 'acc.html', {'username': username})


class CommentCreateView(CreateView):
    form_class = CommentForm
    success_url = '/'
    model = Comments

    def form_valid(self, form):
        form.instance.author = self.request.user
        post_id = form.cleaned_data['connect_post']
        form.instance.connect_post_id = post_id

        post = Post.objects.get(id=post_id)
        subject = f'Новый комментарий к статье {post.title}'
        message = f'Новый комментарий от пользователя {self.request.user.username}'

        mail = EmailMessage(subject, message, to=[post.user.email])
        mail.send()

        return super().form_valid(form)


# Все комментарии пользователя
def user_comments(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    comments = Comments.objects.filter(author=user)
    return render(request, 'comments_for_user.html', {'comments': comments})


# Все комментарии к статьям пользователя
def author_comments(request):
    user_id = request.user.id
    post_from_author = Post.objects.filter(user=user_id)
    comments = Comments.objects.filter(connect_post__in=post_from_author)

    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            comment_id = request.POST['comment_id']
            comment = Comments.objects.get(id=comment_id)
            comment.status = form.cleaned_data['status']
            comment.save()

            subject = 'Статус комментария'
            message = f'Ваш комментарий был {"принят" if comment.status else "отклонен"} автором поста'
            mail = EmailMessage(subject, message, to=[comment.author.email])
            mail.send()

            return redirect('authorcomments')
    else:
        form = StatusForm()

    return render(request, 'comments_for_author.html', {'post_from_author': post_from_author, 'comments': comments, 'form': form})







