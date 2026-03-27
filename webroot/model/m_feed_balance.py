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
            
            in_pig_farm_id          INT,    /* IF this is filled up, this is for farm_balance */
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
        
        if data.pig_farm_id is not None and data.pig_farm_id > 0:
            sql += '%s,'    % data.pig_farm_id
            sql += 'NULL,'
            sql += 'NULL,'
            
        else:
            if data.pig_prod_id is not None and data.pig_prod_id > 0:
                sql += 'NULL,'
                sql += '%s,'    % data.pig_prod_id
                sql += 'NULL,'
                
            else:
                sql += 'NULL,'
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
    
    
    def get_list(self, pig_prod_id = 0, pig_farm_id = 0, date_since = None,
            inc_user_audit = 0):
        
        if pig_prod_id > 0:
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
                            
                        FROM feed_balance 
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
                           
                            
        if pig_farm_id > 0:
            where_clause = 'WHERE a.pig_farm_id = %s ' % pig_farm_id
            if date_since is not None:
                where_clause += 'AND a.date_balance >= "%s"' % date_since
            
            
            # If the given is pig_farm_id, need to include the insemination info 
            
            if inc_user_audit == 0:
                sql =   """
                        SELECT 
                            a.id,
                            a.pig_prod_id,
                            a.date_balance,
                            
                            a.num_gestating,
                            a.num_lactating,
                            a.num_booster,
                            a.num_prestarter,
                            a.num_starter,
                            a.num_grower,
                            a.num_finisher,
                            
                            b.farm_prod_id,
                            b.insemination_type,
                            
                            b.sow_id,
                            c.number,
                            c.name,
                            
                            b.boar_id,
                            d.number,
                            d.name,
                            
                            b.semen_supplier_id,
                            e.name AS semen_supplier_name,
                            
                            b.semen_sup_semen_id,
                            f.name as semen_supplier_semen_name,
                            
                            b.semen_ai_boar_id,
                            g.number,
                            g.name
                            
                        FROM feed_balance a
                        LEFT OUTER JOIN pig_production b    ON a.pig_prod_id = b.id
                        LEFT OUTER JOIN sow_boar c          ON b.sow_id = c.id
                        LEFT OUTER JOIN sow_boar d          ON b.boar_id = d.id
                        
                        LEFT OUTER JOIN common_supplier e   ON b.semen_supplier_id = e.id
                        LEFT OUTER JOIN semen_supplier_semen f ON b.semen_sup_semen_id = f.id
                        LEFT OUTER JOIN sow_boar g          ON b.semen_ai_boar_id = g.id
                        
                        
                        %s
                        ORDER BY a.date_balance DESC, a.pig_prod_id ASC
                        """ % where_clause
                        

            else:
                sql =   """
                        SELECT 
                            a.id,
                            a.pig_prod_id,
                            a.date_balance,
                            
                            a.num_gestating,
                            a.num_lactating,
                            a.num_booster,
                            a.num_prestarter,
                            a.num_starter,
                            a.num_grower,
                            a.num_finisher,
                            
                            b.farm_prod_id,
                            b.insemination_type,
                            
                            b.sow_id,
                            c.number,
                            c.name,
                            
                            b.boar_id,
                            d.number,
                            d.name,
                            
                            b.semen_supplier_id,
                            e.name AS semen_supplier_name,
                            
                            b.semen_sup_semen_id,
                            f.name as semen_supplier_semen_name,
                            
                            b.semen_ai_boar_id,
                            g.number,
                            g.name,
                            
                            h.name_last,
                            h.name_first,
                            a.dt_entry,
                            
                            
                            i.name_last,
                            i.name_first,
                            a.dt_last_update
                            
                        FROM feed_balance a
                        LEFT OUTER JOIN pig_production b    ON a.pig_prod_id = b.id
                        LEFT OUTER JOIN sow_boar c          ON b.sow_id = c.id
                        LEFT OUTER JOIN sow_boar d          ON b.boar_id = d.id
                        
                        LEFT OUTER JOIN common_supplier e   ON b.semen_supplier_id = e.id
                        LEFT OUTER JOIN semen_supplier_semen f ON b.semen_sup_semen_id = f.id
                        LEFT OUTER JOIN sow_boar g          ON b.semen_ai_boar_id = g.id
                        
                        LEFT OUTER JOIN user h          ON a.added_by_user_id = h.id
                        LEFT OUTER JOIN user i          ON a.last_update_user_id = i.id
                        %s
                        ORDER BY a.date_balance DESC, a.pig_prod_id ASC
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
            
            if pig_prod_id > 0:
            
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
        
        
            if pig_farm_id > 0:
                last_date_balance = None
            
                for row in rows:
                    cur_id                  = row[0]
                    cur_pig_prod_id         = row[1]
                    cur_date_balance        = str(row[2])
                    
                    cur_num_gestating       = float(row[3]) if row[3] else None
                    cur_num_lactating       = float(row[4]) if row[4] else None
                    cur_num_booster         = float(row[5]) if row[5] else None
                    cur_num_prestarter      = float(row[6]) if row[6] else None
                    cur_num_starter         = float(row[7]) if row[7] else None
                    cur_num_grower          = float(row[8]) if row[8] else None
                    cur_num_finisher        = float(row[9]) if row[9] else None
                    
                    cur_farm_prod_id        = row[10]
                    cur_insemination_type   = row[11]
                            
                    cur_sow_id              = row[12]
                    cur_sow_number          = row[13]
                    cur_sow_name            = row[14]
                            
                    cur_boar_id             = row[15]
                    cur_boar_number         = row[16]
                    cur_boar_name           = row[17]
                            
                    cur_semen_supplier_id   = row[18]
                    cur_semen_supplier_name = row[19]
                            
                    cur_semen_sup_semen_id  = row[20]
                    cur_semen_name          = row[21]
                            
                    cur_semen_ai_boar_id    = row[22]
                    cur_semen_ai_boar_number= row[23]
                    cur_semen_ai_boar_name  = row[24]
                    

                    
                    if last_date_balance is None or last_date_balance !=  cur_date_balance:
                        cur_entry = {
                            'date_balance': cur_date_balance,
                            'feed_balance': []
                        }
                        
                        result.append(cur_entry)
                        last_date_balance =  cur_date_balance
                    
                    
                    cur_feed_balance = {
                        'id':               cur_id
                    }
                    
                    
                    if cur_num_gestating is not None:
                        cur_feed_balance['num_gestating'] = cur_num_gestating
                    
                    if cur_num_lactating is not None:
                        cur_feed_balance['num_lactating'] = cur_num_lactating
                    
                    if cur_num_booster is not None:
                        cur_feed_balance['num_booster'] = cur_num_booster
                    
                    if cur_num_prestarter is not None:
                        cur_feed_balance['num_prestarter'] = cur_num_prestarter
                    
                    if cur_num_starter is not None:
                        cur_feed_balance['num_starter'] = cur_num_starter
                    
                    if cur_num_grower is not None:
                        cur_feed_balance['num_grower'] = cur_num_grower
                    
                    if cur_num_finisher is not None:
                        cur_feed_balance['num_finisher'] = cur_num_finisher
                    
                    
                    
                    if cur_pig_prod_id is not None:
                        
                        pig_prod = {
                            'pig_production':{
                                'id':               cur_pig_prod_id,
                                'farm_prod_id':     cur_farm_prod_id
                            },
                        
                            'sow': {
                                'id':               cur_sow_id,
                                'number':           cur_sow_number,
                                'name':             cur_sow_name
                            },
                        
                            'insemination': {
                                'insem_type':       cur_insemination_type,
                                
                                'boar': {
                                    'id':           cur_boar_id,
                                    'number':       cur_boar_number,
                                    'name':         cur_boar_name
                                },
                                
                                'ai': {
                                    'semen_supplier':{
                                        'id':       cur_semen_supplier_id,
                                        'name':     cur_semen_supplier_name,
                                        
                                        'semen': {
                                            'id':   cur_semen_sup_semen_id,
                                            'name': cur_semen_name
                                        }
                                    },
                                    
                                    'internal_boar':{
                                        'id':           cur_semen_ai_boar_id,
                                        'number':       cur_semen_ai_boar_number,
                                        'name':         cur_semen_ai_boar_name
                                    }
                                }
                            }
                        }
                    
                        cur_feed_balance['pig_prod'] = pig_prod
                    
                    
                    if inc_user_audit > 0:
                    
                        added_by = {
                            'name_last':        row[25],
                            'name_first':       row[26],
                            'dt_entry':         row[27]
                        }
                        
                        last_update = {
                            'name_last':        row[28],
                            'name_first':       row[29],
                            'dt_update':        str(row[30]) if row[30] else None
                        }
                    
                        cur_feed_balance['added_by']   = added_by
                        cur_feed_balance['last_update'] = last_update
                    
                        
                    cur_entry['feed_balance'].append(cur_feed_balance)
                    
        
            
        return result
    
    
