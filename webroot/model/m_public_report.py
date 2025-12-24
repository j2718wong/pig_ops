# August 23, 2025
# Jack Wong

from common_constants       import *


class PublicReport:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PublicReport'


    def add(self, data = None):
        """
        PROCEDURE public_report_add(
            in_user_id              INT,

            in_supplier_id          INT,
            in_report_type          INT,
            
            in_notes                VARCHAR(160)
        )  
        """
        
        sql =  'CALL public_report_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.supplier_id
        sql += '%s,'    % data.report_type
        
        
        if data.notes is not None:
            sql += '"%s");'   % data.notes
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
                
                'public_report': {
                    'id':               row[3]
                }
            }

        return None
    
    
    