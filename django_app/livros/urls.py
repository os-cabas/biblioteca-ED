from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastrar/", views.cadastrar, name="cadastrar"),
    path("editar/<int:livro_id>/", views.editar, name="editar"),
    path("remover/<int:livro_id>/", views.remover, name="remover"),
]