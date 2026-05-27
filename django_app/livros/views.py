from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .linked_list import livros_db

CAMPOS = [
    "titulo", "autor", "editora", "anoPublicacao", "isbn",
    "categoria", "numeroPaginas", "idioma", "resumo",
    "palavrasChave", "formato", "localizacao",
]


def index(request):
    return render(request, "livros/index.html", {"livros": livros_db.to_list()})


@require_POST
def cadastrar(request):
    data = {campo: request.POST.get(campo, "").strip() for campo in CAMPOS}
    if data["titulo"]:
        livros_db.append(data)
    return redirect("index")


@require_POST
def editar(request, livro_id):
    data = {campo: request.POST.get(campo, "").strip() for campo in CAMPOS}
    livros_db.update(livro_id, data)
    return redirect("index")


@require_POST
def remover(request, livro_id):
    livros_db.remove(livro_id)
    return redirect("index")