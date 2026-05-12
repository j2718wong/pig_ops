# April 19, 2026
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



class System(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def get_sys_stats(self):
        """
        """
        
        params = []
        
        
        rows = self._call_procedure('sys_stats', params)
        
        if rows is None:
            return None
            
        
        result = []
        for row in rows:
            cur_count_user          = row[0]
            cur_user_no_account     = row[1]
            cur_count_account       = row[2]
            cur_account_not_started = row[3]
            cur_account_no_sow_boar = row[4]
           
            cur_entry = {
                'sys': {
                    'count_user':       cur_count_user,
                    'user_no_account':  cur_user_no_account,
                    'count_account':    cur_count_account,
                    'acc_not_started':  cur_account_not_started,
                    'acc_no_sow_boar':  cur_account_no_sow_boar
                }
            }
            
            return cur_entry
            
        
        return None
    
    
    def get_latest_user_list(self, limit= 3):
        sql = """
            SELECT 
                a.email,
                a.name_last,
                a.name_first,
                DATE(a.dt_entry)
            FROM user a 
            ORDER BY a.id DESC 
            LIMIT %s
        """ %limit
        
        rows = self._execute_query(sql, [])
        
        if rows is None:
            return []
        
        result = []
        for row in rows:
            cur_email               = row[0]
            cur_name_last           = row[1]
            cur_name_first          = row[2]
            cur_dt_entry            = row[3]
            
            cur_entry = {
                'email':        cur_email,
                'name_last':    cur_name_last,
                'name_first':   cur_name_first,
                'dt_entry':     str(cur_dt_entry)
            }
            result.append(cur_entry)
        
        return result
    
    
