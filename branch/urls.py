from django.urls import path

from . import views

urlpatterns = [
    path('', views.BranchView.as_view()),
]
