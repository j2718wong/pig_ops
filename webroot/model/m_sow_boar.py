# January 3, 2024
# Jack Wong

from common_constants       import *


class SowBoar:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SowBoar'

    
    def get_sow_status_list(self):
        """
        Will get sow_status list.
        
        
        Returns
        -------
        list of dictionary

        """
            
        sql =   """
                SELECT 
                    id,
                    name
                FROM sow_status
                """ 
        
        
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
            conn.close()
            
        except Exception as e:
            msg = 'get_sow_status_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            for row in rows:
                cur_status_id           = row[0]
                cur_status_name         = row[1]
                
                cur_entry = {
                    'id':               cur_status_id, 
                    'name':             cur_status_name
                }
                
                result.append(cur_entry)

        return result

    
    def add(self, data = None):
        """
        PROCEDURE sow_boar_add(
            in_user_id              INT,
            
            in_pig_farm_id          INT,
            in_birth_prod_id        INT,
            in_line_id              INT,
            in_sow_status_id        INT,
            
            in_sex                  CHAR(1),
                    
            in_number               VARCHAR(10),
            in_name                 VARCHAR(20),
            in_date_of_birth        VARCHAR(10),
            in_description          VARCHAR(160)
        )    
        """
        
        sql =  'CALL sow_boar_add('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_farm_id
        sql += '%s,'    % data.birth_prod_id
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        
        sql += '"%s",'  % data.sex
        
        sql += '"%s",'  % data.number
        
        if data.name is not None:
            sql += '"%s",'    % data.name
        else:
            sql += 'NULL,'
            
        if data.date_of_birth is not None:
            sql += '"%s",'    % data.date_of_birth
        else:
            sql += 'NULL,'            
            
        if data.notes is not None:
            sql += '%s);'   % data.notes
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
                
                'sow_boar': {
                    'id':               row[3],
                    'farm_sow_id':      row[4],
                    'farm_boar_id':     row[5]
                }
            }

        return None

    
    def update(self, data = None):
        """
        PROCEDURE sow_boar_update(
            in_user_id              INT,
            
            in_sow_id               INT,
            in_birth_prod_id        INT,
            in_line_id              INT,
            in_sow_status_id        INT,
            
            in_sow_number           VARCHAR(10),
            in_sow_name             VARCHAR(20),
            in_date_of_birth        VARCHAR(10),
            in_description          VARCHAR(160)
        )    
        """
        
        sql =  'CALL sow_boar_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.sow_boar_id
        sql += '%s,'    % data.birth_prod_id
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        
        sql += '"%s",'  % data.sow_number
        
        if data.sow_name is not None:
            sql += '"%s",'    % data.sow_name
        else:
            sql += 'NULL,'
            
        if data.date_of_birth is not None:
            sql += '"%s",'    % data.date_of_birth
        else:
            sql += 'NULL,'            
            
        if data.notes is not None:
            sql += '%s);'   % data.notes
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
                
                'sow_boar': {
                    'id':               row[3]
                }
            }

        return None

    
    def cull(self, data = None):
        """
        PROCEDURE sow_cull(
            in_user_id              INT,
            
            in_sow_id               INT,
            in_date_culled          VARCHAR(10),
            in_cull_notes           VARCHAR(160)
        )
        """
        
        sql =  'CALL sow_cull('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.sow_id
        
        sql += '"%s",'  % data.date_culled
            
        if data.cull_notes is not None:
            sql += '%s);'   % data.cull_notes
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
                
                'sow': {
                    'id':               row[3]
                }
            }

        return None

    
    def get_sow_boar_list(self, farm_id, sex, list_sow_numbers = None):
        """
        Will get sow_boar list.
        
        
        Returns
        -------
        list of dictionary

        """
        
        where_clause = ''
        if list_sow_numbers is not None:
            s = ''
            count = 0
            for cur_entry in list_sow_numbers:
                if count > 0: 
                    s += ','
                
                s += f"'{cur_entry}'"
                
            values = (farm_id, sex, s)
            where_clause = ' WHERE a.pig_farm_id = %s AND a.sex = "%s" AND a.sow_number  IN (%s) ' % values
        
        else:
            values = (farm_id, sex)
            where_clause = ' WHERE a.pig_farm_id = %s AND a.sex = "%s" ' % values
        
        if sex == 'F':
            sql =   """
                    SELECT 
                        a.id,
                        a.farm_sow_id,
                        a.number,
                        a.name,
                        a.flag,
                        a.birth_prod_id,
                        a.last_prod_id,
                       
                        b.name AS status_name,
                        a.date_of_birth,
                        a.date_culled,
                        a.notes,
                        
                        c.username,
                        c.name_last,
                        c.name_first,
                        
                        d.username,
                        d.name_last,
                        d.name_first,
                        a.dt_last_update,
                        
                        a.dt_entry
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_status b    ON a.sow_status_id      = b.id
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    ORDER BY a.date_of_birth DESC
                    """ % where_clause
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.farm_boar_id,
                        a.number,
                        a.name,
                        a.flag,
                        a.birth_prod_id,
                        a.last_prod_id,
                       
                        b.name AS status_name,
                        a.date_of_birth,
                        a.date_culled,
                        a.notes,
                        
                        c.username,
                        c.name_last,
                        c.name_first,
                        
                        d.username,
                        d.name_last,
                        d.name_first,
                        a.dt_last_update,
                        
                        a.dt_entry
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_status b    ON a.sow_status_id      = b.id
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    ORDER BY a.date_of_birth DESC
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
            conn.close()
            
        except Exception as e:
            msg = 'get_sow_boar_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_id                  = row[0]
                cur_farm_sow_boar_id    = row[1]
                cur_number              = row[2]
                cur_name                = row[3]
                cur_flag                = row[4]
                cur_birth_prod_id       = row[5]
                cur_last_prod_id        = row[6]
                
                cur_status              = row[7]
                
                cur_date_of_birth       = None
                if row[8] is not None:
                    cur_date_of_birth   = str(row[8])
                    
                cur_date_culled         = None
                if row[9] is not None:
                    cur_date_culled     = str(row[9])
                
                cur_notes               = None
                if row[10] is not None:
                    cur_notes           = row[10]
                    
                cur_user_username       = row[11]
                cur_user_name_last      = row[12]
                cur_user_name_first     = row[13]
                
                cur_upd_user_username   = row[14]
                cur_upd_user_name_last  = row[15]
                cur_upd_user_name_first = row[16]
                
                cur_dt_last_update      = None
                if row[17] is not None:
                    cur_dt_last_update  = str(row[17])
                
                cur_dt_entry            = str(row[18])
                
                if sex == 'F':
                    cur_entry = {
                        'id':               cur_id,
                        'farm_sow_id':      cur_farm_sow_boar_id,
                        'number':           cur_number, 
                        'name':             cur_name,
                        'flag':             cur_flag,
                        'birth_prod_id':    cur_birth_prod_id,
                        'last_prod_id':     cur_last_prod_id,
                        
                        'status':           cur_status,
                        'date_of_birth':    cur_date_of_birth,
                        'date_culled':      cur_date_culled,
                        'notes':            cur_notes,
                        
                        'added_by': {
                            'username':     cur_user_username,
                            'name_last':    cur_user_name_last,
                            'name_first':   cur_user_name_first
                        },
                        
                        'dt_entry':         cur_dt_entry
                    }
                
                else:
                    cur_entry = {
                        'id':               cur_id,
                        'farm_boar_id':      cur_farm_sow_boar_id,
                        'number':           cur_number, 
                        'name':             cur_name,
                        'flag':             cur_flag,
                        'birth_prod_id':    cur_birth_prod_id,
                        'last_prod_id':     cur_last_prod_id,
                        
                        'status':           cur_status,
                        'date_of_birth':    cur_date_of_birth,
                        'date_culled':      cur_date_culled,
                        'notes':            cur_notes,
                        
                        'added_by': {
                            'username':     cur_user_username,
                            'name_last':    cur_user_name_last,
                            'name_first':   cur_user_name_first
                        },
                        
                        'dt_entry':         cur_dt_entry
                    }
                    
                
                if cur_upd_user_username is not None:
                    last_update = {
                        'username':     cur_upd_user_username,
                        'name_last':    cur_upd_user_name_last,
                        'name_first':   cur_upd_user_name_first,
                        'dt_update':    cur_dt_last_update
                    }
                    
                    cur_entry['last_update'] = last_update
                else:
                    cur_entry['last_update'] = {}
                
                result.append(cur_entry)

        
        return result


    