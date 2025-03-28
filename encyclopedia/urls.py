from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name='create'),
    path('search/', views.search, name='search'),
    path("<str:title>", views.entry, name = 'entry'),
]
