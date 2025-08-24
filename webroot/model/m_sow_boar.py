# January 3, 2024
# Jack Wong

from common_constants       import *


class SowBoar:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SowBoar'

    
    def get_sow_status_list(self, is_dispose = 0):
        """
        Will get sow_status list.
        
        
        Returns
        -------
        list of dictionary

        """
        
        where_clause = ''
        if is_dispose > 0:
            where_clause = 'WHERE flag = 1'
        
        sql =   """
                SELECT 
                    id,
                    name
                FROM sow_status
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
            
            in_sow_boar_id          INT,
            in_birth_prod_id        INT,
            in_line_id              INT,
            in_sow_status_id        INT,
            
            in_number               VARCHAR(10),
            in_name                 VARCHAR(20),
            in_date_of_birth        VARCHAR(10),
            in_notes                VARCHAR(160)
        )    
        """
        
        sql =  'CALL sow_boar_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.sow_boar_id
        sql += '%s,'    % data.birth_prod_id
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        
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

    
    def dispose(self, data = None):
        """
        PROCEDURE sow_boar_dispose(
            in_user_id              INT,
            
            in_sow_boar_id          INT,
            in_dispose_status_id    INT,
            
            in_date_dispose         VARCHAR(10),
            in_dispose_notes        VARCHAR(160)
        )
        """
        
        sql =  'CALL sow_boar_dispose('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.sow_boar_id
        sql += '%s,'    % data.dispose_status_id
        
        
        sql += '"%s",'  % data.date_dispose
            
        if data.dispose_notes is not None:
            sql += '"%s");'   % data.dispose_notes
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
            msg = 'dispose(); error in executing query[] = ' + sql
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

    
    def get_list(self, farm_id, sex, inc_disposed = 0, 
            inc_user_audit = 0, list_sow_numbers = None, order_by = 0):
        """
        Will get sow_boar list.
        
        
        Returns
        -------
        list of dictionary
        
        order_by : int
            0 = ORDER BY date_of_birth DESC
            1 = ORDER BY id ASC

        """
        
        where_clause = ''
        if list_sow_numbers is not None:
            s = ''
            count = 0
            for cur_entry in list_sow_numbers:
                if count > 0: 
                    s += ','
                
                s += f"'{cur_entry}'"
                
            if sex is not None:
                values = (farm_id, sex, s)
                where_clause = ' WHERE a.pig_farm_id = %s AND a.sex = "%s" AND a.sow_number  IN (%s) ' % values
            else:
                where_clause = ' WHERE a.pig_farm_id = %s AND a.sow_number  IN (%s) '
            
        else:
            if sex is not None:
                if inc_disposed == 0:
                    values = (farm_id, sex)
                    where_clause = ' WHERE a.pig_farm_id = %s AND a.sex = "%s" AND (a.flag & 1) = 0 ' % values
                
                else:
                    values = (farm_id, sex)
                    where_clause = ' WHERE a.pig_farm_id = %s AND a.sex = "%s" ' % values
                
            else:
                
                if inc_disposed == 0:
                    values = (farm_id, sex)
                    where_clause = ' WHERE a.pig_farm_id = %s AND a.sex = "%s" AND (a.flag & 1) = 0 ' % values
                
                else:
                    values = (farm_id, sex)
                    where_clause = ' WHERE a.pig_farm_id = %s AND a.sex = "%s" ' % values
                
        
        if order_by == 0:
            order_clause = ' ORDER BY a.date_of_birth DESC '
        else:
            order_clause = ' ORDER BY a.id ASC '
               
               
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.farm_sow_id,
                        a.farm_boar_id,
                        a.number,
                        a.name,
                        a.flag,
                        a.birth_prod_id,
                        a.last_prod_id,
                       
                        b.name AS status_name,
                        a.date_of_birth,
                        a.date_dispose,
                        a.notes,
                        a.dispose_notes,
                        
                        a.dt_entry
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_status b    ON a.sow_status_id      = b.id
                    %s
                    %s 
                    """ % (where_clause, order_clause)
        
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.farm_sow_id,
                        a.farm_boar_id,
                        a.number,
                        a.name,
                        a.flag,
                        a.birth_prod_id,
                        a.last_prod_id,
                       
                        b.name AS status_name,
                        a.date_of_birth,
                        a.date_dispose,
                        a.notes,
                        a.dispose_notes,
                        
                        c.username,
                        c.name_last,
                        c.name_first,
                         a.dt_entry,
                        
                        d.username,
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_status b    ON a.sow_status_id      = b.id
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    %s 
                    """ % (where_clause, order_clause)
        
        
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
                        'farm_sow_id':          row[1],
                        'farm_boar_id':         row[2],
                        'number':               row[3], 
                        'name':                 row[4],
                        'flag':                 row[5],
                        'birth_prod_id':        row[6],
                        'last_prod_id':         row[7],
                        
                        'status':               row[8],
                        'date_of_birth':        str(row[9]) if row[9] else None,
                        'date_dispose':         str(row[10]) if row[10] else None,
                        'notes':                row[11],
                        'dispose_notes':        row[12],
                    
                        'dt_entry':             str(row[13])
                    }
                     
                else:
                    cur_entry = {
                        'id':                   row[0],
                        'farm_sow_id':          row[1],
                        'farm_boar_id':         row[2],
                        'number':               row[3], 
                        'name':                 row[4],
                        'flag':                 row[5],
                        'birth_prod_id':        row[6],
                        'last_prod_id':         row[7],
                        
                        'status':               row[8],
                        'date_of_birth':        str(row[9]) if row[9] else None,
                        'date_dispose':         str(row[10]) if row[10] else None,
                        'notes':                row[11],
                        'dispose_notes':        row[12],
                        
                        'added_by': {
                            'username':         row[13],
                            'name_last':        row[14],
                            'name_first':       row[15],
                            'dt_entry':         str(row[16])
                        },
                        
                        'last_update':{
                            'username':         row[17],
                            'name_last':        row[18],
                            'name_first':       row[19],
                            'dt_update':        row[20]
                        }                    
                    }
                    
            
                if sex is not None:
                    if sex == 'F':
                        del cur_entry['farm_boar_id']
                    else:
                        del cur_entry['farm_sow_id']

                
                result.append(cur_entry)

        
        return result


    