# September 17, 2025
# Jack Wong

from common_constants       import *


class AddressLevel:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'AddressLevel'


    def get_address_level_1_list(self, country_id, return_tuple = 0):
        """
        Will get address_level_1 list.
        
        
        Returns
        -------
        list of dictionary

        """
        
                   
        sql =   """
                SELECT 
                    id,
                    name
                FROM address_level_1
                WHERE country_id = %s
                ORDER BY sort_priority DESC, name
                """ % country_id
        
        
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
            msg = 'get_address_level_1_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        
        if return_tuple > 0:
            return rows
        
        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_entry = {
                    'id':               row[0], 
                    'name':             row[1]
                }
                
                result.append(cur_entry)

        
        return result
    
    
    def get_address_level_2_list(self, address_level_1_id, return_tuple = 0):
        """
        Will get address_level_2 list.
        
        
        Returns
        -------
        list of dictionary

        """
        
                   
        sql =   """
                SELECT 
                    id,
                    name
                FROM address_level_2
                WHERE address_level_1_id = %s
                ORDER BY sort_priority DESC, name
                """ % address_level_1_id
        
        
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
            msg = 'get_address_level_2_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        
        if return_tuple > 0:
            return rows

        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_entry = {
                    'id':               row[0], 
                    'name':             row[1]
                }
                
                result.append(cur_entry)

        
        return result
    
    
    def get_address_level_3_list(self, address_level_2_id):
        """
        Will get address_level_3 list.
        
        
        Returns
        -------
        list of dictionary

        """
        
                   
        sql =   """
                SELECT 
                    id,
                    name
                FROM address_level_3
                WHERE address_level_2_id = %s
                ORDER BY sort_priority DESC, name
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
            msg = 'get_address_level_3_list(); error in executing query[] = ' + sql
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
    
    
    def get_address_level_names(self, address_level_1_id = 0, address_level_2_id = 0,
            address_level_3_id = 0):
                
        """
        PROCEDURE address_level_get_names(
            in_address_level_1_id       INT,
            in_address_level_2_id       INT,
            in_address_level_3_id       INT
        )
        """
        
        sql =  'CALL address_level_get_names('
        sql += '%s,'    % address_level_1_id
        sql += '%s,'    % address_level_2_id
        sql += '%s);'   % address_level_3_id
        
        
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
            msg = 'get_address_level_names(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            return {
                'level_1_name':     row[0],
                'level_2_name':     row[1],
                'level_3_name':     row[2]
            }

        return None
    
    