from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from api.models.models import Venda, db
from api.schemas.venda_schemas import VendasDto


vendas_dto = VendasDto()
api = vendas_dto.api
venda_model = vendas_dto.venda_model


@api.route("/")
class VendaList(Resource):
    @api.marshal_list_with(venda_model)
    @jwt_required()
    def get(self):
        vendas = Venda.query.all()
        return vendas

    @api.expect(venda_model)
    @api.marshal_with(venda_model, code=201)
    @jwt_required()
    def post(self):
        data = request.json
        venda = Venda(
            cliente_id=data["cliente_id"],
            produto_id=data["produto_id"],
            fornecedor_id=data["fornecedor_id"],
            quantidade=data["quantidade"],
        )
        db.session.add(venda)
        db.session.commit()
        return venda, 201


@api.route("/<int:id>")
@api.response(404, "Venda not found")
class Venda(Resource):
    @api.marshal_with(venda_model)
    @jwt_required()
    def get(self, id):
        venda = Venda.query.get_or_404(id)
        return venda

    @api.expect(venda_model)
    @api.marshal_with(venda_model)
    @jwt_required()
    def put(self, id):
        venda = Venda.query.get_or_404(id)
        data = request.json
        venda.cliente_id = data.get("cliente_id", venda.cliente_id)
        venda.produto_id = data.get("produto_id", venda.produto_id)
        venda.fornecedor_id = data.get("fornecedor_id", venda.fornecedor_id)
        venda.quantidade = data.get("quantidade", venda.quantidade)
        db.session.commit()
        return venda

    @api.response(204, "Venda deleted")
    @jwt_required()
    def delete(self, id):
        venda = Venda.query.get_or_404(id)
        db.session.delete(venda)
        db.session.commit()
        return "", 204
