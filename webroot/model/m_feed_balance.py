# August 31, 2025
# Jack Wong

from common_constants       import *


class FeedBalance:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'FeedBalance'


    def add(self, data = None):
        """
        PROCEDURE feed_balance_add(
            in_user_id              INT,
            
            in_pig_prod_id          INT,
            in_pig_prod_group_id    INT,
            
            in_date_balance         VARCHAR(10),
            
            in_num_pigs             INT,
            
            in_num_lactating        DECIMAL(5,1),
            in_num_booster          DECIMAL(5,1),
            in_num_prestarter       DECIMAL(5,1),
            in_num_starter          DECIMAL(5,1),
            in_num_grower           DECIMAL(5,1),
            in_num_finisher         DECIMAL(5,1)
        )  
        """
        
        sql =  'CALL feed_balance_add('
        sql += '%s,'    % data.user_id
        
        
        if data.pig_prod_id is not None and data.pig_prod_id > 0:
            sql += '%s,'    % data.pig_prod_id
            sql += 'NULL,'
            
        else:
            sql += 'NULL,'
            sql += '%s,'    % data.pig_prod_group_id
    
        
        sql += '"%s",'  % data.date_balance
        
        sql += '%s,'    % data.num_pigs
        
        sql += '%s,'    % data.num_lactating
        sql += '%s,'    % data.num_booster
        sql += '%s,'    % data.num_prestarter
        sql += '%s,'    % data.num_starter
        sql += '%s,'    % data.num_grower
        sql += '%s)'    % data.num_finisher
        
        
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
                
                'feed_buy': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE feed_balance_update(
            in_user_id              INT,
            
            in_feed_balance_id INT,
            
            in_date_balance         VARCHAR(10),
            
            in_num_pigs             INT,
            
            in_num_lactating        DECIMAL(5,1),
            in_num_booster          DECIMAL(5,1),
            in_num_prestarter       DECIMAL(5,1),
            in_num_starter          DECIMAL(5,1),
            in_num_grower           DECIMAL(5,1),
            in_num_finisher         DECIMAL(5,1)
        )  
        """
        
        sql =  'CALL feed_balance_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.feed_balance_id
        
        sql += '"%s",'  % data.date_balance
        
        sql += '%s,'    % data.num_pigs
        
        sql += '%s,'    % data.num_lactating
        sql += '%s,'    % data.num_booster
        sql += '%s,'    % data.num_prestarter
        sql += '%s,'    % data.num_starter
        sql += '%s,'    % data.num_grower
        sql += '%s)'    % data.num_finisher
        
        
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
    
    
    def get_list(self, pig_farm_id, inc_user_audit = 0):
        
        sql =   """
                SELECT 
                    a.pig_prod_id,
                    b.prod_status_id, 
                    
                    a.date_balance,
                    a.num_days_since_birth,
                    a.num_weeks_since_birth,
                    a.num_pigs,
                    
                    a.num_lactating,
                    a.num_booster,
                    a.num_prestarter,
                    a.num_starter,
                    a.num_grower,
                    a.num_finisher,
                    
                    a.num_cons_kg_lactating,
                    a.num_cons_kg_booster,
                    a.num_cons_kg_prestarter,
                    a.num_cons_kg_starter,
                    a.num_cons_kg_grower,
                    a.num_cons_kg_finisher

                    
                FROM feed_balance a
                LEFT OUTER JOIN pig_production b ON a.pig_prod_id = b.id 
                WHERE b.pig_farm_id = %s AND b.status = IN (4,5,6)
                ORDER BY a.pig_prod_id ASC, a.num_days_since_birth 
                """ % pig_farm_id
                    
            
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
                        'feed_buy': {
                            'id':               row[0],
                            'date_buy':         str(row[1]),
                            'quantity':         row[2],
                            'kg_per_unit':      float(row[3]),
                            'kg_total':         float(row[4]),
                            'unit_cost':        float(row[5]),
                            'total_cost':       float(row[6]),
                            'dt_entry':         str(row[7])
                        },
                        
                        'feed_type':{
                            'id':               row[8],
                            'name':             row[9],
                        },
                        
                        'feed_brand':{
                            'id':               row[10],
                            'name':             row[11],
                        },
                        
                        'feed_supplier':{
                            'id':               row[12],
                            'name':             row[13],
                        }
                    }
                    
                else:
                    cur_entry = {
                        'feed_buy': {
                            'id':               row[0],
                            'date_buy':         str(row[1]),
                            'quantity':         row[2],
                            'kg_per_unit':      float(row[3]),
                            'kg_total':         float(row[4]),
                            'unit_cost':        float(row[5]),
                            'total_cost':       float(row[6]),
                            'dt_entry':         str(row[7])
                        },
                        
                        'feed_type':{
                            'id':               row[8],
                            'name':             row[9],
                        },
                        
                        'feed_brand':{
                            'id':               row[10],
                            'name':             row[11],
                        },
                        
                        'feed_supplier':{
                            'id':               row[12],
                            'name':             row[13],
                        },
                        
                        'added_by': {
                            'username':         row[14],
                            'name_last':        row[15],
                            'name_first':       row[16],
                            'dt_entry':         row[17]
                        },
                        
                        'last_update':{
                            'username':         row[18],
                            'name_last':        row[19],
                            'name_first':       row[20],
                            'dt_update':        str(row[21]) if row[21] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    