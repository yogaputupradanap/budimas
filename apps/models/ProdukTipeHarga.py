from apps.models.BaseModel import BaseModel

class ProdukTipeHarga(BaseModel):
    __tablename__ = 'produk_tipe_harga'

    # Kolom tabel
    kode = BaseModel.string(10)
    nama = BaseModel.string(25)

    def __repr__(self):
        return f"ProdukTipeHarga('{self.id}', '{self.nama}')"

    def __init__(self, data=None):
        self.set(data)

    def set(self, data=None):
        if data:
            self.id = data.get('id')
            self.kode = data.get('kode')
            self.nama = data.get('nama')
        return self