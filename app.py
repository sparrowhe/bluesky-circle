from flask import Flask
from flask_cors import CORS

from avatar.routes import avatar_bp
from config import Config
from at_client import at_client_extension

app = Flask(__name__,
    static_folder='./frontend/dist/static',
    template_folder='./frontend/dist'
)
app.config.from_object(Config)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(avatar_bp)

at_client_extension.init_app(app)