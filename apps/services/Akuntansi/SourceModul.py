from .BaseAkuntansi import BaseAkuntansi
from ...handler import handle_error


class SourceModul(BaseAkuntansi):
    def __init__(self):
        super().__init__()

    @handle_error
    def getSourceModulAndListJurnalSettingUsedSourceModul(self):
        query = """
                SELECT source_modul.nama_kolom_view,
                       ARRAY_AGG(DISTINCT jm.nama_mal) AS nama_mal_list
                FROM source_modul
                         LEFT JOIN jurnal_mal_detail jmd
                                   ON source_modul.id_modul = jmd.id_modul
                         LEFT JOIN jurnal_mal jm
                                   ON jm.id_jurnal_mal = jmd.id_jurnal_mal
                GROUP BY source_modul.id_modul, source_modul.nama_kolom_view;

                """
        source_modul = self.query().setRawQuery(query).execute().fetchall().get()

        return source_modul
