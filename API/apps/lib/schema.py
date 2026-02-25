from marshmallow import Schema, fields, ValidationError
from flask import abort

def validateData(data, baseSchema):
    schema = baseSchema()
    try:
        result = schema.load(data)
        return result
    except ValidationError as e:
        return str(e), 500
    
# some class validator
class loginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class getPrincipalsSchema(Schema):
    user_id = fields.Integer(required=True)
    customer_id = fields.Integer(required=True)

class getPrincipalSchema(Schema):
    principal_id = fields.Integer(required=True)
    sales_id = fields.Integer(required=True)
    
class getPlafonProduksSchema(Schema):
    user_id = fields.Integer(required=True)
    customer_id = fields.Integer(required=True)
    principal_id = fields.Integer(required=True)

class productsStockOpname(Schema):
    id_produk = fields.Integer(required=True)
    pieces = fields.Integer(required=True)
    box = fields.Integer(required=True)
    karton = fields.Integer(required=True)

class productNotaRetur(Schema):
    id_sales_order_detail = fields.Integer(required=True)
    pieces_retur = fields.Integer(required=True)
    box_retur = fields.Integer(required=True)
    karton_retur = fields.Integer(required=True)
    keterangan_retur = fields.String()

class salesStockOpname(Schema):
    id_sales = fields.Integer(required=True)
    id_principal = fields.Integer(required=True)
    id_customer = fields.Integer(required=True)
    products = fields.List(fields.Nested(productsStockOpname), required=True)

class createNotaReturSchema(Schema):
    id = fields.Integer(required=True)
    id_sales_order = fields.Integer(required=True)
    no_faktur = fields.String(required=True)
    total_penjualan = fields.Number(required=True)
    total_dana_diterima = fields.Number(required=True)
    products = fields.List(fields.Nested(productNotaRetur), required=True)

class lewatiSalesOrder(Schema):
    id_plafon = fields.Integer(required=True)
    keterangan = fields.String(required=True)
    
class createPaymentSchema(Schema):
    notaFaktur = fields.String(required=True)
    jumlahBayar = fields.Number(required=True)
    metodePembayaran = fields.String(required=True)
    buktiTransfer = fields.String(required=True)
    
class getVoucher2Schema(Schema):
    id_produk = fields.Integer(required=True)
    id_principal = fields.Integer(required=True)

class kode_voucherSchema(Schema):
    id = fields.Number(required=True)
    kode_vouchers = fields.String(required=True)
    diskon = fields.Number()
    nilai_diskon = fields.Number()

class vouchersSalesOrderSchema(Schema):
    id = fields.Number(required=True)
    kode = fields.String(required=True)
    diskon = fields.Number()
    nilai_diskon = fields.Number()
    
class productsSalesOrderSchema(Schema):
    id_produk = fields.Integer(required=True)
    pieces_order = fields.Integer(required=True)
    box_order = fields.Integer(required=True)
    karton_order = fields.Integer(required=True)
    subtotalorder = fields.Number()
    vouchers = fields.List(fields.Nested(vouchersSalesOrderSchema))
    
class salesOrderSchema(Schema):
    id_plafon = fields.String(required=True)
    no_sales_order = fields.String()
    tanggal_order = fields.String(required=True)
    tanggal_jatuh_tempo = fields.String()
    nama_sales = fields.String(required=True)
    subtotal_penjualan = fields.Number(required=True)
    subtotal_diskon = fields.Number(required=True)
    total_penjualan = fields.Number(required=True)
    total_dana_diterima = fields.Number()
    pajak = fields.Number()
    kode_vouchers = fields.List(fields.Nested(kode_voucherSchema))
    products = fields.List(fields.Nested())    
