from django.urls import path

from . import views

urlpatterns = [
    path('fahbatch.png/<int:uid>/', views.index, name='index'),
]

