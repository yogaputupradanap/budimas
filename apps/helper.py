from    flask     import  Flask, jsonify, request
from    pytz      import  timezone
from    datetime  import  date, time, datetime

import  random, re, string, inspect

app = Flask(__name__)
setting_timezone = timezone('Asia/Jakarta')


def empty(value):
    """ Checking if a Value is Empty or equal to `None, '', [], {}, 0` """
    return value is None or (isinstance(value, (str, list, dict, tuple, set)) and not value)

def time_now() :
    """ Getting Current Time `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%H:%M:%S')

def time_now_stamp() :
    """ Getting Current Time `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%H%M%S')

def date_now() :
    """ Getting Current Date `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%Y-%m-%d')

def date_now_stamp() :
    """ Getting Current Date `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%Y%m%d')

def datetime_now() :
    """ Getting Current Date `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%Y-%m-%d %H:%M:%S')

def datetime_now_stamp() :
    """ Getting Current Date `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%Y%m%d%H%M%S')

def date_now_without_day_stamp() :
    """ Getting Current Date Without Day `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%Y%m')

def dateday_now() :
    """ Getting Current Date Day `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%w')

def date_woy_now() :
    """ Getting Current Date Day `Asia/Jakarta Timezone` """
    return datetime.now(setting_timezone).strftime('%U')

def date_woy_by_date(date) :
    """ Getting Week of The Year By Inputed Date `Asia/Jakarta Timezone` """
    return datetime(date.year, date.month, date.day, tzinfo=setting_timezone).strftime('%U')

def datetime_to_string(value) :
    """ Format Datetime to be String """
    if    isinstance(value, time)     : return value.strftime('%H:%M:%S')
    elif  isinstance(value, date)     : return value.strftime('%Y-%m-%d')
    elif  isinstance(value, datetime) : return value.strftime('%Y-%m-%d %H:%M:%S')
    else                              : return value

def string_sanitized(value) :
    """ Removing String Special Characters """
    return re.sub('[^A-Za-z0-9 \-]+','', value)

def string_sanitized2(value) :
    """ Removing String Special Characters, Expect (-, _, +, :) """
    return "'"+re.sub('[^A-Za-z0-9 \-\_\+\:\,\.\|\\\(\)]+', '', value)+"'" if value else 'NULL'

def string_random(length):
    """ Creating Random String """
    return ''.join(random
        .choice(
            string.ascii_lowercase + 
            string.ascii_uppercase + 
            string.digits
        ) 
    for i in range(length))

def number_random(length):
    """ Creating Random Number """
    min = 10 ** (length - 1)
    max = (10 ** length) - 1
    return random.randint(min, max)


class Mapper :
    """ Object Mapper Functionalities """

    def __init__(self, data) :
        """ Set Intial Data """
        self.data       = data
        self.added_cols = []

    def add_col(self, callback, name) :
        """ Add Additional Row Item """
        if not empty(self.data) :
            for i, row in enumerate(self.data):
                if len(inspect.signature(callback).parameters) == 2 :
                    self.added_cols[i].update({name : callback(row, self.data)}) 
                else :
                    self.added_cols[i].update({name : callback(row)}) 
        return  self
    
    def edit_col(self, callback, name):
        """Edit Row Items"""
        if not empty(self.data):
            for i, row in enumerate(self.data):
                self.data[i][name] = callback(row)
        return  self

    def get(self) :
        """ Get the Data """
        if self.added_cols:
            for i, row in enumerate(self.data) : 
                row.update(self.added_cols[i])
        return  self.data

    def to_dict(self) :
        """ Convert Object to a List of Dictionaries """
        rv = []
        if not empty(self.data) :
            if isinstance(self.data, list) :
                for i in self.data :
                    if hasattr(i, '_asdict')      :
                        row = i._asdict()
                    elif hasattr(i, '__dict__')   :
                        row = {key: value for key, value in vars(i).items() if not key.startswith('_')}
                    else                          :
                        row = {}
                    for key, value in row.items() :
                        row[key] = datetime_to_string(value)

                    rv.append(row)

            self.added_cols = [{} for _ in range(len(self.data))]

        self.data = rv
        return self



def set(result):
    '''
        Setting up database fetched result into formated dict.
        @param `result[object]` Fetched result or message.
        @returns `data[dict]` Formated result. 
    '''
    data = []

    if result == None :
        data = data
    
    elif isinstance(result, dict) == True and len(list(result)) > 0 :
        data.append(result)

    elif len(list(result)) > 0 :
        for i in result:
            # Getting a Row of Result Items
            row = i._asdict()
            
            for key, value in row.items():
                if isinstance(value, time):
                    # Convert 'time' objects to strings
                    row[key] = value.strftime('%H:%M:%S')
                elif isinstance(value, date):
                    # Convert 'date' objects to strings
                    row[key] = value.strftime('%Y-%m-%d')

            data.append(row)
    
    elif len(list(result)) == 0 :
        data = data

    data = {
        "result" : data,
        "status" : 200
    }
    
    return data