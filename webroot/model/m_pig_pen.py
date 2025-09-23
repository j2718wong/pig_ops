# September 23, 2025
# Jack Wong

from common_constants       import *


class PigPen:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigPen'


    def add(self, data = None):
        """
        PROCEDURE pig_pen_add(
            in_user_id              INT,

            in_pig_farm_id          INT,
            in_pig_pen_type_id      INT,
            
            in_name                 VARCHAR(20)
        )  
        """
        
        sql =  'CALL pig_pen_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_farm_id
        sql += '%s,'    % data.pig_pen_type_id
        sql += '"%s");' % data.name
        
        
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
                
                'pig_pen': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_pig_pen_update(
            in_user_id                  INT,
            
            in_pig_pig_pen_id           INT,
            
            in_pig_pen_type_id          INT,
            
            in_name                     VARCHAR(20)
        )
        """
       
        sql =  'CALL pig_pen_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_pig_pen_id
        sql += '%s,'    % data.pig_pen_type_id
        sql += '"%s");' % data.name
        
        
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
                
                'pig_pen': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        pig_pen_id          = data['pig_pen_id']
        
        """
        PROCEDURE pig_pen_delete(
            in_user_id                  INT,
            
            in_pig_pen_id               INT
        )
        """
       
        sql =  'CALL pig_pen_delete('
        sql += '%s,'    % user_id
        sql += '%s);'   % pig_pen_id
        
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
                
                'pig_pen': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def get_list(self, pig_farm_id, inc_deleted = 0, inc_user_audit = 0):
        
        if inc_deleted > 0:
            where_clause = 'WHERE a.pig_farm_id = %s' % pig_farm_id 
        else:
            where_clause = 'WHERE a.pig_farm_id = %s AND (a.flag & 1) = 0' % pig_farm_id 
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.pig_pen_type_id,
                        b.name 
                    FROM pig_pen a 
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
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM pig_pen a 
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
                        'description':          row[4],
                        
                        'added_by': {
                            'name_last':        row[5],
                            'name_first':       row[6],
                            'dt_entry':         row[7]
                        },
                        
                        'last_update':{
                            'name_last':        row[8],
                            'name_first':       row[9],
                            'dt_update':        str(row[10]) if row[10] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    