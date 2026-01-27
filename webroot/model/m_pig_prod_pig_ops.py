# August 23, 2025
# Jack Wong

from common_constants       import *


"""
/* account_pig_ops.flag bits*/
DECLARE FLAG_BIT_ACCOUNT_PIG_OPS_IS_DELETED     INT             DEFAULT 1;
DECLARE FLAG_BIT_ACCOUNT_PIG_OPS_IS_MEDVAC      INT             DEFAULT 2;
"""

FLAG_BIT_ACCOUNT_PIG_OPS_IS_MEDVAC      = 2


class PigProdPigOps:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProdPigOps'

    
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
       
        sql =  'CALL pig_prod_pig_ops_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_prod_pig_ops_id
        sql += '%s,'    % data.staff_id
        sql += '%s,'    % data.done_by_user
        sql += '"%s",'  % data.date
        
        if data.notes is not None:
            data.notes = data.notes.strip()
            
            if len(data.notes) > 0:
                sql += '"%s");'  % data.notes
            else:
                sql += 'NULL);'
        else:
            sql += 'NULL);'
            
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        row = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            row = cursor.fetchone()
            cursor.close()

        except Exception as e:
            msg = 'update(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

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
            
        operation_type : can be an integer or tuple
            
        pig_prod_id : int
            pig_production id
        
        sow_boar_id : int
            
        
        order_by : int
            0 = ORDER BY num_days_since ASC
            1 = ORDER BY num_days_since DESC
        """
        
        if isinstance(operation_type, tuple):
            s_operation_type = tuple(str(x) for x in operation_type)
            op_types = ','.join(s_operation_type)
            
            filter_clause = 'a.operation_type IN (%s )' % op_types
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
                        i.dt_last_update
                        
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
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            #conn.close()
            
        except Exception as e:
            msg = 'get_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        result = []
        if rows is not None:
            
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
    
    