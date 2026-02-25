from   apps.handler        import  token_auth
from   apps.handler        import  *
from   apps.helper         import  *
from   flask               import  Blueprint, request, abort
from   werkzeug.exceptions import  HTTPException
from   pytz                import  timezone
from   io                  import  StringIO
import csv, datetime


test = Blueprint('test_routes', __name__, url_prefix='/api/test/')


@test.route('1', methods=['GET'])
def _1() : return "API is working Fine!"

@test.route('2', methods=['GET'])
def _2() : return datetime_now()

@test.route('3', methods=['POST'])
def _3() :
    '''
        Testing Resource.\n
        Testing Pengolahan `Multipart Data` [ Blob / File / Gambar ].

        @todo    Melakukan Pengecekan isi File dengan ekstensi CSV.
        @param   `file`  File dengan ekstensi CSV yang ingin dicek `multipart-request`.
        @return  (json)  Data / Isi dari file CSV yang dikirim.
    '''
    try :
        # Menyimpan File yang Diupload.
        file = request.files['file'] 

        # Mengekstraksi Raw Content dari File.                  
        fileContent = file.stream.read().decode('utf-8') 

        # Merubah Raw Content Menjadi OrderedDict.
        data = csv.DictReader(StringIO(fileContent), delimiter=',') 

        # Merubah OrderedDict Menjadi List Dict.
        data = [row for row in data] 
        
        result = {"result" : data, "status" : 200} if data else abort(HTTPException)

        return result

    except Exception as e :
            return abort(500, description=str(e))
