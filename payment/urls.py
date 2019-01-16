from django.urls import path

from . import views

urlpatterns = [
    path('', views.PaymentView.as_view()),
    # path('<int:payment_id>/', views.PaymentViewId.as_view()),
]
