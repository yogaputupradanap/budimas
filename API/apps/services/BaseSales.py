from apps.services.BaseServices import BaseServices
from apps import native_db
from sqlalchemy import text as sa_text
from apps.lib.helper import get_week_number_cycle, get_current_day_number
class BaseSales(BaseServices):
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

        return final_where_clause, bindParams
  
  # Only used at Sales service and for get kunjungan logic
  def GetSchedule(self):
      # Get current day and week number
        day_number = get_current_day_number()
        week_number = int(get_week_number_cycle())

        week_combo = {
            5: [1, 2], 6: [1, 3],
            7: [1, 4], 8: [2, 3],
            9: [2, 4], 10: [3, 4]
        }

        # Build the week condition logic
        week_conditions = []

        # Regular week condition
        week_conditions.append(f"(plafon_jadwal.id_minggu = {week_number} AND plafon_jadwal.id_hari = {day_number})")

        # Week 11 condition (always active)
        week_conditions.append(f"(plafon_jadwal.id_minggu = 11 AND plafon_jadwal.id_hari = {day_number})")

        # Week combo conditions
        for combo_week, valid_weeks in week_combo.items():
            if week_number in valid_weeks:
                week_conditions.append(f"(plafon_jadwal.id_minggu = {combo_week} AND plafon_jadwal.id_hari = {day_number})")

        # Combine all week conditions with OR
        week_condition_sql = " OR ".join(week_conditions)

        return week_condition_sql
