# September 1, 2025
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


# /* account_pig_ops.flag bits*/
FLAG_BIT_ACCOUNT_PIG_OPS_IS_MEDVAC      = 2


class AccountPigOps(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE account_pig_ops_add(
            in_user_id              INT,
            in_operation_type       INT,
            in_num_days_since       INT,
            
            is_medvac               INT,
            
            in_name                 VARCHAR(50),
            in_short_name           VARCHAR(15),
            in_description          VARCHAR(160)
        )  
        """
        
        params = [
            data.user_id,
            data.operation_type,
            data.num_days_since,
            
            data.is_medvac,
            
            data.name,
            data.short_name        if data.short_name is not None and len(data.short_name.strip()) > 0 else None,
            data.description       if data.description is not None and len(data.description.strip()) > 0 else None
        ]

        res = self._call_procedure('account_pig_ops_add', params)

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
                
                'account_pig_ops': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE account_pig_ops_update(
            in_user_id              INT,
    
            in_account_pig_ops_id   INT,
            in_num_days_since       INT,
            
            is_medvac               INT,
            
            in_name                 VARCHAR(50),
            in_short_name           VARCHAR(15),
            in_description          VARCHAR(160)
        )
        """
        
        params = [
            data.user_id,
            
            data.account_pig_ops_id,
            data.num_days_since,
            
            data.is_medvac,
            
            data.name,
            data.short_name        if data.short_name is not None and len(data.short_name.strip()) > 0 else None,
            data.description       if data.description is not None and len(data.description.strip()) > 0 else None
        ]

        res = self._call_procedure('account_pig_ops_update', params)

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
                
                'account_pig_ops': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        account_pig_ops_id  = data['account_pig_ops_id']
        
        """
        PROCEDURE account_pig_ops_delete(
            in_user_id                  INT,
            
            in_account_pig_ops_id     INT
        )
        """
        
        params = [
            user_id,
            account_pig_ops_id
        ]

        res = self._call_procedure('account_pig_ops_delete', params)

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
                
                'account_pig_ops': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_list(self, account_id, operation_type, inc_deleted = 0, inc_user_audit = 0):
        
        if operation_type is not None:
            values= (account_id, operation_type)
            where_clause = 'WHERE a.account_id = %s AND a.operation_type =%s' % values
            order_clause = 'ORDER BY a.num_days_since'
        
        else:
            where_clause = 'WHERE a.account_id = %s ' % account_id
            order_clause = 'ORDER BY a.operation_type, a.num_days_since'
            
            
        if inc_deleted == 0:
            where_clause += ' AND (a.flag & 1) = 0' 
            
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.num_days_since,
                        a.version_num,
                        a.operation_type,
                        a.flag,
                        
                        a.name,
                        a.short_name,
                        a.description
                    FROM account_pig_ops a
                    %s
                    %s
                    """ % (where_clause, order_clause)
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.num_days_since,
                        a.version_num,
                        a.operation_type,
                        a.flag,
                        
                        a.name,
                        a.short_name,
                        a.description,
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM account_pig_ops a
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    ORDER BY a.num_days_since
                    """ % where_clause

        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
            
        
        result = []
        
            
        for row in rows:
            cur_flag = row[4]
                
            is_medvac   = 0
            if cur_flag & FLAG_BIT_ACCOUNT_PIG_OPS_IS_MEDVAC > 0:
                is_medvac   =   1
                
            
            if inc_user_audit == 0:
                
                cur_entry = {
                    'acc_pig_ops': {
                        'id':               row[0],
                        'num_days_since':   row[1],
                        'version_num':      row[2],
                        'operation_type':   row[3],
                        'is_medvac':        is_medvac,
                        
                        'name':             row[5],
                        'short_name':       row[6],
                        'desc':             row[7]
                    }
                }
            
            else:
                
                cur_entry = {
                    'acc_pig_ops': {
                        'id':               row[0],
                        'num_days_since':   row[1],
                        'version_num':      row[2],
                        'operation_type':   row[3],
                        'is_medvac':        is_medvac,
                        
                        'name':             row[5],
                        'short_name':       row[6],
                        'desc':             row[7]
                    },
                    
                    'added_by': {
                        'name_last':        row[8],
                        'name_first':       row[9],
                        'dt_entry':         str(row[10]) if row[10] else None
                    },
                    
                    'last_update':{
                        'name_last':        row[11],
                        'name_first':       row[12],
                        'dt_update':        str(row[13]) if row[13] else None
                    }
                }
                
            result.append(cur_entry)
    
        return result
    
    
