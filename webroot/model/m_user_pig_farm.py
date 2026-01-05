# January 5, 2026
# Jack Wong

from common_constants       import *


class UserPigFarm:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'UserPigFarm'
    
    
    def add(self, data = None):
        """
        PROCEDURE user_pig_farm_add(
            in_user_id              INT,
            
            in_pig_farm_id          INT,
            in_user_id_to_add       INT
        )   
        """
        
        
        sql =  'CALL user_id_to_add('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_farm_id
        sql += '%s);'   % data.user_id_to_add

        
        
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
                }
            }

        return None

    
    def get_list(self, user_id = 0,  pig_farm_id = 0, inc_deleted = 0, 
            inc_user_audit = 0):
        
        where_clause = ''
        if pig_farm_id > 0:
            where_clause = 'WHERE a.pig_farm_id = %s' % pig_farm_id 
            
            if inc_deleted == 0:
                where_clause += ' AND (a.flag & 1) = 0'  
            
        
        if user_id > 0:
            sql =   """
                    SELECT 
                        a.pig_farm_id
                    FROM user_pig_farm a 
                    WHERE a.user_id = %s AND (a.flag & 1) = 0
                    """ % user_id
        else:
            sql =   """
                    SELECT
                        a.id,
                        a.user_id,
                        b.name_last,
                        b.name_first,
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM user_pig_farm a 
                    LEFT OUTER JOIN user b          ON a.user_id = b.id
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                
                    %s
                    ORDER BY b.name_last, b.name_first
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
                if user_id >0:
                    result.append(row[0])
                    
                else:
                    cur_entry = {
                        'pig_farm_user':{
                            'id':               row[0],
                            'user_id':          row[1],
                            'user_name_last':   row[2],
                            'user_name_first':  row[3]
                        },
                  
                        
                        'added_by': {
                            'name_last':        row[4],
                            'name_first':       row[5],
                            'dt_entry':         row[6]
                        },
                        
                        'last_update':{
                            'name_last':        row[7],
                            'name_first':       row[8],
                            'dt_update':        str(row[9]) if row[9] else None
                        }
                    }
                
                    
                    result.append(cur_entry)
        
        return result
    
    
        