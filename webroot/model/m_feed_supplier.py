# August 24, 2025
# Jack Wong

from common_constants       import *


class FeedSupplier:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'FeedSupplier'


    def add(self, data = None):
        """
        PROCEDURE feed_supplier_add(
            in_user_id              INT,

            in_country_id           INT,
            in_address_level_1_id   INT,
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            
            in_name                 VARCHAR(50)
        )  
        """
        
        sql =  'CALL feed_supplier_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.country_id
        sql += '%s,'    % data.address_level_1_id
        sql += '%s,'    % data.address_level_2_id
        sql += '%s,'    % data.address_level_3_id
        
        sql += '"%s")'  % data.name
        
        
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
                
                'feed_supplier': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE feed_supplier_update(
            in_user_id              INT,
            
            in_feed_supplier_id     INT,
            
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            
            in_name                 VARCHAR(50)
        )  
        """
        
        sql =  'CALL feed_supplier_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.in_feed_supplier_id
        
        sql += '%s,'    % data.address_level_2_id
        sql += '%s,'    % data.address_level_3_id
        
        sql += '"%s")'  % data.name
        
        
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
                
                'feed_supplier': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_list(self, address_level_2_id):
       
        sql =   """
                SELECT 
                    a.id,
                    a.country_id,
                    b.name AS country_name,
                    a.address_level_1_id,
                    a.address_level_2_id,
                    a.address_level_3_id,
                    
                    a.name,
                    a.dt_entry
                FROM feed_supplier a 
                LEFT OUTER JOIN app_country b   ON a.country_id = b.id
                WHERE  a.address_level_2_id = %s 
                ORDER BY a.name
                """ % address_level_2_id
        
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
                    'id':                   row[0],
                    
                    'location':{
                        
                        'country': {
                            'id':           row[1],
                            'name':         row[2]
                        },
                        
                        'address': {
                            'level_1':{
                                'id':       row[3]
                            },
                        
                            'level_2':{
                                'id':       row[4]
                            },
                            
                            'level_3':{
                                'id':       row[5]
                            }
                        }
                    },
                    
                    'name':                 row[6],
                    
                    'dt_entry':             str(row[7])
                }
                    
                result.append(cur_entry)
        
        return result
    
    