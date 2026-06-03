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
        """
        Note: It is possible for an account_bill id to have multiple receipts
        uploaded;
        """
        
        
        sql =   """
                SELECT
                    a.id,
                    a.status_id,
                    a.flag,
                    a.file_path,
                    a.dt_entry,
                    
                    b.name_last,
                    b.name_first
                    
                FROM account_upload_receipt a
                LEFT OUTER JOIN user b      ON a.added_by_user_id = b.id
                WHERE a.account_bill_id = %s
                ORDER BY a.id DESC
                """ % (account_bill_id)
    
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
        
        result = []
            
        for row in rows:
                
            cur_entry = {
                'id':           row[0],
                'status_id':    row[1],
                'flag':         row[2],
                
                'path':         row[3],
                'dt_entry':     str(row[4]),
                
                'name_last':    row[5],
                'name_first':   row[6]
            }
            
            result.append(cur_entry)
            
        return result
    
    
    
    def read_upload_receipt(self, data = None):
        """
        PROCEDURE account_upload_receipt_read(
            in_user_id              INT,
            
            in_account_receipt_id   INT,
    
            is_read_status_id       INT,
    
            
            in_payment_channel_id   INT,
            in_amount_receipt       DECIMAL(8,2),    
            in_payment_reference    VARCHAR(32), 
            in_dt_receipt           VARCHAR(20)
            
        )    
        """
        
        params = [
            data.user_id,
            data.receipt_id,
            data.read_status_id,
            
            data.read_status_id     if data.read_status_id is not None and data.read_status_id > 0 else None,
            data.amount_receipt,
            data.payment_reference,
            data.dt_receipt     
        ]
        
        res = self._call_procedure('account_upload_receipt_read', params)
        
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
    
    

    
