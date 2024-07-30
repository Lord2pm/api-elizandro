from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from api.schemas.venda_schemas import VendasDto
from api.schemas.produto_schemas import ProdutoDto
from api.schemas.cliente_schemas import ClienteDto
from api.services.venda_services import (
    get_all_vendas,
    create_venda,
    delete_venda,
    update_venda,
    get_venda,
)
from api.services.cliente_services import get_all_compras
from api.services.fornecedor_services import (
    get_all_compras as get_all_compras_fornecedor,
)


vendas_dto = VendasDto()
api = vendas_dto.api
venda_model = vendas_dto.venda_model


@api.route("/")
class VendaList(Resource):
    @api.marshal_list_with(venda_model)
    @jwt_required()
    def get(self):
        return get_all_vendas()

    @api.expect(venda_model)
    @api.marshal_with(venda_model, code=201)
    @jwt_required()
    def post(self):
        data = request.json
        return create_venda(data)


@api.route("/<int:id>")
@api.response(404, "Venda not found")
class Venda(Resource):
    @api.marshal_with(venda_model)
    @jwt_required()
    def get(self, id):
        return get_venda(id)

    @api.expect(venda_model)
    @api.marshal_with(venda_model)
    @jwt_required()
    def put(self, id):
        data = request.json
        return update_venda(data, id)

    @api.response(204, "Venda deleted")
    @jwt_required()
    def delete(self, id):
        return delete_venda(id)


@api.route("/fornecedor/<email>")
@api.response(404, "Fornecedor not found")
class VendasByFornecedor(Resource):
    @api.marshal_list_with(venda_model)
    @jwt_required()
    def get(self, email):
        return get_all_compras_fornecedor(email)


@api.route("/cliente/<email>")
@api.response(404, "Fornecedor not found")
class VendasByCliente(Resource):
    @api.marshal_list_with(venda_model)
    @jwt_required()
    def get(self, email):
        return get_all_compras(email)
