# August 31, 2025
# Jack Wong

from common_constants       import *


class PigProdFeedBalance:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProdFeedBalance'


    def add(self, data = None):
        """
        PROCEDURE pig_prod_feed_bal_add(
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
        
        sql =  'CALL pig_prod_feed_bal_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
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
                
                'prod_feed_buy': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_prod_feed_bal_update(
            in_user_id              INT,
            
            in_pig_prod_feed_bal_id INT,
            
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
        
        sql =  'CALL pig_prod_feed_bal_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_feed_bal_id
        
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
                
                'prod_feed_bal': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id = 0, pig_prod_group_id = 0, inc_user_audit = 0):
        

        if inc_user_audit == 0: 
            if pig_prod_id > 0:
                sql =   """
                        SELECT 
                            a.id,
                            
                            a.date_buy,
                            a.quantity,
                            a.kg_per_unit,
                            a.kg_total,
                            
                            a.unit_cost,
                            a.total_cost,
                            
                            a.dt_entry,
                            
                            a.feed_type_id,
                            b.name AS feed_type_name,
                            
                            a.feed_brand_id,
                            c.name AS feed_brand_name,
                            
                            a.feed_vendor_id,
                            d.name AS vendor name
                            
                        FROM prod_feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        WHERE a.pig_prod_id = %s
                        ORDER BY a.id
                        """ % pig_prod_id
                        
            else:
                
                sql =   """
                        SELECT 
                            a.id,
                            
                            a.date_buy,
                            a.quantity,
                            a.kg_per_unit,
                            a.kg_total,
                            
                            a.unit_cost,
                            a.total_cost,
                            
                            a.dt_entry,
                            
                            a.feed_type_id,
                            b.name AS feed_type_name,
                            
                            a.feed_brand_id,
                            c.name AS feed_brand_name,
                            
                            a.feed_vendor_id,
                            d.name AS vendor name
                            
                        FROM prod_feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        WHERE a.pig_prod_group_id = %s
                        ORDER BY a.id
                        """ % pig_prod_group_id
                
                
        else:
            
            if pig_prod_id > 0:
                sql =   """
                        SELECT 
                            a.id,
                            
                            a.date_buy,
                            a.quantity,
                            a.kg_per_unit,
                            a.kg_total,
                            
                            a.unit_cost,
                            a.total_cost,
                            
                            a.dt_entry,
                            
                            a.feed_type_id,
                            b.name AS feed_type_name,
                            
                            a.feed_brand_id,
                            c.name AS feed_brand_name,
                            
                            a.feed_supplier_id,
                            d.name AS feed_supplier_name,
                            
                            
                            e.username,
                            e.name_last,
                            e.name_first,
                            a.dt_entry,
                            
                            
                            f.username,
                            f.name_last,
                            f.name_first,
                            a.dt_last_update
                            
                        FROM prod_feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        LEFT OUTER JOIN user e          ON a.added_by_user_id = e.id
                        LEFT OUTER JOIN user f          ON a.last_update_user_id = f.id
                        WHERE a.pig_prod_id = %s
                        ORDER BY a.id
                        """ % pig_prod_id
                        
            else:
                
                sql =   """
                        SELECT 
                            a.id,
                            
                            a.date_buy,
                            a.quantity,
                            a.kg_per_unit,
                            a.kg_total,
                            
                            a.unit_cost,
                            a.total_cost,
                            
                            a.dt_entry,
                            
                            a.feed_type_id,
                            b.name AS feed_type_name,
                            
                            a.feed_brand_id,
                            c.name AS feed_brand_name,
                            
                            a.feed_supplier_id,
                            d.name AS feed_supplier_name,
                            
                            
                            e.username,
                            e.name_last,
                            e.name_first,
                            a.dt_entry,
                            
                            
                            f.username,
                            f.name_last,
                            f.name_first,
                            a.dt_last_update
                            
                        FROM prod_feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        LEFT OUTER JOIN user e          ON a.added_by_user_id = e.id
                        LEFT OUTER JOIN user f          ON a.last_update_user_id = f.id
                        WHERE a.pig_prod_group_id = %s
                        ORDER BY a.id
                        """ % pig_prod_group_id
            
            
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
    
    