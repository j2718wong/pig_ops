# January 8, 2026
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


class PigMedVac(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE pig_medvac_add(
            in_user_id              INT,
            
            in_sow_boar_id          INT,
            in_pig_prod_id          INT,
            in_pig_prod_pig_ops_id  INT,
            in_health_issue_id      INT,
    
            
            in_date_medvac          VARCHAR(10),
            in_medvac_brand_id      INT,
            in_medvac_type_id       INT,
            in_acc_medvac_id        INT,
            
            in_staff_id             INT,
            in_done_by_user         INT,
            in_notes                VARCHAR(160)
        )    
        """
        
        params = [
            data.user_id,
            
            data.sow_boar_id            if data.sow_boar_id is not None and data.sow_boar_id > 0 else None,
            data.pig_prod_id            if data.pig_prod_id is not None and data.pig_prod_id > 0 else None,
            data.pig_prod_pig_ops_id    if data.pig_prod_pig_ops_id is not None and data.pig_prod_pig_ops_id > 0 else None,
            data.health_issue_id        if data.health_issue_id is not None and data.health_issue_id > 0 else None,
            
            data.date_medvac,
            data.medvac_brand_id        if data.medvac_brand_id is not None and data.medvac_brand_id > 0 else None,
            data.medvac_type_id         if data.medvac_type_id is not None and data.medvac_type_id > 0 else None,
            data.acc_medvac_id,
            
            data.staff_id,
            data.done_by_user,
            data.notes                  if data.notes and data.notes.strip() else None
        ]

        res = self._call_procedure('pig_medvac_add', params)
        
        if res is None:
            return None
        
        
        row = res[0]


        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2]
                },
                
                'pig_medvac': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_medvac_update(
            in_user_id              INT,
            in_pig_medvac_id        INT,

            in_date_medvac          VARCHAR(10),
            in_medvac_brand_id      INT,
            in_medvac_type_id       INT,
            in_acc_medvac_id        INT,
            in_staff_id             INT,
            
            in_notes                VARCHAR(160)
        )    
        """
        
        params = [
            data.user_id,
            data.pig_medvac_id,
            
            data.date_medvac,
            data.medvac_brand_id,
            data.medvac_type_id     if data.medvac_type_id is not None and data.medvac_type_id > 0 else None,
            data.acc_medvac_id,
            data.staff_id,
            
            data.notes if data.notes and data.notes.strip() else None
        ]

        res = self._call_procedure('pig_medvac_update', params)
        
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
        pig_race_line_id    = data['pig_race_line_id']
        
        """
        PROCEDURE pig_race_line_delete(
            in_user_id                  INT,
            
            in_pig_race_line_id         INT
        )
        """
        
        params = [
            user_id,
            pig_race_line_id
        ]
        
        res = self._call_procedure('pig_race_line_delete', params)
        
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
    
    
    def get_list(self, sow_boar_id = 0, pig_prod_id = 0, 
            inc_deleted = 0, inc_user_audit = 0):
        
        if sow_boar_id > 0:
            if inc_deleted > 0:
                where_clause = 'WHERE a.sow_boar_id = %s' % sow_boar_id 
            else:
                where_clause = 'WHERE a.sow_boar_id = %s AND (a.flag & 1) = 0' % sow_boar_id 
        
        if pig_prod_id > 0:
            if inc_deleted > 0:
                where_clause = 'WHERE a.pig_prod_id = %s' % pig_prod_id 
            else:
                where_clause = 'WHERE a.pig_prod_id = %s AND (a.flag & 1) = 0' % pig_prod_id 
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.pig_prod_pig_ops_id,
                        a.health_issue_id,
                        
                        a.date_medvac,
                        
                        a.medvac_brand_id,
                        b.name AS medvac_brand,
                        
                        a.medvac_type_id,
                        c.name AS medvac_type,
                        
                        a.acc_medvac_id,
                        d.name AS medvac_name,
                        
                        a.staff_id,
                        e.name AS staff_name,
                        
                        a.notes
                    FROM pig_medvac a 
                    LEFT OUTER JOIN medvac_brand b  ON a.medvac_brand_id = b.id
                    LEFT OUTER JOIN medvac_type c   ON a.medvac_type_id = c.id
                    LEFT OUTER JOIN account_medvac d ON a.acc_medvac_id = d.id
                    LEFT OUTER JOIN pig_farm_staff e ON a.staff_id = e.id
                    %s
                    ORDER BY a.date_medvac DESC
                    """ % where_clause
        else:
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.pig_prod_pig_ops_id,
                        a.health_issue_id,
                        
                        a.date_medvac,
                        
                        a.medvac_brand_id,
                        b.name AS medvac_brand,
                        
                        a.medvac_type_id,
                        c.name AS medvac_type,
                        
                        a.acc_medvac_id,
                        d.name AS medvac_name,
                        
                        a.staff_id,
                        e.name AS staff_name,
                        
                        a.notes,
                        
                        f.name_last,
                        f.name_first,
                        a.dt_entry,
                        
                        g.name_last,
                        g.name_first,
                        a.dt_last_update
                        
                    FROM pig_medvac a 
                    LEFT OUTER JOIN medvac_brand b  ON a.medvac_brand_id = b.id
                    LEFT OUTER JOIN medvac_type c   ON a.medvac_type_id = c.id
                    LEFT OUTER JOIN account_medvac d ON a.acc_medvac_id = d.id
                    LEFT OUTER JOIN pig_farm_staff e ON a.staff_id = e.id
                    LEFT OUTER JOIN user f          ON a.added_by_user_id = f.id
                    LEFT OUTER JOIN user g          ON a.last_update_user_id = g.id
                    
                    %s
                    ORDER BY a.date_medvac DESC
                    """ % where_clause
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
            
        for row in rows:
            if inc_user_audit == 0:
                cur_entry = {
                    'medvac': {
                        'id':               row[0],
                        
                        'prod_pig_ops_id':  row[1],
                        'health_issue_id':  row[2],
                        
                        'date_medvac':      str(row[3]),
                    
                        'brand':{
                            'id':           row[4],
                            'name':         row[5]
                        },
                        
                        'type':{
                            'id':           row[6],
                            'name':         row[7]
                        },
                        
                        'acc_medvac':{
                            'id':           row[8],
                            'name':         row[9]
                        },
                        
                        'staff':{
                            'id':           row[10],
                            'name':         row[11]
                        },
                        
                        'notes':            row[12]
                    }
                }
                
            else:
                cur_entry = {
                    'medvac': {
                        'id':               row[0],
                        
                        'prod_pig_ops_id':  row[1],
                        'health_issue_id':  row[2],
                        
                        
                        'date_medvac':      str(row[3]),
                    
                        'brand':{
                            'id':           row[4],
                            'name':         row[5]
                        },
                        
                        'type':{
                            'id':           row[6],
                            'name':         row[7]
                        },
                        
                        'acc_medvac':{
                            'id':           row[8],
                            'name':         row[9]
                        },
                        
                        'staff':{
                            'id':           row[10],
                            'name':         row[11]
                        },
                        
                        'notes':            row[12]
                    },
                    
                    'added_by': {
                        'name_last':        row[13],
                        'name_first':       row[14],
                        'dt_entry':         row[15]
                    },
                    
                    'last_update':{
                        'name_last':        row[16],
                        'name_first':       row[17],
                        'dt_update':        str(row[18]) if row[18] else None
                    }
                }
            
                
            result.append(cur_entry)
    
        return result
    
    
    def get_search_keywords(self, account_id, search_str):
        """
        This is used when typing the first few characters of the search keys.
        """
        
        """
        PROCEDURE pig_medvac_search_keys(
            IN p_account_id INT,
            IN p_search_str VARCHAR(255)
        )  
        """
        
        params = [
            account_id,
            search_str
        ]
        
        rows = self._call_procedure('pig_medvac_search_keys', params)
        
        if res is None:
            return []
        
        
        row = res[0]
        
        
        result = []
            
        for row in rows:
            cur_entry = {
                'key':              row[0],
                'hits':             row[1]
            }
            
            result.append(cur_entry)

        return result
    
    
    def get_search_result(self, account_id, search_str):
        """
        This is used when geting the searched rows.
        """
        
        
        
        sql =   f"""
                SELECT 
                    id,
                    date_medvac,
                    sow_boar_id,
                    health_issue_id,
                    
                    u_brand_name,
                    u_type_name,
                    u_acc_medvac_name,
                    notes
                FROM pig_medvac
                WHERE account_id = {account_id}
                    AND (
                        u_brand_name LIKE CONCAT('%', p_search_str, '%') OR
                        u_type_name LIKE CONCAT('%', p_search_str, '%') OR
                        u_acc_medvac_name LIKE CONCAT('%', p_search_str, '%')
                    )
                ORDER BY 
                    CASE 
                        WHEN u_brand_name LIKE CONCAT(p_search_str, '%') THEN 1
                        WHEN u_type_name LIKE CONCAT(p_search_str, '%') THEN 1
                        WHEN u_acc_medvac_name LIKE CONCAT(p_search_str, '%') THEN 1
                        ELSE 2
                    END ASC,
                    id ASC;
                
                """
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        

        result = []
            
        for row in rows:
            cur_entry = {
                'key':              row[0],
                'hits':             row[1]
            }
            
            result.append(cur_entry)

        return result
    
    
    
