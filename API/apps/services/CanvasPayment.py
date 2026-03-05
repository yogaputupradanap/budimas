from apps.handler import handle_error
from flask import abort

from apps.services import BaseServices
from apps.services.SalesCanvas import SalesCanvas
from apps.lib.helper import (
    date_now, 
    extract_data, 
    query_with_filters, 
    format_result_response,
    format_paginated_response, 
)

class CanvasPayment(BaseServices):
    def __init__(self):
        super().__init__()
        self.sales_canvas_service = SalesCanvas()
        
    @handle_error
    def paymentHistoryList(self):
        id_canvas_order = self.req('id_canvas_order') or self.req('id')
        if not id_canvas_order:
            abort(400, "ID Canvas Order tidak ditemukan")

        baseQuery = """
            SELECT 
                sc.id,
                sc.jumlah_setoran AS nominal,
                ARRAY_AGG(s.status_setoran) AS status_setoran,
                sc.tanggal_input,
                co.total_order AS total_tagihan,
                co.nama_customer
            FROM setoran_customer sc
            LEFT JOIN canvas_order co ON sc.id_canvas_order = co.id
            LEFT JOIN setoran s ON sc.id = s.id_setoran_customer
            WHERE sc.id_canvas_order = :id_canvas_order
            GROUP BY sc.id, sc.jumlah_setoran, sc.tanggal_input, co.total_order, co.nama_customer
            ORDER BY sc.tanggal_input DESC
        """
        
        result = self.sales_canvas_service._fetching(
            baseQuery, 
            {"id_canvas_order": id_canvas_order}, 
            fetch_type="all"
        )
        data = []
        for row in result:
            if hasattr(row, "_asdict"):
                data.append(row._asdict())
            elif isinstance(row, dict):
                data.append(row)
            else:
                data.append(dict(row))
                
        return format_result_response(self, result, data)
    
    @handle_error  
    def submitTagihanPembayaran(self):
        id_canvas_order = self.req('id_canvas_order') or self.req('id')
        jumlah_dibayarkan = self.req('jumlah_dibayarkan')
        
        if not id_canvas_order:
            abort(404, "ID Canvas Order tidak ditemukan")
            
        if not jumlah_dibayarkan or float(jumlah_dibayarkan) <= 0:
            abort(400, "Jumlah dibayarkan harus lebih dari 0")

        canvas_order_query = """
            SELECT co.id, cr.id_sales, co.total_order, co.nama_customer
            FROM canvas_order co
            JOIN canvas_request cr ON co.id_canvas_request = cr.id  
            WHERE co.id = :id_canvas_order
        """
        
        canvas_order = self.sales_canvas_service._fetching(canvas_order_query, {
            "id_canvas_order": id_canvas_order
        }, fetch_type="one")
        
        if not canvas_order:
            abort(404, "Canvas Order tidak ditemukan")
        
        # Cek sisa tagihan
        total_setoran_query = """
            SELECT COALESCE(SUM(jumlah_setoran), 0) as total_setoran
            FROM setoran_customer  
            WHERE id_canvas_order = :id_canvas_order
        """
        
        setoran_result = self.sales_canvas_service._fetching(total_setoran_query, {
            "id_canvas_order": id_canvas_order
        }, fetch_type="one")
        
        total_sudah_dibayar = setoran_result.get('total_setoran', 0) if setoran_result else 0
        total_tagihan = canvas_order['total_order']
        sisa_tagihan = total_tagihan - total_sudah_dibayar
        
        if float(jumlah_dibayarkan) > sisa_tagihan:
            abort(400, f"Jumlah dibayarkan ({jumlah_dibayarkan}) melebihi sisa tagihan ({sisa_tagihan})")
        
        # Insert ke setoran_customer
        insert_setoran_customer_query = """
            INSERT INTO setoran_customer (
                id_sales, id_canvas_order, jumlah_setoran, tanggal_input,
                tipe_setoran, is_rekap
            ) VALUES (
                :id_sales, :id_canvas_order, :jumlah_setoran, :tanggal_input,
                :tipe_setoran, :is_rekap
            ) RETURNING id
        """
        
        setoran_result = self.sales_canvas_service._fetching(insert_setoran_customer_query, {
            "id_sales": canvas_order['id_sales'],
            "id_canvas_order": id_canvas_order,
            "jumlah_setoran": float(jumlah_dibayarkan),
            "tanggal_input": date_now(),
            "tipe_setoran": 1,      # 1 = Tunai
            "is_rekap": 0           # 0 = Belum direkap
        }, fetch_type="one")
        
        setoran_customer_id = setoran_result['id'] if setoran_result else None
        
        if not setoran_customer_id:
            abort(500, "Gagal menyimpan pembayaran")
        
        # Insert ke setoran (untuk tracking status)
        insert_tracking_query = """
            INSERT INTO setoran (
                id_setoran_customer, draft_tanggal_input, draft_jumlah_setor, 
                draft_tipe_setor, jumlah_setoran, tipe_setoran, 
                tanggal_setoran_diterima, status_setoran, pj_setoran
            ) VALUES (
                :id_setoran_customer, :tanggal_input, :jumlah_setoran, 
                :tipe_setoran, :jumlah_setoran, :tipe_setoran, 
                :tanggal_input, :status_setoran, :pj_setoran
            )
        """
        
        self.sales_canvas_service._fetching(insert_tracking_query, {
            "id_setoran_customer": setoran_customer_id,
            "tanggal_input": date_now(),
            "jumlah_setoran": float(jumlah_dibayarkan),
            "tipe_setoran": 1,      # 1 = Tunai
            "status_setoran": 3,    # 3 = Audit
            "pj_setoran": 1,        # 1 = Sales
        })
        
        # Hitung sisa setelah pembayaran
        sisa_setelah_bayar = sisa_tagihan - float(jumlah_dibayarkan)
        
        response_data = [{
            "setoran_customer_id": setoran_customer_id,
            "jumlah_dibayarkan": float(jumlah_dibayarkan),
            "sisa_tagihan": sisa_setelah_bayar,
            "is_lunas": sisa_setelah_bayar <= 0,
            "message": "Pembayaran berhasil disimpan"
        }]
        
        return format_result_response(self, [], response_data)

            