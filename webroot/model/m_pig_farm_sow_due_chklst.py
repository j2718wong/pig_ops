# February 2, 2026
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



class PigFarmSowDueChklst(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def get_active_list(self, pig_farm_id):
        sql =   """
                SELECT 
                    a.id,
                    b.name,
                    a.date_checked
                FROM pf_sow_due_chklst_item a
                LEFT OUTER JOIN account_sow_due_chklst b ON a.acc_sow_due_chklst_id = b.id
                INNER JOIN pig_farm p ON p.last_sow_due_chklst_id = a.pf_sow_due_chklst_id
                WHERE p.id = %s
                ORDER BY b.name
                """ % pig_farm_id
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_entry = {
                    'id':               row[0], 
                    'name':             row[1],
                    'dt_checked':       str(row[2]) if row[2] else None
                    
                }
                
                result.append(cur_entry)

        
        return result
    
    
    
    def update_checklist_item(self, data = None):
        """
        PROCEDURE pf_sow_due_chklst_item_update(
            in_user_id              INT,
            in_chklst_item_id       INT,
            in_is_checked           INT
        )  
        """
       
        params = [
            data.user_id,
        
            data.chklst_item_id,
            data.is_checked
        ]
       
        res = self._call_procedure('pf_sow_due_chklst_item_update', params)
        
        if res is None:
            return None
        
        
        row = res[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2]
                }
            }

        return None
    
    
