# August 31, 2025
# Jack Wong

from common_constants       import *


class FeedBuy:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'FeedBuy'


    def add(self, data = None):
        """
        PROCEDURE feed_buy_add(
            in_user_id              INT,
            
            in_pig_farm_id          INT,
            in_pig_prod_id          INT,
            in_prod_group_id        INT,
            
    
            in_date_buy             VARCHAR(10),
            in_feed_type_id         INT,
            in_feed_brand_id        INT,
            in_feed_supplier_id     INT,
            in_quantity             INT,
            in_kg_per_unit          DECIMAL(5,1),
            
            in_unit_cost            DECIMAL(8,2),
            in_total_cost           DECIMAL(8,2)
        )  
        """
        
        sql =  'CALL feed_buy_add('
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
                
        
        sql += '"%s",'  % data.date_buy
        sql += '%s,'    % data.feed_type_id
        sql += '%s,'    % data.feed_brand_id
        sql += '%s,'    % data.feed_supplier_id
        sql += '%s,'    % data.quantity
        sql += '%s,'    % data.kg_per_unit
       
        sql += '%s,'    % data.unit_cost
        sql += '%s)'    % data.total_cost
        
        
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
        PROCEDURE feed_buy_update(
            in_user_id              INT,
            in_feed_buy_id          INT,
            
            in_date_buy             VARCHAR(10),
            in_feed_type_id         INT,
            in_feed_brand_id        INT,
            in_feed_supplier_id     INT,
            in_quantity             INT,
            in_kg_per_unit          DECIMAL(5,1),
            
            in_unit_cost            DECIMAL(8,2),
            in_total_cost           DECIMAL(8,2)
        )  
        """
        
        sql =  'CALL feed_buy_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.feed_buy_id
        sql += '"%s",'  % data.date_buy
        
        sql += '%s,'    % data.feed_type_id
        sql += '%s,'    % data.feed_brand_id
        sql += '%s,'    % data.feed_vendor_id
        sql += '%s,'    % data.kg_per_quantity
       
        sql += '%s,'    % data.unit_cost
        sql += '%s)'    % data.total_cost
        
        
        
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
                
                'feed_buy': {
                    'id':               row[3]
                }
            }

        return None
    
      
    def get_list(self, pig_prod_id = 0, pig_prod_group_id = 0, 
            inc_user_audit = 0, after_date = None):
        

        if inc_user_audit == 0: 
            if pig_prod_id > 0:
                
                s_after_date = ''
                if after_date is not None:
                    s_after_date = ' AND a.date_buy >= "%s"' % after_date
                
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
                            d.name AS feed_supplier_name
                            
                        FROM feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        WHERE a.pig_prod_id = %s %s
                        ORDER BY a.id
                        """ % (pig_prod_id, s_after_date)
                        
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
                            d.name AS feed_supplier_name
                            
                        FROM feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        WHERE a.pig_prod_group_id = %s
                        ORDER BY a.id DESC
                        """ % pig_prod_group_id
                
                
        else:
            
            if pig_prod_id > 0:
                s_after_date = ''
                if after_date is not None:
                    s_after_date = ' AND a.date_buy >= "%s"' % after_date
                
                
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
                            
                            
                            e.name_last,
                            e.name_first,
                            a.dt_entry,
                            
                            
                            f.name_last,
                            f.name_first,
                            a.dt_last_update
                            
                        FROM feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        LEFT OUTER JOIN user e          ON a.added_by_user_id = e.id
                        LEFT OUTER JOIN user f          ON a.last_update_user_id = f.id
                        WHERE a.pig_prod_id = %s %s
                        ORDER BY a.id
                        """ % (pig_prod_id, s_after_date)
                        
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
                            
                            
                            e.name_last,
                            e.name_first,
                            a.dt_entry,
                            
                            
                            f.name_last,
                            f.name_first,
                            a.dt_last_update
                            
                        FROM feed_buy a 
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
                            'name_last':        row[14],
                            'name_first':       row[15],
                            'dt_entry':         row[16]
                        },
                        
                        'last_update':{
                            'name_last':        row[17],
                            'name_first':       row[18],
                            'dt_update':        str(row[19]) if row[19] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    