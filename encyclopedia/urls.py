from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.page, name="page"),
    path("wiki/<str:page>/edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
]
