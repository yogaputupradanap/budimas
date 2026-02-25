from  apps.handler import  *
from  apps.helper  import  *
from  apps.widget  import  *
from  sqlalchemy   import  desc
from  .            import  Base
from  apps.models  import  (
      Produk,
      ProdukUOM as UOM
)


class ProdukService(Base) :

    def __init__(self) :
        super().__init__()


    @handle_error
    def fetch_option(self) :
        with self.db.session.begin() :
            return (
                Produk.query.with_entities(
                    Produk  .id,
                    Produk  .kode_sku  .label('kode'),
                    Produk  .nama,
                )
                .filter_by(**self.set_param())
                .all()
            )

    

    @handle_error
    def fetch_detail_transaksi(self, id):
        with self.db.session.begin():
            result = (
                Produk.query.with_entities(
                    Produk.id.label('produk_id'),
                    Produk.kode_sku.label('kode_sku'),
                    Produk.nama.label('nama'),
                    Produk.harga_beli.label('harga_beli'),
                )
                .filter_by(id=id)
                .first()
            )

            return dict(result._mapping) if result else {}


    @handle_error
    def fetch_detail_transaksi_uom(self, id) :
        with self.db.session.begin() :
            return (
                UOM.query.with_entities(
                    UOM  .id               .label('uom_id'             ),
                    UOM  .kode             .label('uom_kode'           ),
                    UOM  .nama             .label('uom_nama'           ),
                    UOM  .level            .label('uom_level'          ),
                    UOM  .faktor_konversi  .label('uom_faktor_konversi'),
                )
                .filter_by(id_produk = id)
                .order_by(desc(UOM.level))
                .all()
            )


    @handle_error
    def daftar_option(self) :
        text = lambda i : (
            f"[{i['kode']}] {i['nama']}" if i['kode'] else f"{i['nama']}"
        )
        return (
            Mapper(self.fetch_option())
                .to_dict()
                .add_col(lambda i : text(i), "text")
                .get()
        )
    
    @handle_error
    def daftar_option_principal(self,id):
        def text(i):
            return (
                f"[{i['kode']}] {i['nama']}" if i['kode'] else f"{i['nama']}"
            )

        with self.db.session.begin():
            options = (
                Produk.query.with_entities(
                    Produk.id,
                    Produk.kode_sku.label('kode'),
                    Produk.nama,
                )
                .filter_by(id_principal=id)
                .all()
            )

        return (
            Mapper(options)
                .to_dict()
                .add_col(lambda i: text(i), "text")
                .get()
        )



    @handle_error
    def konversi_harga(satuan_target, satuan, produk) :
        satuan_awal   = min(satuan, key=lambda i : i['uom_level'])
        harga_awal    = produk['produk_harga_beli']
        faktor_awal   = satuan_awal['uom_faktor_konversi']
        faktor_target = satuan_target['uom_faktor_konversi']
        
        return harga_awal * (faktor_target / faktor_awal)


    @handle_error
    def konversi_jumlah(satuan_awal) :
        jumlah_awal   = satuan_awal['jumlah']
        faktor_awal   = satuan_awal['uom_faktor_konversi']
        faktor_target = 1
        
        return jumlah_awal * (faktor_awal / faktor_target)
    
    def konversi_jumlah_total(satuan) :
        total = 0
        for satuan_awal in satuan :
            if satuan_awal and satuan_awal['jumlah'] :
                jumlah_awal   = int(satuan_awal['jumlah']) 
                faktor_awal   = int(satuan_awal['uom_faktor_konversi'])
                faktor_target = 1
                total         += jumlah_awal * (faktor_awal / faktor_target)
        
        return total

    