from database import db, User
from flask import Blueprint, app, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import(
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from utils.response import success_response, error_response
from utils.exceptions import NotFoundException, ValidationException, ForbiddenException
from extensions import limiter
user_bp = Blueprint("user", __name__)

ALLOWED_EXTENSTIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSTIONS
    )

def admin_required():
    claims = get_jwt()
    if claims.get("role") != "admin":
        raise ForbiddenException("Akses ditolak. Hanya admin", 403)
    return None

@user_bp.route("/register", methods=["POST"])
def register():
    """
    Register User
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Register berhasil
    """
    data = request.get_json()
    if not data:
        return error_response("Request body wajib diisi", 400)
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return error_response("Username dan password wajib diisi", 400)
    if len(password) < 8:
        return error_response("Password minimal 8 karakter", 400)
    if User.query.filter_by(username=username).first():
        return error_response("Username sudah digunakan", 400)
    hashed_password = generate_password_hash(password)
    user = User(
        username=username,
        password=hashed_password,
        role="user"
    )
    db.session.add(user)
    db.session.commit()
    return success_response(user.to_dict(), message="Register berhasil", status_code=201)

@user_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    """
    Login User
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Login berhasil
    """
    data = request.get_json()
    if not data:
        return error_response("Request body wajib diisi", 400)
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return error_response("Username dan password wajib diisi", 400)
    user = User.query.filter_by(username=username).first()
    if not user:
        return error_response("Username tidak ditemukan", 404)
    if not check_password_hash(user.password, password):
        return error_response("Password salah", 401)
    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )
    refresh_token = create_refresh_token(identity=str(user.id))
    current_app.logger.info(f"User login: {user.username}")
    return success_response(
        {
        "token": token,
        "refresh_token": refresh_token
        },
        message="Login berhasil"
    )

@user_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    indentity = get_jwt_identity()
    user = User.query.get(indentity)
    if not user:
        return error_response("User tidak ditemukan", 404)
    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )
    return success_response(
        {
        "token": token
        },
        message="Refresh token berhasil diperbarui"
    )

@user_bp.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return error_response("File tidak ditemukan", 400)
    file = request.files["file"]
    if file.filename == "":
        return error_response("Tidak ada file yang dipilih", 400)
    if not allowed_file(file.filename):
        return error_response("Format file tidak didukung", 400)
    filename = secure_filename(file.filename)
    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"], filename
    )
    file.save(filepath)
    return success_response(
        {
        "filename": filename
        },
        message="Upload berhasil",
        status_code=201
    )

@user_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    admin_required()
    users = User.query.all()
    return success_response([
        {
            "id": user.id,
            "username": user.username,
            "role": user.role 
        }
        for user in users
    ])