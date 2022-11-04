from django import template
from django.db.models import Count

from women.models import *

register = template.Library()

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}
        ]


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.annotate(Count('women'))
    else:
        cats = Category.objects.annotate(Count('women')).order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag('women/main_menu.html')
def main_menu(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(1)
    return {"menu": user_menu}
