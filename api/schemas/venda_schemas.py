from flask_restx import Namespace, fields

from api.schemas.fornecedor_schemas import FornecedorDto
from api.schemas.cliente_schemas import ClienteDto
from api.schemas.produto_schemas import ProdutoDto


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
            "cliente": fields.Nested(
                ClienteDto.cliente_produto, description="Dados do cliente"
            ),
            "produto": fields.Nested(
                ProdutoDto.produto_model, description="Dados do produto"
            ),
        },
    )

    venda_create = api.model(
        "VendaCreate",
        {
            "id": fields.Integer(readOnly=True, description="ID da venda"),
            "cliente_id": fields.Integer(required=True, description="ID do cliente"),
            "produto_id": fields.Integer(required=True, description="ID do produto"),
            "quantidade": fields.Integer(
                required=True, description="Quantidade do produto"
            ),
            "fornecedor_id": fields.Integer(
                required=True, description="ID do fornecedor"
            )
        },
    )
