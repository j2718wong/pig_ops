# January 3, 2024
# Jack Wong

from common_constants       import *


"""
sow_boar.flag bits
0 = is_disposed
1 = is_external 
2 = is_production_ready

"""

FLAG_BIT_SOW_BOAR_IS_DISPOSED           = 1
FLAG_BIT_SOW_BOAR_IS_EXTERNAL           = 2
FLAG_BIT_SOW_BOAR_IS_PRODUCTION_READY   = 4
        

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
            #conn.close()
            
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
            in_farm_birth_prod_id   INT,
            in_line_id              INT,
            in_sow_status_id        INT,
            
            in_sex                  CHAR(1),
            in_num_nipples          INT,
            in_is_external          INT,
            in_is_production_ready  INT,
                    
            in_number               VARCHAR(10),
            in_name                 VARCHAR(20),
            in_date_of_birth        VARCHAR(10),
            in_date_eartag          VARCHAR(10),
            in_description          VARCHAR(160)
        )    
        """
        
        sql =  'CALL sow_boar_add('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_farm_id
        sql += '%s,'    % data.farm_birth_prod_id
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        
        sql += '"%s",'  % data.sex
        
        if data.num_nipples is not None:
            sql += '%s,'  % data.num_nipples
        else:
            sql += 'NULL,'
        
        
        sql += '%s,'    % data.is_external
        sql += '%s,'    % data.is_production_ready
        
        if data.number is not None and len(data.number) > 0:
            sql += '"%s",'  % data.number
        else:
            sql += 'NULL,'
        
        if data.name is not None and len(data.name) > 0:
            sql += '"%s",'    % data.name
        else:
            sql += 'NULL,'
            
        if data.date_of_birth is not None and len(data.date_of_birth) > 0:
            sql += '"%s",'    % data.date_of_birth
        else:
            sql += 'NULL,'            
            
        if data.date_eartag is not None and len(data.date_eartag) > 0:
            sql += '"%s",'    % data.date_eartag
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
                    'farm_boar_id':     row[5],
                    'is_external':      data.is_external,
                    'is_production_ready': data.is_production_ready
                }
            }

        return None

    
    def update(self, data = None):
        """
        PROCEDURE sow_boar_update(
            in_user_id              INT,
            
            in_sow_boar_id          INT,
            in_farm_birth_prod_id   INT,
            in_line_id              INT,
            in_sow_status_id        INT,
            in_is_external          INT,
            in_is_production_ready  INT,
            
            in_number               VARCHAR(10),
            in_name                 VARCHAR(20),
            in_date_of_birth        VARCHAR(10),
            in_date_eartag          VARCHAR(10),
            in_notes                VARCHAR(160)
        )    
        """
        
        sql =  'CALL sow_boar_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.sow_boar_id
        sql += '%s,'    % data.farm_birth_prod_id
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        sql += '%s,'    % data.is_external
        sql += '%s,'    % data.is_production_ready
        
        if data.number is not None and len(data.number) > 0:
            sql += '"%s",'  % data.number
        else:
            sql += 'NULL,'
        
        if data.name is not None and len(data.name) > 0:
            sql += '"%s",'    % data.name
        else:
            sql += 'NULL,'
            
        if data.date_of_birth is not None:
            sql += '"%s",'    % data.date_of_birth
        else:
            sql += 'NULL,'            
            
        if data.date_eartag is not None and len(data.date_eartag) > 0:
            sql += '"%s",'    % data.date_eartag
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

    
    def get_list(self, farm_id, sex = None, is_disposed = 0, inc_external = 0,
            is_production_ready = None, inc_user_audit = 0,
            minimum_info = 0, order_by = 0):
        """
        Will get sow_boar list.
        
        Parameters
        ----------
        
        sex : char
            M = returns boar
            F = returns gilts/sows
            
        is_disposed : int
            0 = returns active sow/boar
            1 = returns disposed sow/boar
            
        inc_external : int
            include external sow/ boar
            0 = do not include external
            1 = include external
        
        is_production_ready : int
            None = will include both growing and production ready sow, boar
            0 = still growing gilts, boar 
            1 = ready for mating
            
        
        order_by : int
            0 = ORDER BY date_of_birth DESC
            1 = ORDER BY name ASC, number ASC

            
        
        Returns
        -------
        list of dictionary
        
        
        """
        
       
        where_clause = 'WHERE a.pig_farm_id = %s ' % farm_id
        
        if is_disposed == 0:
            where_clause += ' AND a.is_disposed = 0 '
            
            if is_production_ready is not None:
            
                if is_production_ready == 0:
                    where_clause += ' AND a.is_production_ready = 0 '
                    
                    if sex is not None:
                        where_clause += ' AND a.sex = "%s" ' % sex
                else:
                    # production_ready >0, sex is not optional
                    where_clause += ' AND a.is_production_ready = 1 AND a.sex = "%s" '% sex
                    

                    if inc_external == 0:
                        where_clause += ' AND a.is_external = 0 '
                    
                    # if inc_external == 1, sow_boar.is_external will not matter
            else:
                if sex is not None:
                    where_clause += ' AND a.sex = "%s" ' % sex
                
                if inc_external == 0:
                    where_clause += ' AND a.is_external = 0 '
                    
                # if inc_external == 1, sow_boar.is_external will not matter
                
        else:
            # is_disposed > 0
            
            if sex is None:
                where_clause += ' AND a.is_disposed = 1' 
                
            else:
                values = (sex)
                where_clause += ' AND a.sex = "%s" AND a.is_disposed = 1' % values
                
        
        if order_by == 0:
            order_clause = ' ORDER BY a.date_of_birth DESC '
        else:
            order_clause = ' ORDER BY a.name ASC, a.number ASC'
               
               
        if inc_user_audit == 0:
            if minimum_info == 0:
                sql =   """
                        SELECT 
                            a.id,
                            a.farm_sow_id,
                            a.farm_boar_id,
                            a.number,
                            a.name,
                            
                            a.is_disposed,
                            a.is_external,
                            a.is_production_ready,
                            
                            a.farm_birth_prod_id,
                            a.last_prod_id,
                           
                            b.name AS status_name,
                            a.date_of_birth,
                            a.date_eartag,
                            a.date_dispose,
                            c.notes AS add_notes,
                            d.notes AS dispose_notes
                            
                        FROM sow_boar a
                        LEFT OUTER JOIN sow_status b        ON a.sow_status_id     = b.id
                        LEFT OUTER JOIN pig_prod_notes c    ON a.add_notes_id      = c.id
                        LEFT OUTER JOIN pig_prod_notes d    ON a.dispose_notes_id  = d.id
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
                           
                            a.sow_status_id,
                            a.date_of_birth,
                            
                            a.is_external,
                            
                            b.date_insemination,
                            b.date_expected_birth
                            
                        FROM sow_boar a
                        LEFT OUTER JOIN pig_production b    ON a.last_prod_id       = b.id
                        
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
                        
                        a.is_disposed,
                        a.is_external,
                        a.is_production_ready,
                        
                        a.farm_birth_prod_id,
                        a.last_prod_id,
                       
                        b.name AS status_name,
                        a.date_of_birth,
                        a.date_eartag,
                        a.date_dispose,
                        c.notes AS add_notes,
                        d.notes AS dispose_notes,
                        
                        e.name_last,
                        e.name_first,
                        a.dt_entry,
                        
                        f.name_last,
                        f.name_first,
                        a.dt_last_update
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_status b        ON a.sow_status_id      = b.id
                    LEFT OUTER JOIN pig_prod_notes c    ON a.add_notes_id      = c.id
                    LEFT OUTER JOIN pig_prod_notes d    ON a.dispose_notes_id  = d.id
                    LEFT OUTER JOIN user e              ON a.added_by_user_id   = e.id
                    LEFT OUTER JOIN user f              ON a.last_update_user_id = f.id
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
                            'id':                   row[0],
                            'farm_sow_id':          row[1],
                            'farm_boar_id':         row[2],
                            'number':               row[3], 
                            'name':                 row[4],
                            
                            'is_disposed':          row[5],
                            'is_external':          row[6],
                            'is_production_ready':  row[7],
                            
                            'farm_birth_prod_id':   row[8],
                            'last_prod_id':         row[9],
                            
                            'status':               row[10],
                            'date_of_birth':        str(row[11])  if row[11] else None,
                            'date_eartag':          str(row[12])  if row[12] else None,
                            'date_dispose':         str(row[13])  if row[13] else None,
                            'notes':                row[14],
                            'dispose_notes':        row[15]
                        }
                    
                    else:
                        cur_entry = {
                            'id':                   row[0],
                            'farm_sow_id':          row[1],
                            'farm_boar_id':         row[2],
                            'number':               row[3], 
                            'name':                 row[4],
                            'status_id':            row[5],
                            'date_of_birth':        str(row[6])  if row[6] else None,
                            'is_external':          row[7],
                            'date_insemination':    str(row[8])  if row[8] else None
                            'date_expected_birth':  str(row[9])  if row[9] else None
                        }
                    
                    if sex is not None:
                        if sex == 'F':
                            del cur_entry['farm_boar_id']
                        else:
                            del cur_entry['farm_sow_id']
                            del cur_entry['status'] # This refers to sow_status
                
                else:
                    
                    
                    cur_entry = {
                        'sow_boar': {
                            'id':                   row[0],
                            'farm_sow_id':          row[1],
                            'farm_boar_id':         row[2],
                            'number':               row[3], 
                            'name':                 row[4],
                            
                            'is_disposed':          row[5],
                            'is_external':          row[6],
                            'is_production_ready':  row[7],
                            
                            'farm_birth_prod_id':   row[8],
                            'last_prod_id':         row[9],
                            
                            'status':               row[10],
                            'date_of_birth':        str(row[11])  if row[11] else None,
                            'date_eartag':          str(row[12])  if row[12] else None,
                            'date_dispose':         str(row[13])  if row[13] else None,
                            'notes':                row[14],
                            'dispose_notes':        row[15]
                        },
                        
                        'added_by': {
                            'name_last':        row[16],
                            'name_first':       row[17],
                            'dt_entry':         str(row[18])
                        },
                        
                        'last_update':{
                            'name_last':        row[19],
                            'name_first':       row[20],
                            'dt_update':        str(row[21]) if row[21] else None
                        }                    
                    }
                    
            
                    if sex is not None:
                        if sex == 'F':
                            del cur_entry['sow_boar']['farm_boar_id']
                        else:
                            del cur_entry['sow_boar']['farm_sow_id']
                            del cur_entry['sow_boar']['status'] # This refers to sow_status
                
                result.append(cur_entry)

        
        return result


    