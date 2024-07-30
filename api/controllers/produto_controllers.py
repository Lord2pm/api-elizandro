from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from api.schemas.produto_schemas import ProdutoDto
from api.services.produto_services import (
    get_all_produtos,
    get_produto_by_id,
    create_produto,
    update_produto,
    delete_produto,
    get_produtos_by_fornecedor_email,
)


produto_dto = ProdutoDto()
api = produto_dto.api
produto_model = produto_dto.produto_model


@api.route("/")
class ProdutoList(Resource):
    @api.marshal_list_with(produto_model)
    @jwt_required()
    def get(self):
        return get_all_produtos()

    @api.expect(produto_model)
    @api.marshal_with(produto_model, code=201)
    @jwt_required()
    def post(self):
        data = request.json
        return create_produto(data)


@api.route("/<int:id>")
@api.response(404, "Produto not found")
class Produto(Resource):
    @api.marshal_with(produto_model)
    @jwt_required()
    def get(self, id):
        return get_produto_by_id(id)

    @api.expect(produto_model)
    @api.marshal_with(produto_model)
    @jwt_required()
    def put(self, id):
        data = request.json
        return update_produto(id, data)

    @api.response(204, "Produto deleted")
    @jwt_required()
    def delete(self, id):
        return delete_produto(id)


@api.route("/fornecedor/<email>")
@api.response(404, "Fornecedor not found")
class ProdutosByFornecedor(Resource):
    @api.marshal_list_with(produto_model)
    @jwt_required()
    def get(self, email):
        return get_produtos_by_fornecedor_email(email)
