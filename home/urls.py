from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria/', views.categoria, name="categoria"),
    path('categoria/form', views.form_categoria, name="form_categoria"),
    path('categoria/editar/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categoria/remover/<int:id>/', views.remover_categoria, name='remover_categoria'),
    path('categoria/detalhes/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),
    path('cliente/', views.cliente, name='cliente'),
    path('cliente/form', views.form_cliente, name='form_cliente'),
    path('cliente/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/remover/<int:id>/', views.remover_cliente, name='remover_cliente'),

]   