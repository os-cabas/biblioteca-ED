# 📚 Sistema de Controle de Acervo e Empréstimos de Biblioteca

## 👥 Integrantes
- Matheus Camarotto Manfio Domingues  
- Kenzo de Oliveira Senna  
- Hudson Batista Brandão  

---

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python 3, Django
- **Estrutura de dados:** Lista Ligada (LinkedList) implementada do zero
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5

---

## 📖 Descrição
Sistema web para controle de acervo e empréstimos de uma biblioteca, desenvolvido com Django e estruturas de dados nativas do Python (sem banco de dados relacional — os dados são mantidos em memória via Lista Ligada).

---

## ✅ Funcionalidades

### Acervo (Livros)
- Cadastro de livros com título, autor, editora, ISBN, categoria, idioma, formato, localização, resumo e palavras-chave
- Edição e remoção de livros
- **Busca por título ou autor** (filtro server-side com list comprehension)
- **Ordenação por título A → Z ou Z → A** (server-side com `sorted()`)

### Membros
- Cadastro de membros com nome, matrícula, e-mail e telefone
- Remoção de membros
- Histórico completo de empréstimos por membro

### Empréstimos
- Registro de empréstimo com prazo configurável (7, 14, 21 ou 30 dias)
- Registro de devolução
- **Fila de espera automática** — quando um livro está emprestado, o membro entra na fila e recebe o livro automaticamente na próxima devolução

---

## 🗂️ Estrutura de Dados
O projeto implementa uma **Lista Ligada (LinkedList)** em `django_app/livros/linked_list.py`, utilizada como banco de dados em memória para livros, membros e empréstimos. A estrutura suporta inserção, remoção, busca por ID, busca por campo e atualização, com controle de concorrência via `threading.Lock`.

---

## 🚀 Como Executar

```bash
git clone https://github.com/os-cabas/biblioteca-ED.git
cd biblioteca-ED

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

cd django_app
pip install -r requirements.txt
python manage.py runserver
```

Acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

> **Atenção:** os dados são armazenados em memória e são perdidos ao reiniciar o servidor.
