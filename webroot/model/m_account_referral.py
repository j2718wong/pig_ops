# March 18, 2026
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



class AccountReferral(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE account_access_code_add(
            in_user_id              INT,
            
            in_user_group_num       INT
        )  
        """
        
        params = [
            data.user_id,
            data.group_num
        ]
        
        res = self._call_procedure('account_access_code_add', params)
        
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
                
                'access_code': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update_hashid(self, data = None):
        access_id       = data['access_id']
        hashid          = data['hashid']
        
        values = (hashid, access_id)
        
        sql =   """
                UPDATE account_access_code SET
                    access_code    = "%s"
                WHERE id = %s;
                """ % values
        
        return self.model.execute_sql(sql)
    
        
    def get_list(self, account_id):
        
        sql =   """
                SELECT 
                    a.id,
                    b.name,
                    a.flag,
                    
                    a.business_date_active,
                    a.dt_entry
                FROM account_referral a
                LEFT OUTER JOIN account b    ON a.referred_account_id = b.id
                WHERE a.account_id = %s
                ORDER BY a.id DESC
                """ % account_id
    
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
            
        for row in rows:
            cur_id              = row[0]
            cur_referred_acc    = row[1]
            cur_flag            = row[2]
            
            cur_date_active     = row[3]
            curdt_entry         = row[4]
            
                
            cur_entry = {
            
                'account_referral': {
                    'id':               cur_id,
                    'flag':             cur_flag,
                    
                    'referred_account':{
                        'name':         cur_referred_acc,
                    },
                    
                    'date_active':      cur_date_active,
                        
                    'dt_entry':         str(row[6])
                }
            }
            
            
            if name_last is None:
                del cur_entry['access_code']['used_by_user']
                
            result.append(cur_entry)
    
        return result
    
    
