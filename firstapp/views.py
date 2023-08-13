from django.shortcuts import render
from .models import Post
from django.views import generic
# Create your views here.


class Blogview(generic.DetailView):
    model = Post
    template_name = "blog.html"