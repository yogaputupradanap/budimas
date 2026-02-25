from flask import request

from apps.lib.paginateV2 import PaginateV2
from .BaseAkuntansi import BaseAkuntansi
from ...handler import handle_error, handle_error_rollback, nonServerErrorException
from ...models import CoaModel


class Coa(BaseAkuntansi):
    def __init__(self):
        super().__init__()

    @handle_error
    def getCoaList(self):
            id_perusahaan = self.req('id_perusahaan')
            is_active = self.req('is_active')
            is_main = self.req('is_main') # Tambahkan param ini

            query = """
                SELECT c.id_coa, c.nama_akun, c.nomor_akun, c.id_kategori,
                    c.principal_id, c.id_perusahaan, c.is_active, c.parent_id,
                    cc.nama_kategori, pr.nama AS nama_principal,
                    cp.nama_akun AS nama_parent, p.nama AS nama_perusahaan,
                    COUNT(DISTINCT jm.id_jurnal_mal) AS total_used
                FROM coa c
                JOIN coa_category cc ON c.id_kategori = cc.id_category
                JOIN perusahaan p ON c.id_perusahaan = p.id
                LEFT JOIN principal pr ON c.principal_id = pr.id
                LEFT JOIN coa cp ON c.parent_id = cp.id_coa
                LEFT JOIN jurnal_mal_detail jmd ON c.id_coa = jmd.id_coa
                LEFT JOIN jurnal_mal jm ON jmd.id_jurnal_mal = jm.id_jurnal_mal
                WHERE c.is_deleted = FALSE 
            """
            
            bindParams = {}

            # Filter Perusahaan
            if id_perusahaan:
                query += " AND c.id_perusahaan = :id_perusahaan"
                bindParams['id_perusahaan'] = id_perusahaan

            # Filter COA Utama (Yang tidak punya parent)
            if is_main == 'true':
                query += " AND c.parent_id IS NULL"

            # Filter Active
            if is_active is not None and is_active != '':
                query += " AND c.is_active = :is_active"
                bindParams['is_active'] = str(is_active).lower() == 'true'

            query += """
                GROUP BY c.id_coa, c.nama_akun, c.nomor_akun, c.id_kategori,
                        c.principal_id, c.id_perusahaan, c.is_active, c.parent_id,
                        cc.nama_kategori, pr.nama, cp.nama_akun, p.nama
            """
            
            return PaginateV2(request=request, query=query, bindParams=bindParams).paginate()
    
    @handle_error
    def getCoaList2(self):
            id_perusahaan = self.req('id_perusahaan')

            query = """
                SELECT id_coa, nama_akun
                FROM coa
                WHERE is_deleted = FALSE
                AND parent_id IS NULL
                AND id_perusahaan = :id_perusahaan
                ORDER BY id_coa ASC
            """

            result = self.db.execute(text(query), {
                "id_perusahaan": id_perusahaan
            })

            return {
                "result": [dict(row) for row in result.fetchall()]
            }

    @handle_error
    def getCoasByIdCoa(self):
        id_coa = self.req('id_coa')
        if not id_coa:
            raise nonServerErrorException(400, "id_coa harus diisi")

        query = """
                SELECT c.id_coa, c.nama_akun, c.nomor_akun
                FROM coa c
                WHERE c.is_deleted = FALSE
                AND c.parent_id = :id_coa
                """

        try:
            # Jalankan query
            res = (
                self.query()
                .setRawQuery(query)
                .bindparams({'id_coa': id_coa})
                .execute()
                .fetchall()
            )

            # Pastikan kita mengambil datanya. 
            # Jika library Anda menggunakan .result, ambil res.result.
            # Jika res sendiri sudah berupa list, gunakan res.
            coa_data = res.result if hasattr(res, 'result') else res

            # SAFETY CHECK: Flask akan error jika return None.
            # Pastikan return minimal [] jika data tidak ditemukan.
            return {
                "status": "success",
                "result": coa_data if coa_data is not None else []
            }

        except Exception as e:
            # Selalu return sesuatu jika terjadi error di level query
            return {
                "status": "error",
                "message": str(e)
            }, 500

    @handle_error_rollback
    def insertCoa(self):
        """
        Insert a new Chart of Account (CoA).
        """

        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, "Token tidak ditemukan")
        token = token.split(" ")[1] if " " in token else token

        user = (
            self.query().setRawQuery(
                "SELECT id FROM users WHERE tokens = :token",
            )
            .bindparams({
                'token': token
            })
            .execute()
            .fetchone()
            .result
        )

        created_by = user.get('id') if user else None

        id_kategori = self.req('id_kategori')
        nomor_akun = self.req('nomor_akun')
        nama_akun = self.req('nama_akun')
        id_perusahaan = self.req('id_perusahaan')
        parent_id = self.req('parent_id')
        principal_id = self.req('principal_id')

        if not id_kategori or not nomor_akun or not nama_akun or not created_by:
            raise nonServerErrorException(400, "data tidak lengkap")

        insert_coa = CoaModel(
            id_kategori=id_kategori,
            nomor_akun=nomor_akun,
            nama_akun=nama_akun,
            id_perusahaan=id_perusahaan,
            created_by=created_by,
            is_active=True,
            parent_id=parent_id,
            principal_id=principal_id
        )

        self.add(insert_coa).flush()
        self.commit()

        return {
            "status": "success",
            "message": "CoA berhasil disimpan",
            "data": {
                "id_coa": insert_coa.id_coa,
                "nama_akun": insert_coa.nama_akun,
                "nomor_akun": insert_coa.nomor_akun,
                "id_kategori": insert_coa.id_kategori
            }
        }

    @handle_error_rollback
    def updateCoa(self):
        """
        Update an existing Chart of Account (CoA).
        """

        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, "Token tidak ditemukan")
        token = token.split(" ")[1] if " " in token else token

        user = (
            self.query().setRawQuery(
                "SELECT id FROM users WHERE tokens = :token",
            )
            .bindparams({
                'token': token
            })
            .execute()
            .fetchone()
            .result
        )

        updated_by = user.get('id') if user else None

        id_coa = self.req('id_coa')
        id_kategori = self.req('id_kategori')
        nomor_akun = self.req('nomor_akun')
        nama_akun = self.req('nama_akun')
        id_perusahaan = self.req('id_perusahaan')
        is_active = self.req('is_active')
        parent_id = self.req('parent_id')
        principal_id = self.req('principal_id')

        if parent_id == id_coa:
            raise nonServerErrorException(400, "Parent CoA tidak boleh sama dengan CoA itu sendiri")

        if not id_coa or not id_kategori or not nomor_akun or not nama_akun or not updated_by:
            raise nonServerErrorException(400, "data tidak lengkap")

        coa = CoaModel.query.filter_by(id_coa=id_coa).first()
        if not coa:
            return {
                "status": "error",
                "message": "CoA tidak ditemukan"
            }

        coa.id_kategori = id_kategori
        coa.nomor_akun = nomor_akun
        coa.nama_akun = nama_akun
        coa.id_perusahaan = id_perusahaan
        coa.is_active = is_active if is_active is not None else coa.is_active
        coa.parent_id = parent_id
        coa.principal_id = principal_id

        self.commit()

        return {
            "status": "success",
            "message": "CoA berhasil diperbarui",
            "data": {
                "id_coa": coa.id_coa,
                "nama_akun": coa.nama_akun,
                "nomor_akun": coa.nomor_akun,
                "id_kategori": coa.id_kategori,
                "is_active": coa.is_active
            }
        }
