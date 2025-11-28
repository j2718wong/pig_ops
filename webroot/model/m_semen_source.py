# August 17, 2025
# Jack Wong

from common_constants       import *


class SemenSource:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SemenSource'

    
    def add(self, data = None):
        """
        PROCEDURE semen_source_add(
            in_user_id              INT,

            in_pig_farm_id          INT,
    
            in_boar_id              INT,
            
            in_semen_supplier_id    INT,
            in_pig_race_line_id     INT,
            
            in_name                 VARCHAR(50),
            in_description          VARCHAR(160)
        )  
        """
        
        sql =  'CALL semen_source_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_farm_id
        
        if data.boar_id is not None:
            sql += '%s,'    % data.boar_id
            
            sql += 'NULL,'
            sql += 'NULL,'
            
        else:
            sql += 'NULL,'
            
            sql += '%s,'    % data.semen_supplier_id
            sql += '%s,'    % data.pig_race_line_id
            
        
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
                
                'semen_source': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None

    
    def update(self, data = None):
        """
        PROCEDURE semen_source_update(
            in_user_id              INT,
            
            in_semen_source_id      INT,
            
            in_pig_farm_id          INT,
            in_boar_id              INT,
            
            in_semen_supplier_id    INT,
            in_pig_race_line_id     INT,
            
            
            in_name                 VARCHAR(50),
            in_description          VARCHAR(160)
        )
        """
       
        sql =  'CALL semen_source_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.semen_source_id
        
        sql += '%s,'    % data.pig_farm_id
        
        if data.boar_id is not None:
            sql += '%s,'    % data.boar_id
            
            sql += 'NULL,'
            sql += 'NULL,'
            
        else:
            sql += 'NULL,'
            
            sql += '%s,'    % data.semen_supplier_id
            sql += '%s,'    % data.pig_race_line_id
        
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
                
                'semen_source': {
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
    
    
    def get_list(self, account_id, inc_deleted = 0, inc_user_audit = 0, 
            minimum_info = 0):
        """
        Will get semen_source list.
        
        
        Returns
        -------
        list of dictionary

        """
        
        where_clause = 'WHERE a.account_id = %s' % account_id 
        
        if inc_deleted == 0:
            where_clause += ' AND (a.flag & 1) = 0' 
        
        
        if inc_user_audit == 0:
            
            if minimum_info == 0:
                sql =   """
                        SELECT 
                            a.id,
                            a.name,
                            a.description,
                            
                            a.boar_id,
                            b.number,
                            b.name AS boar_name,
                            
                            a.semen_supplier_id,
                            c.name AS semen_supplier_name,
                            
                            a.pig_race_line_id,
                            d.name AS pig_race_line_name
                            
                        FROM semen_source a 
                        LEFT OUTER JOIN sow_boar b          ON a.boar_id = b.id
                        LEFT OUTER JOIN semen_supplier c    ON a.semen_supplier_id = c.id
                        LEFT OUTER JOIN pig_race_line d     ON a.pig_race_line_id = d.id
                        
                        %s
                        """ % where_clause
            
            else:
                sql =   """
                        SELECT 
                            a.id,
                            a.name,
                            a.description
                            
                        FROM semen_source a 
                        %s
                        """ % where_clause
                    
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.name,
                        a.description,
                        
                        a.boar_id,
                        b.number,
                        b.name AS boar_name,
                        
                        a.semen_supplier_id,
                        c.name AS semen_supplier_name,
                        
                        a.pig_race_line_id,
                        d.name AS pig_race_line_name,
                        
                        
                        e.name_last,
                        e.name_first,
                        a.dt_entry,
                        
                        f.name_last,
                        f.name_first,
                        a.dt_last_update
                        
                    FROM semen_source a 
                    LEFT OUTER JOIN sow_boar b          ON a.boar_id = b.id
                    LEFT OUTER JOIN semen_supplier c    ON a.semen_supplier_id = c.id
                    LEFT OUTER JOIN pig_race_line d     ON a.pig_race_line_id = d.id
                    
                    LEFT OUTER JOIN user e              ON a.added_by_user_id   = e.id
                    LEFT OUTER JOIN user f              ON a.last_update_user_id = f.id
                
                    %s
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
                            'semen_source': {
                                'id':               row[0], 
                                'name':             row[1],
                                'description':      row[2]
                            },
                            
                            'boar': {
                                'id':               row[3],
                                'number':           row[4],
                                'name':             row[5]
                            },
                            
                            'external_semen': {
                                'supplier_id':      row[6],
                                'supplier_name':    row[7],
                            },
                            
                            'pig_race_line':{
                                'id':               row[8],
                                'name':             row[9]
                            }
                        }
                        
                    else:
                        cur_entry = {
                            'semen_source': {
                                'id':               row[0], 
                                'name':             row[1],
                                'description':      row[2]
                            }
                        }
                    
                else:
                    
                    cur_entry = {
                        'semen_source': {
                            'id':               row[0], 
                            'name':             row[1],
                            'description':      row[2]
                        },
                        
                        'boar': {
                            'id':               row[3],
                            'number':           row[4],
                            'name':             row[5]
                        },
                        
                        'external_semen': {
                            'supplier_id':      row[6],
                            'supplier_name':    row[7],
                        },
                        
                        'pig_race_line':{
                            'id':               row[8],
                            'name':             row[9]
                        }
                        
                        'added_by': {
                            'name_last':        row[10],
                            'name_first':       row[11],
                            'dt_entry':         str(row[12])
                        },
                        
                        'last_update':{
                            'name_last':        row[13],
                            'name_first':       row[14],
                            'dt_update':        str(row[15]) if row[15] else None
                        }
                        
                    }
                    
                    
                if 'boar' in cur_entry:
                    cur_id = cur_entry['boar']['id']
                    if cur_id is None or cur_id == 0:
                        del cur_entry['boar']
                    
                if 'external_semen' in cur_entry:
                    cur_id = cur_entry['external_semen']['supplier_id']
                    if cur_id is None or cur_id == 0:
                        del cur_entry['external_semen']
                       
                
                result.append(cur_entry)

        
        return result
    
    