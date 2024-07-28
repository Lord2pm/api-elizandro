from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .config import Config
from api.models.models import db
from api.controllers import (
    cliente_controllers,
    fornecedor_controllers,
    produto_controllers,
    venda_controllers,
)
from api.utils import send_email


app = Flask(__name__)
app.config.from_object(Config)

api = Api(
    app,
    title="API do Elizandro",
    version="1.0",
    description="API para gerenciar as operações de um App de venda de produtos agrícolas",
)
db.init_app(app)
JWTManager(app)
CORS(app)
ma = Migrate(app, db)
send_email.mail.init_app(app)

api.add_namespace(cliente_controllers.api, path="/auth/clientes")
api.add_namespace(venda_controllers.api, path="/vendas")
api.add_namespace(produto_controllers.api, path="/produtos")
api.add_namespace(fornecedor_controllers.api, path="/auth/fornecedores")


if __name__ == "__main__":
    app.run()
