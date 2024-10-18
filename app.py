from flask import Flask
from flask_cors import CORS
from avatar.routes import avatar_bp
from config import Config
from at_client import at_client_extension

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(avatar_bp)

at_client_extension.init_app(app)