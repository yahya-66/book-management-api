from flask import Flask, jsonify, request
from database import db, User
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
load_dotenv()
import logging
from logging.handlers import RotatingFileHandler
from flasgger import Swagger
from routes._init_ import register_routes
from utils.response import error_response
from utils.exceptions import (APIException)
from extensions import limiter
from flask_migrate import Migrate
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
Swagger(app)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB
jwt = JWTManager(app)
limiter.init_app(app)
@jwt.unauthorized_loader
def unauthorized(error):
	return jsonify({
		"status": "error",
		"message": "Token tidak ditemukan"
	}), 401

@jwt.invalid_token_loader
def invalid_token(error):
	return jsonify({
		"status": "error",
		"message": "Token tidak valid"
	}), 422

@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
	return jsonify({
		"status": "error",
		"message": "Token telah kadaluarsa"
	}), 401

app.config["SQLALCHEMY_DATABASE_URI"] = (
	f"postgresql+psycopg2://"
	f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
	f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
register_routes(app)
migrate = Migrate(app, db)

@app.errorhandler(APIException)
def handle_api_exception(e):
	app.logger.warning(f"APIException: {e.message} (status code: {e.status_code})")
	return error_response(message=e.message, status_code=e.status_code)

@app.route("/")
def home():
	return jsonify({
		"status": "success",
		"message": "REST API",
		"version": "1.0"
	})

@app.errorhandler(404)
def not_found(error):
	return jsonify({
		"status": "error",
		"message": "Endpoint tidak ditemukan"
	}), 404

@app.errorhandler(500)
def internal_error(error):
	return jsonify({
		"status": "error",
		"message": "Terjadi kesalahan pada server"
	}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
	return jsonify({
		"status": "error",
		"message": "Terlalu banyak percobaan, silakan coba lagi nanti"
	}), 429

if not app.debug:
	handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter(
		"%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]"
	)
	handler.setFormatter(formatter)
	app.logger.addHandler(handler)
	app.logger.setLevel(logging.INFO)

if __name__== "__main__":
	app.run(debug=True)

