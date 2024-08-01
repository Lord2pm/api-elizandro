from flask_restx import Namespace, fields


class ProdutoDto:
    api = Namespace("produtos", description="Operações relacionadas a produtos")

    produto_model = api.model(
        "Produto",
        {
            "id": fields.Integer(readOnly=True, description="ID do produto"),
            "nome": fields.String(required=True, description="Nome do produto"),
            "preco": fields.Float(required=True, description="Preço do produto"),
            "categoria": fields.String(
                required=True, description="Categoria do produto"
            ),
            "imagem": fields.String(required=False, description="Foto do produto"),
            "qtd_stock": fields.Integer(
                required=False, description="Quantidade em estoque"
            ),
            "vendedor_id": fields.Integer(required=True, description="ID do vendedor"),
        },
    )
