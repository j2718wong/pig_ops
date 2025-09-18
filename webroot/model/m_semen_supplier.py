# August 24, 2025
# Jack Wong

from common_constants       import *


class SemenSupplier:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SemenSupplier'


    def add(self, data = None):
        """
        PROCEDURE semen_supplier_add(
            in_user_id              INT,

            in_country_id           INT,
            in_address_level_1_id   INT,
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            
            in_name                 VARCHAR(50)
        )  
        """
        
        sql =  'CALL semen_supplier_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.country_id
        sql += '%s,'    % data.address_level_1_id
        sql += '%s,'    % data.address_level_2_id
        
        if data.address_level_3_id is not None and data.address_level_3_id > 0:
            sql += '%s,'    % data.address_level_3_id
        else:
            sql += 'NULL,'
        
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
                
                'semen_supplier': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
        
    def get_list(self, country_id, address_level_1_id = None, 
            inc_deleted = 0, inc_user_audit = 0):
        
        where_clause = 'WHERE a.country_id = %s ' % country_id
        if address_level_1_id is not None:
            where_clause += ' AND address_level_1_id = %s ' %  address_level_1_id
                
        if inc_deleted == 0:
            where_clause += 'AND (a.flag & 1) = 0'  
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.country_id,
                        b.name AS country_name,
                        a.address_level_1_id,
                        a.address_level_2_id,
                        
                        a.name,
                        a.dt_entry
                    FROM semen_supplier a 
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
                        a.address_level_1_id,
                        a.address_level_2_id,
                        
                        a.name,
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM semen_supplier a 
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
                            },
                            
                            'address': {
                                'level_1':{
                                    'id':       row[3]
                                },
                            
                                'level_2':{
                                    'id':       row[4]
                                }
                            }
                        },
                        
                        'name':                 row[5],
                        
                        'dt_entry':             str(row[6])
                    }
                    
                else:
                    cur_entry = {
                        'id':                   row[0],
                        
                        'location':{
                            
                            'country': {
                                'id':           row[1],
                                'name':         row[2]
                            },
                            
                            'address_level_1':{
                                'id':           row[3]
                            },
                            
                            'address_level_2':{
                                'id':           row[4]
                            }
                        },
                        
                        'name':                 row[5],
                        
                        'added_by': {
                            'name_last':        row[6],
                            'name_first':       row[7],
                            'dt_entry':         row[8]
                        },
                        
                        'last_update':{
                            'name_last':        row[9],
                            'name_first':       row[10],
                            'dt_update':        str(row[11]) if row[11] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    