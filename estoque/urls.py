from django.urls import path
from . import views

app_name = 'estoque'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('ingredientes/novo/', views.editar, name='novo'),
    path('ingredientes/<int:pk>/editar/', views.editar, name='editar'),
]
