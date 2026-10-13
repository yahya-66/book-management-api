from routes.buku import buku_bp
from routes.user import user_bp

def register_routes(app):
    app.register_blueprint(buku_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")