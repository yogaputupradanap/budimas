from flask import Flask, abort
from pytz import timezone
from datetime import date, time, datetime, timedelta
import json
from re import search, IGNORECASE
import random, re, string, inspect
from google.cloud import storage
import holidays

app = Flask(__name__)
setting_timezone = timezone("Asia/Jakarta")


def empty(value):
    """Checking if a Value is Empty or equal to `None, '', [], {}, 0`"""
    return value is None or (
        isinstance(value, (str, list, dict, tuple, set)) and not value
    )


def time_now():
    """Getting Current Time `Asia/Jakarta Timezone`"""
    return datetime.now(setting_timezone).strftime("%H:%M:%S")


def time_now_stamp():
    """Getting Current Time `Asia/Jakarta Timezone`"""
    return datetime.now(setting_timezone).strftime("%H%M%S")


def date_now():
    """Getting Current Date `Asia/Jakarta Timezone`"""
    return datetime.now(setting_timezone).strftime("%Y-%m-%d")

def date_now_obj():
    """Getting Current Date as a Date Object `Asia/Jakarta Timezone`"""
    return datetime.now(setting_timezone)


def date_now_stamp(add_days: int = 0):
    """Getting Current Date `Asia/Jakarta Timezone` with optional offset"""
    now = datetime.now(setting_timezone) + timedelta(days=add_days)
    return now.strftime("%Y%m%d")


def datetime_now(add_days: int = 0):
    """Getting Current Date `Asia/Jakarta Timezone` with optional offset"""
    now = datetime.now(setting_timezone) + timedelta(days=add_days)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def datetime_now_stamp():
    """Getting Current Date `Asia/Jakarta Timezone`"""
    return datetime.now(setting_timezone).strftime("%Y%m%d%H%M%S")


def dateday_now():
    """Getting Current Date Day `Asia/Jakarta Timezone`"""
    return datetime.now(setting_timezone).strftime("%w")


def date_woy_now():
    """Getting Current Date Day `Asia/Jakarta Timezone`"""
    return datetime.now(setting_timezone).strftime("%U")


def date_woy_by_date(date):
    """Getting Week of The Year By Inputed Date `Asia/Jakarta Timezone`"""
    return datetime(date.year, date.month, date.day, tzinfo=setting_timezone).strftime(
        "%U"
    )


def datetime_to_string(value):
    """Format Datetime to be String"""
    if isinstance(value, time):
        return value.strftime("%H:%M:%S")
    elif isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    elif isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return value


def string_sanitized(value):
    """Removing String Special Characters"""
    return re.sub("[^A-Za-z0-9 \-]+", "", value)


def string_sanitized2(value):
    """Removing String Special Characters, Expect (-, _, +, :)"""
    return (
        "'" + re.sub("[^A-Za-z0-9 \-\_\+\:\,\.\|\\\(\)]+", "", value) + "'"
        if value
        else "NULL"
    )


def string_random(length):
    """Creating Random String"""
    return "".join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        for i in range(length)
    )


def number_random(length):
    """Creating Random Number"""
    min = 10 ** (length - 1)
    max = (10**length) - 1
    return random.randint(min, max)


class Mapper:
    """Object Mapper Functionalities"""

    def __init__(self, data):
        """Set Intial Data"""
        self.data = data
        self.added_cols = []

    def add_col(self, callback, name):
        """Add Additional Row Item"""
        if not empty(self.data):
            for i, row in enumerate(self.data):
                if len(inspect.signature(callback).parameters) == 2:
                    self.added_cols[i].update({name: callback(row, self.data)})
                else:
                    self.added_cols[i].update({name: callback(row)})
        return self

    def edit_col(self, callback, name):
        """Edit Row Items"""
        if not empty(self.data):
            for i, row in enumerate(self.data):
                self.data[i][name] = callback(row)
        return self

    def get(self):
        """Get the Data"""
        if self.added_cols:
            for i, row in enumerate(self.data):
                row.update(self.added_cols[i])
        return self.data

    def to_dict(self):
        """Convert Object to a List of Dictionaries"""
        rv = []
        if not empty(self.data):
            if isinstance(self.data, list):
                for i in self.data:
                    if hasattr(i, "_asdict"):
                        row = i._asdict()
                    elif hasattr(i, "__dict__"):
                        row = {
                            key: value
                            for key, value in vars(i).items()
                            if not key.startswith("_")
                        }
                    else:
                        row = {}
                    for key, value in row.items():
                        row[key] = datetime_to_string(value)

                    rv.append(row)

            self.added_cols = [{} for _ in range(len(self.data))]

        self.data = rv
        return self


