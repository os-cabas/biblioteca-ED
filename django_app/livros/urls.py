from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Livros
    path("cadastrar/", views.cadastrar, name="cadastrar"),
    path("editar/<int:livro_id>/", views.editar, name="editar"),
    path("remover/<int:livro_id>/", views.remover, name="remover"),
    # Membros
    path("membros/cadastrar/", views.cadastrar_membro, name="cadastrar_membro"),
    path("membros/remover/<int:membro_id>/", views.remover_membro, name="remover_membro"),
    path("membros/<int:membro_id>/historico/", views.historico_membro, name="historico_membro"),
    # Empréstimos
    path("emprestimos/registrar/", views.registrar_emprestimo, name="registrar_emprestimo"),
    path("emprestimos/devolver/<int:emprestimo_id>/", views.registrar_devolucao, name="registrar_devolucao"),
]
