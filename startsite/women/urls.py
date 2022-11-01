from django.urls import path, re_path
from .views import *
import re

"""Class View"""
urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
]

"""Function View"""
# urlpatterns = [
#     path('', index, name='home'),
#     path('about/', about, name='about'),
#     path('addpage/', addpage, name='add_page'),
#     path('contact/', contact, name='contact'),
#     path('login/', login, name='login'),
#     path('category/<slug:cat_slug>/', show_category, name='category'),
#     path('post/<slug:post_slug>/', show_post, name='post'),
# ]
