# August 23, 2025
# Jack Wong

from common_constants       import *


class PigRaceLine:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigRaceLine'


    def add(self, data = None):
        """
        PROCEDURE pig_race_line_add(
            in_user_id              INT,

            in_pig_race_id          INT,
            
            in_name                 VARCHAR(50),
            in_description          VARCHAR(160)
        )  
        """
        
        sql =  'CALL pig_race_line_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_race_id
        sql += '"%s",'  % data.name
        
        if data.description is not None:
            sql += '"%s");'   % data.description
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
                
                'pig_race_line': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_race_line_update(
            in_user_id                  INT,
            
            in_pig_race_line_id         INT,
            in_pig_race_id              INT,
            
            in_name                     VARCHAR(50),
            in_description              VARCHAR(160)
        )
        """
       
        sql =  'CALL pig_race_line_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_race_line_id
        sql += '%s,'    % data.pig_race_id
        
        sql += '"%s",'  % data.name
        
        if data.description is not None:
            sql += '"%s");'   % data.description
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
                
                'pig_race_line': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
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
    
    
    def get_list(self, account_id, inc_deleted = 0,
            inc_user_audit = 0):
        
        if inc_deleted > 0:
            where_clause = 'WHERE a.account_id = %s' % account_id 
        else:
            where_clause = 'WHERE a.account_id = %s AND (a.flag & 1) = 0' % account_id 
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.pig_race_id,
                        b.name AS pig_race_name,
                        
                        a.name,
                        a.description,
                        a.dt_entry
                    FROM pig_race_line a 
                    LEFT OUTER JOIN pig_race b ON a.pig_race_id = b.id
                    %s
                    ORDER BY a.name
                    """ % where_clause
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.pig_race_id,
                        b.name AS pig_race_name,
                        
                        a.name,
                        a.description,
                        
                        c.username,
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.username,
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM pig_race_line a 
                    LEFT OUTER JOIN pig_race b      ON a.pig_race_id = b.id
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                
                    %s
                    ORDER BY a.name
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
                if inc_user_audit == 0:
                    cur_entry = {
                        'id':                   row[0],
                        
                        'pig_race':{
                            'id':               row[1],
                            'name':             row[2],
                        },
                        
                        'name':                 row[3],
                        'desc':                 row[4],
                        
                        'dt_entry':             str(row[5])
                    }
                    
                else:
                    cur_entry = {
                        'id':                   row[0],
                        
                        'pig_race':{
                            'id':               row[1],
                            'name':             row[2],
                        },
                        
                        'name':                 row[3],
                        'desccription':         row[4],
                        
                        'added_by': {
                            'username':         row[5],
                            'name_last':        row[6],
                            'name_first':       row[7],
                            'dt_entry':         row[8]
                        },
                        
                        'last_update':{
                            'username':         row[9],
                            'name_last':        row[10],
                            'name_first':       row[11],
                            'dt_update':        str(row[12]) if row[12] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    