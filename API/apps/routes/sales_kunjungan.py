from flask import Blueprint

from apps.lib.encryption import encrypt_response
from apps.services.BaseServices import token_auth
from apps.services import SalesKunjungan

sales_kunjungan = Blueprint('sales_kunjungan_bp', __name__, url_prefix='/api/sales-kunjungan/')
sales_kunjungan.before_request(lambda: token_auth.login_required(lambda: None)())

# Endpoint 1: Mendapatkan daftar kunjungan berdasarkan User ID
# userId dijamin sebagai integer
@sales_kunjungan.route('get-list-kunjungan/<int:userId>')
# @encrypt_response
def get_list_kunjungan(userId): 
    """Mengambil daftar kunjungan untuk user tertentu."""
    return SalesKunjungan().getListKunjungan(userId)

# Endpoint 2: Check-in Kunjungan
# kunjunganId diubah menjadi integer (jika ID adalah integer)
@sales_kunjungan.route('check-in-kunjungan/<int:kunjunganId>', methods=["PUT"])
def check_in_kunjungan(kunjunganId): 
    """Melakukan check-in kunjungan (status 1)."""
    return SalesKunjungan().checkInOrOutKunjungan(kunjunganId, 1)

# Endpoint 3: Check-out Kunjungan
# kunjunganId diubah menjadi integer (jika ID adalah integer)
@sales_kunjungan.route('check-out-kunjungan/<int:kunjunganId>', methods=["PUT"])
def check_out_kunjungan(kunjunganId): 
    """Melakukan check-out kunjungan (status 2)."""
    return SalesKunjungan().checkInOrOutKunjungan(kunjunganId, 2)

# Endpoint 4: Membuat Sales Kunjungan
@sales_kunjungan.route('create-sales-kunjungan', methods=["POST"])
def create_sales_kunjungan(): 
    """Mengkonversi plafon jadwal menjadi sales kunjungan."""
    return SalesKunjungan().convertPlafonJadwal()