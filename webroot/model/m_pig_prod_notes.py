# August 23, 2025
# Jack Wong

from common_constants       import *


class PigProdNotes:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProdNotes'


    def add(self, data = None):
        """
        PROCEDURE pig_prod_notes_add(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            in_notes                VARCHAR(160)
        )  
        """
        
        sql =  'CALL pig_prod_notes_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
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
                
                'pig_prod_notes': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_prod_notes_update(
            in_user_id              INT,
           
            in_pig_prod_notes_id    INT,
            in_notes                VARCHAR(160)
        )
        """
       
        sql =  'CALL pig_prod_notes_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_prod_notes_id
    
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
                
                'pig_prod_notes': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        pig_race_line_id    = data['pig_race_line_id']
        
        """
        PROCEDURE pig_race_line_delete(
            in_user_id                  INT,
            
            in_pig_race_line_id         INT
        )
        """
       
        sql =  'CALL pig_race_line_delete('
        sql += '%s,'    % user_id
        sql += '%s);'   % pig_race_line_id
        
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
            msg = 'delete(); error in executing query[] = ' + sql
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
                
                'pig_race_line': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id):
        
        sql =   """
                SELECT 
                    a.id,
                    a.notes,
                    a.dt_entry
                    
                    b.username,
                    b.name_last,
                    b.name_first
                
                FROM pig_prod_notes a 
                LEFT OUTER JOIN user b ON a.added_by_user_id = b.id
                WHERE a.pig_prod_id = %s
                ORDER BY a.id DESC
                """ % pig_prod_id
       
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
                    'prod_notes': {
                        'id':               row[0],
                        'notes':            row[1],
                        'dt_entry':         str(row[2])
                    },
                    
                    'added_by_user':{
                        'username':         row[3],
                        'name_first':       row[4],
                        'name_last':        row[5]
                    }
                }
                
                result.append(cur_entry)
        
        return result
    
    