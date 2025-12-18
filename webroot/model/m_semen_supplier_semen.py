# August 24, 2025
# Jack Wong

from common_constants       import *


class SemenSupplierSemen:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SemenSupplierSemen'


    def add(self, data = None):
        """
        PROCEDURE semen_supplier_semen_add(
            in_user_id              INT,

            in_semen_supplier_id    INT,
            in_name                 VARCHAR(50)
        )
        """
        
        sql =  'CALL semen_supplier_semen_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.semen_supplier_id
        
        sql += '"%s");'  % data.name
        
        
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
                
                'semen_sup_semen': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE semen_supplier_semen_update(
            in_user_id              INT,
            
            in_semen_sup_semen_id   INT, 

            in_name                 VARCHAR(50)
        )  
        """
        
        sql =  'CALL semen_supplier_semen_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.semen_sup_semen_id
        
        sql += '"%s");'  % data.name
        
       
        
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
                
                'semen_sup_semen': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    

    def get_list(self, semen_supplier_id):
       
        sql =   """
                SELECT 
                    id,
                    name
                    
                FROM semen_supplier_semen
                WHERE semen_supplier_id = %s
                ORDER BY a.name
                """ % semen_supplier_id
        
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
                cur_entry = {
                    'id':               row[0],
                    'name':             row[1]
                }
                    
                result.append(cur_entry)
        
        return result
    
    