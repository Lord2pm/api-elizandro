from flask_restx import Namespace, fields


class FornecedorDto:
    api = Namespace("fornecedores", description="Operações relacionadas a fornecedores")

    fornecedor = api.model(
        "Fornecedor",
        {
            "id": fields.Integer(readOnly=True, description="ID do fornecedor"),
            "email": fields.String(required=True, description="E-mail do fornecedor"),
            "nome_completo": fields.String(
                required=True, description="Nome do fornecedor"
            ),
            "telefone": fields.String(
                required=True, description="Número de telefone do fornecedor"
            ),
            "senha": fields.String(required=True, description="Senha do fornecedor"),
            "loja": fields.String(description="Nome da loja do fornecedor"),
            "endereco": fields.String(description="Endereço do fornecedor"),
            "subscription_status": fields.String(
                description="Status da subscrição do fornecedor"
            ),
            "subscription_end_date": fields.DateTime(
                description="Data do fim da subscrição do fornecedor"
            ),
        },
    )

    fornecedor_produto = api.model(
        "FornecedorProduto",
        {
            "id": fields.Integer(readOnly=True, description="ID do fornecedor"),
            "email": fields.String(required=True, description="E-mail do fornecedor"),
            "nome_completo": fields.String(
                required=True, description="Nome do fornecedor"
            ),
            "telefone": fields.String(
                required=True, description="Número de telefone do fornecedor"
            ),
            "loja": fields.String(description="Nome da loja do fornecedor"),
            "endereco": fields.String(description="Endereço do fornecedor"),
            "subscription_status": fields.String(
                description="Status da subscrição do fornecedor"
            ),
            "subscription_date": fields.String(
                description="Data do fim da subscrição do fornecedor"
            ),
        },
    )

    fornecedor_login = api.model(
        "FornecedorLogin",
        {
            "email": fields.String(required=True, description="E-mail do fornecedor"),
            "senha": fields.String(required=True, description="Senha do fornecedor"),
        },
    )

    fornecedor_password_recovery = api.model(
        "FornecedorPasswordRecovery",
        {"email": fields.String(required=True, description="E-mail do fornecedor")},
    )
