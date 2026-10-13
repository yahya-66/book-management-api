from database import Buku, db

def get_all():
    return Buku.query.all()

def get_by_id(id):
    return Buku.query.get(id)

def create(judul, penulis):
    buku = Buku(judul=judul, penulis=penulis)
    db.session.add(buku)
    db.session.commit()
    return buku 

def delete(id):
    buku = Buku.query.get(id)
    if buku:
        db.session.delete(buku)
        db.session.commit()
        return True
    return None

def update(id, judul, penulis):
    buku = Buku.query.get(id)
    if buku:
        buku.judul = judul
        buku.penulis = penulis
        db.session.commit()
        return buku
    return None

def search(judul=None, penulis=None):
    query = Buku.query
    if judul:
        query = query.filter(Buku.judul.like(f"%{judul}%"))
    if penulis:
        query = query.filter(Buku.penulis.like(f"%{penulis}%"))
    return query.all()