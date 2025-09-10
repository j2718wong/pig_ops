# August 23, 2025
# Jack Wong

from common_constants       import *


class AppAnalytics:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'AppAnalytics'


    def add(self, data = None):
        """
        PROCEDURE app_analytics_add(
            in_user_id              INT,

            in_app_function_id      INT
        )  
        """
        
        
        sql =  'CALL app_analytics_add('
        sql += '%s,'    % data['user_id']
        sql += '%s'     % data['app_function_id']
        sql += ');'
        
        
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

       
        return None
    
    