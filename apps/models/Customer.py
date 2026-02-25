from apps.conn2 import db
from apps.datatables import DataTables, DictMapper
from apps.models.BaseModel import BaseModel
from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request
from sqlalchemy import text
from sqlalchemy.orm import relationship

from apps.widget import btn_actions

db

class Customer(BaseModel):
    __tablename__ = 'customer'


    # Kolom tabel
    nama = BaseModel.string(50)
    alamat = BaseModel.string(100)
    telepon = BaseModel.string(20)
    npwp = BaseModel.string(25)
    id_wilayah1 = BaseModel.integer()
    id_wilayah2 = BaseModel.integer()
    id_wilayah3 = BaseModel.bigInteger()
    id_wilayah4 = BaseModel.bigInteger()
    id_tipe = BaseModel.foreign('customer_tipe.id')
    id_cabang = BaseModel.foreign('cabang.id')
    no_rekening = BaseModel.string(20)
    pic = BaseModel.string(50)
    longitude = BaseModel.string(25)
    latitude = BaseModel.string(25)
    telepon2 = BaseModel.string(20)
    kode = BaseModel.string(30)
    id_rute = BaseModel.integer()
    id_tipe_harga = BaseModel.integer()
    is_ppn = BaseModel.integer()
    email = BaseModel.string(50)
    nama_wajib_pajak = BaseModel.string(50)
    alamat_wajib_pajak = BaseModel.string(100)

    # Relationships
    tipe = BaseModel.one_to_many('CustomerTipe', 'customer_tipe', [id_tipe])
    cabang = BaseModel.one_to_many('Cabang', 'cabang', [id_cabang])
    order_batches = relationship(
            "OrderBatchModel",
            back_populates="customer"
        )

    def __repr__(self):
        return f"data('{self.id}', '{self.nama}')"

    # def __init__(self, data=None):
    #     self.set(data)

    def set(self, data=None):
        if data:
            self.id = data.get('id')
            self.nama = data.get('nama')
            self.alamat = data.get('alamat')
            self.telepon = data.get('telepon')
            self.npwp = data.get('npwp')
            self.id_wilayah1 = data.get('id_wilayah1')
            self.id_wilayah2 = data.get('id_wilayah2')
            self.id_wilayah3 = data.get('id_wilayah3')
            self.id_wilayah4 = data.get('id_wilayah4')
            self.id_tipe = data.get('id_tipe')
            self.id_cabang = data.get('id_cabang')
            self.no_rekening = data.get('no_rekening')
            self.pic = data.get('pic')
            self.longitude = data.get('longitude')
            self.latitude = data.get('latitude')
            self.telepon2 = data.get('telepon2')
            self.kode = data.get('kode')
            self.id_rute = data.get('id_rute')
            self.id_tipe_harga = data.get('id_tipe_harga')
            self.is_ppn = data.get('is_ppn')
            self.email = data.get('email')
            self.nama_wajib_pajak = data.get('nama_wajib_pajak')
            self.alamat_wajib_pajak = data.get('alamat_wajib_pajak')
        return self

    @staticmethod
    def allOpt():
        try:
            # Parse request parameters
            term = request.args.get('term', '').strip()
            page = max(1, int(request.args.get('page', 1)))
            selected_id = request.args.get('selected_id')
            page_size = 20

            # If we're fetching initial value (selected_id is present and term is empty)
            if selected_id and not term:
                # First, get the selected item
                selected_query = """
                    SELECT 
                        customer.id,
                        CONCAT('[', customer.kode, '] - [', customer.nama, '] - [', COALESCE(cabang.nama, ''), ']') as display_text,
                        customer.id_cabang
                    FROM customer
                    LEFT JOIN cabang ON cabang.id = customer.id_cabang
                    WHERE customer.id = :selected_id
                """
                selected_result = db.session.execute(text(selected_query), {'selected_id': selected_id}).fetchone()

                if selected_result:
                    return jsonify({
                        'results': [{
                            'id': str(selected_result[0]),
                            'text': selected_result[1],
                            'id_cabang': selected_result[2]
                        }],
                        'pagination': {'more': False}
                    })

            # Regular search query
            query = """
                SELECT 
                    customer.id,
                    CONCAT('[', customer.kode, '] - [', customer.nama, '] - [', COALESCE(cabang.nama, ''), ']') as display_text,
                    customer.id_cabang
                FROM customer
                LEFT JOIN cabang ON cabang.id = customer.id_cabang
                WHERE 1=1
            """
            params = {}

            # Add search condition
            if term:
                query += " AND (LOWER(customer.nama) LIKE :term OR LOWER(customer.kode) LIKE :term)"
                params['term'] = f'%{term.lower()}%'

            # Add ordering
            query += " ORDER BY customer.nama LIMIT :limit OFFSET :offset"

            # Add pagination parameters
            params.update({
                'limit': page_size + 1,
                'offset': (page - 1) * page_size
            })

            # Execute query and format results
            result = db.session.execute(text(query), params)
            items = []
            has_more = False

            for i, row in enumerate(result, 1):
                if i <= page_size:
                    items.append({
                        'id': str(row[0]),
                        'text': row[1],
                        'id_cabang': row[2]
                    })
                else:
                    has_more = True
                    break

            return jsonify({
                'results': items,
                'pagination': {'more': has_more}
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'results': [],
                'pagination': {'more': False},
                'error': str(e)
            }), 500

    base_query = """
    select 
        customer.id,
        customer.nama,
        customer.kode,
        customer_tipe.nama as tipe,
        cabang.nama as nama_cabang,
        produk_tipe_harga.nama as tipe_harga,
        customer.id_cabang,
        customer.pic,
        customer.id_rute,
        customer.id_tipe,
        customer.id_tipe_harga,
        customer.npwp,
        customer.no_rekening,
        customer.telepon,
        customer.telepon2,
        customer.latitude,
        customer.longitude,
        customer.alamat,
        customer.id_wilayah1,
        customer.id_wilayah2,
        customer.id_wilayah3,
        customer.id_wilayah4,
        customer.is_ppn,
        customer.nama_wajib_pajak,
        customer.alamat_wajib_pajak,
        customer.email,
        rute.nama_rute
        
        
    from customer
    left join customer_tipe on customer_tipe.id = customer.id_tipe
    left join cabang on cabang.id = customer.id_cabang
    left join produk_tipe_harga on produk_tipe_harga.id = customer.id_tipe_harga
    left join rute on rute.id = customer.id_rute
    
    """

    @classmethod
    def all_table(cls):
        return DataTables(db).handle(
            base_query=cls.base_query,
            transformer=lambda data: (
                DictMapper(data)
                .to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_actions(i['id']), "actions")
                .get()
            )
        )