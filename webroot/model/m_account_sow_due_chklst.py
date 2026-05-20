# May 20, 2026
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



class AccountSowDueChklst(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE account_sow_due_chklst_add(
            in_user_id              INT,
            in_name                 VARCHAR(50)
        )   
        """
        
        params = [
            data.user_id,
            data.name
        ]
        
        res = self._call_procedure('account_sow_due_chklst_add', params)
        
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
                
                'account_checklist': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE account_sow_due_chklst_update(
            in_user_id              INT,
            
            in_acc_chklst_id        INT,
            in_name                 VARCHAR(50)
        )
        """
       
        params = [
            data.user_id,
            data.acc_chklst_id,
            data.name
        ]
        
        res = self._call_procedure('account_sow_due_chklst_update', params)
        
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
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        acc_chklst_id       = data['acc_chklst_id']
        
        """
        PROCEDURE account_sow_due_chklst_delete(
            in_user_id                  INT,
            
            in_acc_chklst_id            INT
        )
        """
       
        params = [
            user_id,
            acc_chklst_id
        ]
        
        res = self._call_procedure('account_sow_due_chklst_delete', params)
        
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
                
                'account_pig_ops': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_list(self, account_id, inc_deleted = 0, inc_user_audit = 0):
        
        where_clause = 'WHERE account_id = %s' % account_id
            
        if inc_deleted == 0:
            where_clause += ' AND (flag & 1) = 0' 
            

        sql =   """
                SELECT 
                    id,
                    name
                FROM account_sow_due_chklst 
                %s
                ORDER BY name
                """ % where_clause

        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
        
            
        for row in rows:
                
            cur_entry = {                
                'id':               row[0],
                'name':             row[1]
            }
        
                
            result.append(cur_entry)
    
        return result
    
    