def set(result):
    """
    Setting up database fetched result into formated dict.
    @param `result[object]` Fetched result or message.
    @returns `data[dict]` Formated result.
    """
    data = []

    if result == None:
        data = data

    elif isinstance(result, dict) == True and len(list(result)) > 0:
        data.append(result)

    elif len(list(result)) > 0:
        for i in result:
            # Getting a Row of Result Items
            row = i._asdict()

            for key, value in row.items():
                if isinstance(value, time):
                    # Convert 'time' objects to strings
                    row[key] = value.strftime("%H:%M:%S")
                elif isinstance(value, date):
                    # Convert 'date' objects to strings
                    row[key] = value.strftime("%Y-%m-%d")

            data.append(row)

    elif len(list(result)) == 0:
        data = data

    return data


class parseJson:
    def __init__(self, request):
        self.request = request
        self.json_string = request.data.decode("utf-8")
        self.loadJson = json.loads(self.json_string)

    def json(self, param):
        jsonData = self.loadJson.get(param)
        return jsonData if jsonData else ""

    def jsonType(self, param):
        jsonData = self.request.json[param]
        return jsonData if jsonData else ""


def allowed_file(filename):
    image_extensions_pattern = r"\.(jpg|jpeg|png|gif|bmp|tiff)$"

    # Case insensitive matching
    return search(image_extensions_pattern, filename, IGNORECASE) is not None


def extraUploadImage(file):
    """
    untuk upload data.
    @result `dict` nama file bucket.
    """
    if file.filename == "":
        return abort(500, description="No File Uploaded")
    if file and allowed_file(file.filename):
        filename = f"budimas-{time_now_stamp()}-{file.filename}"
        
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket("buktitransaksi")
            blob = bucket.blob(filename)
            
            blob.upload_from_file(file, if_generation_match=0)
            result = set({"filename": filename})

            return result[0]
        except Exception as e:
            return abort(500, description=str(e))
        
def parse_orm_result(data): return [{column.name: getattr(
    row, column.name) for column in row.__table__.columns} for row in data]

def ends_with_brackets(value):
    """
    Check if the given value ends with '[' and ']'.

    Args:
    value (str): The string to check.

    Returns:
    bool: True if the value ends with '[' and ']', False otherwise.
    """
    return value.startswith('[') and value.endswith(']')

def to_array_string(value):
    is_array_string = ends_with_brackets(str(value))
    new_value = value if is_array_string else f"[{value}]"
    
    return new_value


def string_to_date(date_str):
    """
    Convert string date format 'YYYY-MM-DD' to date object

    @param date_str: String date in format 'YYYY-MM-DD'
    @return: date object
    """
    date_parts = date_str.split('-')
    return date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))


