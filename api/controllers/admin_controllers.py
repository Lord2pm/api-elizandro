from flask import request, abort
from flask_restx import Resource

from api.services.admin_services import (
    create_admin,
    admin_login,
    get_admin,
    get_qtd_users,
    get_all_admins,
    get_qtd_fornecedores,
    get_qtd_clientes,
    get_qtd_users_with_active_subscription,
    get_qtd_produtos,
    get_qtd_vendas,
)
from api.schemas.admin_schemas import AdminDto
from api.models.models import Admin, db

api = AdminDto.api
_admin = AdminDto.admin


@api.route("/")
class AdminList(Resource):
    @api.doc("list_admins")
    @api.marshal_list_with(_admin)
    def get(self):
        """Lista todos os admins"""
        return get_all_admins()

    @api.response(201, "Admin criado com sucesso.")
    @api.expect(_admin, validate=True)
    @api.marshal_with(_admin)
    @api.doc("create_admin")
    def post(self):
        """Cria um novo admin"""
        data = request.json
        admin = create_admin(data)
        if admin:
            return admin, 201
        else:
            return abort(400, "Admin já existe ou erro nos dados fornecidos")


@api.route("/login")
class AdminLogin(Resource):
    @api.expect(_admin, validate=True)
    @api.doc("login_admin")
    def post(self):
        """Faz login de um admin"""
        data = request.json
        tokens = admin_login(data)
        if tokens:
            return tokens, 200
        else:
            return abort(401, "E-mail ou senha inválidos")


@api.route("/<int:id>")
@api.param("id", "O identificador do Admin")
@api.response(404, "Admin não encontrado.")
class Admin(Resource):
    @api.doc("get_admin")
    @api.marshal_with(_admin)
    def get(self, id):
        """Obtém um admin pelo ID"""
        admin = get_admin(id)
        if admin:
            return admin
        else:
            return abort(404, "Admin não encontrado")


@api.route("/get-qtd-users")
@api.response(200, "Buscar qtd de usuários cadastrados")
class GetQtdUsers(Resource):
    @api.doc("get_qtd_users")
    def get(self):
        """Buscar qtd de usuários cadastrados"""
        return get_qtd_users(), 200


@api.route("/get-qtd-clientes")
@api.response(200, "Buscar qtd de clientes cadastrados")
class GetQtdClientes(Resource):
    @api.doc("get_qtd_clientes")
    def get(self):
        """Buscar qtd de clientes cadastrados"""
        return get_qtd_clientes(), 200


@api.route("/get-qtd-fornecedores")
@api.response(200, "Buscar qtd de fornecedores cadastrados")
class GetQtdFornecedores(Resource):
    @api.doc("get_qtd_fornecedores")
    def get(self):
        """Buscar qtd de fornecedores cadastrados"""
        return get_qtd_fornecedores(), 200


@api.route("/get-qtd-with-active-subscription")
@api.response(200, "Buscar qtd de usuários com subscrição activa")
class GetQtdWithActiveSubscription(Resource):
    @api.doc("get_qtd_with_active_subscription")
    def get(self):
        """Buscar qtd de usuários coom subscrição activa"""
        return get_qtd_users_with_active_subscription(), 200


@api.route("/get-qtd-produtos")
@api.response(200, "Buscar qtd de produtos")
class GetQtdProdutos(Resource):
    @api.doc("get_qtd_products")
    def get(self):
        """Buscar qtd de produtos"""
        return get_qtd_produtos(), 200


@api.route("/get-qtd-transacoes")
@api.response(200, "Buscar qtd de transações")
class GetQtdTransacoes(Resource):
    @api.doc("get_qtd_transations")
    def get(self):
        """Buscar qtd de transações"""
        return get_qtd_vendas(), 200
