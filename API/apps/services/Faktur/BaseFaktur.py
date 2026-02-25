from apps.services.BaseServices import BaseServices
from apps.lib.helper import GetWhereBindParams
class BaseFaktur(BaseServices):
    def __init__(self):
        super().__init__()

    def _NormalizeId(self, faktur_ids):
        if isinstance(faktur_ids, (list, tuple, set)):
            return tuple(int(x) for x in faktur_ids)
        return (int(faktur_ids),)

    def GetFaktur(self):
        try:
          query = "SELECT * FROM faktur"
          rows = (
              self.query()
              .setRawQuery(query)
              .execute()
              .fetchall()
              .get()
          )
          return rows or []
        except Exception as e:
            print(e)
            return False

    def GetFakturById(self, id_faktur):
        try:
            conditions = {
                "id_faktur": "id = :id_faktur"
            }
            query = f"""
                select * from faktur
                where {conditions}
                """
            rows = (
                self.query()
                .setRawQuery(query)
                .bindparams({"id_faktur": int(id_faktur)})
                .execute()
                .fetchone()
                .get()
            )
            return rows or {}
        except Exception as e:
            print(e)
            return False

    def UpdateFakturBy(self, clauses_data={}, clauses={}, data={}):
      try:
          # print("====== data ======= \n", data)
          where_clauses, bindParams = GetWhereBindParams(clauses_data, clauses)
          if not bindParams or not where_clauses:
              return None
          set_parts = []
          valueBindParams = {}
          for key, value in data.items():
              placeholder = f"{key}"
              set_parts.append(f"{key} = :{placeholder}")
              valueBindParams[placeholder] = value

          set_value = ', '.join(set_parts)
          where_clause = f"""WHERE {where_clauses}"""
          query = f"""
            UPDATE faktur
            SET {set_value}  
            {where_clause}
           """
          params = {**bindParams, **valueBindParams}
          self.query().setRawQuery(query).bindparams(params).execute()
          return True
      except Exception as e:
          print(e)
          return False

    def GetDataFakturBy(self, clauses_data, clauses):
        try:
            where_clauses, bindParams = GetWhereBindParams(clauses_data, clauses)
            if not bindParams:
                return None
            query = f"""
                select * from faktur
                where {where_clauses}
                """
            row = (
                self.query()
                .setRawQuery(query)
                .bindparams(bindParams)
                .execute()
                .fetchall()
                .get()
            )
            return row
        except Exception as e:
            print("error get data faktur by:", str(e))
            return None