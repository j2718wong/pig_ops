# March 12, 2026
# Jack Wong

from common_constants       import *



class CustomerFeedback:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProdNotes'


    def add(self, data = None):
        """
        PROCEDURE customer_feedback_add(
            in_user_id              INT,
           
            in_notes                VARCHAR(500)
        )  
        """
        
        sql =  'CALL customer_feedback_add('
        sql += '%s,'    % data.user_id
        sql += '"%s");'  % data.notes
        
        
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
                
                'customer_feedback': {
                    'id':               row[3]
                }
            }

        return None
    
    
