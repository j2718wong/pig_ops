# April 11, 2026
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


class Business(BaseModel):
    def __init__(self, model):
        super().__init__(model)



    def get_pricing(self, country_id):
        # Note: The country_id = 0, is the default pricing
        
        if country_id is not None:
            where_clause = 'WHERE a.country_id IN (0, %s)' % country_id
        else:
            where_clause = 'WHERE a.country_id = 0'
        
        sql =   """
                SELECT 
                    a.id,
                    a.country_id,
                    a.flag,
                    b.name,
                    a.currency_code,  
                    a.price_per_head, 
                    a.tax_name_1,     
                    a.tax_name_2,     
                    a.tax_rate_1,     
                    a.tax_rate_2
                    
                FROM biz_pricing a
                LEFT OUTER JOIN app_country b ON a.country_id = b.id
                %s
                """ % where_clause
    
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        
        result = []
            
        for row in rows:
            cur_id                      = row[0]
            cur_country_id              = row[1]
            cur_flag                    = row[2]
            cur_country_name            = row[3]
            cur_currency_code           = row[4]
            cur_price_per_head          = float(row[5])
            
            cur_tax_name_1              = row[6]
            cur_tax_name_2              = row[7]
            cur_tax_rate_1              = float(row[8]) if row[8] is not None else None
            cur_tax_rate_2              = float(row[9]) if row[9] is not None else None
            
            
            
            cur_entry = {
                'pricing': {
                    'id':               cur_id,
                    'country_id':       cur_country_id,
                    'country_name':     cur_country_name,
                    'flag':             cur_flag,
                    'currency_code':    cur_currency_code,
                    'price_per_head':   cur_price_per_head
                }
                
            }
        
            if cur_tax_name_1 is not None:
                tax_1 = {
                    'name':             cur_tax_name_1,
                    'rate':             cur_tax_rate_1
                }
                
                cur_entry['tax_1']      = tax_1
        
        
            if cur_tax_name_2 is not None:
                tax_2 = {
                    'name':             cur_tax_name_2,
                    'rate':             cur_tax_rate_2
                }
                
                cur_entry['tax_2']      = tax_2
                
            result.append(cur_entry)
    
        return result
    
   
    def get_payment_channel(self):
        
        if country_id is not None:
            where_clause = 'WHERE a.country_id IN (0, %s)' % country_id
        else:
            where_clause = 'WHERE a.country_id = 0'
        
        sql =   """
                SELECT 
                    a.id,
                    a.country_id,
                    a.flag,
                    b.name,
                    a.currency_code,  
                    a.price_per_head, 
                    a.tax_name_1,     
                    a.tax_name_2,     
                    a.tax_rate_1,     
                    a.tax_rate_2
                    
                FROM biz_pricing a
                LEFT OUTER JOIN app_country b ON a.country_id = b.id
                %s
                """ % where_clause
    
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        
        result = []
            
        for row in rows:
            cur_id                      = row[0]
            cur_country_id              = row[1]
            cur_flag                    = row[2]
            cur_country_name            = row[3]
            cur_currency_code           = row[4]
            cur_price_per_head          = float(row[5])
            
            cur_tax_name_1              = row[6]
            cur_tax_name_2              = row[7]
            cur_tax_rate_1              = float(row[8]) if row[8] is not None else None
            cur_tax_rate_2              = float(row[9]) if row[9] is not None else None
            
            
            
            cur_entry = {
                'pricing': {
                    'id':               cur_id,
                    'country_id':       cur_country_id,
                    'country_name':     cur_country_name,
                    'flag':             cur_flag,
                    'currency_code':    cur_currency_code,
                    'price_per_head':   cur_price_per_head
                }
                
            }
        
            if cur_tax_name_1 is not None:
                tax_1 = {
                    'name':             cur_tax_name_1,
                    'rate':             cur_tax_rate_1
                }
                
                cur_entry['tax_1']      = tax_1
        
        
            if cur_tax_name_2 is not None:
                tax_2 = {
                    'name':             cur_tax_name_2,
                    'rate':             cur_tax_rate_2
                }
                
                cur_entry['tax_2']      = tax_2
                
            result.append(cur_entry)
    
        return result
    
   
