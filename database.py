from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Buku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False, index=True)
    penulis = db.Column(db.String(100), nullable=False, index=True)
    tahun_penerbit = db.Column(db.Integer, nullable=True)
    def to_dict(self):
        return{
            "id": self.id,
            "judul": self.judul,
            "penulis": self.penulis,
            "tahun_penerbit": self.tahun_penerbit
        }

class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), default="user")
    def to_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "role": self.role
        }