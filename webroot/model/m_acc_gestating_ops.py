# January 3, 2024
# Jack Wong

from common_constants       import *


class AccountGestatingOps:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'AccountGestatingOps'


    def get_account_gestating_ops_list(self, account_id):
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
            msg = 'get_account_gestating_ops_list(); error in executing query[] = ' + sql
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
    
