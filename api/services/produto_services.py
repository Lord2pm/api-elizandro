from flask import abort
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path

from api.models.models import Produto, Fornecedor, db


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "../../uploads" / "img"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    if file.filename == "":
        raise ValueError("Nenhum arquivo selecionado")
    if not allowed_file(file.filename):
        raise ValueError("Extensão de arquivo não permitida")

    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{timestamp}_{filename}"
    upload_folder = UPLOAD_FOLDER
    file_path = upload_folder / new_filename
    file.save(file_path)
    return new_filename


def get_all_produtos():
    return Produto.query.all()


def get_produto_by_id(id):
    return Produto.query.get_or_404(id)


def create_produto(data):
    try:
        produto = Produto(
            nome=data["nome"].title().strip(),
            preco=data["preco"],
            categoria=data["categoria"].title().strip(),
            qtd_stock=data.get("qtd_stock"),
            vendedor_id=data["vendedor_id"],
        )
        db.session.add(produto)
        db.session.commit()
        return produto, 201
    except KeyError:
        return abort(
            400, "Verifique os campos exigidos no corpo da requisição e tente novamente"
        )


def update_produto(id, data):
    produto = get_produto_by_id(id)
    produto.nome = data.get("nome", produto.nome)
    produto.preco = data.get("preco", produto.preco)
    produto.categoria = data.get("categoria", produto.categoria)
    produto.qtd_stock = data.get("qtd_stock", produto.qtd_stock)
    db.session.commit()
    return produto


def delete_produto(id):
    produto = get_produto_by_id(id)
    db.session.delete(produto)
    db.session.commit()
    return "", 204


def get_produtos_by_fornecedor_email(email):
    fornecedor = Fornecedor.query.filter_by(email=email).first()
    if fornecedor:
        return fornecedor.produtos
    return abort(404, "Fornecedor não encontrado")


def get_produtos_by_categoria(categoria: str):
    produtos = Produto.query.filter_by(categoria=categoria.title().strip()).all()
    if produtos:
        return produtos
    return abort(404, "Nenhum produto encontrado")
