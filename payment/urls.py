from django.urls import path

from . import views

urlpatterns = [
    path('', views.PaymentView.as_view(), name='payments'),
    path('<int:payment_id>/', views.PaymentViewId.as_view()),
]
