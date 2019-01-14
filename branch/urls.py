from django.urls import path

from . import views

urlpatterns = [
    path('', views.BranchView.as_view()),
    path('<int:branch_id>/', views.BranchViewId.as_view()),
]
