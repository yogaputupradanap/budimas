from apps.conn2 import db
from apps.models import BaseModel
class Wilayah1(BaseModel):
    __tablename__ = 'wilayah1'
    # id = db.Column(db.Integer, primary_key=True)
    # nama = db.Column(db.String(100))

    nama = BaseModel.string(100)

class Wilayah2(BaseModel):
    __tablename__ = 'wilayah2'
    # id = db.Column(db.Integer, primary_key=True)
    # nama = db.Column(db.String(100))
    # id_wilayah1 = db.Column(db.Integer, db.ForeignKey('wilayah1.id'))

    nama = BaseModel.string(100)
    id_wilayah1 = BaseModel.foreign('wilayah1.id')

class Wilayah3(BaseModel):
    __tablename__ = 'wilayah3'
    # id = db.Column(db.Integer, primary_key=True)
    # nama = db.Column(db.String(100))
    # id_wilayah2 = db.Column(db.Integer, db.ForeignKey('wilayah2.id'))

    nama = BaseModel.string(100)
    id_wilayah2 = BaseModel.foreign('wilayah2.id')

class Wilayah4(BaseModel):
    __tablename__ = 'wilayah4'
    # nama = db.Column(db.String(100))
    # id_wilayah3 = db.Column(db.Integer, db.ForeignKey('wilayah3.id'))

    id = db.Column(db.BigInteger, primary_key=True)
    nama = BaseModel.string(100)
    id_wilayah3 = BaseModel.foreign('wilayah3.id')