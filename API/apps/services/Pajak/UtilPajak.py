from apps.services import convert_uom
from apps.services.BaseServices import BaseServices
import xml.etree.ElementTree as ET
from apps import native_db
from apps.models.produk_uom import produk_uom
from collections import defaultdict

from sqlalchemy import text as sa_text
class UtilPajak(BaseServices):
  def __init__(self):
    super().__init__()
    self.BaseFromQ = """FROM faktur
                    JOIN sales_order ON faktur.id_sales_order = sales_order.id
                    JOIN plafon ON sales_order.id_plafon = plafon.id
                    JOIN principal ON plafon.id_principal = principal.id
                    JOIN customer ON plafon.id_customer = customer.id
                    LEFT JOIN perusahaan ON perusahaan.id = principal.id_perusahaan
                    LEFT JOIN pajak ON faktur.id = pajak.id_faktur 
                    LEFT JOIN cabang on customer.id_cabang = cabang.id
              """
    self.BaseDetailFromQ = """ FROM sales_order_detail
                          JOIN sales_order ON sales_order_detail.id_sales_order = sales_order.id 
                          JOIN faktur ON sales_order.id = faktur.id_sales_order 
                          JOIN produk ON sales_order_detail.id_produk = produk.id
                      """
    self.basefactor = {"pieces": 1, "box": 50, "karton": 200}
    self.level_to_uom = {1: "pieces", 2: "box", 3: "karton"}
    self.status_faktur_pajak = {
        0: "Draft",
        1: "Sudah Export",
        2: "Approved",
        3: "Canceled",
        4: "Amanded"
      }
    
  def GetDataFakturTable(self, where_clauses, bindParams):
    try:
      query = f"""
        SELECT
            faktur.id AS id,
            faktur.no_faktur AS no_faktur,
            pajak.nsfp as nsfp,
            customer.nama AS nama_customer,
            principal.nama AS nama_principal,
            sales_order.tanggal_faktur AS tanggal_faktur,
            faktur.dpp AS dpp,
            faktur.subtotal_penjualan AS subtotal_penjualan,
            faktur.pajak AS pajak,
            faktur.status_faktur_pajak AS status_faktur_pajak
        {self.BaseFromQ}
        {where_clauses}
      """
      print("Get query data faktur table:", query, bindParams)
      row = (
        self
        .query()
        .setRawQuery(query)
        .bindparams(bindParams)
        .execute()
        .fetchall()
        .get()
      )

      for r in row:
        r["status_faktur_pajak"] = self.status_faktur_pajak.get(r["status_faktur_pajak"], 'Draft')
      
      return row
    except Exception as e:
      print("error get data faktur table:", str(e))
      return None

  def GetDataFilterDetailFaktur(self, where_clauses, bindParams):
      try:
        query = f"""
          SELECT 
            faktur.no_faktur AS no_faktur,
            sales_order.tanggal_faktur AS tanggal_faktur,
            customer.nama AS nama_customer,
            customer.kode AS kode_customer,
            principal.nama AS nama_principal,
            customer.npwp AS npwp
          {self.BaseFromQ}
          {where_clauses}
        """
        row = (
            self
            .query()
            .setRawQuery(query)
            .bindparams(bindParams)
            .execute()
            .fetchone()
            .get()
          )
        
        if not row or len(row) == 0:
          return None

        return row
      except Exception as e:
        print("error get data filter detail faktur:", str(e))
        raise e

  def GetDataDetailFakturTable(self, where_clauses, bindParams):
     try:
        query = f"""
                  select 
                  faktur.id AS faktur_id,
                  sales_order_detail.id AS id, 
                  produk.id AS id_produk,
                  produk.nama AS nama_produk, 
                  produk.kode_sku as kode_sku,
                  produk.ppn AS produk_ppn,
                  sales_order_detail.pieces_delivered AS pieces_delivered, 
                  sales_order_detail.box_delivered AS box_delivered,
                  sales_order_detail.karton_delivered AS karton_delivered,
                  sales_order_detail.hargaorder AS harga,
                  sales_order_detail.total_nilai_discount AS total_nilai_discount,
                  faktur.subtotal_diskon as subtotal_diskon,
                  faktur.status_faktur_pajak AS status_faktur_pajak,
                  faktur.total_penjualan AS total_penjualan,
                  sales_order_detail.subtotalorder AS subtotalorder
                  {self.BaseDetailFromQ}
                  {where_clauses}
            """
        print("Get query data detail faktur table:", query, bindParams)

        rows = (
          self
          .query()
          .setRawQuery(query)
          .bindparams(bindParams)
          .execute()
          .fetchall()
          .get()
        )

        ids_uom = []
        for row in rows:
           id_produk = row["id_produk"]
           if id_produk is None:
            continue
           ids_uom.append(row["id_produk"])

        print("============== IDs UOM ==============\n", ids_uom)
        if len(ids_uom) == 0:
           return []
        factor_uom = self.GetUomFactor(ids_uom)
        
        items = []
        for row in rows:
            # siapkan sumber qty dan konversi ke 'pieces' via convert_uom
            qty_src = {
                "pieces": int(row["pieces_delivered"] or 0),
                "box": int(row["box_delivered"] or 0),
                "karton": int(row["karton_delivered"] or 0),
            }

            factor = factor_uom.get(row["id_produk"], {}) if factor_uom else self.basefactor

            converter = convert_uom(qty_src, factor)
            jumlah_pieces = int(converter.convert_to("pieces").get().get("pieces", 0))

            # hitung nilai turunan
            ppn_rate = (int(row["produk_ppn"] or 11)) / 100  # 11 -> 0.11
            hpp_val = jumlah_pieces * int(row["harga"] or 0)
            dpp_val = hpp_val * 11/12
            pajak_val = hpp_val * ppn_rate

            items.append({
                "faktur_id": row["faktur_id"],
                "kode_sku": row["kode_sku"],
                "nama_produk": row["nama_produk"],
                "jumlah_uom_1": jumlah_pieces,   # dari convert_uom
                "harga": int(row["harga"] or 0),
                "dpp": dpp_val,                   # pakai subtotaldelivered dari SQL
                "pajak": pajak_val,
                "hpp": hpp_val,
                "ppn_rate": ppn_rate,
                "subtotal_diskon": int(row["subtotal_diskon"] or 0),
                "ppn_percentage": int(row["produk_ppn"] or 0),
                "subtotalorder": int(row["subtotalorder"] or 0),
                "total_penjualan": int(row["total_penjualan"] or 0),
                "status_faktur_pajak": self.status_faktur_pajak.get(row["status_faktur_pajak"], 'Draft'),
            })
        print("items detail faktur: \n", items)
        return items
        
     except Exception as e:
        print("error get data detail faktur table:", str(e))
        raise e
     
  def GetDataDetailXmlFakturTable(self, where_clauses, bindParams):
     try:
        query = f"""
                  select 
                  faktur.id AS faktur_id,
                  sales_order_detail.id AS id, 
                  produk.id AS id_produk,
                  produk.nama AS nama_produk, 
                  produk.kode_sku as kode_sku,
                  produk.ppn AS produk_ppn,
                  sales_order_detail.pieces_delivered AS pieces_delivered, 
                  sales_order_detail.box_delivered AS box_delivered,
                  sales_order_detail.karton_delivered AS karton_delivered,
                  sales_order_detail.hargaorder AS harga,
                  sales_order_detail.total_nilai_discount AS total_nilai_discount,
                  faktur.subtotal_diskon as subtotal_diskon,
                  faktur.status_faktur_pajak AS status_faktur_pajak,
                  faktur.total_penjualan AS total_penjualan,
                  sales_order_detail.subtotalorder AS subtotalorder
                  {self.BaseDetailFromQ}
                  {where_clauses}
            """
        print("Get query data detail faktur table:", query, bindParams)

        rows = (
          self
          .query()
          .setRawQuery(query)
          .bindparams(bindParams)
          .execute()
          .fetchall()
          .get()
        )

        ids_uom = []
        for row in rows:
           id_produk = row["id_produk"]
           if id_produk is None:
            continue
           ids_uom.append(row["id_produk"])

        print("============== IDs UOM ==============\n", ids_uom)
        if len(ids_uom) == 0:
           return []
        factor_uom = self.GetUomFactor(ids_uom)
        
        items = []
        for row in rows:
            # siapkan sumber qty dan konversi ke 'pieces' via convert_uom
            qty_src = {
                "pieces": int(row["pieces_delivered"] or 0),
                "box": int(row["box_delivered"] or 0),
                "karton": int(row["karton_delivered"] or 0),
            }

            factor = factor_uom.get(row["id_produk"], {}) if factor_uom else self.basefactor

            converter = convert_uom(qty_src, factor)
            jumlah_pieces = int(converter.convert_to("pieces").get().get("pieces", 0))

            # hitung nilai turunan
            ppn_rate = (int(row["produk_ppn"] or 0)) / 100  # 11 -> 0.11
            hpp_val = jumlah_pieces * int(row["harga"] or 0)
            dpp_val = hpp_val * 11/12
            pajak_val = hpp_val * ppn_rate

            items.append({
                "faktur_id": row["faktur_id"],
                "kode_sku": row["kode_sku"],
                "nama_produk": row["nama_produk"],
                "jumlah_uom_1": jumlah_pieces,   # dari convert_uom
                "harga": int(row["harga"] or 0),
                "dpp": dpp_val,                   # pakai subtotaldelivered dari SQL
                "pajak": pajak_val,
                "hpp": hpp_val,
                "ppn_rate": ppn_rate,
                "subtotal_diskon": int(row["subtotal_diskon"] or 0),
                "ppn_percentage": int(row["produk_ppn"] or 0),
                "subtotalorder": int(row["subtotalorder"] or 0),
                "total_penjualan": int(row["total_penjualan"] or 0),
                "status_faktur_pajak": self.status_faktur_pajak.get(row["status_faktur_pajak"], 'Draft'),
            })
        print("items detail faktur: \n", items)
        return items
        
     except Exception as e:
        print("error get data detail faktur table:", str(e))
        raise e
  

  def GetDataForExportFaktur(self, where_clauses, bindParams):
     try:
        query = f"""
                SELECT 
                  distinct on (faktur.id)
					        faktur.id As faktur_id,
                  faktur.no_faktur AS no_faktur,
                  sales_order.tanggal_faktur AS tanggal_faktur,
                  customer.npwp AS npwp,
                  customer.nama AS nama_customer,
                  customer.alamat AS alamat,
                  customer.email AS email,
                  principal.id AS id_principal,
                  produk.ppn as produk_ppn
                {self.BaseFromQ}
                  LEFT JOIN sales_order_detail on sales_order.id = sales_order_detail.id_sales_order 
                  LEFT JOIN produk on sales_order_detail.id_produk = produk.id
                {where_clauses}
            """
        
        print("Get query data for export faktur:", query, bindParams)
        rows = (
            self
            .query()
            .setRawQuery(query)
            .bindparams(bindParams)
            .execute()
            .fetchall()
            .get()
        )

        return rows
     except Exception as e:
        print("error get data for export faktur:", str(e))
        raise e 

  def ConvertToXMLFaktur(self, parent_result, child_result, perusahaan):
    try:
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root = ET.Element("TaxInvoiceBulk", 
              attrib={
              "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation": "TaxInvoice.xsd"
              }
            )
        
        ET.SubElement(root, "TIN").text = perusahaan.get("npwp", "")
        listTaxInvoices_elem = ET.SubElement(root, "ListOfTaxInvoice")

        for faktur in parent_result:
            produk_ppn = int(faktur.get("produk_ppn", 0) or 0)
            produk_is_ppn = bool(produk_ppn > 0)
            dpp_val = float(faktur.get("dpp") or 0)
            OtherTaxBase = dpp_val * 0.11 if produk_is_ppn else 0
            npwp = str(faktur.get("npwp", "") or "").replace(".", "").replace("-", "").replace(" ", "")
            if npwp is None or npwp.strip() == "" or len(npwp) < 15:
                npwp = "000000000000000"

            taxInvoices_elem = ET.SubElement(listTaxInvoices_elem, "TaxInvoice")
            ET.SubElement(taxInvoices_elem, "TaxInvoiceDate").text = str(faktur.get("tanggal_faktur", ""))
            ET.SubElement(taxInvoices_elem, "TaxInvoiceOpt").text = "Normal"

            # Id principal dari greenfields yaitu 14
            ET.SubElement(taxInvoices_elem, "TrxCode").text = "04" if produk_is_ppn else "08"
            
            ET.SubElement(taxInvoices_elem, "AddInfo").text = None
            ET.SubElement(taxInvoices_elem, "CustomDoc").text = "-"
            ET.SubElement(taxInvoices_elem, "CustomDocMonthYear").text = None
            ET.SubElement(taxInvoices_elem, "RefDesc").text = str(faktur.get("no_faktur", ""))
            ET.SubElement(taxInvoices_elem, "FacilityStamp").text = "-"
            ET.SubElement(taxInvoices_elem, "SellerIDTKU").text = str(perusahaan.get("npwp", "")) + "000000"
            ET.SubElement(taxInvoices_elem, "BuyerTin").text = npwp
            ET.SubElement(taxInvoices_elem, "BuyerDocument").text = "TIN"
            ET.SubElement(taxInvoices_elem, "BuyerCountry").text = "IDN"
            ET.SubElement(taxInvoices_elem, "BuyerDocumentNumber").text = "-"
            ET.SubElement(taxInvoices_elem, "BuyerName").text = str(faktur.get("nama_customer", ""))
            ET.SubElement(taxInvoices_elem, "BuyerAdress").text = str(faktur.get("alamat", ""))
            ET.SubElement(taxInvoices_elem, "BuyerEmail").text = str(faktur.get("email", ""))
            ET.SubElement(taxInvoices_elem, "BuyerIDTKU").text = npwp + "000000"

            listOfGoodServices_elem = ET.SubElement(taxInvoices_elem, "ListOfGoodService")

            faktur_details = [
                d for d in child_result if d.get("faktur_id") == faktur.get("faktur_id")
            ]

            for det in faktur_details:
                GoodServices_elem = ET.SubElement(listOfGoodServices_elem, "GoodService")
                ET.SubElement(GoodServices_elem, "Opt").text = "A"
                ET.SubElement(GoodServices_elem, "Code").text = str(det.get("kode_sku", ""))
                ET.SubElement(GoodServices_elem, "Name").text = str(det.get("nama_produk", ""))
                ET.SubElement(GoodServices_elem, "Price").text = str(det.get("harga", 0))
                ET.SubElement(GoodServices_elem, "Unit").text = "-"
                ET.SubElement(GoodServices_elem, "Qty").text = str(det.get("jumlah_uom_1", 0))
                ET.SubElement(GoodServices_elem, "TotalDiscount").text = str(det.get("total_nilai_discount", 0))
                ET.SubElement(GoodServices_elem, "TaxBase").text = f"{int(det.get('dpp', 0))}"
                ET.SubElement(GoodServices_elem, "OtherTaxBase").text = f"{int(OtherTaxBase or 0)}"
                ET.SubElement(GoodServices_elem, "VATRate").text = "11"
                ET.SubElement(GoodServices_elem, "VAT").text = f"{int(det.get('pajak', 0))}"
                ET.SubElement(GoodServices_elem, "STLGRate").text = "0"
                ET.SubElement(GoodServices_elem, "STLG").text = "0"
        ET.indent(root, space="  ")
        xml_bytes = ET.tostring(root, encoding='utf-8', xml_declaration=True)
        return xml_bytes.decode('utf-8')
    except Exception as e:
        return str(e)
    
  def _GetNotListedIdfaktur(self, faktur_ids=None, pajak_ids=None, keep_order=True):
      faktur_ids = list(faktur_ids or [])
      pajak_set = list(pajak_ids or [])

      if keep_order:
          # preservasi urutan faktur_ids
          not_in_pajak = [x for x in faktur_ids if x not in pajak_set]
          same_ids = [x for x in faktur_ids if x in pajak_set]
      else:
          faktur_set = set(faktur_ids)
          not_in_pajak = list(faktur_set - pajak_set)
          same_ids = list(faktur_set & pajak_set)

      return not_in_pajak, same_ids
  
  def GetDataPajakNotFromPajak(self, clauses, bindParams=None):
    try:
      query = f"""
              SELECT 
                faktur.id AS id_faktur,
                cabang.id as id_cabang,
                perusahaan.id AS id_perusahaan,
                faktur.no_faktur AS no_faktur,
                faktur.nama_fakturist AS nama_fakturist,
                faktur.total_penjualan AS total_penjualan,
                sales_order.tanggal_faktur AS tanggal_faktur,
                faktur.subtotal_diskon,
                faktur.status_faktur_pajak AS status_faktur_pajak,
                sales_order_detail.hargaorder AS harga,
                sales_order_detail.pieces_delivered AS pieces_delivered, 
                sales_order_detail.box_delivered AS box_delivered,
                sales_order_detail.karton_delivered AS karton_delivered,
                produk.id AS id_produk
                {self.BaseFromQ}
                JOIN sales_order_detail on sales_order.id = sales_order_detail.id 
                JOIN produk on sales_order_detail.id_produk = produk.id
                {clauses}
        """
      
      print("Get query data pajak not from pajak:", query)
      print("With bind params:", bindParams)
      print("Get Clauses:", clauses)
      rows = (
        self
        .query()
        .setRawQuery(query)
        .bindparams(bindParams)
        .execute()
        .fetchall()
        .get()
      )

      ids_uom = []
      for row in rows:
          id_produk = row["id_produk"]
          if id_produk is None:
            continue
          ids_uom.append(row["id_produk"])
      factor_uom = self.GetUomFactor(ids_uom)
      items = []
      for r in rows:
          qty_src = {
              "pieces": int(r["pieces_delivered"] or 0),
              "box": int(r["box_delivered"] or 0),
              "karton": int(r["karton_delivered"] or 0),
          }
          factor = factor_uom.get(row["id_produk"], {}) if factor_uom else self.basefactor
          converter = convert_uom(qty_src, factor)
          jumlah_pieces = int(converter.convert_to("pieces").get().get("pieces", 0))
          dpp_val = int(r["harga"] or 0) * 11/12
          ppn_val = dpp_val * 0.11
          hpp_val = jumlah_pieces * int(r["harga"] or 0)

          items.append({
              **r,
              "dpp": dpp_val,
              "pajak": ppn_val,
              "subtotal_penjualan": hpp_val
          })

      return items
    except Exception as e:
      print("error get data pajak not from pajak:", str(e))
      return None
    
  def GetUomFactor(self, ids_produk = []):
     try:
        if not ids_produk or len(ids_produk) == 0:
           return None
        result = produk_uom.query.filter(produk_uom.id_produk.in_(ids_produk)).all()
        konversi_map = defaultdict(dict)
        for p in result:
            konversi_map[p.id_produk][self.level_to_uom.get(p.level, 1)] = p.faktor_konversi  
        return konversi_map
     except Exception as e:
        print("error get uom factor:", str(e))
        return None  