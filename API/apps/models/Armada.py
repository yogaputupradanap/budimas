from apps.conn2 import db
from apps.datatables import DataTables, DictMapper
from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request
from  .  import  BaseModel
from apps.widget import btn_actions


class Armada(BaseModel) :
    id_cabang = BaseModel.foreign('cabang.id')
    id_tipe = BaseModel.foreign('armada_tipe.id')
    nama = BaseModel.string(50)
    no_pelat = BaseModel.string(16)
    kubikasi = BaseModel.integer()
    tanggal_stnk = BaseModel.date()
    tanggal_uji = BaseModel.date()
    keterangan = BaseModel.string(25)
    id_status = BaseModel.integer()

    base_query = """
                                    
        SELECT      armada.id,
                    armada.id_tipe,
                    armada.nama,
                    armada.no_pelat,
                    armada.kubikasi,
                    armada.tanggal_stnk,
                    armada.tanggal_uji,
                    armada.keterangan,
                    armada.id_status,
                    armada_tipe.nama AS tipe,
                    cabang.nama AS nama_cabang,
                    armada.id_cabang
                    
        FROM        armada
                    
        LEFT JOIN   cabang 
            ON      cabang.id = armada.id_cabang
                    
        LEFT JOIN   armada_tipe 
            ON      armada_tipe.id = armada.id_tipe
                                    
        """

    @classmethod
    def all(cls):
        return DB(request).setRawQuery(cls.base_query).execute().fetchall().get()

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
    
    