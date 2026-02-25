from apps.services.BaseServices import BaseServices

class BaseAkuntansi(BaseServices):
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

        return where_clauses, bindParams

    def buildWhereClause(self, conditions, additional_conditions=None):
        """
        Build WHERE clause with proper AND handling
        
        Args:
            conditions: dict of conditions from poolRequest
            additional_conditions: list of additional WHERE conditions
            
        Returns:
            tuple: (where_clause_string, bind_params)
        """
        where_clauses, bindParams = self.poolRequest(conditions)
        
        # Add additional conditions if provided
        if additional_conditions:
            if isinstance(additional_conditions, str):
                additional_conditions = [additional_conditions]
            where_clauses.extend(additional_conditions)
        
        # Build final WHERE clause
        if where_clauses:
            where_clause = "WHERE " + " AND ".join(where_clauses)
        else:
            where_clause = ""
            
        return where_clause, bindParams

    def addWhereCondition(self, existing_where, new_condition, bind_params=None):
        """
        Safely add condition to existing WHERE clause
        
        Args:
            existing_where: existing WHERE clause string
            new_condition: new condition to add
            bind_params: additional bind parameters
            
        Returns:
            tuple: (updated_where_clause, updated_bind_params)
        """
        if not existing_where or existing_where.strip() == "":
            where_clause = f"WHERE {new_condition}"
        elif existing_where.strip().upper().startswith("WHERE"):
            where_clause = f"{existing_where} AND {new_condition}"
        else:
            where_clause = f"WHERE {existing_where} AND {new_condition}"
            
        return where_clause, bind_params or {}