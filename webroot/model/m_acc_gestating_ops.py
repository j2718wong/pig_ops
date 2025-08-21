# January 3, 2024
# Jack Wong

from common_constants       import *


class AccountGestatingOps:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'AccountGestatingOps'


    def get_list(self, account_id):
        sql =   """
                SELECT 
                    id,
                    num_days_since_insem,
                    
                    name,
                    description,
                    dt_entry
                FROM account_gestating_ops
                WHERE account_id = %s
                ORDER BY num_days_since_insem
                """ % account_id
        
        
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
                cur_entry = {
                    'id':                   row[0],
                    'num_days_since_insem': row[1],
                    'name':                 row[2],
                    'desc':                 row[3],
                    
                    'dt_entry':             row[4]
                    
                }
                    
                result.append(cur_entry)
        
        return result
    
    
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
        
        sql += '%s,'    % data.country_id
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
    