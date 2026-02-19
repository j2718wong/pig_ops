# August 24, 2025
# Jack Wong

from common_constants       import *


class PublicLookup:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'FeedType'


    def get_list_feed_type(self):
        
      
        sql =   """
                SELECT 
                    id,
                    name
                    
                FROM feed_type 
                ORDER BY id
                """ 
    
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
            msg = 'get_list_feed_type(); error in executing query[] = ' + sql
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
                    'name':                 row[1]
                }

                result.append(cur_entry)
        
        return result
    
    
    
    def get_list_harvest_type(self):
        
      
        sql =   """
                SELECT 
                    id,
                    name
                    
                FROM harvest_type 
                ORDER BY id
                """ 
    
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
            msg = 'get_list_harvest_type(); error in executing query[] = ' + sql
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
                    'name':                 row[1]
                }

                result.append(cur_entry)
        
        return result
    
    

