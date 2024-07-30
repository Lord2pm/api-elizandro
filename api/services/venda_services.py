from flask import abort, request

from api.models.models import Venda, Produto, db


def get_all_vendas():
    return Venda.query.all()


def create_venda(data):
    produto = Produto.query.filter_by(id=data["produto_id"]).first()

    if produto:
        if produto.qtd_stock >= data["quantidade"]:
            produto.qtd_stock -= data["quantidade"]
            venda = Venda(
                cliente_id=data["cliente_id"],
                produto_id=data["produto_id"],
                fornecedor_id=data["fornecedor_id"],
                quantidade=data["quantidade"],
            )
            db.session.add(venda)
            db.session.commit()
            return venda, 201

        return abort(400, "Quantidade em stock inferior a pretendida")

    return abort(400, "Produto não encontrado")


def delete_venda(id):
    venda = Venda.query.get_or_404(id)
    db.session.delete(venda)
    db.session.commit()
    return "", 204


def update_venda(data, id):
    venda = Venda.query.get_or_404(id)
    venda.cliente_id = data.get("cliente_id", venda.cliente_id)
    venda.produto_id = data.get("produto_id", venda.produto_id)
    venda.fornecedor_id = data.get("fornecedor_id", venda.fornecedor_id)
    venda.quantidade = data.get("quantidade", venda.quantidade)
    db.session.commit()
    return venda


def get_venda(id):
    return Venda.query.get_or_404(id)
