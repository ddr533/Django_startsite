from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from women.forms import AddPostForm, RegisterUserForm, LoginUserForm
from women.models import *
from women.utils import DataMixin

"""Class view"""


class WomenHome(ListView):
    paginate_by = 2
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True).order_by('-time_create').select_related('cat')


class WomenCategory(ListView):
    paginate_by = 2
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).order_by('-time_create').select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        с = context['posts'][0]
        context['title'] = 'Категория - ' + str(с.cat)
        context['cat_selected'] = с.cat_id
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    context_object_name = 'post'
    allow_empty = False
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        return context


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    login_url = '/admin/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context


"""Function view"""

# def index(request):
#     posts = Women.objects.all().order_by('-time_create')
#     context = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'cat_selected': 0
#     }
#     return render(request, 'women/index.html', context=context)
#
#
# def show_category(request, cat_slug):
#     cat_id = Category.objects.filter(slug=cat_slug)[0].pk
#     posts = Women.objects.filter(cat_id=cat_id).order_by('-time_create')
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'title': 'Выбранная категория',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'women/index.html', context=context)


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)
#
#
# # def addpage(request):
# #     if request.method == 'POST':
# #         form = AddPostForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             try:
# #                 Women.objects.create(**form.cleaned_data)
# #                 return redirect('home')
# #             except:
# #                 form.add_error(None, 'Ошибка добавления поста')
# #     else:
# #         form = AddPostForm()
# #     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})
#
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})
#

## def login(request):
#     return HttpResponse("Авторизация")

def logout_user(request):
    logout(request)
    return redirect('login')


def about(request):
    return render(request, 'women/about.html')


def contact(request):
    return HttpResponse("Обратная связь")


def categories(request, cat):
    if (request.GET):
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1>{cat}</p>")


def archive(request, year):
    if int(year) > 2020:
        raise Http404()
    if int(year) == 2020:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
