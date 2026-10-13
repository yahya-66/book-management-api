from flask import Blueprint, jsonify, request
from database import Buku, db
from services.buku_service import (
    cari_buku,
    tambah_buku as tambah_buku_service,
    hapus_buku as hapus_buku_service,
    update_buku as update_buku_service,
    daftar_buku,
    validasi_buku
)
from flask_jwt_extended import jwt_required, get_jwt
from utils.exceptions import NotFoundException
from utils.response import success_response, error_response
from flask import current_app 
buku_bp = Blueprint("buku", __name__)

def admin_required():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Akses ditolak. Hanya admin"}), 403
    return None

"""
Menampilkan daftar buku
---
tags:
  - Buku
responses:
  200:
    description: Berhasil mengambil data buku
"""
@buku_bp.route("/buku", methods=["GET"])
@jwt_required()
def get_buku():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)
    sort = request.args.get("sort", "id")
    order = request.args.get("order", "asc")
    judul = request.args.get("judul")
    penulis = request.args.get("penulis")
    semua_buku, total = daftar_buku(
        page=page,
        limit=limit,
        sort=sort,
        order=order,
        judul=judul,
        penulis=penulis
    )
    return success_response(
        data={
            "page": page,
            "limit": limit,
            "total": total,
            "data": [buku.to_dict() for buku in semua_buku]
        },
        message="Berhasil mengambil data buku"
    )

"""
Mengambil detail buku berdasarkan ID
---
tags:
  - Buku
parameters:
  - name: id
    in: path
    type: integer
    required: true
resposes:
  200:
    description: Berhasil mengambil data buku
  400:
    description: Buku tidak ditemukan
"""
@buku_bp.route("/buku/<int:id>", methods=["GET"])
@jwt_required()
def get_buku_by_id(id):
    id_buku = cari_buku(id)
    if id_buku is None: 
        raise NotFoundException("Buku tidak ditemukan")
    return success_response(
        data=id_buku.to_dict(),
        message="Buku ditemukan"
    )
"""
Mengubah data buku
---
tags:
  - Buku
parameters:
  - name: id
    in: path
    type: integer
    requireed: true
  - in: body
    name: body
    required: true
    schema:
      properties:
         judul:
           type: string
         penulis: 
           type: string
responses:
   200:
     description: Buku berhasil diupdate
   404:
     description: Buku tidak ditemukan
"""
@buku_bp.route("/buku/<int:id>", methods=["PUT"])
@jwt_required()
def update_buku(id):
    cek = admin_required()
    if cek:
        return cek
    data = request.get_json()
    validasi_buku(data)
    buku = update_buku_service(
        id,
        data["judul"],
        data["penulis"]
    )
    if buku is None:
        raise NotFoundException("Buku tidak ditemukan")
    current_app.logger.info(f"Buku diupdate: {buku.judul}")
    return success_response(
        data=buku.to_dict(),
        message="Buku berhasil diupdate"
    )

"""
Menghapus buku
---
tags:
  - Buku
parameters:
  - name: id
    in: path
    type: integer
    required: true
responses:
  200:
    description: Buku berhasil dihapus
  404:
    description: Buku tidak ditemukan
"""
@buku_bp.route("/buku/<int:id>", methods=["DELETE"])
@jwt_required()
def hapus_buku(id):
    cek = admin_required()
    if cek:
        return cek
    berhasil = hapus_buku_service(id)
    if not berhasil:
        raise NotFoundException("Buku tidak ditemukan")
    current_app.logger.info(f"Buku dihapus: {id}")
    return success_response(message="Buku berhasil dihapus")

"""
Menambahkan buku baru
---
tags:
  - Buku
security: 
  - Bearer: []
parameters:
  - in: body
    name: body
    required: true
    schema: 
      properties:
         judul:
           type: string
         penulis:
           type: string
responses:
  201:
    descrption: Buku berhasil ditambahkan
  400:
    description: Data tidak valid
"""
@buku_bp.route("/buku", methods=["POST"])
@jwt_required()
def tambah_buku():
    cek = admin_required()
    if cek:
        return cek
    data = request.get_json()
    validasi_buku(data)
    buku_baru = tambah_buku_service(
        data["judul"],
        data["penulis"]
    )
    current_app.logger.info(f"Buku baru ditambahkan: {buku_baru.judul}")
    return success_response(data=buku_baru.to_dict(), message="Buku berhasil ditambahkan", status_code=201)
