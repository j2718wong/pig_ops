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
    
        
