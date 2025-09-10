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
    
    
    def get_list(self, account_id, inc_deleted = 0, inc_user_audit = 0):
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
            
            sql =   """
                    SELECT 
                        a.id,
                        a.pig_farm_id,
                        b.name AS farm_name,
                        
                        a.flag,
                        
                        a.boar_id,
                        c.number,
                        c.name AS boar_name,
                        
                        a.semen_supplier_id,
                        d.name AS semen_supplier_name,
                        
                        a.pig_race_line_id,
                        e.name AS pig_race_line_name,
                        
                        a.name,
                        a.description,
                        
                        a.dt_entry
                        
                    FROM semen_source a 
                    LEFT OUTER JOIN pig_farm b          ON a.pig_farm_id = b.id
                    LEFT OUTER JOIN sow_boar c          ON a.boar_id = c.id
                    LEFT OUTER JOIN semen_supplier d    ON a.semen_supplier_id = d.id
                    LEFT OUTER JOIN pig_race_line e     ON a.pig_race_line_id = e.id
                    
                    %s
                    """ % where_clause
                    
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.pig_farm_id,
                        b.name AS farm_name,
                        
                        a.flag,
                        
                        a.boar_id,
                        c.number,
                        c.name AS boar_name,
                        
                        a.semen_supplier_id,
                        d.name AS semen_supplier_name,
                        
                        a.pig_race_line_id,
                        e.name AS pig_race_line_name,
                        
                        a.name,
                        a.description,
                        
                        f.name_last,
                        f.name_first,
                        a.dt_entry,
                        
                        g.name_last,
                        g.name_first,
                        a.dt_last_update
                        
                    FROM semen_source a 
                    LEFT OUTER JOIN pig_farm b          ON a.pig_farm_id = b.id
                    LEFT OUTER JOIN sow_boar c          ON a.boar_id = c.id
                    LEFT OUTER JOIN semen_supplier d    ON a.semen_supplier_id = d.id
                    LEFT OUTER JOIN pig_race_line e     ON a.pig_race_line_id = e.id
                    
                    LEFT OUTER JOIN user f              ON a.added_by_user_id   = f.id
                    LEFT OUTER JOIN user g              ON a.last_update_user_id = g.id
                
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
               
                    cur_entry = {
                        'id':                   row[0], 
                        
                        'pig_farm': {
                            'id':               row[1],
                            'name':             row[2]
                        },
                        
                        'flag':                 row[3],
                        
                        'boar': {
                            'id':               row[4],
                            'number':           row[5],
                            'name':             row[6]
                        },
                        
                        'external_semen': {
                            'supplier_id':      row[7],
                            'supplier_name':    row[8],
                            
                            'pig_race_line':{
                                'id':           row[9],
                                'name':         row[10]
                            }
                        },
                        
                        
                        'name':                 row[11],
                        'description':          row[12],
                        
                        'dt_entry':             row[13]
                        
                    }
                    
                else:
                    
                    cur_entry = {
                        'id':                   row[0], 
                        
                        'pig_farm': {
                            'id':               row[1],
                            'name':             row[2]
                        },
                        
                        'flag':                 row[3],
                        
                        'boar': {
                            'id':               row[4],
                            'number':           row[5],
                            'name':             row[6]
                        },
                        
                        'external_semen': {
                            'supplier_id':      row[7],
                            'supplier_name':    row[8],
                            
                            'pig_race_line':{
                                'id':           row[9],
                                'name':         row[10]
                            }
                        },
                        
                        
                        'name':                 row[11],
                        'description':          row[12],
                        
                        'added_by': {
                            'name_last':        row[13],
                            'name_first':       row[14],
                            'dt_entry':         row[15]
                        },
                        
                        'last_update':{
                            'name_last':        row[16],
                            'name_first':       row[17],
                            'dt_update':        str(row[18]) if row[18] else None
                        }
                        
                    }
                    
                
                cur_boar_id = cur_entry['boar']['id']
                if cur_boar_id is None or cur_boar_id == 0:
                    del cur_entry['boar']
                    
                cur_semen_supplier_id = cur_entry['external_semen']['supplier_id']
                if cur_semen_supplier_id is None or cur_semen_supplier_id == 0:
                    del cur_entry['external_semen']
                   
                
                result.append(cur_entry)

        
        return result
    
    