from apps.services import BaseServices

class BaseAkuntasi(BaseServices):
    def __init__(self):
        super().__init__()

    def poolRequest(self, conditions):
        where_clauses = []
        bindParams = {}

        for key, condition in conditions.items():
            value = self.req(key)
            if value:
                where_clauses.append(condition)
                bindParams[key] = value

        where = " and ".join(where_clauses)
        final_where_clause = f"{where} and" if len(where) else where

        return final_where_clause, bindParams, where