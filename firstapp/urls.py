from django.urls import path
from . import views

urlpatterns = [
    path("<slug:slug>", views.Blogview.as_view(), name="blog_view"),
    path("about/", views.aboutview.as_view(), name="about_view"),
    path("", views.postlist.as_view(), name="home")
]
