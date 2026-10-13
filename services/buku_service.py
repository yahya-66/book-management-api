from database import Buku, db
from utils.exceptions import ValidationException
import repositories.buku_repository as buku_repo

def validasi_buku(data):
    if not data:
        raise ValidationException("Body JSON tidak boleh kosong")
    if "judul" not in data or "penulis" not in data:
        raise ValidationException("Judul dan Penulis wajib diisi.")
    if not data["judul"].strip() or not data["penulis"].strip():
        raise ValidationException("Judul dan penulis tidak boleh kosong.")
    if len(data["judul"].strip()) < 3:
        raise ValidationException("Nama judul minimal 3 karakter")
    if len(data["penulis"].strip()) < 3:
        raise ValidationException("Nama penulis minimal 3 karakter")

def semua_buku():
    return buku_repo.get_all()

def cari_buku(id):
    return buku_repo.get_by_id(id)

def tambah_buku(judul, penulis):
    return buku_repo.create(judul, penulis)

def hapus_buku(id):
    return buku_repo.delete(id)

def update_buku(id, judul, penulis):
    buku = buku_repo.get_by_id(id)
    if buku is None:
        return None
    return buku_repo.update(id, judul, penulis)

def daftar_buku(page=1, limit=5, sort="id", order="asc", judul=None, penulis=None):
    query = Buku.query
    if judul:
        query = query.filter(
            Buku.judul.like(f"%{judul}%")
        )
    if penulis:
        query = query.filter(
            Buku.penulis.like(f"%{penulis}%")
        )
    total = query.count()
    if hasattr(Buku, sort):
        kolom = getattr(Buku, sort)
        if order == "desc":
            query = query.order_by(kolom.desc())
        else:
            query = query.order_by(kolom.asc())
            semua_buku = query.offset(
                (page - 1) * limit
            ).limit(limit).all()
            return semua_buku, total
