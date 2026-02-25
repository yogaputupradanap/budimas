

from apps.handler import handle_error, handle_error_rollback, nonServerErrorException

from apps.services import BaseServices
from apps.models import CreditNote, faktur, plafon


class CreditNoteService(BaseServices):
    @handle_error
    def getCreditNoteList(self):
        """
        Get list of Credit Notes with pagination.
        """

        id_customer = self.req('customer_id')
        id_principal = self.req('id_principal')

        data = (
            self.query()
            .setRawQuery(
                """
                select cn.total_cn, cn.kode_cn, cn.id_cn from credit_note cn
                WHERE
                    cn.id_principal = :id_principal
                  AND cn.id_customer = :customer_id
                    AND cn.status_cn = 0
                ORDER BY cn.id_cn ASC
                """
            )
            .bindparams(
                {
                    'id_principal': id_principal,
                    'customer_id': id_customer
                }
            )
            .execute()
            .fetchall()
            .get()
        )

        return {
            'status': True,
            'message': 'List of Credit Notes',
            'data': data
        }

    @handle_error_rollback
    def useCreditNote(self):
        print("credit_note")
        id_cn = self.req('id_cn')
        id_faktur = self.req('id_faktur')

        print("credit_note")
        if not id_cn or not id_faktur:
            raise nonServerErrorException('id_cn and id_faktur are required')

        # Check if Credit Note exists and is not used
        credit_note = (
            CreditNote.query
            .with_for_update()
            .filter(CreditNote.id_cn == id_cn, CreditNote.status_cn == 0)
            .first()
        )
        if not credit_note:
            raise nonServerErrorException('Credit Note not found or already used')

        faktur_data = (
            self.query()
            .setRawQuery(
                """
               WITH data_cte AS (
                             SELECT
                                 f.no_faktur,
                                 f.id AS id_faktur,
                                 p.id AS id_plafon,
                                 so.tanggal_faktur,
                                 f.total_penjualan,
                                 ABS(
                                         COALESCE(
                                                 (
                                                     SELECT SUM(s.jumlah_setoran)
                                                     FROM setoran s
                                                     WHERE s.id_sales_order = so.id
                                                            AND s.status_setoran = 3
                                                 ),
                                                 0
                                         ) -( f.total_penjualan - COALESCE(f.nominal_retur, 0))
                                 ) AS setoran --ini yg harus dibayarkan
                             FROM faktur f
                                      JOIN sales_order so ON so.id = f.id_sales_order
                                      JOIN plafon p ON p.id = so.id_plafon
                                      JOIN customer c ON c.id = p.id_customer
                                      JOIN principal pp ON pp.id = p.id_principal
                             WHERE f.status_faktur = 2
                               AND f.id = :id_faktur
                                 
                                ORDER BY so.tanggal_jatuh_tempo ASC
                         )
                         SELECT *
                         FROM data_cte      
                """
            )
            .bindparams({'id_faktur': id_faktur})
            .execute()
            .fetchone()
            .result
        )

        if not faktur_data:
            raise nonServerErrorException('Faktur not found or already paid')

        if faktur_data.get('setoran') < credit_note.total_cn:
            raise nonServerErrorException(
                'Credit Note amount exceeds the payable amount for this Faktur'
            )

        # Update Credit Note status to used
        credit_note.status_cn = 1
        credit_note.id_faktur = id_faktur

        faktur_update = (
            faktur.query
            .with_for_update()
            .filter(faktur.id == id_faktur)
            .first()
        )

        faktur_update.nominal_retur = (faktur_update.nominal_retur or 0) + credit_note.total_cn

        plafon_update = (
            plafon.query
            .with_for_update()
            .filter(plafon.id == faktur_data.get('id_plafon'))
            .first()
        )

        plafon_update.sisa_bon = (plafon_update.sisa_bon or 0) + credit_note.total_cn

        # Save changes
        self.add(credit_note)
        self.add(faktur_update)
        self.add(plafon_update)

        self.commit()

        return {
            'status': True,
            'message': 'Credit Note used successfully',
        }




