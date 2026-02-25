from flask import Blueprint

from apps.lib.pubsub import received_messages
from apps.services.Akuntansi import *
from apps.services.BaseServices import token_auth

akuntansi = Blueprint('akuntansi', __name__, url_prefix='/api/akuntansi/')
akuntansi.before_request(lambda: token_auth.login_required(lambda: None)())
pubsub = Blueprint('pubsub', __name__, url_prefix='/api/pubsub/')


# routes for jurnal
@akuntansi.route('get-jurnal', methods=['GET'])
def _getJurnal():
    return Jurnal().getJurnal()

@akuntansi.route('get-bukubesar', methods=['GET'])
def _getBukubesar():
    return Jurnal().getBukuBesar()


@akuntansi.route('detail-jurnal/<id_jurnal>', methods=['GET'])
def _detailJurnal(id_jurnal):
    return Jurnal().detailJurnal(id_jurnal)


# routes for hutang
@akuntansi.route('get-hutang', methods=['GET'])
def _getHutang(): return Hutang().getHutang()


@akuntansi.route('get-tagihan-purchase', methods=['GET'])
def _getAddTagihan(): return Hutang().getAddTagihan()


@akuntansi.route('create-tagihan-purchase', methods=['POST'])
def _createTagihanPurchase(): return Hutang().createTagihanPurchase()


@akuntansi.route('detail-tagihan-purchase', methods=['GET'])
def _detailtagihanPurchase(): return Hutang().detailTagihanPurchasing()


@akuntansi.route('create-pembayaran-tagihan', methods=['POST'])
def _createPembayaranTagihan(): return Hutang().updatePembayaranTagihan()


# get list setoran tunai tipe setoran : 1 (tunai), 2 (non tunai)
@akuntansi.route('list-setoran-tunai', methods=['GET'])
def _listSetoran():
    # print("ROUTE HIT")
    return Setoran().getListSetoran(1)


@akuntansi.route('list-setoran-non-tunai', methods=['GET'])
def _listSetoranNonTunai(): return Setoran().getListSetoran(2)


@akuntansi.route('detail-setoran', methods=['GET'])
def _detailSetoran(): return Setoran().getDetailListSetoran()


@akuntansi.route('konfirmasi-setoran', methods=['POST'])
def _konfirmasiSetoran(): return Setoran().konfirmasiSetoran()


@akuntansi.route('add-biaya-lain', methods=['POST'])
def _addBiayaLain(): return Setoran().addBiayaLainnya()


@akuntansi.route('get-list-pengeluaran-kasir', )
def _getListPengeluaranKasir(): return Kasir().getListPengeluaranKasir()


@akuntansi.route('add-pengeluaran-kasir', methods=['POST'])
def _addPengeluaranKasir(): return Kasir().addPengeluaranKasir()


@akuntansi.route('get-konfirmasi-pengeluaran', methods=['GET'])
def _getKonfirmasiPengeluaranKasir(): return Kasir().getKonfirmasiPengeluaranKasir()


@akuntansi.route('konfirmasi-pengeluaran', methods=['POST'])
def _konfirmasiPengeluaranKasir(): return Kasir().konfirmasiPengeluaranKasir()


@akuntansi.route('list-laporan-kasir', methods=['GET'])
def _listLaporanKasir(): return Kasir().listLaporanKasir()


@akuntansi.route('get-detail-laporan-kasir')
def _getDetailLaporanKasir(): return Kasir().getDetailLaporanKasir()


@akuntansi.route('get-lph', methods=['GET'])
def _getLph(): return lph().getLph()


@akuntansi.route('get-add-lph', methods=['GET'])
def _getAddLph(): return lph().getAddLph()


@akuntansi.route('get-add-lph-customer', methods=['GET'])
def _getAddLphByCustomer(): return lph().getAddLphByCustomer()


@akuntansi.route('get-add-lph-modal', methods=['GET'])
def _getAddLphModal(): return lph().getAddLphModal()


@akuntansi.route('get-add-lph-customer-modal', methods=['GET'])
def _getAddLphCustomerModal(): return lph().getAddLphCustomerModal()


@akuntansi.route('add-lph', methods=['POST'])
def _addLph(): return lph().addLph()


@akuntansi.route('get-detail-lph', methods=['GET'])
def _getDetailLph(): return lph().getDetailLph()


@akuntansi.route('cetak-ulang-lph', methods=['POST'])
def _cetakUlangLph(): return lph().cetakUlangLph()


