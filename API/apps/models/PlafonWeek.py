from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request


class PlafonWeek() :
    
    def get_current_week() :
        """
        """
        # Mendapatkan Penyesuaian Week Terbaru dari Plafon Week
        result = DB().setRawQuery("""
            SELECT * FROM plafon_week 
            WHERE tanggal = (SELECT MAX(tanggal) FROM plafon_week)
        """).execute().fetchone().result

        tanggal = result['tanggal']

        # Periode dari Minggu yang Sedang Berlangsung Berdasarkan Minggu Tahun (asli).
        # Minggu Tahun diambil dari Tanggal Penyesuan Minggu di Plafon Week.
        a = date_woy_by_date(tanggal)
        a = int(a) % 4

        # Periode dari Minggu yang Sedang Berlangsung Berdasarkan Minggu Tahun yang
        # Telah Disesuaikan. Minggu Tahun yang Disesuaikan Diinputkan Manual Oleh User. 
        # Minggu Tahun yang Disesuaikan akan Diperoleh dari Kolom Minggu pada Plafon Week.
        b = result['minggu']

        # Jika Perhitungan Selisih Minggu Maju
        selish = a - b
        if selish < 0 : selish += 4

        # Perhitungan Minggu yang Akan Disesuaikan. Jika Perhitungan Selisih Minggu Maju
        woy    = date_woy_now()
        minggu = (int(woy) % 4) - selish
        if minggu < 0    : minggu += 4
        elif minggu == 0 : minggu = 4

        return {"minggu" : minggu}