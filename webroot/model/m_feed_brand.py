# August 24, 2025
# Jack Wong

from common_constants       import *


class FeedBrand:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'FeedBrand'


    def add(self, data = None):
        """
        PROCEDURE feed_brand_add(
            in_user_id              INT,

            in_country_id           INT,
            
            in_name                 VARCHAR(50)
        )  
        """
        
        sql =  'CALL feed_brand_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.country_id
        
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
                
                'feed_brand': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
        
    def get_list(self, country_id, inc_deleted = 0, inc_user_audit = 0):
        
        where_clause = 'WHERE a.country_id = %s ' % country_id
                
        if inc_deleted == 0:
            where_clause += 'AND (a.flag & 1) = 0'  
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.country_id,
                        b.name AS country_name,

                        a.name,
                        a.dt_entry
                    FROM feed_brand a 
                    LEFT OUTER JOIN app_country b   ON a.country_id = b.id
                    %s
                    ORDER BY a.name
                    """ % where_clause
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.country_id,
                        b.name AS country_name,

                        a.name,
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM feed_brand a 
                    LEFT OUTER JOIN app_country b   ON a.country_id = b.id
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
                        
                        'location':{
                            
                            'country': {
                                'id':           row[1],
                                'name':         row[2]
                            }
                        },
                        
                        'name':                 row[3],
                        
                        'dt_entry':             str(row[4])
                    }
                    
                else:
                    cur_entry = {
                        'id':                   row[0],
                        
                        'location':{
                            
                            'country': {
                                'id':           row[1],
                                'name':         row[2]
                            }
                        },
                        
                        'name':                 row[3],
                        
                        'added_by': {
                            'name_last':        row[4],
                            'name_first':       row[5],
                            'dt_entry':         str(row[6])
                        },
                        
                        'last_update':{
                            'name_last':        row[7],
                            'name_first':       row[8],
                            'dt_update':        str(row[9]) if row[9] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    