@akuntansi.route('simpan-kasir-setoran', methods=['POST'])
def _simpanKasirSetoran(): return Setoran().simpanKasirSetoran()


@akuntansi.route('insert-mutasi', methods=['POST'])
def _insertMutasi(): return Mutasi().insertMutasi()


@akuntansi.route('get-list-konfirmasi-setoran-nontunai', methods=['GET'])
def _getListKonfirmasiSetoranNonTunai():
    return Mutasi().getListKonfirmasiSetoranNonTunai()


@akuntansi.route('get-detail-setoran-nontunai/<id_mutasi>', methods=['GET'])
def _getDetailKonfirmasiSetoranNonTunai(id_mutasi):
    return Mutasi().getDetailKonfirmasiSetoranNonTunai(id_mutasi)


@akuntansi.route("get-list-faktur-setoran/<type>", methods=["GET"])
def _getListFakturSetoran(type):
    return Setoran().getListFakturSetoran(type)


@akuntansi.route("insert-setoran-konfirmasi-non-tunai/customer/<id_mutasi>", methods=["POST"])
def _insertSetoranKonfirmasiNonTunaiByCustomer(id_mutasi):
    return Setoran().insertSetoranKonfirmasiNonTunaiByCustomer(id_mutasi)


@akuntansi.route("insert-setoran-konfirmasi-non-tunai/sales/<id_mutasi>", methods=["POST"])
def _insertSetoranKonfirmasiNonTunaiBySales(id_mutasi):
    return Setoran().insertSetoranKonfirmasiNonTunaiBySales(id_mutasi)


@akuntansi.route('get-list-credit-note', methods=['GET'])
def _getListCreditNote():
    return CreditNote().getCreditNoteList()


@akuntansi.route('get-list-konfirmasi-setoran-tunai', methods=['GET', 'OPTIONS'])
def _getListKonfirmasiSetoranTunai():
    return Setoran().getListKonfirmasiSetoranTunai()


@akuntansi.route('get-detail-setoran-tunai/<nama_pj>/<draft_tanggal_input>', methods=['GET'])
def _getDetailKonfirmasiSetoranTunai(nama_pj, draft_tanggal_input):
    return Setoran().getDetailKonfirmasiSetoranTunai(nama_pj, draft_tanggal_input)


@akuntansi.route('konfirmasi-setoran-tunai', methods=['POST'])
def _konfirmasiSetoranTunai():
    return Setoran().konfirmasiSetoranTunai()


@akuntansi.route('get-list-transaksi', methods=['GET'])
def _getListTransaksi():
    return Transaksi().getListTransaksi()


@akuntansi.route('insert-transaksi', methods=['POST'])
def _insertTransaksi():
    return Transaksi().insertTransaksi()


@akuntansi.route('update-transaksi', methods=['PUT'])
def updateTransaksi():
    return Transaksi().updateTransaksi()


@akuntansi.route('get-list-coa', methods=['GET'])
def _getCoaList():
    return Coa().getCoaList()

@akuntansi.route('get-list-coa-list', methods=['GET'])
def _getCoaList2():
    return Coa().getCoaList2()


@akuntansi.route('insert-coa', methods=['POST'])
def _insertCoa():
    return Coa().insertCoa()


@akuntansi.route('update-coa', methods=['PUT'])
def _updateCoa():
    return Coa().updateCoa()


@akuntansi.route("insert-jurnal-mal", methods=["POST"])
def _insertJurnalMal():
    return JurnalMal().insert_jurnal_mal()


@akuntansi.route("get-jurnal-mal-list", methods=["GET"])
def _getJurnalMalList():
    return JurnalMal().get_jurnal_mal_list()


@akuntansi.route("get-jurnal-mal-detail/<id_jurnal_mal>", methods=["GET"])
def _getJurnalMalDetail(id_jurnal_mal):
    return JurnalMal().get_jurnal_mal_detail(id_jurnal_mal)


@akuntansi.route("update-jurnal-mal", methods=["PUT"])
def _updateJurnalMal():
    return JurnalMal().update_jurnal_mal()


@akuntansi.route("coa-used-jurnal", methods=["GET"])
def _coaUsedJurnal():
    return JurnalMal().get_jurnal_active_use_coa()


@akuntansi.get("coa-used-coa")
def _coaUsedCoa():
    return Coa().getCoasByIdCoa()


@akuntansi.get("get-source-modul-use-jurnal-setting")
def _getSourceModulUseJurnalSetting():
    return SourceModul().getSourceModulAndListJurnalSettingUsedSourceModul()


