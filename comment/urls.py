from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("askquestion/", views.ask_question, name="ask_question"),
]
