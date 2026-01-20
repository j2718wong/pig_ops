# January 20, 2026
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
        

class SowBoarMate:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SowBoarMate'

    
    def add_boar_external_mate(self, data = None):
        """
        Adding an external mate for a farm owned boar will not 
        create a pig_production entry.
        
        This should not be used when a farm owned sow is mated to an external boar.
        
        PROCEDURE boar_external_mate_add(
            in_user_id              INT,
            
            in_boar_id              INT,
            in_boar_customer_id     INT,    /* This is mapped to account_pig_buyer*/
            
            in_customer_sow_name    VARCHAR(50),
            
            in_date_mate            VARCHAR(10),
            in_notes                VARCHAR(160)
        )    
        """
        
        sql =  'CALL boar_external_mate_add('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.boar_id
        sql += '%s,'    % data.boar_customer_id
        
        if data.customer_sow_name is not None and len(data.customer_sow_name) > 0:
            sql += '"%s",'  % data.customer_sow_name
        else:
            sql += 'NULL,'
        
        sql += '"%s",'    % data.date_mate
            
        
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
            msg = 'add_boar_external_mate(); error in executing query[] = ' + sql
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
                
                'sow_boar_mate': {
                    'id':               row[3]
                }
            }

        return None

    
    def update_boar_external_mate(self, data = None):
        """
        PROCEDURE boar_external_mate_update(
            in_user_id              INT,
            in_sow_boar_mate_id     INT,
            
            in_boar_customer_id     INT,    /* This is mapped to account_pig_buyer*/
            
            in_customer_sow_name    VARCHAR(50),
            
            in_date_mate            VARCHAR(10),
            in_notes                VARCHAR(160)
        )    
        """
        
        sql =  'CALL boar_external_mate_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.sow_boar_mate_id
        
        sql += '%s,'    % data.boar_customer_id
        
        if data.customer_sow_name is not None and len(data.customer_sow_name) > 0:
            sql += '"%s",'  % data.customer_sow_name
        else:
            sql += 'NULL,'
        
        sql += '"%s",'    % data.date_mate
            
        
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
            msg = 'update_boar_external_mate(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            
            res_update = {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2]
                }
            }
            
            return res_update;

        return None

     
    def get_list(self, sow_boar_id, is_external: int = 0):
        """
        Will get sow_boar_mate list.
        
        Parameters
        ----------
        
        sow_id : int
            will get all sow_boar_mate data of the sow
        
        boar_id:
            will get all sow_boar_mate data of the boar
            
        is_external: int
            this is ignored if sow_id is given
            
            if is_external 0, will return mated farm owned sows 
            if is_external > 0, will return mated external sows(not farm owned)
        
            
        Returns
        -------
        list of dictionary
        
        
        """
        
        if is_external == 0:
            
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.pig_prod_id,
                        
                        a.mate_sow_boar_id,
                        a.date_mate
                        
                        b.name,
                        b.number
                        
                    FROM sow_boar_mate a
                    LEFT OUTER JOIN sow_boar b          ON a.mate_sow_boar_id  = b.id
                    WHERE a.sow_boar_id = %s 
                    ORDER BY a.date_mate DESC 
                    """ % sow_boar_id
            
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.date_mate
                        a.boar_customer_id,
                        b.name,
                        
                        a.customer_sow_name,
                        
                        c.notes
                        
                    FROM sow_boar_mate a
                    LEFT OUTER JOIN account_pig_buyer b     ON a.boar_customer_id = b.id
                    LEFT OUTER JOIN pig_prod_notes c        ON a.notes_id = c.id
                    WHERE a.sow_boar_id = %s
                    ORDER BY a.date_mate DESC 
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
                if is_external == 0:
                    cur_entry = {
                        'id':               row[0],
                        'pig_prod_id':      row[1],
                        'date_mate':        str(row[3]),
                        
                        'mate_sow_boar':{
                            'id':           row[2],
                            'name':         row[4],
                            'number':       row[5]
                        }
                    }
                    
                else:
                    cur_entry = {
                        'id':               row[0],
                        'date_mate':        str(row[1]),
                        
                        'boar_customer':{
                            'id':           row[2],
                            'name':         row[3],
                            'sow_name':     row[4]
                        },
                        
                        'notes':            row[5]
                    }
                    
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

    
    