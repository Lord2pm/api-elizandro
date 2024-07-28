from flask_restx import Namespace, fields


class ClienteDto:
    api = Namespace("clientes", description="Operações relacionadas a clientes")

    cliente = api.model(
        "Cliente",
        {
            "id": fields.Integer(readOnly=True, description="ID do cliente"),
            "email": fields.String(required=True, description="E-mail do cliente"),
            "nome_completo": fields.String(
                required=True, description="Nome do cliente"
            ),
            "telefone": fields.String(
                required=True, description="Número de telefone do cliente"
            ),
            "senha": fields.String(required=True, description="Senha do cliente"),
            "endereco": fields.String(description="Endereço do cliente"),
        },
    )

    cliente_login = api.model(
        "ClienteLogin",
        {
            "email": fields.String(required=True, description="E-mail do cliente"),
            "senha": fields.String(required=True, description="Senha do cliente"),
        },
    )

    cliente_password_recovery = api.model(
        "ClientePasswordRecovery",
        {"email": fields.String(required=True, description="E-mail do cliente")},
    )
