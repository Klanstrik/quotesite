from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_quote, name="add_quote"),
    path("source/add/", views.add_source, name="add_source"),
    path("popular/", views.popular, name="popular"),
    path("vote/<int:pk>/", views.vote, name="vote"),  # голосование
]
