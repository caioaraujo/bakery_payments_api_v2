from django.urls import path

from . import views

urlpatterns = [
    path('', views.BranchView.as_view(), name='branches'),
    path('<int:branch_id>/', views.BranchViewId.as_view(), name='branches-by-id'),
    path('<int:branch_id>/payments/', views.BranchPaymentsView.as_view(), name='branches-payments')
]
