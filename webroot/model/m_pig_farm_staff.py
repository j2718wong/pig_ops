# August 26, 2025
# Jack Wong

from common_constants       import *


class PigFarmStaff:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigFarmStaff'


    def add(self, data = None):
        """
        PROCEDURE pig_farm_staff_add(
            in_user_id                  INT,

            in_pig_farm_id              INT,
            in_set_user_as_staff        INT,
            in_name                     VARCHAR(50)
        )  
        """
        
        sql =  'CALL pig_farm_staff_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_farm_id
        sql += '%s,'    % data.set_user_as_staff
        
        if data.name is not None:
            sql += '"%s");' % data.name
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
                
                'pig_farm_staff': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_farm_staff_update(
            in_user_id                  INT,
            
            in_pig_farm_staff_id        INT,
            in_staff_user_id            INT,
            
            in_name                     VARCHAR(50)
        )
        """
       
        sql =  'CALL pig_farm_staff_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_farm_staff_id
        sql += '%s,'    % data.staff_user_id
        
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
                
                'pig_farm_staff': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        pig_farm_staff_id    = data['pig_farm_staff_id']
        
        """
        PROCEDURE pig_farm_staff_delete(
            in_user_id                  INT,
            
            in_pig_farm_staff_id        INT
        )
        """
       
        sql =  'CALL pig_farm_staff_delete('
        sql += '%s,'    % user_id
        sql += '%s);'   % pig_farm_staff_id
        
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
                
                'pig_farm_staff': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_list(self, pig_farm_id, inc_deleted = 0,
            inc_user_audit = 0, minimum_info = 0):
        
        if inc_deleted > 0:
            where_clause = 'WHERE a.pig_farm_id = %s' % pig_farm_id 
        else:
            where_clause = 'WHERE a.pig_farm_id = %s AND (a.flag & 1) = 0' % pig_farm_id 
        
        
        if inc_user_audit == 0:
            if minimum_info == 0:
                sql =   """
                        SELECT 
                            a.id,
                            a.name,
                            a.user_id
                        FROM pig_farm_staff a 
                        %s
                        ORDER BY a.name
                        """ % where_clause
            else:
                sql =   """
                        SELECT 
                            a.id,
                            a.name
                        FROM pig_farm_staff a 
                        %s
                        ORDER BY a.name
                        """ % where_clause
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.name,
                        a.user_id,
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM pig_farm_staff a 
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
                    if minimum_info == 0:
                        cur_entry = {
                            'pig_farm_staff': {
                                'id':               row[0],
                                'name':             row[1],
                                'user_id':          row[2]
                            }
                        }
                    else:
                        cur_entry = {
                            'pig_farm_staff': {
                                'id':               row[0],
                                'name':             row[1]
                            }
                        }
                    
                else:
                    cur_entry = {
                        'pig_farm_staff': {
                            'id':               row[0],
                            'name':             row[1],
                            'user_id':          row[2]
                        },
                        
                        'added_by': {
                            'name_last':        row[3],
                            'name_first':       row[4],
                            'dt_entry':         row[5]
                        },
                        
                        'last_update':{
                            'name_last':        row[6],
                            'name_first':       row[7],
                            'dt_update':        str(row[8]) if row[8] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    