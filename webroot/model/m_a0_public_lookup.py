# August 24, 2025
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


"""
/* app_country.flag
bit 0: FLAG_BIT_SELECTABLE
0 = cannot be selected in countries dropdown
1 = Can be selected in Selct Countries drop down; default

bit 1: FLAG_BIT_HAS_ADDRESS_LEVELS
0 = No address levels
1 = Has address level;


*/

"""


class PublicLookup(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        
    
    def get_active_country_list(self):
        sql =   """
                SELECT 
                    id,
                    country_code,
                    name
                FROM app_country
                WHERE flag & 1 > 0
                ORDER BY  name
                """
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_entry = {
                    'id':               row[0], 
                    'country_code':     row[1],
                    'name':             row[2]
                }
                
                result.append(cur_entry)

        
        return result
    
    
    def get_country_details(self, country_id):
        sql =   """
                SELECT 
                    id,
                    country_code,
                    name,
                    report_languages
                FROM app_country
                WHERE id = %s 
                """ %country_id
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
        
        
        if rows is not None:
            
            
            for row in rows:
                cur_entry = {
                    'id':               row[0], 
                    'country_code':     row[1],
                    'name':             row[2]
                }
                
                if row[3] is not None:
                    cur_entry['report_languages'] = row[3]
                
                return cur_entry

        
        return None
    
    
    def get_country_ave_feed_price(self, country_id):
        sql =   """
                SELECT 
                    ave_price_puwt_gestating, 
                    ave_price_puwt_lactating, 
                    ave_price_puwt_booster,   
                    ave_price_puwt_prestarter,
                    ave_price_puwt_starter,   
                    ave_price_puwt_grower,    
                    ave_price_puwt_finisher  

                    
                FROM app_country
                WHERE id = %s 
                """ %country_id
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
        
        
        if rows is not None:
            cur_ave_price_puwt_gestating    = row[0] 
            cur_ave_price_puwt_lactating    = row[1] 
            cur_ave_price_puwt_booster      = row[2]   
            cur_ave_price_puwt_prestarter   = row[3]
            cur_ave_price_puwt_starter      = row[4]   
            cur_ave_price_puwt_grower       = row[5]    
            cur_ave_price_puwt_finisher     = row[6]
            
            
            for row in rows:
                cur_entry = [
                    cur_ave_price_puwt_gestating, 
                    cur_ave_price_puwt_lactating, 
                    cur_ave_price_puwt_booster,   
                    cur_ave_price_puwt_prestarter,
                    cur_ave_price_puwt_starter,   
                    cur_ave_price_puwt_grower,    
                    cur_ave_price_puwt_finisher  
                ]
                
                return cur_entry

        return None
    
    
    
    
    def get_list_feed_type(self):
        
      
        sql =   """
                SELECT 
                    id,
                    name
                    
                FROM feed_type 
                ORDER BY id
                """ 
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
        if rows is not None:
            
            for row in rows:
                
                cur_entry = {
                    'id':                   row[0],
                    'name':                 row[1]
                }

                result.append(cur_entry)
        
        return result
    
    
    
    def get_list_harvest_type(self):
        
      
        sql =   """
                SELECT 
                    id,
                    name
                    
                FROM harvest_type 
                ORDER BY id
                """ 
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
        if rows is not None:
            
            for row in rows:
                
                cur_entry = {
                    'id':                   row[0],
                    'name':                 row[1]
                }

                result.append(cur_entry)
        
        return result
    


    def get_list_of_values(self):
        """
        This will return a dictionry, not a list
        """
        sql =   """
                SELECT 
                    name,
                    val_int
                    
                FROM a01_list_of_values 
                ORDER BY id
                """ 
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = {}
        if rows is not None:
            
            for row in rows:
                result[row[0]] = row[1]
                
        return result
    
        