@pubsub.route("/pubsub-handle", methods=["POST"])
@pubsub.route("/pubsub-handle/", methods=["POST"])
def _pubsubHandle():
    data = received_messages()
    print("LOG: Data masuk ke Handler:", data) # <-- Tambahkan ini
    id_fitur_mals = data.get('id_fitur_mal')

    # pastikan selalu dalam bentuk list
    if isinstance(id_fitur_mals, int):
        id_fitur_mals = [id_fitur_mals]
    elif not isinstance(id_fitur_mals, list):
        id_fitur_mals = []  # fallback kosong kalau bukan int/list

    # looping semua id_fitur_mal yang dikirim
    for id_fitur_mal in id_fitur_mals:
        match id_fitur_mal:
            case 1:
                print("Handling konfirmasi purchase", data)
                PubSubService().handle_konfirmasi_purchase(data=data)
            case 2:
                print("Handling konfirmasi tagihan", data)
                PubSubService().handle_konfirmasi_tagihan(data=data)
            case 3:
                print("Handling picking", data)
                PubSubService().handle_picking(data=data)
            case 4:
                print("Handling shipping", data)
                PubSubService().handle_shipping(data=data)
            case 5:
                print("Handling realisasi", data)
                PubSubService().handle_realisasi(data=data)
            case 6:
                print("Handling piutang non tunai", data)
                PubSubService().handle_piutang_non_tunai(data=data)
            case 7:
                print("Handling terima stock opname", data)
                PubSubService().handle_terima_stock_opname(data=data)
            case 8:
                print("Handling close eskalasi stock opname", data)
                PubSubService().handle_close_eskalasi_stock_opname(data=data)
            case 9:
                print("Handling konfirmasi penerimaan stock transfer", data)
                PubSubService().handle_konfirmasi_penerimaan_stock_transfer(data=data)
            case 10:
                print("Handling konfirmasi close eskalasi stock transfer", data)
                PubSubService().handle_konfirmasi_close_eskalasi_penerimaan_stock_transfer(data=data)
            case 11:
                print("Handling konfirmasi pengeluaran kasir", data)
                PubSubService().handle_konfirmasi_pengeluaran_kasir(data=data)
            case 12:
                print("Handling piutang tunai", data)
                PubSubService().handle_piutang_tunai(data=data)
            case 13:
                print("Handling konfirmasi kasir tunai sales", data)
                PubSubService().handle_konfirmasi_kasir_tunai_sales(data=data)
            case 14:
                print("Handling konfirmasi kasir tunai kepala gudang", data)
                PubSubService().handle_konfirmas_kasir_tunai_kepala_gudang(data=data)
            case 15:
                print("Handling ajukan pengeluaran kasir", data)
                PubSubService().handle_ajukan_pengeluaran_kasir(data=data)
            case 16:
                print("Handling realisasi cod", data)
                PubSubService().handle_realisasi_cod(data=data)
            case 17:
                print("Handling request purchase", data)
                PubSubService().handle_request_purchase(data=data)
            case 18:
                print("Handling konfirmasi request purchase", data)
                PubSubService().handle_konfirmasi_purchase(data=data)
            case 19:
                print("Handling penerimaan barang", data)
                PubSubService().handle_penerimaan_barang(data=data)
            case 20:
                print("Handling konfirmasi purchase potongan hutang", data)
                PubSubService().handle_konfirmasi_purchase_potongan_hutang(data=data)
            case 21:
                print("Handling buat tagihan", data)
                PubSubService().handle_buat_tagihan(data=data)
            case 22:
                print("Handling buat tagihan potongan hutang", data)
                PubSubService().handle_buat_tagihan_potongan_hutang(data=data)
            case 23:
                print("Handling konfirmasi tagihan potongan hutang", data)
                PubSubService().handle_konfirmasi_tagihan_potongan_hutang(data=data)
            case 24:
                print("Handling ajukan kasbon klaim", data)
                PubSubService().handle_ajukan_kasbon_klaim(data=data)
            case 25:
                print("Handling konfirmasi kasbon klaim", data)
                PubSubService().handle_konfirmasi_kasbon_klaim(data=data)
            case 26:
                print("Handling klaim sudah digunakan", data)
                PubSubService().handle_klaim_sudah_digunakan(data=data)
            case _:
                print(f"Tidak ada handler untuk id_fitur_mal = {id_fitur_mal}")

    return {"message": "All handlers executed successfully"}
