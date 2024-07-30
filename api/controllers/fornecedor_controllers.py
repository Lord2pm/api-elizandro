from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from api.schemas.fornecedor_schemas import FornecedorDto
from api.utils.send_email import email_send
from api.services.fornecedor_services import (
    create_fornecedor,
    fornecedor_login,
    get_fornecedor,
    fornecedor_password_recovery,
    activate_fornecedor,
)

api = FornecedorDto.api
_fornecedor = FornecedorDto.fornecedor
_fornecedor_login = FornecedorDto.fornecedor_login
_fornecedor_password_recovery = FornecedorDto.fornecedor_password_recovery


@api.route("/create-account")
class FornecedorCreateList(Resource):
    @api.response(code=201, description="Conta criada com sucesso")
    @api.expect(_fornecedor, validate=True)
    @api.marshal_with(_fornecedor)
    def post(self):
        data = request.json
        fornecedor = create_fornecedor(data=data)

        if fornecedor:
            email_send(
                f"A sua conta foi criada com sucesso. Use o botão abaixo para activar.\n\nhttp://localhost/auth/active-account/{fornecedor.email}",
                fornecedor.email,
                "Conta criada com sucesso",
            )
            return fornecedor, 201

        return api.abort(400, "E-mail já cadastrado")


@api.route("/active-account/<email>")
class ActiveAccount(Resource):
    @api.response(code=200, description="Conta activada com sucesso")
    def get(self, email):
        activate_fornecedor(email)
        return "Conta activada", 200


@api.route("/login")
class FornecedorLogin(Resource):
    @api.response(code=200, description="Login feito com sucesso")
    @api.expect(_fornecedor_login, validate=True)
    def post(self):
        data = request.json
        fornecedor_tokens = fornecedor_login(data=data)

        if not fornecedor_tokens:
            return api.abort(
                400,
                "E-mail ou senha inválidos. Se já criou uma conta, verifique os dados de login ou vá para sua caixa de e-mail e active sua conta",
            )

        return fornecedor_tokens


@api.route("/get-fornecedor")
class GetFornecedorByToken(Resource):
    @api.response(code=200, description="Fornecedor encontrado com sucesso")
    @api.marshal_with(_fornecedor)
    @jwt_required()
    def get(self):
        fornecedor = get_fornecedor()
        return fornecedor


@api.route("/password-recovery")
class PasswordRecovery(Resource):
    @api.response(code=200, description="Senha recuperada com sucesso")
    @api.expect(_fornecedor_password_recovery, validate=True)
    @api.marshal_with(_fornecedor, code=200)
    def put(self):
        data = request.json
        fornecedor, senha = fornecedor_password_recovery(data)

        if not fornecedor:
            return api.abort(400, "E-mail não encontrado")

        email_send(
            f"A sua nova senha é: {senha}",
            fornecedor.email,
            "Recuperação de senha",
        )
        return fornecedor
