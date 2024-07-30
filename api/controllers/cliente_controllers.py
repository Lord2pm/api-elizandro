from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from api.schemas.cliente_schemas import ClienteDto
from api.utils.send_email import email_send
from api.services.cliente_services import (
    create_cliente,
    cliente_login,
    get_cliente,
    cliente_password_recovery,
    activate_cliente,
)

api = ClienteDto.api
_cliente = ClienteDto.cliente
_cliente_login = ClienteDto.cliente_login
_cliente_password_recovery = ClienteDto.cliente_password_recovery


@api.route("/create-account")
class ClienteCreateList(Resource):
    @api.response(code=201, description="Conta criada com sucesso")
    @api.expect(_cliente, validate=True)
    @api.marshal_with(_cliente)
    def post(self):
        data = request.json
        cliente = create_cliente(data=data)

        if cliente:
            email_send(
                f"A sua conta foi criada com sucesso. Use o botão abaixo para activar.\n\nhttp://localhost/auth/clientes/active-account/{cliente.email}",
                cliente.email,
                "Conta criada com sucesso",
            )
            return cliente, 201

        return api.abort(400, "E-mail já cadastrado")


@api.route("/active-account/<email>")
class ActiveAccount(Resource):
    @api.response(code=200, description="Conta activada com sucesso")
    def get(self, email):
        activate_cliente(email)
        return "Conta activada", 200


@api.route("/login")
class ClienteLogin(Resource):
    @api.response(code=200, description="Login feito com sucesso")
    @api.expect(_cliente_login, validate=True)
    def post(self):
        data = request.json
        cliente_tokens = cliente_login(data=data)

        if not cliente_tokens:
            return api.abort(
                400,
                "E-mail ou senha inválidos. Se já criou uma conta, verifique os dados de login ou vá para sua caixa de e-mail e active sua conta",
            )

        return cliente_tokens


@api.route("/get-cliente")
class GetClienteByToken(Resource):
    @api.response(code=200, description="Cliente encontrado com sucesso")
    @api.marshal_with(_cliente)
    @jwt_required()
    def get(self):
        cliente = get_cliente()
        return cliente


@api.route("/password-recovery")
class PasswordRecovery(Resource):
    @api.response(code=200, description="Senha recuperada com sucesso")
    @api.expect(_cliente_password_recovery, validate=True)
    @api.marshal_with(_cliente, code=200)
    def put(self):
        data = request.json
        cliente, senha = cliente_password_recovery(data)

        if not cliente:
            return api.abort(400, "E-mail não encontrado")

        email_send(
            f"A sua nova senha é: {senha}",
            cliente.email,
            "Recuperação de senha",
        )
        return cliente
