# May 15, 2026
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



class Admin(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def get_payment_channels_list(self, country_id = 1):
      
        sql =   """
                SELECT 
                    id,
                    channel_type,
                    channel_name,
                    account_name,
                    account_number
                    
                FROM biz_payment_channel 
                """ 
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
        if rows is not None:
            
            for row in rows:
                
                cur_entry = {
                    'id':                   row[0],
                    'channel_type':         row[1],
                    'channel_name':         row[2],
                    'account_name':         row[3],
                    'account_number':       row[4]
                }

                result.append(cur_entry)
        
        return result
    


    def get_uploaded_receipts_for_reading(self, user_id_data_entry = 0, 
            number_last_read = 10):
        
        sql = """
            SELECT * FROM (
                -- Query 1: Unread receipts (status_id = 0)
                SELECT
                    id,
                    status_id,
                    flag,
                    file_path,
                    payment_channel_id,
                    
                    amount_receipt,
                    payment_reference,
                    dt_receipt,
                    dt_input_data_entry
                FROM account_upload_receipt
                WHERE status_id = 0
                
                UNION ALL
                
                -- Query 2: Read receipts by this user (limited)
                SELECT
                    id,
                    status_id,
                    flag,
                    file_path,
                    payment_channel_id,
                    
                    amount_receipt,
                    payment_reference,
                    dt_receipt,
                    dt_input_data_entry
                FROM account_upload_receipt
                WHERE data_entry_user_id = %s
                ORDER BY id DESC
                LIMIT %s
            ) AS combined
            ORDER BY id DESC
        """ %(user_id_data_entry, number_last_read)
        
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
        
        result = []
            
        for row in rows:
            cur_id                  = row[0]
            cur_status_id           = row[1]
            cur_flag                = row[2]
            cur_file_path           = row[3]
            cur_payment_channel_id  = row[4]
            
            cur_amount_receipt      = float(row[5]) if row[5] else None
            cur_payment_reference   = row[6]
            cur_dt_receipt          = str(row[7])   if row[7] else None 
            cur_dt_input_data_entry = str(row[8])
                
            cur_entry = {
                'id':                    cur_id,                             
                'status_id':             cur_status_id,          
                'flag':                  cur_flag,               
                'file_path':             cur_file_path,          
                'payment_channel_id':    cur_payment_channel_id, 
                                         
                'amount_receipt':        cur_amount_receipt,     
                'payment_reference':     cur_payment_reference,  
                'dt_receipt':            cur_dt_receipt,         
                'dt_input_data_entry':   cur_dt_input_data_entry
                
            }
            
            
            return cur_entry
            
        return None
    
    

    
