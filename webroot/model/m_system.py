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
           
           
           
           
            
            cur_entry = {
                'sys': {
                    'count_user':   cur_count_user,
                    'email':        cur_email,
                    'name_last':    cur_name_last,
                    'name_first':   cur_name_first,
                    'flag':         cur_flag
                },
                
                'user_group': {
                    'id':           cur_user_group_id,
                    'group_num':    cur_group_num,
                    'name':         cur_group_name
                }
            }
            result.append(cur_entry)
        
        return result
    
