from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from api.schemas.venda_schemas import VendasDto
from api.services.venda_services import (
    get_all_vendas,
    create_venda,
    delete_venda,
    update_venda,
    get_venda,
)


vendas_dto = VendasDto()
api = vendas_dto.api
venda_model = vendas_dto.venda_model


@api.route("/")
class VendaList(Resource):
    @api.marshal_list_with(venda_model)
    # @jwt_required()
    def get(self):
        return get_all_vendas()

    @api.expect(venda_model)
    @api.marshal_with(venda_model, code=201)
    # @jwt_required()
    def post(self):
        data = request.json
        return create_venda(data)


@api.route("/<int:id>")
@api.response(404, "Venda not found")
class Venda(Resource):
    @api.marshal_with(venda_model)
    # @jwt_required()
    def get(self, id):
        return get_venda(id)

    @api.expect(venda_model)
    @api.marshal_with(venda_model)
    # @jwt_required()
    def put(self, id):
        data = request.json
        return update_venda(data, id)

    @api.response(204, "Venda deleted")
    # @jwt_required()
    def delete(self, id):
        return delete_venda(id)
