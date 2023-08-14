from django.shortcuts import render
from .models import Post
from django.views import generic
# Create your views here.


class Blogview(generic.DetailView):
    model = Post
    template_name = "blog.html"

class aboutview(generic.TemplateView):
    template_name = "about.html"

class postlist(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-date_created")
    template_name="index.html"