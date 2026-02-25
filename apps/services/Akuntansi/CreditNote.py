import datetime

from flask import request

from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.lib.helper import date_now, datetime_now, date_for_code
from apps.lib.paginate import Paginate
from apps.models.pengeluaran_kasir import pengeluaran_kasir
from .BaseAkuntansi import BaseAkuntansi
from typing import List

from ...lib.paginateV2 import PaginateV2
from ...models import Customer, MutasiBank, RekeningPerusahaan
from ...models.sales_detail import SalesDetail


class CreditNote(BaseAkuntansi):
    def __init__(self):
        super().__init__()

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
