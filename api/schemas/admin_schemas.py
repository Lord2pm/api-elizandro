from flask_restx import Namespace, fields


class AdminDto:
    api = Namespace("admin", description="Operações relacionadas a admin")

    admin = api.model(
        "Admin",
        {
            "id": fields.Integer(readOnly=True, description="ID do Admin"),
            "email": fields.String(required=True, description="E-mail do Admin"),
            "senha": fields.String(required=True, description="Senha do Admin")
        },
    )
