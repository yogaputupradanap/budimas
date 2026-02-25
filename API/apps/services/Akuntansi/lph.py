from flask import request


from .BaseAkuntansi import BaseAkuntansi
from ...handler import handle_error, nonServerErrorException, handle_error_rollback
from ...lib.paginate import Paginate
from ...lib.helper import string_to_date, get_week_number_for_date, get_day_number_for_date, is_holiday, \
    get_saturday_of_week, datetime_now, date_to_string
from ...models.lph import lph as LphModel
from ...models.lph_detail import lph_detail as LphDetailModel


class lph(BaseAkuntansi):
    def __init__(self):
        super().__init__()

    def _build_schedule_condition(self, tanggal):
        """
        Membuat kondisi SQL untuk menentukan jadwal plafon berdasarkan tanggal
        
        @param tanggal: string tanggal dalam format 'YYYY-MM-DD'
        @return: tuple (condition_sql, params) untuk WHERE clause
        """
        if not tanggal:
            return "", {}
        
        # Convert string to date object
        input_date = string_to_date(tanggal)
        
        # Check if it's a holiday
        # if is_holiday(input_date):
        #     return "1 = 0", {}  # Return false condition for holidays
        
        # Get day and week number for the input date
        day_number = get_day_number_for_date(input_date)
        week_number = get_week_number_for_date(input_date)
        
        # Week combination mapping
        week_combo = {
            5: [1, 2], 6: [1, 3],
            7: [1, 4], 8: [2, 3], 
            9: [2, 4], 10: [3, 4]
        }
        
        # Build week conditions
        week_conditions = []
        
        # Regular week condition
        week_conditions.append("(pj.id_minggu = :week_number AND pj.id_hari = :day_number)")
        
        # Week 11 condition (always active)
        week_conditions.append("(pj.id_minggu = 11 AND pj.id_hari = :day_number)")
        
        # Week combo conditions
        for combo_week, valid_weeks in week_combo.items():
            if week_number in valid_weeks:
                week_conditions.append(f"(pj.id_minggu = {combo_week} AND pj.id_hari = :day_number)")
        
        # Combine all conditions with OR
        condition_sql = f"EXISTS (SELECT 1 FROM plafon_jadwal pj WHERE pj.id_plafon = pl.id AND pj.id_status = 1 AND ({' OR '.join(week_conditions)}))"
        
        params = {
            'week_number': week_number,
            'day_number': day_number
        }
        
        return condition_sql, params

    def _check_plafon_schedule(self, tanggal, id_sales=None):
        """
        Mengecek plafon mana saja yang memiliki jadwal pada tanggal tertentu
        
        @param tanggal: string tanggal dalam format 'YYYY-MM-DD'  
        @param id_sales: optional, filter berdasarkan sales tertentu
        @return: list of plafon IDs yang memiliki jadwal pada tanggal tersebut
        """
        if not tanggal:
            return []
            
        schedule_condition, params = self._build_schedule_condition(tanggal)
        
        if not schedule_condition:
            return []
        
        # Base query untuk mendapatkan plafon yang memiliki jadwal
        query = f"""
            SELECT DISTINCT pl.id as id_plafon
            FROM plafon pl
            WHERE {schedule_condition}
        """
        
        # Add sales filter if provided
        if id_sales:
            query += " AND pl.id_sales = :id_sales"
            params['id_sales'] = id_sales
        
        result = self.query().setRawQuery(query).bindparams(params).execute().fetchall().get()
        
        return [row['id_plafon'] for row in result]

    @handle_error
    def getLph(self):
        id_cabang = self.req('id_cabang')
        
        # Validasi id_cabang wajib diisi
        if not id_cabang:
            raise nonServerErrorException(500, 'ID Cabang wajib diisi')

        query = """
        SELECT
            lph.id,
            TO_CHAR(lph.tanggal_lph, 'YYYY-MM-DD HH24:MI:SS') as tanggal_lph,
            lph.kode_lph,
            lph.id_user as id_pencetak,
            lph.id_sales,
            u_sales.nama as nama_sales,
            u_pencetak.nama as nama_pencetak
        FROM lph
        JOIN sales s ON s.id = lph.id_sales
        JOIN users u_sales ON u_sales.id = s.id_user 
        JOIN users u_pencetak ON u_pencetak.id = lph.id_user AND u_pencetak.id_cabang = :id_cabang
        """

        bindparams = {'id_cabang': id_cabang}

        return Paginate(request, query, bindparams).paginate()

    @handle_error
    def getAddLph(self):
        id_cabang = self.req('id_cabang')
        id_sales = self.req('id_sales')
        tanggal = self.req('tanggal')
        is_cp = self.req('is_cp')

        # Validasi id_cabang wajib diisi
        required_fields = {
            'id_cabang': 'ID Cabang wajib diisi',
            'id_sales': 'ID Sales wajib diisi',
            'tanggal': 'Tanggal wajib diisi',
            'is_cp': 'Status Call Plan wajib diisi'
        }

        for field, message in required_fields.items():
            if not locals()[field]:
                raise nonServerErrorException(500, message)

        # Base query
        query = """
                select
                      c.id as id_customer,
                      c.nama as nama_customer,
                      c.kode as kode_customer,
                      so.id as id_sales_order,
                        f.nominal_retur,
                      so.tanggal_faktur,
                      f.id as id_faktur,
                      f.total_penjualan,
                      f.no_faktur,
                      so.tanggal_jatuh_tempo,
                      pl.id as id_plafon,
                      s.id as id_sales,
                      u.nama as nama_sales,
                      pr.nama as nama_perusahaan,
                        STRING_AGG(cn.kode_cn, ', ') as kode_cn,
                      pr.kode as kode_perusahaan,
                      (f.total_penjualan - coalesce(st_total.total_setoran, 0) - coalesce(f.nominal_retur, 0)) as sisa_pembayaran
                from sales_order so
                join faktur f on so.id = f.id_sales_order and f.status_faktur = 2 -- unpaid
                join plafon pl on pl.id = so.id_plafon
                join customer c on c.id = pl.id_customer
                join sales s on s.id = pl.id_sales and s.id = :id_sales
                join users u on u.id = s.id_user
                join principal p on p.id = pl.id_principal
                join perusahaan pr on pr.id = p.id_perusahaan
                left join credit_note cn on cn.id_faktur = f.id
                left join (
                    select 
                        st.id_sales_order,
                        sum(st.jumlah_setoran) as total_setoran
                    from setoran st
                    where st.status_setoran = 3 -- sudah disetor
                    group by st.id_sales_order
                ) st_total on so.id = st_total.id_sales_order
                where so.id_cabang = :id_cabang                    
        """

        bindparams = {'id_cabang': id_cabang, 'id_sales': id_sales}

        # Jika tanggal diisi, filter berdasarkan is_cp
        if tanggal:
            if is_cp == '1':  # Call Plan
                # Filter berdasarkan jadwal plafon
                schedule_condition, schedule_params = self._build_schedule_condition(tanggal)
                if schedule_condition:
                    query += f" AND {schedule_condition}"
                    bindparams.update(schedule_params)

                # Filter tanggal jatuh tempo sampai hari Sabtu di minggu yang sama
                saturday_date = get_saturday_of_week(tanggal)
                if saturday_date:
                    query += " AND so.tanggal_terkirim <= :saturday_date"
                    bindparams['saturday_date'] = saturday_date
                    
            elif is_cp == '0':  # Tidak Call Plan
                # Filter yang tidak sesuai jadwal
                schedule_condition, schedule_params = self._build_schedule_condition(tanggal)
                if schedule_condition:
                    query += f" AND NOT ({schedule_condition})"
                    bindparams.update(schedule_params)

                # Filter tanggal jatuh tempo sampai tanggal parameter
                query += " AND so.tanggal_jatuh_tempo <= :tanggal_param"
                bindparams['tanggal_param'] = tanggal

            query += ("""
             group by 
    c.id, c.nama, c.kode,
    so.id, f.nominal_retur, so.tanggal_faktur,
    f.id, f.total_penjualan, f.no_faktur,
    so.tanggal_jatuh_tempo,
    pl.id, s.id, u.nama, pr.nama, pr.kode, st_total.total_setoran""")

        return self.query().setRawQuery(query).bindparams(bindparams).execute().fetchall().get()

    @handle_error
    def getAddLphByCustomer(self):
        id_cabang = self.req('id_cabang')
        id_customer = self.req('id_customer')
        tanggal = self.req('tanggal')

        required_fields = {
            'id_cabang': 'ID Cabang wajib diisi',
            'id_customer': 'ID Customer wajib diisi',
        }

        for field, message in required_fields.items():
            field_value = locals()[field]
            if not field_value or field_value == '':
                raise nonServerErrorException(400, message)

        base_params = {
            'id_cabang': id_cabang,
            'id_customer': id_customer,
        }
        
        extra_params = {}
        if tanggal:
            extra_params['tanggal_param'] = tanggal

        custom_join = "JOIN sales s ON s.id = pl.id_sales"
        return self._execute_lph_query(base_params, custom_join=custom_join)

    def BASE_QUERY_LPH_MODAL(self):
        return """
            SELECT
                c.id as id_customer,
                c.nama as nama_customer,
                c.kode as kode_customer,
                so.id as id_sales_order,
                f.nominal_retur,
                so.tanggal_faktur,
                f.id as id_faktur,
                f.total_penjualan,
                f.no_faktur,
                so.tanggal_jatuh_tempo,
                pl.id as id_plafon,
                s.id as id_sales,
                u.nama as nama_sales,
                pr.nama as nama_perusahaan,
                STRING_AGG(DISTINCT cn.kode_cn, ', ') as kode_cn,                    
                pr.kode as kode_perusahaan,
                (f.total_penjualan - COALESCE(st_total.total_setoran, 0) - COALESCE(f.nominal_retur, 0)) as sisa_pembayaran
            FROM sales_order so
            JOIN faktur f ON so.id = f.id_sales_order AND f.status_faktur = 2 -- unpaid
            JOIN plafon pl ON pl.id = so.id_plafon
            JOIN customer c ON c.id = pl.id_customer AND c.id = :id_customer
            {diff_join} -- dynamic join
            JOIN users u ON u.id = s.id_user
            JOIN principal p ON p.id = pl.id_principal
            JOIN perusahaan pr ON pr.id = p.id_perusahaan
            LEFT JOIN credit_note cn ON cn.id_faktur = f.id                    
            LEFT JOIN (
                SELECT 
                    st.id_sales_order,
                    SUM(st.jumlah_setoran) as total_setoran
                FROM setoran st
                WHERE st.status_setoran = 3 -- sudah disetor
                GROUP BY st.id_sales_order
            ) st_total ON so.id = st_total.id_sales_order
            WHERE so.id_cabang = :id_cabang
            AND (f.total_penjualan - COALESCE(st_total.total_setoran, 0) - COALESCE(f.nominal_retur, 0)) > 0
            GROUP BY 
                c.id, c.nama, c.kode,
                so.id, f.nominal_retur, so.tanggal_faktur,
                f.id, f.total_penjualan, f.no_faktur,
                so.tanggal_jatuh_tempo,
                pl.id, s.id, u.nama, pr.nama, pr.kode, st_total.total_setoran
        """
    
    def _execute_lph_query(self, base_params, extra_params=None, custom_join=""):
        if isinstance(custom_join, list):
            diff_join = " ".join(custom_join)
        elif isinstance(custom_join, str) and custom_join.strip():
            diff_join = custom_join
        else:
            diff_join = "JOIN sales s ON s.id = pl.id_sales AND s.id = :id_sales"
            
        query = self.BASE_QUERY_LPH_MODAL().format(diff_join=diff_join)
        
        bindParams = base_params.copy() if base_params else {}
        if extra_params and isinstance(extra_params, dict):
            bindParams.update(extra_params)

        return self.query().setRawQuery(query).bindparams(bindParams).execute().fetchall().get()

    @handle_error
    def getAddLphModal(self):
        id_cabang = self.req('id_cabang')
        id_sales = self.req('id_sales')
        id_customer = self.req('id_customer')

        required_fields = {
            'id_cabang': 'ID Cabang wajib diisi',
            'id_sales': 'ID Sales wajib diisi',
            'id_customer': 'ID Customer wajib diisi'
        }

        for field, message in required_fields.items():
            if not locals()[field]:
                raise nonServerErrorException(500, message)
            
        base_params = {
            'id_cabang': id_cabang,
            'id_sales': id_sales,
            'id_customer': id_customer
        }

        return self._execute_lph_query(base_params, custom_join="")
    
    @handle_error
    def getAddLphCustomerModal(self):
        id_cabang = self.req("id_cabang")
        id_customer = self.req("id_customer")

        required_fields = {
            'id_cabang': 'ID Cabang wajib diisi',
            'id_customer': 'ID Customer wajib diisi'
        }
        
        for field, message in required_fields.items():
            if not locals()[field]:
                raise nonServerErrorException(400, message)
            
        base_params = {
            'id_cabang': id_cabang,
            'id_customer': id_customer
        }
            
        custom_join = "JOIN sales s ON s.id = pl.id_sales"

        return self._execute_lph_query(base_params, custom_join=custom_join)

    def _generate_kode_lph(self, kode_perusahaan, tanggal, is_cp):
        """Generate kode LPH dengan format: TT{kode_perusahaan}/YYYYMM/XXXX"""
        tanggal_obj = string_to_date(tanggal)
        tahun_bulan = tanggal_obj.strftime('%Y%m')

        prefix = f"TTCP{kode_perusahaan}" if is_cp == 1 else f"TT{kode_perusahaan}"

        # Fix: gunakan LphModel bukan lph
        count = LphModel.query.filter(
            LphModel.kode_lph.like(f"{prefix}/{tahun_bulan}/%")
        ).count()

        nomor_urut = count + 1
        return f"{prefix}/{tahun_bulan}/{nomor_urut:04d}"

    @handle_error_rollback
    def addLph(self):
        # Ambil data dari request
        data = {
            'id_cabang': self.req('id_cabang'),
            'id_sales': self.req('id_sales'),
            'tanggal': self.req('tanggal'),
            'is_cp': self.req('is_cp'),
            'id_user': self.req('id_user'),
            'kode_perusahaan': self.req('kode_perusahaan'),
            'jumlah_ditagih': self.req('jumlah_ditagih'),
            'data_tagihan': self.req('data_tagihan'),
            'total_retur': self.req('total_retur')
        }
        timestamp = datetime_now()


        # Validasi input
        required_fields = ['id_cabang', 'id_sales', 'tanggal', 'id_user', 'kode_perusahaan', 'jumlah_ditagih',
                           'data_tagihan']
        for field in required_fields:
            if data[field] is None or data[field] == '':
                raise nonServerErrorException(500, f'{field} wajib diisi')

        if not isinstance(data['data_tagihan'], list) or len(data['data_tagihan']) == 0:
            raise nonServerErrorException(500, 'Data tagihan harus berupa array dan tidak boleh kosong')

        # Generate kode LPH
        kode_lph = self._generate_kode_lph(data['kode_perusahaan'], data['tanggal'], data['is_cp'])

        # Insert LPH
        new_lph = LphModel(
            id_sales=data['id_sales'],
            id_user=data['id_user'],
            kode_lph=kode_lph,
            tanggal_lph=data['tanggal'],
            jumlah_ditagih=data['jumlah_ditagih'],
            batch_cetak=1,
            is_cp=data['is_cp'],
            tanggal_dicetak=timestamp,
            total_retur=data['total_retur'],
        )
        self.db.session.add(new_lph)
        self.db.session.flush()

        # Insert LPH Detail
        for tagihan in data['data_tagihan']:
            print(tagihan['kode_cn'])
            detail = LphDetailModel(
                id_lph=new_lph.id,
                id_faktur=tagihan['id_faktur'],
                jumlah_tagihan=tagihan['sisa_pembayaran'],
                nominal_retur=tagihan['nominal_retur'],
                kode_cn=tagihan['kode_cn']  # Gunakan get untuk menghindari KeyError
            )
            self.db.session.add(detail)

        self.db.session.commit()

        # Prepare data untuk response
        nama_perusahaan = data['data_tagihan'][0]['nama_perusahaan']
        data_perusahaan = (
            self.query().setRawQuery(
                """
                SELECT pr.alamat, pr.nama FROM sales s
                JOIN principal p 
                ON p.id = s.id_principal                
                JOIN perusahaan pr
                ON pr.id = p.id_perusahaan                
                 WHERE 
                s.id = :id_sales
                """
            )
            .bindparams({'id_sales': data['id_sales']})
            .execute()
            .fetchone()
            .result
        )
        
        if not data_perusahaan:
            raise nonServerErrorException(404, 'Data perusahaan tidak ditemukan untuk sales terkait')
        
        nama_sales = data['data_tagihan'][0]['nama_sales']
        total_tagihan = sum(item['sisa_pembayaran'] for item in data['data_tagihan'])
        total_retur = sum((item.get('nominal_retur') or 0) for item in data['data_tagihan'])

        # Return response data untuk FE
        return {
            'success': True,
            'message': 'LPH berhasil dibuat',
            'data': {
                'id_lph': new_lph.id,
                'kode_lph': new_lph.kode_lph,
                'tanggal_lph': date_to_string(new_lph.tanggal_lph),
                'nama_perusahaan': data_perusahaan['nama'],
                'alamat_perusahaan': data_perusahaan['alamat'],
                'nama_sales': nama_sales,
                'total_tagihan': total_tagihan,
                'jumlah_ditagih': data['jumlah_ditagih'],
                'total_retur': total_retur,
                'is_cp': data['is_cp'],
                'tanggal_dicetak': new_lph.tanggal_dicetak,
                'data_tagihan': data['data_tagihan']
            }
        }

    @handle_error
    def getDetailLph(self):
        id_lph = self.req('id_lph')

        # Validasi id_lph wajib diisi
        if not id_lph:
            raise nonServerErrorException(500, 'ID LPH wajib diisi')

        query = """
            select 
                ld.id,
                ld.id_lph,
                ld.id_faktur,
                l.kode_lph,
                u.nama as nama_sales,
                l.tanggal_lph,
                c.nama as nama_customer,
                c.kode as kode_customer,
                c.id as id_customer,
                s.id as id_sales,
                so.tanggal_faktur,
                f.no_faktur,    
                ld.kode_cn,
                ld.jumlah_tagihan as sisa_pembayaran, 
                so.tanggal_jatuh_tempo,
                ld.nominal_retur,
                l.total_retur,
                l.batch_cetak,
                pr.nama as nama_perusahaan,
                pr.alamat as alamat_perusahaan
            from lph_detail ld
            join lph l on l.id = ld.id_lph and l.id = :id_lph
            join faktur f on f.id = ld.id_faktur
            join sales_order so on so.id = f.id_sales_order
            join plafon pl on pl.id = so.id_plafon
            join customer c on c.id = pl.id_customer
            join sales s on s.id = pl.id_sales
            join users u on u.id = s.id_user
            join principal p on p.id = pl.id_principal
            join perusahaan pr on pr.id = p.id_perusahaan
        """

        bindparams = {'id_lph': id_lph}

        return self.query().setRawQuery(query).bindparams(bindparams).execute().fetchall().get()

    @handle_error_rollback
    def cetakUlangLph(self):
        id_lph = self.req('id_lph')
        batch_cetak = self.req('batch_cetak')

        # Validasi id_lph wajib diisi
        if not id_lph:
            raise nonServerErrorException(500, 'ID LPH wajib diisi')
        if not batch_cetak:
            raise nonServerErrorException(500, 'Batch cetak wajib diisi')

        lph = LphModel.query.filter_by(id=id_lph).first()

        if not lph:
            raise nonServerErrorException(404, 'LPH tidak ditemukan')

        lph.batch_cetak = batch_cetak

        self.db.session.commit()

        return {
            'success': True,
            'message': 'LPH berhasil dicetak ulang',
        }