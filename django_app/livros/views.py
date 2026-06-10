from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .linked_list import livros_db, membros_db, emprestimos_db, filas_espera

CAMPOS_LIVRO = [
    "titulo", "autor", "editora", "anoPublicacao", "isbn",
    "categoria", "numeroPaginas", "idioma", "resumo",
    "palavrasChave", "formato", "localizacao",
]

CAMPOS_MEMBRO = ["nome", "matricula", "email", "telefone"]


def index(request):
    livros = livros_db.to_list()
    membros = membros_db.to_list()

    membro_map = {m["id"]: m for m in membros}
    livro_map = {l["id"]: l for l in livros}

    for livro in livros:
        livro.setdefault("disponivel", True)
        fila_ids = filas_espera.get(livro["id"], [])
        livro["fila_espera"] = [membro_map.get(mid, {}).get("nome", "?") for mid in fila_ids]

    emprestimos_ativos = []
    for emp in emprestimos_db.to_list():
        if emp["status"] == "ativo":
            info = dict(emp)
            info["livro_titulo"] = livro_map.get(emp["livro_id"], {}).get("titulo", "Removido")
            info["membro_nome"] = membro_map.get(emp["membro_id"], {}).get("nome", "Removido")
            emprestimos_ativos.append(info)

    return render(request, "livros/index.html", {
        "livros": livros,
        "membros": membros,
        "emprestimos_ativos": emprestimos_ativos,
    })


# ── Livros ────────────────────────────────────────────────────────────

@require_POST
def cadastrar(request):
    data = {campo: request.POST.get(campo, "").strip() for campo in CAMPOS_LIVRO}
    if data["titulo"]:
        data["disponivel"] = True
        livros_db.append(data)
    return redirect("index")


@require_POST
def editar(request, livro_id):
    livro = livros_db.find_by_id(livro_id)
    if livro:
        data = {campo: request.POST.get(campo, "").strip() for campo in CAMPOS_LIVRO}
        data["disponivel"] = livro.get("disponivel", True)
        livros_db.update(livro_id, data)
    return redirect("index")


@require_POST
def remover(request, livro_id):
    livros_db.remove(livro_id)
    filas_espera.pop(livro_id, None)
    return redirect("index")


# ── Membros ───────────────────────────────────────────────────────────

@require_POST
def cadastrar_membro(request):
    data = {campo: request.POST.get(campo, "").strip() for campo in CAMPOS_MEMBRO}
    if data["nome"]:
        membros_db.append(data)
    return redirect("index")


@require_POST
def remover_membro(request, membro_id):
    membros_db.remove(membro_id)
    return redirect("index")


# ── Empréstimos ───────────────────────────────────────────────────────

@require_POST
def registrar_emprestimo(request):
    livro_id = int(request.POST.get("livro_id", 0))
    membro_id = int(request.POST.get("membro_id", 0))
    prazo_dias = int(request.POST.get("prazo_dias", 14))

    livro = livros_db.find_by_id(livro_id)
    membro = membros_db.find_by_id(membro_id)

    if not livro or not membro:
        return redirect("index")

    if livro.get("disponivel", True):
        agora = datetime.now()
        emprestimos_db.append({
            "livro_id": livro_id,
            "membro_id": membro_id,
            "data_emprestimo": agora.strftime("%d/%m/%Y"),
            "data_prevista_devolucao": (agora + timedelta(days=prazo_dias)).strftime("%d/%m/%Y"),
            "data_devolucao": "",
            "status": "ativo",
        })
        novo_livro = dict(livro)
        novo_livro["disponivel"] = False
        livros_db.update(livro_id, novo_livro)
    else:
        fila = filas_espera.setdefault(livro_id, [])
        if membro_id not in fila:
            fila.append(membro_id)

    return redirect("index")


@require_POST
def registrar_devolucao(request, emprestimo_id):
    emprestimo = emprestimos_db.find_by_id(emprestimo_id)
    if not emprestimo:
        return redirect("index")

    livro_id = emprestimo["livro_id"]
    livro = livros_db.find_by_id(livro_id)

    novo_emp = dict(emprestimo)
    novo_emp["data_devolucao"] = datetime.now().strftime("%d/%m/%Y")
    novo_emp["status"] = "devolvido"
    emprestimos_db.update(emprestimo_id, novo_emp)

    fila = filas_espera.get(livro_id, [])
    if fila:
        proximo_id = fila.pop(0)
        agora = datetime.now()
        emprestimos_db.append({
            "livro_id": livro_id,
            "membro_id": proximo_id,
            "data_emprestimo": agora.strftime("%d/%m/%Y"),
            "data_prevista_devolucao": (agora + timedelta(days=14)).strftime("%d/%m/%Y"),
            "data_devolucao": "",
            "status": "ativo",
        })
    elif livro:
        novo_livro = dict(livro)
        novo_livro["disponivel"] = True
        livros_db.update(livro_id, novo_livro)

    return redirect("index")


# ── Histórico ─────────────────────────────────────────────────────────

def historico_membro(request, membro_id):
    historico = emprestimos_db.find_all_by("membro_id", membro_id)
    resultado = []
    for emp in historico:
        livro = livros_db.find_by_id(emp["livro_id"])
        resultado.append({
            **emp,
            "livro_titulo": livro["titulo"] if livro else "Livro removido",
        })
    return JsonResponse({"historico": resultado})
