# January 12, 2026
import os
import sys

from common_constants       import *

# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)

from base_model             import BaseModel


class MedVacType(BaseModel):

    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE medvac_type_add(
            in_user_id              INT,

           
            in_name                 VARCHAR(50)
        )  
        """
        
        params =[
            data.user_id,
            data.name
        ]
        
        
        res = self._call_procedure('medvac_type_add', params)
        
        if res is None:
            return None
        
        
        row = res[0]
        
        
        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'medvac_type': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
        
    def get_list(self,  inc_deleted = 0, inc_user_audit = 0):
        
        where_clause  = ''
        if inc_deleted == 0:
            where_clause += 'WHERE (a.flag & 1) = 0'  
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.name
                    FROM medvac_type a 
                    %s
                    ORDER BY a.name
                    """ % where_clause
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.name,
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM medvac_type a 
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                
                    %s
                    ORDER BY a.name
                    """ % where_clause
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        result = []

            
        for row in rows:
            if inc_user_audit == 0:
                cur_entry = {
                    'id':                   row[0],
                    'name':                 row[1]
                }
                
            else:
                cur_entry = {
                    'id':                   row[0],
                    'name':                 row[1],
                    
                    'added_by': {
                        'name_last':        row[2],
                        'name_first':       row[3],
                        'dt_entry':         str(row[4])
                    },
                    
                    'last_update':{
                        'name_last':        row[5],
                        'name_first':       row[6],
                        'dt_update':        str(row[7]) if row[7] else None
                    }
                }
            
                
            result.append(cur_entry)
    
        return result
    
    
