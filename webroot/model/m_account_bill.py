# May 5, 2026
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



class AccountBill(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add_upload_receipt(self, data = None):
        """
        PROCEDURE account_upload_receipt_add(
            in_user_id              INT,
            in_account_bill_id      INT,
            
            in_file_path            VACHAR(255)
        )  
        """
        
        params = [
            data['user_id'],
            data['account_bill_id'],
            data['file_path']
        ]
        
        res = self._call_procedure('account_upload_receipt_add', params)
        
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
                
                'upload_receipt': {
                    'id':               row[3]
                }
            }

        return None
    
    
    
    def get_uploaded_receipt(self, account_bill_id):
        
        sql =   """
                SELECT 
                    b.file_path
                    
                FROM account_bill a
                LEFT OUTER JOIN account_upload_receipt b    ON a.upload_receipt_id = b.id
                WHERE a.id = %s
                """ % (account_bill_id)
    
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
        
            
        for row in rows:
    
                
            cur_entry = {
            
                'upload_receipt': {
                    'path':         row[0]
                    
                }
            }
            
            
            return cur_entry
            
        return None
    
    

    
