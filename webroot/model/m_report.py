# March 30, 2026
# Jack Wong
import os
import sys

from common_constants       import *

# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)

from base_model             import BaseModel


class Report(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE pig_farm_report_add_or_update(
            in_user_id              INT,
            
            in_pig_farm_id          INT,
            in_report_type_id       INT,
            
            in_report_date          VARCHAR(10),
            in_report_language      VARCHAR(8),
            
            in_file_path            VARCHAR(255),
            in_notes                VARCHAR(160)
        )    
        """
        
        params = [
            data.user_id,
            
            data.pig_farm_id,
            data.report_type_id,
            
            data.report_date,
            data.language,
            
            data.file_path,
            data.notes              if data.notes and data.notes.strip() else None
        ]
        
        
        res = self._call_procedure('pig_farm_report_add_or_update', params)
        
        if res is None:
            return None
        
        
        row = res[0]
        
        
        # First result set: status
        if row is not None:
            return {
                'result': {
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'report': {
                    'id':               row[3]
                }
            }
            
        return None



    def get_list(self, pig_farm_id, report_type_id, date_min = None):
        values = (pig_farm_id, report_type_id)
        where_clause = 'WHERE a.pig_farm_id = %s AND a.report_type_id = %s' % values
        
        if date_min is not None:
            where_clause += ' AND a.report_date >= "%s"' % date_min 
        
        
        sql =   """
                SELECT 
                    a.id,
                    a.report_type_id,
                    a.report_date,
                    a.notes,
                    
                    b.name_last,
                    b.name_first,
                    a.dt_entry
                    
                FROM pig_farm_report a 
                LEFT OUTER JOIN user b          ON a.added_by_user_id   = b.id
                %s
                ORDER BY a.report_date DESC
                """ % where_clause
    
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        
        result = []
            
        for row in rows:
            cur_id                      = row[0]
            cur_report_type_id          = row[1]
            cur_report_date             = str(row[2])
            cur_notes                   = row[3]
            
            cur_name_last               = row[4]
            cur_name_first              = row[5]
            cur_dt_entry                = str(row[6])    
            
            
            
            cur_entry = {
                'report': {
                    'id':               cur_id,
                    'type_id':          cur_report_type_id,
                    'date':             cur_report_date
                },
                
                'added_by': {
                    'name_last':        row[3],
                    'name_first':       row[4],
                    'dt_entry':         str(row[5])
                }
            }
        
            if cur_notes is not None:
                cur_entry['report']['notes'] = cur_notes
        
                
            result.append(cur_entry)
    
        return result
    
    
    def get_report_file_path(self, report_id):
        
        sql =   """
                SELECT 
                    file_path
                    
                FROM pig_farm_report 
                WHERE id = %s
                """ % report_id
    
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
        
        
        result = []
            
        for row in rows:
            cur_file_path               = row[0]
    
            return cur_file_path
    
        return None
    
    
    
    
