from flask import Blueprint, request, jsonify
from apps.services.BaseServices import token_auth
from apps.lib.helper import extraUploadImage
from apps.lib.query import DB

extra = Blueprint("extra", __name__, url_prefix="/api/extra/")
# extra.before_request(lambda: token_auth.login_required(lambda: None)())

@extra.route("getCustomerOpt", methods=["GET"])
def get_customer_opt():
    rows = (
        DB(request)
        .setRawQuery("""
            SELECT 
                c.id,
                c.kode,
                c.nama,
                ct.nama AS tipe,
                cb.nama AS nama_cabang
            FROM customer c
            LEFT JOIN customer_tipe ct ON ct.id = c.id_tipe
            LEFT JOIN cabang cb ON cb.id = c.id_cabang
            ORDER BY c.nama
        """)
        .execute()
        .fetchall()
    )

    # rows HARUS list of Row
    result = [dict(row._mapping) for row in rows]

    return jsonify(result)

@extra.route("getCustomer", methods=["GET"])
def get_customer_datatable():
    # === PARAM DATATABLES ===
    draw = int(request.args.get("draw", 1))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))
    search_value = request.args.get("search[value]", "")

    order_index = request.args.get("order[0][column]", None)
    order_dir = request.args.get("order[0][dir]", "asc")

    order_column = "nama"  # default aman

    if order_index is not None:
        col_key = f"columns[{order_index}][data]"
        order_column = request.args.get(col_key, "nama")

    allowed_columns = {
        "kode": "c.kode",
        "nama": "c.nama",
        "tipe": "ct.nama",
        "nama_cabang": "cb.nama",
        "nama_rute": "r.nama"
    }

    order_by = allowed_columns.get(order_column, "c.nama")
    order_dir = "DESC" if order_dir.lower() == "desc" else "ASC"

    # === BASE QUERY ===
    base_query = """
        FROM customer c
        LEFT JOIN customer_tipe ct ON ct.id = c.id_tipe
        LEFT JOIN cabang cb ON cb.id = c.id_cabang
        WHERE 1=1
    """

    params = {}

    if search_value:
        base_query += """
            AND (
                c.kode ILIKE :search
                OR c.nama ILIKE :search
                OR ct.nama ILIKE :search
                OR cb.nama ILIKE :search
            )
        """
        params["search"] = f"%{search_value}%"

    # === TOTAL DATA ===
    total = (
        DB()
        .setRawQuery("SELECT COUNT(*) " + base_query)
        .bindparams(params)
        .execute()
        .fetchone()
        .result
    )[0]

    # === DATA QUERY ===
    data_query = f"""
        SELECT
            c.id,
            c.kode,
            c.nama,
            ct.nama AS tipe,
            cb.nama AS nama_cabang
        {base_query}
        ORDER BY {order_by} {order_dir}
        LIMIT :limit OFFSET :offset
    """

    params.update({
        "limit": length,
        "offset": start
    })

    rows = (
        DB()
        .setRawQuery(data_query)
        .bindparams(params)
        .execute()
        .fetchall()
    )

    data = [dict(row._mapping) for row in rows]

    # === RESPONSE DATATABLES ===
    return jsonify({
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data
    })
    print("ORDER INDEX:", order_index)
    print("ORDER COLUMN:", order_column)
    print("ORDER SQL:", order_by, order_dir)

@extra.route("upload-foto", methods=["POST"])
def _1(): 
    file = request.files["file"]
    return extraUploadImage(file)

@extra.route("global/<string:key_column>")
def _2(key_column):
    global_table = (
        DB()
        .setRawQuery("SELECT value_column FROM global_table WHERE key_column = :key")
        .bindparams({"key": key_column})
        .execute()
        .fetchone()
        .result
    )["value_column"] or 'null'

    return global_table

"""
endpoint to update table dynamically with request argument 
@argument 'table' nama of the table that want to be updated
@argument 'where' conditional to add in DB query
have additional form-data key value used for set table column
with new value
"""
@extra.route('update-builder', methods=["POST"])
def _3():
    tablename = request.args.get("table")
    
    build = (
        DB(request=request)
        .setTable(tablename)
        .update()
        .execute()
    )
    
    return build.response