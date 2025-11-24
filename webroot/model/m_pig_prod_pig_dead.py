# August 23, 2025
# Jack Wong

from common_constants       import *


class PigProdPigDead:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProdPigDead'


    def add(self, data = None):
        """
        PROCEDURE pig_prod_pig_dead_add(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            in_pig_prod_group_id    INT,
            
            in_date_dead            VARCHAR(10),
            in_num_pigs_dead        INT,
            in_notes                VARCHAR(160)
        )  
        """
        
        sql =  'CALL pig_prod_pig_dead_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        sql += '%s,'    % data.pig_prod_group_id
        
        sql += '"%s",'  % data.date_dead
        sql += '%s,'    % data.num_pigs_dead
        
        if data.notes is not None and len(data.notes) > 0:
            sql += '"%s");'   % data.comments
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
                
                'pig_prod_pig_dead': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_prod_pig_dead_update(
            in_user_id                  INT,
    
            in_pig_prod_pig_dead_id     INT,
            
            in_date_dead                VARCHAR(10),
            in_num_pigs_dead            INT,
            in_notes                    VARCHAR(160)
        )
        """
       
        sql =  'CALL pig_prod_pig_dead_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_pig_dead_id
        sql += '"%s",'  % data.date_dead
        sql += '%s,'    % data.num_pigs_dead
                
        if data.notes is not None and len(data.notes) > 0:
            sql += '"%s");'   % data.notes
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
                
                'pig_prod_pig_dead': {
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
                    a.date_dead,
                    a.num_pigs_dead,
                    d.notes,
                    
                    b.name_last,
                    b.name_first,
                    a.dt_entry,
                    
                    c.name_last,
                    c.name_first,
                    a.dt_last_update
                    
                FROM pig_prod_pig_dead a 
                LEFT OUTER JOIN user b          ON a.added_by_user_id   = b.id
                LEFT OUTER JOIN user c          ON a.last_update_user_id = c.id
                LEFT OUTER JOIN pig_prod_notes d ON a.notes_id = d.id
            
                WHERE pig_prod_id = %s
                ORDER a.date_dead DESC
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
                    'pig_dead':{
                        'id':               row[0],
                        'date_dead':        str(row[1]),
                        'num_pigs_dead':    row[2],
                        'notes':            row[3],
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
    
    