from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("notes/", views.notes),
    path("notes/<int:id>/", views.note_detail),
]