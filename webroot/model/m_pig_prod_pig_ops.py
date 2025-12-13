# August 23, 2025
# Jack Wong

from common_constants       import *


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
            in_date                     VARCHAR(10),
            in_notes                    VARCHAR(160)
        )
        """
       
        sql =  'CALL pig_prod_pig_ops_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_prod_pig_ops_id
        sql += '%s,'    % data.staff_id
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
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod_pig_ops': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id, operation_type, inc_user_audit = 0):
        
               
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.date_target,
                        a.date_actual,
                        a.dt_entry,
                        
                        a.account_pig_ops_id,
                        b.name,
                        b.num_days_since,
                        b.flag AS account_pig_ops_flag,
                        b.description,
                        
                        a.staff_id,
                        c.name  AS staff_name,
                        
                        a.notes_id,
                        d.notes
                        
                        
                    FROM pig_prod_pig_ops a 
                    LEFT OUTER JOIN account_pig_ops b   ON a.account_pig_ops_id = b.id
                    LEFT OUTER JOIN pig_farm_staff c    ON a.staff_id = c.id
                    LEFT OUTER JOIN pig_prod_notes d    ON a.notes_id = d.id
                    WHERE a.pig_prod_id = %s AND a.operation_type = %s
                    ORDER BY b.num_days_since
                    """ % (pig_prod_id, operation_type)
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.date_target,
                        a.date_actual,
                        a.dt_entry,
                        
                        a.account_pig_ops_id,
                        b.name,
                        b.num_days_since,
                        b.flag AS account_pig_ops_flag,
                        b.description,
                        
                        a.staff_id,
                        c.name  AS staff_name,
                        
                        a.notes_id,
                        d.notes,
                        
                        e.name_last,
                        e.name_first,
                        a.dt_last_update
                        
                    FROM pig_prod_pig_ops a 
                    LEFT OUTER JOIN account_pig_ops b   ON a.account_pig_ops_id = b.id
                    LEFT OUTER JOIN pig_farm_staff c    ON a.staff_id = c.id
                    LEFT OUTER JOIN pig_prod_notes d    ON a.notes_id = d.id
                    LEFT OUTER JOIN user e              ON a.last_update_user_id = e.id
                    
                    WHERE a.pig_prod_id = %s AND a.operation_type =%s
                    ORDER BY b.num_days_since
                    """ % (pig_prod_id, operation_type)
        
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
                if inc_user_audit == 0:
                    cur_entry = {
                    
                        'pig_prod_pig_ops': {
                            'id':               row[0],
                            'date_target':      str(row[1]),
                            'date_actual':      str(row[2]) if row[2] else None,
                            'dt_entry':         str(row[3])
                        },
                        
                        'account_pig_ops':{
                            'id':               row[4],
                            'name':             row[5],
                            'num_days_since':   row[6],
                            'flag':             row[7],
                            'description':      row[8]
                        },
                        
                        'staff': {
                            'id':               row[9],
                            'name':             row[10]
                        },
                        
                        'notes': {
                            'id':               row[11],
                            'notes':            row[12]
                        }
                    }
                    
                else:
                    cur_entry = {
                        'pig_prod_pig_ops': {
                            'id':               row[0],
                            'date_target':      str(row[1]),
                            'date_actual':      str(row[2]) if row[2] else None,
                            'dt_entry':         str(row[3])
                        },
                        
                        'account_pig_ops': {
                            'id':               row[4],
                            'name':             row[5],
                            'num_days_since':   row[6],
                            'flag':             row[7],
                            'description':      row[8]
                        },
                        
                        'staff': {
                            'id':               row[9],
                            'name':             row[10]
                        },
                        
                        'notes': {
                            'id':               row[11],
                            'notes':            row[12]
                        },
                        
                        'last_update': {
                            'name_last':        row[13],
                            'name_first':       row[14],
                            'dt_update':        str(row[15]) if row[15] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    