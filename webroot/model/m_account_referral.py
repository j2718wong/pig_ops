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
        
        where_clause = 'WHERE a.account_id = %s ' %account_id
        where_clause += ' AND (a.flag & 1) = 0' 
            
        
        sql =   """
                SELECT 
                    a.id,
                    b.group_num,
                    
                    c.name_last,
                    c.name_first,
                    
                    d.name_last,
                    d.name_first,
                    
                    
                    a.dt_entry
                FROM account_access_code a
                LEFT OUTER JOIN user_group b    ON a.user_group_id = b.id
                LEFT OUTER JOIN user c          ON a.used_by_user_id = c.id
                LEFT OUTER JOIN user d          ON a.issued_by_user_id = d.id
                %s
                ORDER BY a.id DESC
                """ % (where_clause)
    
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
            
        for row in rows:
            name_last =    row[2]
            
                
            cur_entry = {
            
                'access_code': {
                    'id':               row[0],
                    'user_group':{  
                        'number':       row[1]
                    },
                    
                    'used_by_user':{
                        'name_last':    name_last,
                        'name_first':   row[3]
                    },
                    
                    'dt_entry':         str(row[6])
                }
            }
            
            
            if name_last is None:
                del cur_entry['access_code']['used_by_user']
                
            result.append(cur_entry)
    
        return result
    
    
