# August 23, 2025
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


FLAG_BIT_NOTES_IS_PIG_HEALTH_ISSUE      = 2

class PigProdNotes(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE pig_prod_notes_add(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            in_sow_boar_id          INT,
            
            in_is_health_issue      INT,
            
            in_date_notes           VARCHAR(10),
            in_notes                VARCHAR(160)
        )  
        """
        
        params = [
            data.user_id,
            
            data.pig_prod_id         if data.pig_prod_id is not None and data.pig_prod_id > 0 else None,
            data.sow_boar_id         if data.sow_boar_id is not None and data.sow_boar_id > 0 else None,
            
            data.is_health_issue,
            
            data.date_notes,
            data.notes
        ]
        
        res = self._call_procedure('pig_prod_notes_add', params)
        
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
                
                'pig_prod_notes': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_prod_notes_update(
            in_user_id              INT,
           
            in_pig_prod_notes_id    INT,
            in_date_notes           VARCHAR(10),
            in_notes                VARCHAR(160)
        )
        """
       
        params = [
            data.user_id,
        
            data.pig_prod_notes_id,
            data.date_notes,
            data.notes
        ]
       
        res = self._call_procedure('pig_prod_notes_update', params)
        
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
                
                'pig_prod_notes': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        pig_prod_notes_id    = data['pig_prod_notes_id']
        
        """
        PROCEDURE pig_prod_notes_delete(
            in_user_id                  INT,
            
            in_pig_prod_notes_id         INT
        )
        """
       
        params = [user_id, pig_prod_notes_id]
       
        res = self._call_procedure('pig_prod_notes_update', params)
        
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
                
                'pig_prod_notes': {
                    'id'
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id = 0, sow_boar_id = 0, 
        inc_deleted = 0, inc_user_audit = 0):
        
        # Note: pig_prod_notes and health_issue is merged;
        # pig_prod_notes.flag.FLAG_BIT_NOTES_IS_PIG_HEALTH_ISSUE
        # is the indicator that it is a pig health issue;
        
        where_clause = ''
        
        if pig_prod_id > 0:
            where_clause = 'WHERE a.pig_prod_id = %s AND a.sow_boar_id IS NULL AND a.notes IS NOT NULL' % pig_prod_id
        
        if sow_boar_id > 0:
            where_clause = 'WHERE a.sow_boar_id = %s AND a.notes IS NOT NULL' % sow_boar_id
        
        if inc_deleted == 0:
            where_clause += ' AND a.flag & 1 = 0'
        
        sql =   """
                SELECT 
                    a.id,
                    b.farm_prod_id,
                    a.date_notes,
                    a.flag,
                    a.notes,
                    
                    a.last_pig_medvac_id,
                    c.acc_medvac_id,
                    d.name AS acc_medvac_name,
                    c.notes AS medvac_notes,
                    
                    
                    e.name_last,
                    e.name_first,
                    a.dt_entry,
                
                    f.name_last,
                    f.name_first,
                    a.dt_last_update
                    
                FROM pig_prod_notes a 
                LEFT OUTER JOIN pig_production b    ON a.pig_prod_id = b.id
                LEFT OUTER JOIN pig_medvac c        ON a.last_pig_medvac_id = c.id
                LEFT OUTER JOIN account_medvac d    ON c.acc_medvac_id = d.id
                LEFT OUTER JOIN user e              ON a.added_by_user_id = e.id
                LEFT OUTER JOIN user f              ON a.last_update_user_id = f.id
                
                %s
                ORDER BY a.date_notes DESC
                """ % where_clause
       
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []

            
        for row in rows:
            cur_id                  = row[0]
            cur_farm_prod_id        = row[1]
            cur_date_notes          = str(row[2])
            cur_flag                = row[3]
            cur_notes               = row[4]
            
            cur_pig_medvac_id       = row[5]
            cur_acc_medvac_id       = row[6]
            cur_acc_medvac_name     = row[7]
            cur_pig_medvac_notes    = row[8]
            
            
            is_health_issue = 0
            if cur_flag & FLAG_BIT_NOTES_IS_PIG_HEALTH_ISSUE > 0:
                is_health_issue = 1
            
            cur_entry = {
                'prod_notes': {
                    'id':               cur_id,
                    'farm_prod_id':     cur_farm_prod_id,
                    'date_notes':       cur_date_notes,
                    'notes':            cur_notes
                },
                
                'added_by':{
                    'name_last':        row[9],
                    'name_first':       row[10],
                    'dt_entry':         str(row[11])
                },
                
                'last_update':{
                    'name_last':        row[12],
                    'name_first':       row[13],
                    'dt_update':        str(row[14]) if row[14] else None
                }
            }
            
            if cur_pig_medvac_id is not None:
                pig_medvac = {
                    'id':               cur_pig_medvac_id,
                    'acc_medvac_name':  cur_acc_medvac_name,
                    'medvac_notes':     cur_pig_medvac_notes
                }
                
                cur_entry['pig_medvac'] = pig_medvac
            
            
            if is_health_issue > 0:
                cur_entry['prod_notes']['is_health_issue'] = 1
            
            
            
            if cur_entry['last_update']['dt_update'] is None:
                del cur_entry['last_update']
                
            
            result.append(cur_entry)
        
        return result
    
    
