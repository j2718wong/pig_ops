# August 31, 2025
# Jack Wong

from common_constants       import *


class FeedBalance:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'FeedBalance'


    def add(self, data = None):
        """
        PROCEDURE feed_balance_add_or_update(
            in_user_id              INT,
            
            in_pig_prod_id          INT,
            in_prod_group_id        INT,
            
            in_date_balance         VARCHAR(10),
            
            in_num_pigs             INT, /* This can be entered null; 
                                        if entered null, this is computed.*/
            
            in_num_gestating        DECIMAL(5,1),
            in_num_lactating        DECIMAL(5,1),
            in_num_booster          DECIMAL(5,1),
            in_num_prestarter       DECIMAL(5,1),
            in_num_starter          DECIMAL(5,1),
            in_num_grower           DECIMAL(5,1),
            in_num_finisher         DECIMAL(5,1)
        )  
        """
        
        sql =  'CALL feed_balance_add_or_update('
        sql += '%s,'    % data.user_id
        
        
        if data.pig_prod_id is not None and data.pig_prod_id > 0:
            sql += '%s,'    % data.pig_prod_id
            sql += 'NULL,'
            
        else:
            sql += 'NULL,'
            sql += '%s,'    % data.pig_prod_group_id
    
        
        sql += '"%s",'  % data.date_balance
        
        if data.num_pigs is not None and data.num_pigs > 0:
            sql += '%s,'    % data.num_pigs
        else:
            sql += 'NULL,'
        
        if data.num_gesta is not None:
            sql += '%s,'    % data.num_gesta
        else:
            sql += 'NULL,'
            
        if data.num_lacta is not None:
            sql += '%s,'    % data.num_lacta
        else:
            sql += 'NULL,'
        
        if data.num_booster is not None:
            sql += '%s,'    % data.num_booster
        else:
            sql += 'NULL,'
        
        if data.num_prestarter is not None:
            sql += '%s,'    % data.num_prestarter
        else:
            sql += 'NULL,'
        
        if data.num_starter is not None:
            sql += '%s,'    % data.num_starter
        else:
            sql += 'NULL,'
        
        if data.num_grower is not None:
            sql += '%s,'    % data.num_grower
        else:
            sql += 'NULL,'
        
        if data.num_finisher is not None:
            sql += '%s);'    % data.num_finisher
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
                
                'feed_balance': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE feed_balance_add_or_update(
            in_user_id              INT,
            
            in_pig_prod_id          INT,
            in_prod_group_id        INT,
            
            in_date_balance         VARCHAR(10),
            
            in_num_pigs             INT, /* This can be entered null; 
                                        if entered null, this is computed.*/
            
            in_num_gestating        DECIMAL(5,1),
            in_num_lactating        DECIMAL(5,1),
            in_num_booster          DECIMAL(5,1),
            in_num_prestarter       DECIMAL(5,1),
            in_num_starter          DECIMAL(5,1),
            in_num_grower           DECIMAL(5,1),
            in_num_finisher         DECIMAL(5,1)
        )  
        """
        
        sql =  'CALL feed_balance_add_or_update('
        sql += '%s,'    % data.user_id
        
        
        if data.pig_prod_id is not None and data.pig_prod_id > 0:
            sql += '%s,'    % data.pig_prod_id
            sql += 'NULL,'
            
        else:
            sql += 'NULL,'
            sql += '%s,'    % data.pig_prod_group_id
    
        
        sql += '"%s",'  % data.date_balance
        
        if data.num_pigs is not None and data.num_pigs > 0:
            sql += '%s,'    % data.num_pigs
        else:
            sql += 'NULL,'
        
        if data.num_gesta is not None:
            sql += '%s,'    % data.num_gesta
        else:
            sql += 'NULL,'
            
        if data.num_lacta is not None:
            sql += '%s,'    % data.num_lacta
        else:
            sql += 'NULL,'
        
        if data.num_booster is not None:
            sql += '%s,'    % data.num_booster
        else:
            sql += 'NULL,'
        
        if data.num_prestarter is not None:
            sql += '%s,'    % data.num_prestarter
        else:
            sql += 'NULL,'
        
        if data.num_starter is not None:
            sql += '%s,'    % data.num_starter
        else:
            sql += 'NULL,'
        
        if data.num_grower is not None:
            sql += '%s,'    % data.num_grower
        else:
            sql += 'NULL,'
        
        if data.num_finisher is not None:
            sql += '%s);'    % data.num_finisher
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
                
                'feed_balance': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id, inc_user_audit = 0):
        if inc_user_audit == 0:
                        sql =   """
                    SELECT 
                        id,
                        date_balance,
                        
                        num_pigs,
                        
                        num_gestating,
                        num_lactating,
                        num_booster,
                        num_prestarter,
                        num_starter,
                        num_grower,
                        num_finisher
                        
                    FROM feed_balance a
                    WHERE pig_prod_id = %s
                    ORDER BY date_balance DESC
                    """ % pig_prod_id
                        

        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.date_balance,
                        
                        a.num_pigs,
                        
                        a.num_lactating,
                        a.num_booster,
                        a.num_prestarter,
                        a.num_starter,
                        a.num_grower,
                        a.num_finisher,
                        
                        b.name_last,
                        b.name_first,
                        a.dt_entry,
                        
                        
                        c.name_last,
                        c.name_first,
                        a.dt_last_update
                        
                    FROM feed_balance a
                    LEFT OUTER JOIN user b          ON a.added_by_user_id = b.id
                    LEFT OUTER JOIN user c          ON a.last_update_user_id = c.id
                    WHERE a.pig_prod_id = %s
                    ORDER BY a.date_balance DESC
                    """ % pig_prod_id
                        
                
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
                cur_num_gestating       = float(row[3]) if row[3] else None
                cur_num_lactating       = float(row[4]) if row[4] else None
                cur_num_booster         = float(row[5]) if row[5] else None
                cur_num_prestarter      = float(row[6]) if row[6] else None
                cur_num_starter         = float(row[7]) if row[7] else None
                cur_num_grower          = float(row[8]) if row[8] else None
                cur_num_finisher        = float(row[9]) if row[9] else None
                
                
                
                cur_entry = {
                    'feed_balance': {
                        'id':               row[0],
                        'date_balance':     str(row[1]),
                        'num_pigs':         row[2]
                    }
                }
                
                
                if cur_num_gestating is not None:
                    cur_entry['feed_balance']['num_gestating'] = cur_num_gestating
                
                if cur_num_lactating is not None:
                    cur_entry['feed_balance']['num_lactating'] = cur_num_lactating
                
                if cur_num_booster is not None:
                    cur_entry['feed_balance']['num_booster'] = cur_num_booster
                
                if cur_num_prestarter is not None:
                    cur_entry['feed_balance']['num_prestarter'] = cur_num_prestarter
                
                if cur_num_starter is not None:
                    cur_entry['feed_balance']['num_starter'] = cur_num_starter
                
                if cur_num_grower is not None:
                    cur_entry['feed_balance']['num_grower'] = cur_num_grower
                
                if cur_num_finisher is not None:
                    cur_entry['feed_balance']['num_finisher'] = cur_num_finisher
                
                
                if inc_user_audit > 0:
                
                    added_by = {
                        'name_last':        row[10],
                        'name_first':       row[11],
                        'dt_entry':         row[12]
                    }
                    
                    last_update = {
                        'name_last':        row[13],
                        'name_first':       row[14],
                        'dt_update':        str(row[15]) if row[15] else None
                    }
                
                    cur_entry['added_by']   = added_by
                    cur_entry['last_update'] = last_update
                
                    
                result.append(cur_entry)
        
        return result
    
    