def get_week_number_cycle():
    # Dapatkan tanggal hari ini
    current_date = string_to_date(date_now())
    year = current_date.year

    # Cari hari Minggu pertama di tahun ini
    first_sunday = date(year, 1, 1)
    while first_sunday.weekday() != 6:  # 6 = Sunday
        first_sunday += timedelta(days=1)

    # Jika tanggal saat ini sebelum hari Minggu pertama tahun ini
    if current_date < first_sunday:
        # Gunakan hari Minggu pertama tahun sebelumnya
        year -= 1
        first_sunday = date(year, 1, 1)
        while first_sunday.weekday() != 6:
            first_sunday += timedelta(days=1)

    # Hitung minggu ke berapa
    days_diff = (current_date - first_sunday).days
    week_number = (days_diff // 7) + 1

    # Handle kasus minggu 53
    if week_number == 53:
        # Jika ada minggu 53, reset ke minggu 1
        week_number = 1
    elif week_number > 52:
        # Jika lebih dari 52 (karena tahun kabisat atau kasus khusus)
        week_number = 52

    # Return siklus 1-4
    return ((week_number - 1) % 4) + 1

def get_current_day_number():
    """
    Get current day number where Monday=1, Tuesday=2, ..., Sunday=7
    Converts to different format where Sunday=1, Monday=2, ..., Saturday=7

    @return: int representing day number (1-7)
    """
    day_raw = int(datetime.now(setting_timezone).strftime("%u"))
    return 1 if day_raw == 7 else day_raw + 1


def get_now_datetime():
    """
    Get current datetime with the correct timezone for holiday checking

    @return: datetime object with timezone
    """
    return datetime.now(setting_timezone)


def get_week_number_for_date(input_date):
    """
    Menghitung nomor minggu (siklus 1-4) untuk tanggal tertentu
    Menggunakan logika yang sama dengan getWeekNumberOfCurrentMonth

    @param input_date: datetime object
    @return: int (1-4)
    """
    year = input_date.year

    # Find first Sunday of the year
    first_sunday = datetime(year, 1, 1)
    while first_sunday.weekday() != 6:  # 6 = Sunday
        first_sunday += timedelta(days=1)

    # If current date is before first Sunday of the year
    if input_date < first_sunday:
        year -= 1
        first_sunday = datetime(year, 1, 1)
        while first_sunday.weekday() != 6:
            first_sunday += timedelta(days=1)

    # Calculate week number
    days_diff = (input_date - first_sunday).days
    week_number = (days_diff // 7) + 1

    # Handle week 53
    if week_number == 53:
        week_number = 1
    elif week_number > 52:
        week_number = 52

    # Convert to cycle 1-4
    return ((week_number - 1) % 4) + 1


def get_day_number_for_date(input_date):
    """
    Menghitung nomor hari untuk tanggal tertentu
    Sunday=1, Monday=2, ..., Saturday=7

    @param input_date: datetime object
    @return: int (1-7)
    """
    day_raw = input_date.weekday()  # 0 = Monday, 6 = Sunday
    return 1 if day_raw == 6 else day_raw + 2

def date_for_code():
    """Getting Current Date `Asia/Jakarta Timezone` for Kode"""
    return datetime.now(setting_timezone).strftime("%Y%m")

def get_saturday_of_week(tanggal):
    """
    Mendapatkan tanggal hari Sabtu dari minggu yang sama dengan tanggal input

    @param tanggal: string tanggal dalam format 'YYYY-MM-DD'
    @return: string tanggal hari Sabtu dalam format 'YYYY-MM-DD'
    """
    if not tanggal:
        return None

    input_date = string_to_date(tanggal)

    # Hitung berapa hari lagi sampai Sabtu
    # weekday(): Monday=0, Sunday=6
    days_until_saturday = (5 - input_date.weekday()) % 7

    # Jika hari ini adalah Sabtu, days_until_saturday akan menjadi 0
    saturday_date = input_date + timedelta(days=days_until_saturday)

    return saturday_date.strftime('%Y-%m-%d')

def date_to_string(value):
    """Format Date to be String"""
    return value.strftime("%Y-%m-%d") if isinstance(value, date) else value


def is_holiday(input_date):
    """
    Mengecek apakah tanggal tertentu adalah hari libur Indonesia

    @param input_date: datetime object
    @return: boolean
    """

    date_with_tz = setting_timezone.localize(input_date)
    id_holidays = holidays.country_holidays('ID')
    return date_with_tz in id_holidays

def format_angka(number):
    """
    Membulatkan angka menjadi 2 angka di belakang koma.
    Jika hasilnya bilangan bulat, mengembalikan sebagai int,
    jika ada desimal, mengembalikan sebagai float.
    
    @param number: Angka yang akan dibulatkan (string, int, atau float)
    @return: int atau float hasil pembulatan
    
    Contoh:
    - 10000.2321 menjadi 10000.23 (float)
    - 10000.0 menjadi 10000 (int)
    - "10000.2321" menjadi 10000.23 (float)
    - "10000" menjadi 10000 (int)
    """
    # Konversi input ke float apapun tipe datanya
    value = float(number)
    
    # Bulatkan ke 2 angka di belakang koma
    rounded = round(value, 2)
    
    # Cek apakah hasilnya bilangan bulat
    if rounded == int(rounded):
        return int(rounded)
    else:
        return rounded
    
def format_rupiah(number):
    """
    Memformat angka dengan format Indonesia:
    - Titik sebagai pemisah ribuan
    - Koma untuk desimal
    - Bulatkan ke 2 angka di belakang koma jika ada desimal
    - Jika angka bulat, tidak menampilkan koma desimal
    
    @param number: Angka yang akan diformat (string, int, atau float)
    @return: string hasil format
    
    Contoh:
    - 1000000 menjadi "1.000.000"
    - 1000000.00 menjadi "1.000.000"
    - 1000000.3423532 menjadi "1.000.000,34"
    - "1.000.000" tetap "1.000.000"
    - "1.000.000,00" menjadi "1.000.000"
    """
    # Jika input sudah berupa string, hapus separator ribuan dan ganti koma dengan titik
    if isinstance(number, str):
        # Ganti karakter pemisah ribuan (titik) dengan string kosong
        cleaned = number.replace(".", "")
        # Ganti karakter pemisah desimal (koma) dengan titik untuk dikonversi ke float
        cleaned = cleaned.replace(",", ".")
        try:
            number = float(cleaned)
        except ValueError:
            # Jika tidak bisa dikonversi ke float, kembalikan string aslinya
            return number
    
    # Konversi input ke float
    value = float(number)
    
    # Bulatkan ke 2 angka di belakang koma
    rounded = round(value, 2)
    
    # Pisahkan bagian bulat dan desimal
    int_part = int(rounded)
    decimal_part = rounded - int_part
    
    # Format bagian bulat dengan pemisah ribuan (titik)
    formatted_int = "{:,}".format(int_part).replace(",", ".")
    
    # Jika ada desimal dan tidak nol, gabungkan dengan bagian bulat
    if decimal_part > 0:
        # Format bagian desimal dengan dua angka di belakang koma
        decimal_str = "{:.2f}".format(decimal_part)[1:].replace(".", ",")
        return formatted_int + decimal_str
    else:
        # Jika tidak ada desimal, kembalikan hanya bagian bulat
        return formatted_int


def status_order(status):
    """
    Mengembalikan status order dalam format yang sesuai.

    @param status: Status order (int)
    @return: string status order
    """
    status_map = {
        -1: "denied",
        0: "draft",
        1: "booked",
        2: "scheduled",
        3: "picked",
        4: "shipping",
        5: "revision",
        6: "delivered",
        7: "canceled",
        8: "return",
        9: "reschedule",
        10: "rescheduled",
        11: "reshipping",
    }
    return status_map.get(status, "Tidak Diketahui")

def status_faktur(status):
    """
    Mengembalikan status faktur dalam format yang sesuai.

    @param status: Status faktur (int)
    @return: string status faktur
    """
    status_map = {
        -1: "denied",
        0: "draft",
        1: "printed",
        2: "unpaid",
        3: "paid",
        4: "canceled",
    }
    return status_map.get(status, "Tidak Diketahui")

def GetWhereBindParams(data = {}, clauses = {}):
    """
    data: dict parameter input, mis. {"id_faktur": [1,2], "tanggal_awal": "2024-01-01"}
    clauses: dict peta key->kondisi, mis.
        {
          "id_faktur": "faktur.id IN :id_faktur",
          "tanggal_awal": "sales_order.tanggal_faktur >= :tanggal_awal",
          "tanggal_akhir": "sales_order.tanggal_faktur <= :tanggal_akhir",
        }
    return: (where_sql, bind_params)
      where_sql: string tanpa prefix 'WHERE'
      bind_params: dict untuk bindparams()
    """
    if not isinstance(data, dict) or not isinstance(clauses, dict) or not clauses:
        return "", {}

    parts = []
    bind = {}
    for key, condition in clauses.items():
        if key in data and data[key] not in (None, "", []):
            parts.append(condition)
            bind[key] = data[key]

    where_sql = " AND ".join(parts)
    return where_sql, bind
