from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from women.forms import AddPostForm
from women.models import *


def index(request):
    posts = Women.objects.all().order_by('-time_create')
    context = {
        'posts': posts,
        'title': 'Главная страница',
        'cat_selected': 0
    }
    return render(request, 'women/index.html', context=context)

def show_category(request, cat_slug):
    cat_id = Category.objects.filter(slug=cat_slug)[0].pk
    posts = Women.objects.filter(cat_id=cat_id).order_by('-time_create')
    if len(posts) == 0:
        raise Http404()
    context = {
        'posts': posts,
        'title': 'Выбранная категория',
        'cat_selected': cat_id,
    }
    return render(request, 'women/index.html', context=context)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'women/post.html', context=context)

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 Women.objects.create(**form.cleaned_data)
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})

def about(request):
    return render(request, 'women/about.html')

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

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