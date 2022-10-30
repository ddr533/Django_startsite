from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from women.models import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
def test():
    return
def index(request):
    posts = Women.objects.all()
    context = {
        'posts': posts,
        'menu' : menu,
        'title': 'Главная страница',
        'cat_selected': 0
    }
    return render(request, 'women/index.html', context=context)

def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)
    if len(posts) == 0:
        raise Http404()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Выбранная категория',
        'cat_selected': cat_id,
    }
    return render(request, 'women/index.html', context=context)

def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")

def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})

def addpage(request):
    return HttpResponse("Добавление статьи")

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