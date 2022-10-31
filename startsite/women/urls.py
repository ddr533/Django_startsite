from django.urls import path, re_path
from .views import *
import re


urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('category/<int:cat_id>/', show_category, name='category'),
    path('post/<slug:post_slug>/', show_post, name='post'),
]