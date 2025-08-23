# January 3, 2024
# Jack Wong

from common_constants       import *


class AccountGestatingOps:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'AccountGestatingOps'


    def add(self, data = None):
        """
        PROCEDURE account_gestating_ops_add(
            in_user_id              INT,

            in_num_days_since_insem INT,
            
            in_name                 VARCHAR(50),
            in_description          VARCHAR(160)
        )  
        """
        
        sql =  'CALL account_gestating_ops_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.num_days_since_insem
        sql += '"%s",'  % data.name
        
        if data.description is not None:
            sql += '"%s");'   % data.description
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
            msg = 'add(); error in executing query[] = ' + sql
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
                
                'acc_gestating_ops': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE account_gestating_ops_update(
            in_user_id                  INT,
    
            in_acc_gestating_ops_id     INT,
            in_num_days_since_insem     INT,
            
            in_name                     VARCHAR(50),
            in_description              VARCHAR(160)
        )
        """
       
        sql =  'CALL account_gestating_ops_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.acc_gest_ops_id
        sql += '%s,'    % data.num_days_since_insem
        
        sql += '"%s",'  % data.name
        
        if data.description is not None:
            sql += '"%s");'   % data.description
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
                
                'acc_gestating_ops': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_acc_gestating_ops_list(self, account_id, inc_deleted = 0,
            inc_user_audit = 0):
                
        if inc_deleted > 0:
            where_clause = 'WHERE a.account_id = %s' % account_id 
        else:
            where_clause = 'WHERE a.account_id = %s AND (a.flag & 1) = 0' % account_id 
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.num_days_since_insem,
                        
                        a.name,
                        a.description,
                        a.dt_entry
                    FROM account_gestating_ops a
                    %s
                    ORDER BY a.num_days_since_insem
                    """ % where_clause
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.num_days_since_insem,
                        
                        a.name,
                        a.description,
                        
                        c.username,
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.username,
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM account_gestating_ops a
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    ORDER BY a.num_days_since_insem
                    """ % where_clause

            
        
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
            conn.close()
            
        except Exception as e:
            msg = 'get_acc_gestating_ops_list(); error in executing query[] = ' + sql
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
                        'id':                   row[0],
                        'num_days_since_insem': row[1],
                        'name':                 row[2],
                        'desc':                 row[3],
                        
                        'dt_entry':             str(row[4])
                    }
                
                else:
                    cur_entry = {
                        'id':                   row[0],
                        'num_days_since_insem': row[1],
                        'name':                 row[2],
                        'desc':                 row[3],
                        
                        'added_by': {
                            'username':         row[4],
                            'name_last':        row[5],
                            'name_first':       row[6],
                            'dt_entry':         row[7]
                        },
                        
                        'last_update':{
                            'username':         row[8],
                            'name_last':        row[9],
                            'name_first':       row[10],
                            'dt_update':        str(row[11]) if row[11] else None
                        }
                    }
                    
                result.append(cur_entry)
        
        return result
    
    