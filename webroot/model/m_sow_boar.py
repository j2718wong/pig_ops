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
            in_line_id              INT,
            in_sow_status_id        INT,
            
            in_sex                  CHAR(1),
            in_num_nipples          INT,
            in_is_external          INT,
            in_is_production_ready  INT,
            
            in_parent_sow_id        INT,
            in_parent_boar_id       INT,
    
                    
            in_number               VARCHAR(10),
            in_name                 VARCHAR(20),
            in_date_of_birth        VARCHAR(10),
            in_description          VARCHAR(160)
        )    
        """
        
        sql =  'CALL sow_boar_add('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_farm_id
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        
        sql += '"%s",'  % data.sex
        
        if data.num_nipples is not None and data.num_nipples > 0:
            sql += '%s,'  % data.num_nipples
        else:
            sql += 'NULL,'
        
        
        sql += '%s,'    % data.is_external
        sql += '%s,'    % data.is_production_ready
        
        if data.parent_sow_id > 0:
            sql += '%s,'    % data.parent_sow_id
        else:
            sql += 'NULL,'
            
        if data.parent_boar_id > 0:
            sql += '%s,'    % data.parent_boar_id
        else:
            sql += 'NULL,'
        
        
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
            in_line_id              INT,
            in_sow_status_id        INT,
            in_is_external          INT,
            in_is_production_ready  INT,
            
            in_parent_sow_id        INT,
            in_parent_boar_id       INT,
    
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
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        sql += '%s,'    % data.is_external
        sql += '%s,'    % data.is_production_ready
        
        
        if data.parent_sow_id > 0:
            sql += '%s,'    % data.parent_sow_id
        else:
            sql += 'NULL,'
            
        if data.parent_boar_id > 0:
            sql += '%s,'    % data.parent_boar_id
        else:
            sql += 'NULL,'
        
        
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
        
        print(sql)
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
            
            sow_boar_id = row[3]
            
            res_update = {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2]
                }
            }
            
            sow_boar_list = self.get_list(sow_boar_id = sow_boar_id)
            
            # return whole sow_boar
            if sow_boar_list is not None:
                res_update['sow_boar'] = sow_boar_list[0]['sow_boar']
            
            
            return res_update;

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

    
    def get_entry(self, sow_boar_id):
        sql =   """
                SELECT 
                    id,
                    farm_sow_id,
                    farm_boar_id,
                    number,
                    name,
                    sex,
                    sow_status_id
                    
                FROM sow_boar 
                WHERE id = %s
                """ % sow_boar_id
        
        
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
        
        
        except Exception as e:
            msg = 'get_entry(); error in executing query[] = ' + sql
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
                    'id':                   row[0],
                    'farm_sow_id':          row[1],
                    'farm_boar_id':         row[2],
                    'number':               row[3], 
                    'name':                 row[4],
                    'sex':                  row[5],
                    'sow_status_id':        row[6]
                }
                
                return cur_entry

        
        return None

    
    def get_list(self, pig_farm_id = None, sex = None, sow_boar_id = None, 
            inc_user_audit = 0, order_by = 0):
        """
        Will get sow_boar list.
        
        Parameters
        ----------
        
        sex : char
            M = returns boar
            F = returns gilts/sows
            

        order_by : int
            0 = ORDER BY date_of_birth DESC
            1 = ORDER BY name ASC, number ASC

            
        
        Returns
        -------
        list of dictionary
        
        
        """
       
        if sow_boar_id is None:
            where_clause = 'WHERE a.pig_farm_id = %s ' % pig_farm_id
            where_clause += ' AND a.is_disposed = 0 '
            
            if sex is not None:
                where_clause += ' AND a.sex = "%s" ' % sex
            
            
            if order_by == 0:
                order_clause = ' ORDER BY a.date_of_birth DESC '
            else:
                order_clause = ' ORDER BY a.name ASC, a.number ASC'
        
        else:
            where_clause = 'WHERE a.id = %s ' % sow_boar_id
            order_clause = ''
               
        if inc_user_audit == 0:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.farm_sow_id,
                        a.farm_boar_id,
                        a.number,
                        a.name,
                       
                        a.sow_status_id,
                        a.birth_pig_prod_id,
                        
                        a.parent_sow_id,
                        b.number,
                        b.name,
                       
                        a.parent_boar_id,
                        c.number,
                        c.name,
                        
                        a.date_of_birth,
                        a.date_eartag,
                        
                        a.is_external,
                        a.is_production_ready,
                        
                        a.num_nipples,
                        
                        d.farm_prod_id,
                        d.date_insemination,
                        d.date_expected_birth,
                        
                        a.last_mate_sow_boar_id,
                        a.mate_count,
                        a.date_last_mate,
                        
                        e.notes AS add_notes
                        
                        
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_boar b          ON a.parent_sow_id          = b.id
                    LEFT OUTER JOIN sow_boar c          ON a.parent_boar_id         = c.id
                    LEFT OUTER JOIN pig_production d    ON a.last_pig_production_id  = d.id
                    LEFT OUTER JOIN pig_prod_notes e    ON a.add_notes_id           = e.id
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
                        a.birth_pig_prod_id,
                        
                        a.parent_sow_id,
                        b.number,
                        b.name,
                       
                        a.parent_boar_id,
                        c.number,
                        c.name,
                        
                        a.date_of_birth,
                        a.date_eartag,
                        
                        a.is_external,
                        a.is_production_ready,
                        
                        a.num_nipples,
                        
                        d.farm_prod_id,
                        d.date_insemination,
                        d.date_expected_birth,
                        
                        a.last_mate_sow_boar_id,
                        a.mate_count,
                        a.date_last_mate,
                        
                        e.notes AS add_notes
                        
                        
                        f.name_last,
                        f.name_first,
                        a.dt_entry,
                        
                        g.name_last,
                        g.name_first,
                        a.dt_last_update
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_boar b          ON a.parent_sow_id          = b.id
                    LEFT OUTER JOIN sow_boar c          ON a.parent_boar_id         = c.id
                    LEFT OUTER JOIN pig_production d    ON a.last_pig_production_id = d.id
                    LEFT OUTER JOIN pig_prod_notes e    ON a.add_notes_id       = e.id
                    LEFT OUTER JOIN user f              ON a.added_by_user_id   = f.id
                    LEFT OUTER JOIN user g              ON a.last_update_user_id = g.id
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
               
                sow_boar = {
                    'id':                   row[0],
                    'farm_sow_id':          row[1],
                    'farm_boar_id':         row[2],
                    'number':               row[3], 
                    'name':                 row[4],
                    
                    'status_id':            row[5],
                    'birth_pig_prod_id':    row[6],
                    
                    'parent_sow_id':        row[7],
                    'parent_sow_name':      row[8],
                    'parent_sow_number':    row[9],
                    
                    'parent_boar_id':       row[10],
                    'parent_boar_name':     row[11],
                    'parent_boar_number':   row[12],
                    
                    'date_of_birth':        str(row[13])  if row[13] else None,
                    'date_eartag':          str(row[14])  if row[14] else None,
                    
                    'is_external':          row[15],
                    'is_production_ready':  row[16],
                    
                    'num_nipples':          row[17],
                    
                    'last_farm_prod_id':    row[18],
                    'date_insemination':    str(row[19]) if row[19] else None,
                    'date_expected_birth':  str(row[20]) if row[20] else None,
                    
                    'last_mate_sow_boar_id': row[21],
                    'mate_count':           row[22],
                    'date_last_mate':       str(row[23]) if row[23] else None,
                  
                    'add_notes':            row[24]
                }
                
                if sex is not None:
                    if sex == 'F':
                        del sow_boar['farm_boar_id']
                        del sow_boar['is_external']
                        
                        if sow_boar['num_nipples'] is None:
                            del sow_boar['num_nipples']
                            
                        if sow_boar['date_insemination'] is None:
                            del sow_boar['date_insemination']
                            
                        if sow_boar['date_expected_birth'] is None:
                            del sow_boar['date_expected_birth']
                            
                        
                    else:
                        # These are for sow only
                        del sow_boar['farm_sow_id'] 
                        del sow_boar['status_id']
                        del sow_boar['num_nipples'] 
                        del sow_boar['date_insemination'] 
                        del sow_boar['date_expected_birth']
            
                
                # Remove null entries if possible
                if sow_boar['parent_sow_id'] is None:
                    del sow_boar['parent_sow_id']
                    del sow_boar['parent_sow_name']
                    del sow_boar['parent_sow_number']
                    
                    
                if sow_boar['parent_boar_id'] is None:
                    del sow_boar['parent_boar_id']
                    del sow_boar['parent_boar_name']
                    del sow_boar['parent_boar_number']
                    
                    
                if sow_boar['date_eartag'] is None:
                    del sow_boar['date_eartag']
                
                if sow_boar['last_farm_prod_id'] is None:
                   del sow_boar['last_farm_prod_id']
                
                if sow_boar['last_mate_sow_boar_id'] is None:
                    del sow_boar['last_mate_sow_boar_id']
                
                if sow_boar['date_last_mate'] is None:
                    del sow_boar['date_last_mate']
                
                if sow_boar['add_notes'] is None:
                    del sow_boar['add_notes']
                
                
                
                if inc_user_audit > 0:
                    
                    cur_entry = {'sow_boar': sow_boar}
                    
                    added_by = {
                        'name_last':        row[25],
                        'name_first':       row[26],
                        'dt_entry':         str(row[27])
                    }
                    
                    last_update:{
                        'name_last':        row[28],
                        'name_first':       row[29],
                        'dt_update':        str(row[30]) if row[30] else None
                    }
                
                    cur_entry['added_by']    = added_by
                    cur_entry['last_update'] = last_update
                            
                
                cur_entry = {'sow_boar': sow_boar}
                    
                result.append(cur_entry)

        
        return result


    def get_list_disposed(self, farm_id):
        """
        Dedicated query for disposed pigs. This will return maximum information
        bacuse the user edit is also returned. This will return both sows and 
        boars.
        
        Parameters
        ----------
        
        
        Returns
        -------
        list of dictionary
        
        
        """
        
       
            
        sql =   """
                SELECT 
                    a.id,
                    a.farm_sow_id,
                    a.farm_boar_id,
                    a.number,
                    a.name,
                    a.sex,
                    
                    a.is_external,
                    a.is_production_ready,
                    
                    b.farm_prod_id,
                    
                    a.num_nipples,
                    
                    a.last_mate_sow_boar_id,
                    a.mate_count, 
                   
                    a.sow_status_id,
                    a.dispose_status_id,
                    
                    a.date_of_birth,
                    a.date_eartag,
                    a.date_dispose,
                    a.date_last_mate,
                    
                    c.notes AS add_notes,
                    d.notes AS dispose_notes,
                    
                    e.name_last,
                    e.name_first,
                    a.dt_entry,
                    
                    f.name_last,
                    f.name_first,
                    a.dt_last_update
                    
                FROM sow_boar a
                LEFT OUTER JOIN pig_production b    ON a.last_pig_production_id = b.id
                LEFT OUTER JOIN pig_prod_notes c    ON a.add_notes_id      = c.id
                LEFT OUTER JOIN pig_prod_notes d    ON a.dispose_notes_id  = d.id
                LEFT OUTER JOIN user e              ON a.added_by_user_id   = e.id
                LEFT OUTER JOIN user f              ON a.last_update_user_id = f.id
                WHERE a.pig_farm_id = %s AND is_disposed = 1
                ORDER BY a.date_dispose DESC;
                """ % farm_id
        
        
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
                cur_sex     = row[5]
                
                cur_entry = {
                    'sow_boar': {
                        'id':                   row[0],
                        'farm_sow_id':          row[1],
                        'farm_boar_id':         row[2],
                        'number':               row[3], 
                        'name':                 row[4],
                        'sex':                  row[5],
                        
                        'is_external':          row[6],
                        'is_production_ready':  row[7],
                        
                        
                        'last_prod_id':         row[8],
                        
                        'num_nipples':          row[9],
                        
                        'last_mate_sow_boar_id':row[10],
                        'mate_count':           row[11],
                                                
                        'status_id':            row[12],
                        'dispose_status_id':    row[13],
                        
                        'date_of_birth':        str(row[14])  if row[14] else None,
                        'date_eartag':          str(row[15])  if row[15] else None,
                        'date_dispose':         str(row[16])  if row[16] else None,
                        'date_last_mate':       str(row[17])  if row[17] else None,
                        
                        'add_notes':            row[18],
                        'dispose_notes':        row[19]
                    },
                    
                    'added_by': {
                        'name_last':        row[20],
                        'name_first':       row[21],
                        'dt_entry':         str(row[22])
                    },
                    
                    'last_update':{
                        'name_last':        row[23],
                        'name_first':       row[24],
                        'dt_update':        str(row[25]) if row[25] else None
                    }                    
                }
                
                if cur_sex == 'F':
                    del cur_entry['sow_boar']['farm_boar_id']
                    del cur_entry['sow_boar']['is_external']
                else:
                    # These are for sow only
                    del cur_entry['sow_boar']['farm_sow_id'] 
                    del cur_entry['sow_boar']['num_nipples'] 
                    
                
                result.append(cur_entry)

        
        return result

    
    def get_parent_trace(self, sow_id, boar_id, pig_farm_id):
        """
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        """
        
        """
        Notes:
        
        1.) The sow_boar.parent_sow_id and sow_boar.parent_boar_id
            are set by user when sow_boar.birth_pig_prod_id was not set.
            
        2.) The sow_boar.birth_pig_prod_id is set by the system;
            This is when a production piglet is ear tagged or a production
            pig is harvested as sow or boar;
            
            When a piglet is eartagged at production or a production pig is 
            harvested as sow or boar, this pig parents will be computed by the system.
            This should not be editable by user.
            
            
        3.) When sow_boar.birth_pig_prod_id is set, it will read the 
            insemination information of this pig_production entry.
        
        4.) There are 3 insemination types
            - sow + boar
            - sow + artifical insemination, external semen (semen brought from outside the farm`)
            - sow + artifical insemination, internal semen (taken from one of the farm boars)
        
        """
        
        
        if pig_farm_id > 0:
            where_clause = 'WHERE a.pig_farm_id = %s AND a.is_disposed = 0' % pig_farm_id
        
        else:
            list_id = []
            
            if sow_id > 0:
                list_id.append(str(sow_id))
                
            if boar_id > 0:
                list_id.append(str(boar_id))
            
            where_clause = ','.join(list_id)
            
            
        sql =   """
                SELECT 
                    a.id,
                    a.birth_pig_prod_id,
                    
                    a.parent_sow_id,
                    b.name,
                    b.number,
                    b.is_disposed,
                    
                    a.parent_boar_id,
                    c.name,
                    c.number,
                    c.is_disposed,
                    
                    d.insemination_type,
                    d.sow_id,
                    d.boar_id,
                    d.semen_ai_boar_id,
                    
                    d.semen_supplier_id,
                    e.name AS semen_supplier_name,
                    
                    d.semen_sup_semen_id,
                    f.name AS semen_name,
                    
                    a.sex
                    
                FROM sow_boar a
                LEFT OUTER JOIN sow_boar b              ON a.parent_sow_id = b.id
                LEFT OUTER JOIN sow_boar c              ON a.parent_boar_id = c.id
                
                LEFT OUTER JOIN pig_production d        ON a.birth_pig_prod_id = d.id
                LEFT OUTER JOIN common_supplier e       ON d.semen_supplier_id = e.id
                LEFT OUTER JOIN semen_supplier_semen f  ON d.semen_sup_semen_id = f.id
                
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
            msg = 'get_parent_trace(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            for row in rows:
                cur_id                      = row[0]
                cur_birth_pig_prod_id       = row[1]
                    
                cur_parent_sow_id           = row[2]
                cur_parent_sow_name         = row[3]
                cur_parent_sow_number       = row[4]
                cur_parent_sow_is_disposed  = row[5]
                    
                cur_parent_boar_id          = row[6]
                cur_parent_boar_name        = row[7]
                cur_parent_boar_number      = row[8]
                cur_parent_boar_is_disposed = row[9]
                    
                    
                cur_insem_type              = row[10]
                cur_insem_sow_id            = row[11]
                cur_insem_boar_id           = row[12]
                cur_insem_semen_ai_boar_id  = row[13]
                    
                cur_semen_supplier_id       = row[14]
                cur_semen_supplier_name     = row[15]
                    
                cur_semen_sup_semen_id      = row[16]
                cur_semen_sup_semen_name    = row[17]

                cur_sex                     = row[18]
                
                cur_entry = {
                    'sow_boar':{
                        'id':               cur_id,
                        'sex':              cur_sex
                    },
                    
                    'parent_sow':{
                        'id':               cur_parent_sow_id,
                        'name':             cur_parent_sow_name,
                        'number':           cur_parent_sow_number,
                        'is_disposed':      cur_parent_sow_is_disposed
                    },
                    
                    
                    'parent_boar':{
                        'id':               cur_parent_boar_id,
                        'name':             cur_parent_boar_name,
                        'number':           cur_parent_boar_number,
                        'is_disposed':      cur_parent_boar_is_disposed
                    },
                    
                    
                    'insemination':{
                        'type':             cur_insem_type,
                        'sow_id':           cur_insem_sow_id,
                        'boar_id':          cur_insem_boar_id,
                        'ai_boar_id':       cur_insem_semen_ai_boar_id,
                        
                        'semen_supplier':{
                            'id':           cur_semen_supplier_id,
                            'name':         cur_semen_supplier_name,
                                
                            'semen':     {
                                'id':       cur_semen_sup_semen_id,
                                'name':     cur_semen_sup_semen_name
                            }
                        }
                    }
                }
                
                if cur_entry['insemination']['ai_boar_id'] is None:
                    del cur_entry['insemination']['ai_boar_id']
                
                if cur_entry['insemination']['semen_supplier']['id'] is None:
                    del cur_entry['insemination']['semen_supplier']
                
                result.append(cur_entry)

        return result

    
    