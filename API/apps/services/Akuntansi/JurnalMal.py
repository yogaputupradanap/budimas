import datetime

from flask import request

from apps.models import JurnalMalModel, CoaModel, SourceModulModel, JurnalMalDetailModel
from .BaseAkuntansi import BaseAkuntansi
from ...handler import handle_error_rollback, nonServerErrorException, handle_error
from ...lib.paginateV2 import PaginateV2


class JurnalMal(BaseAkuntansi):
    def __init__(self):
        super().__init__()

    @handle_error_rollback
    def insert_jurnal_mal(self):
        """
        Insert a new jurnal mal entry into the database.
        """
        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, 'Token is missing')

        token = token.split(' ')[1] if ' ' in token else token

        user = self.query().setRawQuery(
            'SELECT id FROM users WHERE tokens = :token',

        ).bindparams({'token': token}).execute().fetchone().result

        if not user:
            raise nonServerErrorException(401, 'Invalid token')

        created_by = user.get('id')

        id_coa_main = self.req("id_coa_main")
        id_fitur_mal = self.req("id_fitur_mal")
        id_modul = self.req("id_modul")
        id_perusahaan = self.req("id_perusahaan")
        nama_mal = self.req("nama_mal")

        detail = self.req(
            "detail")  # Expecting a list of dicts with 'id_coa', 'type', 'id_source_data', 'urutan'

        if not id_perusahaan or not id_fitur_mal or not nama_mal or not detail or not id_coa_main:
            raise nonServerErrorException(400, 'Missing required fields')

        if not isinstance(detail, list) or not all(isinstance(item, dict) for item in detail):
            raise nonServerErrorException(400, 'Detail must be a list of dictionaries')
        if not all(all(key in item for key in ['id_coa', 'type', 'id_source_data', 'urutan']) for item in
                   detail):
            raise nonServerErrorException(400,
                                          'Each detail item must contain id_coa, type, id_source_data, and urutan')

        # # validasi duplikat data insert
        # seen = set()
        # for item in detail:
        #     identifier = (item['id_coa'], item['id_modul'], item['id_source_data'], item['type'])
        #     if identifier in seen:
        #         raise nonServerErrorException(400, 'Duplicate entries found in detail')
        #     seen.add(identifier)
        #
        # validasi data coa, modul, source data
        # validasi coa
        # validasi COA
        coa_ids = [item['id_coa'] for item in detail]

        valid_coas = CoaModel.query.filter(
            CoaModel.id_coa.in_(coa_ids),
            CoaModel.id_perusahaan == id_perusahaan
        ).all()

        if len(valid_coas) != len(set(coa_ids)):
            raise nonServerErrorException(400, 'One or more COA IDs are invalid for the given company')

        # # validasi Modul
        # modul_ids = [item['id_modul'] for item in detail]
        #
        # valid_moduls = ModulModel.query.filter(
        #     ModulModel.id_modul.in_(modul_ids)
        # ).all()
        #
        # if len(valid_moduls) != len(set(modul_ids)):
        #     raise nonServerErrorException(400, 'One or more Modul IDs are invalid')

        # validasi Source Data
        source_data_ids = [item['id_source_data'] for item in detail]

        valid_source_data = SourceModulModel.query.filter(
            SourceModulModel.id_source_data.in_(source_data_ids)
        ).all()

        if len(valid_source_data) != len(set(source_data_ids)):
            raise nonServerErrorException(400, 'One or more Source Data IDs are invalid')

        # validasi type
        for item in detail:
            if item['type'] not in [1, 2]:
                raise nonServerErrorException(400, 'Tipe must be either "debit" or "kredit"')

        insert_jurnal_mal = JurnalMalModel(
            id_perusahaan=id_perusahaan,
            id_fitur_mal=id_fitur_mal,
            main_coa_id=id_coa_main,
            nama_mal=nama_mal,
            created_by=created_by
        )

        self.add(insert_jurnal_mal).flush()

        jurnal_mal_id = insert_jurnal_mal.id_jurnal_mal

        for item in detail:
            item['id_jurnal_mal'] = jurnal_mal_id

            insert_jurnal_mal_detail = JurnalMalDetailModel(
                id_jurnal_mal=item['id_jurnal_mal'],
                id_source_data=item['id_source_data'],
                id_coa=item['id_coa'],
                type=item['type'],
                urutan=item['urutan'],
                created_by=created_by
            )

            self.add(insert_jurnal_mal_detail)

        self.commit()

        return {
            'status': 'success',
            'message': 'Jurnal mal berhasil disimpan',
            'data': {
                'id_jurnal_mal': insert_jurnal_mal.id_jurnal_mal,
                'nama_mal': insert_jurnal_mal.nama_mal,
                'id_perusahaan': insert_jurnal_mal.id_perusahaan,
                'id_fitur_mal': insert_jurnal_mal.id_fitur_mal,
                'detail': detail
            }
        }

    @handle_error
    def get_jurnal_mal_list(self):
        """
        Retrieve a list of jurnal mal entries from the database.
        """
        id_perusahaan = self.req('id_perusahaan')

        query = """
                SELECT jm.nama_mal, jm.id_jurnal_mal
                FROM jurnal_mal jm \
                WHERE is_deleted = FALSE
                """
        params = {}
        if id_perusahaan:
            if 'WHERE' in query:
                query += " AND jm.id_perusahaan = :id_perusahaan"
            else:
                query += " WHERE jm.id_perusahaan = :id_perusahaan"
            params['id_perusahaan'] = id_perusahaan

        return PaginateV2(request=request, query=query, bindParams=params).paginate()

    @handle_error
    def get_jurnal_mal_detail(self, id_jurnal_mal):
        """
        Retrieve details of a specific jurnal mal entry from the database.
        """
        if not id_jurnal_mal:
            raise nonServerErrorException(400, 'id_jurnal_mal is required')

        query = """
                SELECT JSON_AGG(
                               JSONB_BUILD_OBJECT(
                                       'id_mal_detail', jmd.id_mal_detail,
                                       'id_coa', jmd.id_coa,
                                       'nama_akun', c.nama_akun,
                                       'type', jmd.type,
                                       'urutan', jmd.urutan,
                                       'id_modul', jmd.id_modul,
                                       'id_source_data', jmd.id_source_data,
                                       'nama_kolom_view', sm.nama_kolom_view
                               ) ORDER BY jmd.urutan ASC
                       )
                           AS detail,
                       jm.nama_mal,
                       jm.id_perusahaan,
                       jm.id_fitur_mal,
                       jm.main_coa_id
                FROM jurnal_mal_detail jmd
                         JOIN jurnal_mal jm
                              ON jmd.id_jurnal_mal = jm.id_jurnal_mal
                         JOIN source_modul sm ON jmd.id_source_data = sm.id_source_data
                         JOIN coa c ON jmd.id_coa = c.id_coa
                WHERE jmd.id_jurnal_mal = :id_jurnal_mal
                  AND jm.is_deleted = FALSE
                  AND jmd.is_deleted = FALSE
                GROUP BY jm.id_jurnal_mal
                """
        params = {'id_jurnal_mal': id_jurnal_mal}

        result = self.query().setRawQuery(query).bindparams(params).execute().fetchone().result

        return {
            'status': 'success',
            'data': result
        }

    @handle_error_rollback
    def update_jurnal_mal(self):
        """
        Insert a new jurnal mal entry into the database.
        """
        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, 'Token is missing')

        token = token.split(' ')[1] if ' ' in token else token

        user = self.query().setRawQuery(
            'SELECT id FROM users WHERE tokens = :token',

        ).bindparams({'token': token}).execute().fetchone().result

        if not user:
            raise nonServerErrorException(401, 'Invalid token')

        created_by = user.get('id')

        id_coa_main = self.req("id_coa_main")
        id_journal_mal = self.req("id_jurnal_mal")
        id_perusahaan = self.req("id_perusahaan")
        nama_mal = self.req("nama_mal")
        detail = self.req(
            "detail")  # Expecting a list of dicts with 'id_coa', 'type', 'id_modul', 'id_source_data', 'urutan'

        if not id_journal_mal or not nama_mal or not detail:
            raise nonServerErrorException(400, 'Missing required fields')

        if not isinstance(detail, list) or not all(isinstance(item, dict) for item in detail):
            raise nonServerErrorException(400, 'Detail must be a list of dictionaries')
        if not all(all(key in item for key in ['id_coa', 'type', 'id_source_data', 'urutan']) for item in
                   detail):
            raise nonServerErrorException(400,
                                          'Each detail item must contain id_coa, type, id_source_data, and urutan')

        # # validasi duplikat data insert
        # seen = set()
        # for item in detail:
        #     identifier = (item['id_coa'], item['id_modul'], item['id_source_data'], item['type'])
        #     if identifier in seen:
        #         raise nonServerErrorException(400, 'Duplicate entries found in detail')
        #     seen.add(identifier)
        #
        # validasi data coa, modul, source data
        # validasi coa
        # validasi COA
        coa_ids = [item['id_coa'] for item in detail]

        valid_coas = CoaModel.query.filter(
            CoaModel.id_coa.in_(coa_ids),
            CoaModel.id_perusahaan == id_perusahaan
        ).all()

        if len(valid_coas) != len(set(coa_ids)):
            raise nonServerErrorException(400, 'One or more COA IDs are invalid for the given company')

        #         # validasi Modul
        #         modul_ids = [item['id_modul'] for item in detail]
        #
        #         valid_moduls = ModulModel.query.filter(
        #             ModulModel.id_modul.in_(modul_ids)
        #         ).all()
        #
        #         if len(valid_moduls) != len(set(modul_ids)):
        #             raise nonServerErrorException(400, 'One or more Modul IDs are invalid')

        # validasi Source Data
        source_data_ids = [item['id_source_data'] for item in detail]

        valid_source_data = SourceModulModel.query.filter(
            SourceModulModel.id_source_data.in_(source_data_ids)
        ).all()

        if len(valid_source_data) != len(set(source_data_ids)):
            raise nonServerErrorException(400, 'One or more Source Data IDs are invalid')

        # validasi type
        for item in detail:
            if item['type'] not in [1, 2]:
                raise nonServerErrorException(400, 'Tipe must be either "debit" or "kredit"')

        update_jurnal_mal = JurnalMalModel().query.filter_by(id_jurnal_mal=id_journal_mal).first()
        if not update_jurnal_mal:
            raise nonServerErrorException(400, 'Jurnal mal not found')
        update_jurnal_mal.nama_mal = nama_mal
        update_jurnal_mal.main_coa_id = id_coa_main

        self.add(update_jurnal_mal)

        ids_jurnal_mal_detail = [item.get('id_mal_detail') for item in detail if item.get('id_mal_detail')]

        (
            JurnalMalDetailModel.query
            .filter(JurnalMalDetailModel.id_mal_detail.notin_(ids_jurnal_mal_detail))
            .filter(JurnalMalDetailModel.id_jurnal_mal == id_journal_mal)
            .update({'is_deleted': True, 'deleted_at': datetime.datetime.now()},
                    synchronize_session=False)
        )

        for item in detail:
            item['id_jurnal_mal'] = id_journal_mal

            if 'id_mal_detail' in item and item['id_mal_detail']:
                existing_detail = JurnalMalDetailModel().query.filter_by(id_mal_detail=item['id_mal_detail']).first()
                if existing_detail:
                    existing_detail.id_coa = item['id_coa']
                    existing_detail.id_modul = item['id_modul']
                    existing_detail.id_source_data = item['id_source_data']
                    existing_detail.type = item['type']
                    existing_detail.urutan = item['urutan']
                    self.add(existing_detail)
                else:
                    raise nonServerErrorException(400, f"Jurnal mal detail with id {item['id_mal_detail']} not found")
            else:
                insert_jurnal_mal_detail = JurnalMalDetailModel(
                    id_jurnal_mal=item['id_jurnal_mal'],
                    id_modul=item['id_modul'],
                    id_source_data=item['id_source_data'],
                    id_coa=item['id_coa'],
                    type=item['type'],
                    urutan=item['urutan'],
                    created_by=created_by
                )

                self.add(insert_jurnal_mal_detail)

        self.commit()

        return {
            'status': 'success',
            'message': 'Jurnal mal berhasil diupdate',
            'data': {
                'id_jurnal_mal': id_journal_mal,
                'nama_mal': nama_mal,
                'detail': detail
            }
        }

    @handle_error
    def get_jurnal_active_use_coa(self):
        id_coa = self.req('id_coa')
        query = """
                SELECT DISTINCT jm.id_jurnal_mal, jm.nama_mal
                FROM jurnal_mal_detail jmd
                         JOIN jurnal_mal jm ON jmd.id_jurnal_mal = jm.id_jurnal_mal
                WHERE jmd.id_coa = :id_coa
                  AND jm.is_deleted = FALSE;
                """
        params = {'id_coa': id_coa}
        result = self.query().setRawQuery(query).bindparams(params).execute().fetchall().get()

        return result
