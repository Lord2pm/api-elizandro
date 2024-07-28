from flask_restx import Namespace, fields


class VendasDto:
    api = Namespace("vendas", description="Operações relacionadas a vendas")

    venda_model = api.model(
        "Venda",
        {
            "id": fields.Integer(readOnly=True, description="ID da venda"),
            "cliente_id": fields.Integer(required=True, description="ID do cliente"),
            "produto_id": fields.Integer(required=True, description="ID do produto"),
            "quantidade": fields.Integer(
                required=True, description="Quantidade do produto"
            ),
            "fornecedor_id": fields.Integer(
                required=True, description="ID do fornecedor"
            ),
        },
    )
