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
            in_sow_boar_id          INT,
            in_prod_group_id        INT,
            
            in_date_notes           VARCHAR(10),
            in_notes                VARCHAR(160)
        )  
        """
        
        sql =  'CALL pig_prod_notes_add('
        sql += '%s,'    % data.user_id
        
        if data.pig_prod_id is not None and data.pig_prod_id > 0:
            sql += '%s,'    % data.pig_prod_id
        else:
            sql += 'NULL,'
            
        if data.sow_boar_id is not None and data.sow_boar_id > 0:
            sql += '%s,'    % data.sow_boar_id
        else:
            sql += 'NULL,'
        
            
        if data.production_group_id is not None and data.production_group_id > 0:
            sql += '%s,'    % data.production_group_id
        else:
            sql += 'NULL,'
        
        if data.date_notes is not None:
            sql += '"%s",'  % data.date_notes
        else:
            sql += 'NULL,'
            
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
            in_date_notes           VARCHAR(10),
            in_notes                VARCHAR(160)
        )
        """
       
        sql =  'CALL pig_prod_notes_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_prod_notes_id
        
        if data.date_notes is not None:
            sql += '"%s",'  % data.date_notes
        else:
            sql += 'NULL,'
        
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
        pig_prod_notes_id    = data['pig_prod_notes_id']
        
        """
        PROCEDURE pig_prod_notes_delete(
            in_user_id                  INT,
            
            in_pig_prod_notes_id         INT
        )
        """
       
        sql =  'CALL pig_prod_notes_delete('
        sql += '%s,'    % user_id
        sql += '%s);'   % pig_prod_notes_id
        
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
                
                'pig_prod_notes': {
                    'id'
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id = 0, sow_boar_id = 0, inc_deleted = 0):
        
        if pig_prod_id > 0:
            where_clause = 'WHERE a.pig_prod_id = %s ' % pig_prod_id
        
        if sow_boar_id > 0:
            where_clause = 'WHERE a.sow_boar_id = %s ' % sow_boar_id
        
        if inc_deleted == 0:
            where_clause += ' AND a.flag & 1 = 0'
        
        sql =   """
                SELECT 
                    a.id,
                    a.date_notes,
                    a.notes,
                    
                    b.name_last,
                    b.name_first,
                    a.dt_last_update,
                    
                    c.name_last,
                    c.name_first,
                    a.dt_entry
                
                FROM pig_prod_notes a 
                LEFT OUTER JOIN user b ON a.last_update_user_id = c.id
                LEFT OUTER JOIN user c ON a.added_by_user_id = b.id
                
                %s
                ORDER BY a.id DESC
                """ % where_clause
       
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
                        'date_notes':       str(row[1]),
                        'notes':            row[2],
                        
                    },
                    
                    'added_by':{
                        'name_first':       row[3],
                        'name_last':        row[4],
                        'dt_entry':         str(row[2])
                    }
                }
                
                result.append(cur_entry)
        
        return result
    
    