# January 20, 2026
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

        

class SowBoarMate(BaseModel):
    def __init__(self, model):
        super().__init__(model)

    
    def add_boar_external_mate(self, data = None):
        """
        Adding an external mate for a farm owned boar  to an external sow.
        This will not  create a pig_production entry.
        
        This should not be used when a farm owned sow is mated to an external boar.
        
        PROCEDURE boar_external_mate_add(
            in_user_id              INT,
            
            in_boar_id              INT,
            in_boar_customer_id     INT,    /* This is mapped to account_pig_buyer*/
            
            in_customer_sow_name    VARCHAR(50),
            
            in_date_mate            VARCHAR(10),
            in_date_expected_birth  VARCHAR(10),
            in_date_expected_payment VARCHAR(10),
    
            in_notes                VARCHAR(160)
        )    
        """
        
        params = [
            data.user_id,
            data.boar_id,
            data.boar_customer_id,
            
            data.customer_sow_name      if data.customer_sow_name and len(data.customer_sow_name) > 0 else None,
            
            data.date_mate,
            data.date_expected_birth    if data.date_expected_birth and len(data.date_expected_birth) > 0 else None,
            data.date_expected_payment  if data.date_expected_payment and len(data.date_expected_payment) > 0 else None,
            
            data.notes                  if data.notes and len(data.notes) > 0 else None
        ]
        
        res =  self._call_procedure('boar_external_mate_add', params)
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
                
                'sow_boar_mate': {
                    'id':               row[3]
                }
            }

        return None

    
    def update_boar_external_mate(self, data=None):
        """
        PROCEDURE boar_external_mate_update(
            in_user_id              INT,
            in_sow_boar_mate_id     INT,
            
            in_boar_customer_id     INT,    /* This is mapped to account_pig_buyer*/
            
            in_customer_sow_name    VARCHAR(50),
            
            in_date_mate            VARCHAR(10),
            in_date_expected_birth  VARCHAR(10),
            in_date_expected_payment VARCHAR(10),
            
            in_notes                VARCHAR(160)
        )    
        """
        
        params = [
            data.user_id,
            data.sow_boar_mate_id,
            data.boar_customer_id,
            data.customer_sow_name if data.customer_sow_name and data.customer_sow_name.strip() else None,
            data.date_mate,
            data.date_expected_birth if data.date_expected_birth and data.date_expected_birth.strip() else None,
            data.date_expected_payment if data.date_expected_payment and data.date_expected_payment.strip() else None,
            data.notes if data.notes and data.notes.strip() else None
        ]
        
        res = self._call_procedure('boar_external_mate_update', params)
        
        if res is None:
            return None
        
        
        row = res[0]
            
            
        if row is not None:    
            return {
                'result': {
                    'num': row[0],
                    'code': row[1],
                    'desc': row[2]
                }
            }
        
        return None

     
    def get_list(self, sow_boar_id = 0, is_external: int = 0, pig_farm_id = 0):
        """
        Will get sow_boar_mate list.
        
        Parameters
        ----------
        
        sow_boar_id : int
            will get all sow_boar_mate data of the either sow or boar
        
        is_external: int
            if is_external 0, will return mated farm owned sows 
            if is_external > 0, will return mated external sows(not farm owned)
        
        pig_farm_id: int
            if pig_farm_id > 0: 
                will return boar external mates for all boars;
                Note: this includes already disposed boars. 
            
        Returns
        -------
        list of dictionary
        """
        
        # Build query based on parameters
        if pig_farm_id == 0:
            
            if is_external == 0:
                # Internal: farm owned sows
                sql = """
                    SELECT 
                        a.id,
                        a.pig_prod_id,
                        b.farm_prod_id,
                        
                        a.mate_sow_boar_id,
                        a.date_mate,
                        
                        c.name,
                        c.number
                        
                    FROM sow_boar_mate a
                    LEFT OUTER JOIN pig_production b    ON a.pig_prod_id = b.id 
                    LEFT OUTER JOIN sow_boar c          ON a.mate_sow_boar_id = c.id
                    WHERE a.sow_boar_id = %s AND a.boar_customer_id IS NULL
                    ORDER BY a.date_mate DESC
                """ % sow_boar_id
                
                
            else:
                # External: mated external sows
                sql = """
                    SELECT 
                        a.id,
                        
                        a.date_mate,
                        a.date_expected_birth,
                        a.date_expected_payment,
                        
                        a.boar_customer_id,
                        b.name AS boar_customer_name,
                        
                        a.customer_sow_name,
                        
                        c.notes
                        
                    FROM sow_boar_mate a
                    LEFT OUTER JOIN account_pig_buyer b     ON a.boar_customer_id = b.id
                    LEFT OUTER JOIN pig_prod_notes c        ON a.notes_id = c.id
                    WHERE a.sow_boar_id = %s AND a.boar_customer_id IS NOT NULL
                    ORDER BY a.date_mate DESC
                """ % sow_boar_id 
                
        
        else:
            # Get boar external mates for all boars in a farm
            sql = """
                SELECT 
                    a.id,
                    
                    a.sow_boar_id,
                    b.name      AS boar_name,
                    b.number    AS boar_number,
                    
                    a.date_mate,
                    a.date_expected_birth,
                    a.date_expected_payment,
                    
                    a.boar_customer_id,
                    c.name AS boar_customer_name,
                    
                    a.customer_sow_name,
                    
                    d.notes
                    
                FROM sow_boar_mate a
                LEFT OUTER JOIN sow_boar b              ON a.sow_boar_id = b.id
                LEFT OUTER JOIN account_pig_buyer c     ON a.boar_customer_id = c.id
                LEFT OUTER JOIN pig_prod_notes d        ON a.notes_id = d.id
                WHERE a.pig_farm_id = %s AND a.boar_customer_id IS NOT NULL
                ORDER BY a.date_mate DESC
            """ % pig_farm_id
            
        
        # Execute query using BaseModel method
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        result = []
        
        for row in rows:
            
            if pig_farm_id == 0:
                
                if is_external == 0:
                    # Internal mates - column mapping
                    cur_id                       = row[0]
                    cur_pig_prod_id              = row[1]
                    cur_farm_prod_id             = row[2]
                    
                    cur_mate_sow_boar_id         = row[3]
                    cur_date_mate                = row[4]
                    
                    cur_mate_sow_boar_name       = row[5]
                    cur_mate_sow_boar_number     = row[6]
                    
                    cur_entry = {
                        'id':               cur_id,
                        'pig_prod_id':      cur_pig_prod_id,
                        'farm_prod_id':     cur_farm_prod_id,
                        'date_mate':        str(cur_date_mate) if cur_date_mate else None,
                        'mate_sow_boar': {
                            'id':           cur_mate_sow_boar_id,
                            'name':         cur_mate_sow_boar_name,
                            'number':       cur_mate_sow_boar_number
                        }
                    }
                    
                else:
                    # External mates - column mapping
                    cur_id                       = row[0]
                    
                    cur_date_mate                = row[1]
                    cur_date_expected_birth      = row[2]
                    cur_date_expected_payment    = row[3]
                    
                    cur_boar_customer_id         = row[4]
                    cur_boar_customer_name       = row[5]
                    
                    cur_customer_sow_name        = row[6]
                    
                    cur_notes                    = row[7]
                    
                    cur_entry = {
                        'id':                       cur_id,
                        'date_mate':                str(cur_date_mate) if cur_date_mate else None,
                        'date_expected_birth':      str(cur_date_expected_birth) if cur_date_expected_birth else None,
                        'date_expected_payment':    str(cur_date_expected_payment) if cur_date_expected_payment else None,
                        'boar_customer': {
                            'id':                   cur_boar_customer_id,
                            'name':                 cur_boar_customer_name,
                            'sow_name':             cur_customer_sow_name
                        },
                        'notes':                    cur_notes
                    }
            
            else:
                # Farm-level external mates - column mapping
                cur_id                           = row[0]
                
                cur_sow_boar_id                  = row[1]
                cur_boar_name                    = row[2]
                cur_boar_number                  = row[3]
                
                cur_date_mate                    = row[4]
                cur_date_expected_birth          = row[5]
                cur_date_expected_payment        = row[6]
                
                cur_boar_customer_id             = row[7]
                cur_boar_customer_name           = row[8]
                
                cur_customer_sow_name            = row[9]
                
                cur_notes                        = row[10]
                
                cur_entry = {
                    'id':                           cur_id,
                    
                    'sow_boar': {
                        'id':                       cur_sow_boar_id,
                        'name':                     cur_boar_name,
                        'number':                   cur_boar_number
                    },
                    
                    'date_mate':                    str(cur_date_mate) if cur_date_mate else None,
                    'date_expected_birth':          str(cur_date_expected_birth) if cur_date_expected_birth else None,
                    'date_expected_payment':        str(cur_date_expected_payment) if cur_date_expected_payment else None,
                    
                    'boar_customer': {
                        'id':                       cur_boar_customer_id,
                        'name':                     cur_boar_customer_name
                    },
                    
                    'customer_sow_name':            cur_customer_sow_name,
                    'notes':                        cur_notes
                }
            
            result.append(cur_entry)
        
        return result
