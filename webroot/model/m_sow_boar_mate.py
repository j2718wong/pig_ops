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
                        b.farm_prod_id,
                        
                        a.mate_sow_boar_id,
                        a.date_mate,
                        
                        c.name,
                        c.number
                        
                    FROM sow_boar_mate a
                    LEFT OUTER JOIN pig_production b    ON a.pig_prod_id = b.id 
                    LEFT OUTER JOIN sow_boar c          ON a.mate_sow_boar_id  = c.id
                    WHERE a.sow_boar_id = %s 
                    ORDER BY a.date_mate DESC 
                    """ % sow_boar_id
            
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.date_mate,
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
                        'farm_prod_id':     row[2],
                        'date_mate':        str(row[4]),
                        
                        'mate_sow_boar':{
                            'id':           row[3],
                            'name':         row[5],
                            'number':       row[6]
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

