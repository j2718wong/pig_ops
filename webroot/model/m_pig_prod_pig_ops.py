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


"""
/* account_pig_ops.flag bits*/
DECLARE FLAG_BIT_ACCOUNT_PIG_OPS_IS_DELETED     INT             DEFAULT 1;
DECLARE FLAG_BIT_ACCOUNT_PIG_OPS_IS_MEDVAC      INT             DEFAULT 2;
"""

FLAG_BIT_ACCOUNT_PIG_OPS_IS_MEDVAC      = 2


class PigProdPigOps(BaseModel):
    def __init__(self, model):
        super().__init__(model)

    
    def update(self, data = None):
        """
        PROCEDURE pig_prod_pig_ops_update(
            in_user_id                  INT,
           
            in_pig_prod_pig_ops_id      INT,
            in_staff_id                 INT,
            in_done_by_user             INT,
            
            in_date                     VARCHAR(10),
            in_notes                    VARCHAR(160)
        )
        """
        
        params = [
            data.user_id,
            data.pig_prod_pig_ops_id,
            data.staff_id               if data.staff_id is not None and data.staff_id > 0 else None,
            data.done_by_user,
            data.date,
            data.notes                  if data.notes and data.notes.strip() else None
        ]

        res = self._call_procedure('pig_prod_pig_ops_update', params)
        
        if res is None:
            return None
        
        
        row = res[0]
        

        if row is not None:
            added_new_staff = row[4]
            pig_farm_id     = row[5]
            
            cur_entry = {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod_pig_ops': {
                    'id':               row[3]
                }
            }
            
            if added_new_staff > 0:
                cur_entry['added_new_staff']= 1
                cur_entry['pig_farm_id']    = pig_farm_id  
        
            return cur_entry
        
        return None
    
    
    def update_with_medvac(self, data = None):
        """
        PROCEDURE pig_prod_pig_ops_medvac_update(
            in_user_id              INT,
           
            in_pig_prod_pig_ops_id  INT,
            in_staff_id             INT,
            in_done_by_user         INT,
            
            in_medvac_brand_id      INT,
            in_medvac_type_id       INT,
            in_acc_medvac_id        INT,
            
            in_date                 VARCHAR(10),
            in_notes                VARCHAR(160)
        )
        """
        
        params = [
            data.user_id,
            
            data.pig_prod_pig_ops_id,
            data.staff_id               if data.staff_id is not None and data.staff_id > 0 else None,
            data.done_by_user,
            
            data.medvac_brand_id,
            data.medvac_type_id,
            data.acc_medvac_id,
            
            data.date,
            data.notes                  if data.notes and data.notes.strip() else None
        ]

        res = self._call_procedure('pig_prod_pig_ops_medvac_update', params)
        
        
        if res is None:
            return None
        
        
        row = res[0]
        

        if row is not None:
            added_new_staff = row[4]
            pig_farm_id     = row[5]
            
            cur_entry = {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod_pig_ops': {
                    'id':               row[3]
                }
            }
            
            if added_new_staff > 0:
                cur_entry['added_new_staff']= 1
                cur_entry['pig_farm_id']    = pig_farm_id  
        
            return cur_entry
        
        return None
    
    
    def get_list(self, operation_type, pig_prod_id = None,  sow_boar_id = None,
            inc_user_audit = 0, order_by = 0):
        
        """
        Paremeters
        ----------
            
        operation_type : PIG_OPERATION_TYPE constant
            
        pig_prod_id : int
            pig_production id
        
        sow_boar_id : int
            
        
        order_by : int
            0 = ORDER BY num_days_since ASC
            1 = ORDER BY num_days_since DESC
        """
        
        if operation_type == PIG_OPERATION_TYPE_LACTATING_COMBINED:
            filter_clause = 'a.operation_type IN (2,3)'
        else:
            filter_clause = 'a.operation_type = %s ' % operation_type
        
        if pig_prod_id is not None:
            where_clause =  'WHERE a.pig_prod_id = %s AND %s' %(pig_prod_id, filter_clause)
        else:
            where_clause =  'WHERE a.sow_boar_id = %s AND %s' %(sow_boar_id, filter_clause)
        
        
        order_clause = ''
        if order_by > 0:
            order_clause += ' DESC'
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.operation_type,
                        a.date_target,
                        a.date_actual,
                        a.dt_entry,
                        
                        a.account_pig_ops_id,
                        b.name,
                        b.num_days_since,
                        b.flag AS account_pig_ops_flag,
                        b.description,
                        
                        a.pig_medvac_id,
                        c.medvac_brand_id,
                        d.name AS medvac_brand,
                        
                        c.medvac_type_id,
                        e.name AS medvac_type,
                        
                        c.acc_medvac_id,
                        f.name AS medvac_name,
                        
                        a.staff_id,
                        g.name  AS staff_name,
                        
                        a.notes_id,
                        h.notes
                        
                        
                    FROM pig_prod_pig_ops a 
                    LEFT OUTER JOIN account_pig_ops b   ON a.account_pig_ops_id = b.id
                    
                    LEFT OUTER JOIN pig_medvac c        ON a.pig_medvac_id = c.id
                    LEFT OUTER JOIN medvac_brand d      ON c.medvac_brand_id = d.id
                    LEFT OUTER JOIN medvac_type e       ON c.medvac_type_id = e.id
                    LEFT OUTER JOIN account_medvac f    ON c.acc_medvac_id = f.id
                    
                    LEFT OUTER JOIN pig_farm_staff g    ON a.staff_id = g.id
                    LEFT OUTER JOIN pig_prod_notes h    ON a.notes_id = h.id
                    %s
                    ORDER BY b.num_days_since %s
                    """ % (where_clause, order_clause)
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.operation_type,
                        a.date_target,
                        a.date_actual,
                        a.dt_entry,
                        
                        a.account_pig_ops_id,
                        b.name,
                        b.num_days_since,
                        b.flag AS account_pig_ops_flag,
                        b.description,
                        
                        a.pig_medvac_id,
                        c.medvac_brand_id,
                        d.name AS medvac_brand,
                        
                        c.medvac_type_id,
                        e.name AS medvac_type,
                        
                        c.acc_medvac_id,
                        f.name AS medvac_name,
                        
                        a.staff_id,
                        g.name  AS staff_name,
                        
                        a.notes_id,
                        h.notes,
                        
                        i.name_last,
                        i.name_first,
                        a.dt_last_update
                        
                    FROM pig_prod_pig_ops a 
                    LEFT OUTER JOIN account_pig_ops b   ON a.account_pig_ops_id = b.id
                    
                    LEFT OUTER JOIN pig_medvac c        ON a.pig_medvac_id = c.id
                    LEFT OUTER JOIN medvac_brand d      ON c.medvac_brand_id = d.id
                    LEFT OUTER JOIN medvac_type e       ON c.medvac_type_id = e.id
                    LEFT OUTER JOIN account_medvac f    ON c.acc_medvac_id = f.id
                    
                    LEFT OUTER JOIN pig_farm_staff g    ON a.staff_id = g.id
                    LEFT OUTER JOIN pig_prod_notes h    ON a.notes_id = h.id
                    
                    LEFT OUTER JOIN user i              ON a.last_update_user_id = i.id
                    
                    %s
                    ORDER BY b.num_days_since %s
                    """ % (where_clause, order_clause)
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
            
        
        result = []
            
        for row in rows:
            is_medvac  = 0
            cur_acc_pig_ops_flag = row[8]
            
            
            if cur_acc_pig_ops_flag & FLAG_BIT_ACCOUNT_PIG_OPS_IS_MEDVAC > 0:
                is_medvac  = 1
                    
            
            cur_entry = {
                
                
                'pig_prod_pig_ops': {
                    'id':               row[0],
                    'operation_type':   row[1],
                    'date_target':      str(row[2]),
                    'date_actual':      str(row[3]) if row[3] else None,
                    'dt_entry':         str(row[4])
                },
                
                'account_pig_ops':{
                    'id':               row[5],
                    'name':             row[6],
                    'num_days_since':   row[7],
                    'is_medvac':        is_medvac,
                    'description':      row[9]
                },
                
                
                'pig_medvac':{
                    'id':               row[10],
                    
                    'brand': {
                        'id':           row[11],
                        'name':         row[12]
                    },
                    
                    'type': {
                        'id':           row[13],
                        'name':         row[14]
                    },
                    
                    'acc_medvac':{
                        'id':           row[15],
                        'name':         row[16]
                    }
                
                },
                
                
                'staff': {
                    'id':               row[17],
                    'name':             row[18]
                },
                
                'notes': {
                    'id':               row[19],
                    'notes':            row[20]
                }
            }
            
            
            if inc_user_audit > 0:
                
                if row[21] is not None:
                    
                    last_update = {
                        'name_last':        row[21],
                        'name_first':       row[22],
                        'dt_update':        str(row[23]) if row[23] else None
                    }
            
                    cur_entry['last_update'] = last_update
            
            
            if cur_entry['pig_medvac']['id'] is None:
                del cur_entry['pig_medvac']
            
                
            result.append(cur_entry)
    
        return result
    
    
    def get_entry(self, pig_prod_pig_ops_id, inc_user_audit = 0):
        
        """
        Paremeters
        ----------
        Will just return one entry 
        
        """
     
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.operation_type,
                        a.date_target,
                        a.date_actual,
                        a.dt_entry,
                        
                        a.account_pig_ops_id,
                        b.name,
                        b.num_days_since,
                        b.flag AS account_pig_ops_flag,
                        b.description,
                        
                        a.pig_medvac_id,
                        c.medvac_brand_id,
                        d.name AS medvac_brand,
                        
                        c.medvac_type_id,
                        e.name AS medvac_type,
                        
                        c.acc_medvac_id,
                        f.name AS medvac_name,
                        
                        a.staff_id,
                        g.name  AS staff_name,
                        
                        a.notes_id,
                        h.notes
                        
                        
                    FROM pig_prod_pig_ops a 
                    LEFT OUTER JOIN account_pig_ops b   ON a.account_pig_ops_id = b.id
                    
                    LEFT OUTER JOIN pig_medvac c        ON a.pig_medvac_id = c.id
                    LEFT OUTER JOIN medvac_brand d      ON c.medvac_brand_id = d.id
                    LEFT OUTER JOIN medvac_type e       ON c.medvac_type_id = e.id
                    LEFT OUTER JOIN account_medvac f    ON c.acc_medvac_id = f.id
                    
                    LEFT OUTER JOIN pig_farm_staff g    ON a.staff_id = g.id
                    LEFT OUTER JOIN pig_prod_notes h    ON a.notes_id = h.id
                    WHERE a.id = %s
                    """ % (pig_prod_pig_ops_id)
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.operation_type,
                        a.date_target,
                        a.date_actual,
                        a.dt_entry,
                        
                        a.account_pig_ops_id,
                        b.name,
                        b.num_days_since,
                        b.flag AS account_pig_ops_flag,
                        b.description,
                        
                        a.pig_medvac_id,
                        c.medvac_brand_id,
                        d.name AS medvac_brand,
                        
                        c.medvac_type_id,
                        e.name AS medvac_type,
                        
                        c.acc_medvac_id,
                        f.name AS medvac_name,
                        
                        a.staff_id,
                        g.name  AS staff_name,
                        
                        a.notes_id,
                        h.notes,
                        
                        i.name_last,
                        i.name_first,
                        a.dt_last_update
                        
                    FROM pig_prod_pig_ops a 
                    LEFT OUTER JOIN account_pig_ops b   ON a.account_pig_ops_id = b.id
                    
                    LEFT OUTER JOIN pig_medvac c        ON a.pig_medvac_id = c.id
                    LEFT OUTER JOIN medvac_brand d      ON c.medvac_brand_id = d.id
                    LEFT OUTER JOIN medvac_type e       ON c.medvac_type_id = e.id
                    LEFT OUTER JOIN account_medvac f    ON c.acc_medvac_id = f.id
                    
                    LEFT OUTER JOIN pig_farm_staff g    ON a.staff_id = g.id
                    LEFT OUTER JOIN pig_prod_notes h    ON a.notes_id = h.id
                    
                    LEFT OUTER JOIN user i              ON a.last_update_user_id = i.id
                    
                    WHERE a.id = %s
                    """ % (pig_prod_pig_ops_id)
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
            
        
        result = []
            
        for row in rows:
            is_medvac  = 0
            cur_acc_pig_ops_flag = row[8]
            
            
            if cur_acc_pig_ops_flag & FLAG_BIT_ACCOUNT_PIG_OPS_IS_MEDVAC > 0:
                is_medvac  = 1
                    
            
            cur_entry = {
                
                
                'pig_prod_pig_ops': {
                    'id':               row[0],
                    'operation_type':   row[1],
                    'date_target':      str(row[2]),
                    'date_actual':      str(row[3]) if row[3] else None,
                    'dt_entry':         str(row[4])
                },
                
                'account_pig_ops':{
                    'id':               row[5],
                    'name':             row[6],
                    'num_days_since':   row[7],
                    'is_medvac':        is_medvac,
                    'description':      row[9]
                },
                
                
                'pig_medvac':{
                    'id':               row[10],
                    
                    'brand': {
                        'id':           row[11],
                        'name':         row[12]
                    },
                    
                    'type': {
                        'id':           row[13],
                        'name':         row[14]
                    },
                    
                    'acc_medvac':{
                        'id':           row[15],
                        'name':         row[16]
                    }
                
                },
                
                
                'staff': {
                    'id':               row[17],
                    'name':             row[18]
                },
                
                'notes': {
                    'id':               row[19],
                    'notes':            row[20]
                }
            }
            
            
            if inc_user_audit > 0:
                
                if row[21] is not None:
                    
                    last_update = {
                        'name_last':        row[21],
                        'name_first':       row[22],
                        'dt_update':        str(row[23]) if row[23] else None
                    }
            
                    cur_entry['last_update'] = last_update
            
            
            if cur_entry['pig_medvac']['id'] is None:
                del cur_entry['pig_medvac']
            
                
            result.append(cur_entry)
    
        return result
    
    
    def get_list_medvac_pig_ops_before_date_target(self, account_id):
        """
        Get gestating MedVac operations scheduled for 
        TODAY + account.num_days_prep_lead  pig_ops.date_target.
        """
        
        sql = """
            SELECT 
                a.id,
                a.date_target,
                
                a.pig_prod_id,
                b.farm_prod_id AS pig_production_pid,
                b.sow_id,
                b.date_insemination,
                
                c.name AS sow_name,
                c.number AS sow_number,
                
                d.name AS pig_ops_name,
                d.num_days_since AS pig_ops_num_days,
                d.description AS pig_ops_description
                
            FROM pig_prod_pig_ops a
            INNER JOIN pig_production b ON a.pig_prod_id = b.id
            INNER JOIN sow_boar c ON b.sow_id = c.id
            INNER JOIN account_pig_ops d ON a.account_pig_ops_id = d.id
            INNER JOIN account e ON a.account_id = e.id

            WHERE a.account_id = %s
                AND a.operation_type = 1
                AND a.date_actual IS NULL
                AND (d.flag & 2) > 0
                AND b.prod_status_id = 1 
                AND DATEDIFF(a.date_target, CURDATE()) = e.num_days_prep_lead
        """ % account_id
        
        
        rows = self._execute_query(sql)
        
        if rows is None or len(rows) == 0:
            return []
        
        
        result = []
        
        for row in rows:
            cur_id                          = row[0]
            cur_date_target                 = str(row[1]) if row[1] else None
            
            cur_pig_prod_id                 = row[2]
            cur_pig_prod_pid                = row[3]
            cur_pig_prod_sow_id             = row[4]
            cur_pig_prod_date_insemination  = str(row[5]) if row[5] else None
            
            cur_sow_name                    = row[6] if row[6] else ''
            cur_sow_number                  = row[7] if row[7] else ''
            
            cur_pig_ops_name                = row[8] if row[8] else ''
            cur_pig_ops_num_days_since      = row[9] if row[9] else 0
            cur_pig_ops_description         = row[10] if row[10] else ''
            
            cur_entry = {
                'pig_prod_pig_ops': {
                    'id':                   cur_id,
                    'date_target':          cur_date_target,
                    'pig_ops': {
                        'name':             cur_pig_ops_name,
                        'num_days_since':   cur_pig_ops_num_days_since,
                        'description':      cur_pig_ops_description
                    }
                },
                
                'pig_production': {
                    'id':                   cur_pig_prod_id,
                    'farm_prod_id':         cur_pig_prod_pid,
                    'date_insem':           cur_pig_prod_date_insemination,
                    'sow': {
                        'id':               cur_pig_prod_sow_id,
                        'name':             cur_sow_name,
                        'number':           cur_sow_number
                    }
                }
            }
            
            result.append(cur_entry)
        
        return result
        
    
    
    
    
