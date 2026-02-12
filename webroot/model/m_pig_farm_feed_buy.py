# February 2, 2026
# Jack Wong

from common_constants       import *


class PigFarmFeedBuy:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigFarmFeedBuy'


    def add(self, data = None):
        """
        PROCEDURE pig_farm_feed_buy_add(
            in_user_id              INT,
            
            in_pig_farm_id          INT,
            
            in_date_buy             VARCHAR(10),
            in_feed_supplier_id     INT
        )  
        """
        
        sql =  'CALL pig_farm_feed_buy_add('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_farm_id
        sql += '"%s",'  % data.date_buy
        sql += '%s)'    % data.feed_supplier_id
        
        
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
                
                'pf_feed_buy': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_farm_feed_buy_update(
            in_user_id              INT,
            
            in_pig_farm_feed_buy_id INT,
    
            in_date_buy             VARCHAR(10),
            in_feed_supplier_id     INT
        )  
        """
        
        sql =  'CALL pig_farm_feed_buy_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pf_feed_buy_id
        
        sql += '"%s",'  % data.date_buy
        
        sql += '%s)'    % data.feed_supplier_id
        
        
        
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
                
                'pf_feed_buy': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def get_list(self, pig_farm_id, page_number = 1, limit =  50):
        
        offset = (page_number - 1) * limit
        
        sql =   """
                SELECT 
                    a.id,
                    
                    a.date_buy,
                    
                    a.total_feed_cost,
                    a.other_cost,
                    
                    a.feed_supplier_id,
                    b.name AS feed_supplier_name
                    
                FROM pig_farm_feed_buy a 
                LEFT OUTER JOIN common_supplier b     ON a.feed_supplier_id = b.id
                WHERE a.pig_farm_id = %s
                ORDER BY a.date_buy DESC
                LIMIT %s OFFSET %s 
                """ % (pig_farm_id, limit, offset)
        
            
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
                cur_id                  = row[0]
                    
                cur_date_buy            = str(row[1])

                cur_total_feed_cost     = float(row[2]) if row[2] is not None else None
                cur_other_cost          = float(row[3]) if row[3] is not None else None

                cur_feed_supplier_id    = row[4]
                cur_feed_supplier_name  = row[5]


                    
                cur_entry = {
                    'pf_feed_buy': {
                        'id':               cur_id,
                        'date_buy':         cur_date_buy,
                        'total_feed_cost':  cur_total_feed_cost,
                        'other_cost':       cur_other_cost
                        
                    },
                    
                    
                    'feed_supplier':{
                        'id':               cur_feed_supplier_id,
                        'name':             cur_feed_supplier_name
                    }
                }
                result.append(cur_entry)
                
                feed_items = self.get_list_items(cur_id)
                cur_entry['feed_items'] = feed_items
                    

        return result
    
    
      
    def get_list_items(self, feed_buy_id):
        
        
        """
        # This will not work, because the feed_buy row will black if there
        # are no feed_items; The only option is query feed_items by feed_buy_id
        
        SELECT 
                    a.id,
                    
                    a.date_buy,
                    
                    a.total_feed_cost,
                    a.other_cost,
                    
                    a.feed_supplier_id,
                    b.name AS feed_supplier_name,
                    
                    c.id,
                    c.feed_type_id,
                    c.feed_brand_id,
                    
                    c.quantity,
                    c.kg_per_unit,
                    c.kg_total,
                    
                    c.unit_cost,
                    c.total_cost,
    
                    d.name  AS feed_type_name,
                    e.name  AS feed_brand_name
                    
                FROM pig_farm_feed_buy a 
                LEFT OUTER JOIN feed_supplier b     ON a.feed_supplier_id = b.id
                RIGHT JOIN pig_farm_feed_buy_item c ON c. pig_farm_feed_buy_id = a.id
                LEFT OUTER JOIN feed_type d         ON c.feed_type_id = d.id
                LEFT OUTER JOIN feed_type e         ON c.feed_brand_id = e.id
                WHERE a.pig_farm_id = %s
                ORDER BY a.date_buy DESC, c.id ASC
                LIMIT %s OFFSET %s 
        
        """ 

        
        
        
        sql =   """
                SELECT 
                    
                    a.id,
                    a.feed_type_id,
                    a.feed_brand_id,
                    
                    a.quantity,
                    a.kg_per_unit,
                    a.kg_total,
                    
                    a.unit_cost,
                    a.total_cost,

                    b.name_short  AS feed_type_name,
                    c.name  AS feed_brand_name
                    
                FROM pig_farm_feed_buy_item a 
                LEFT OUTER JOIN feed_type b         ON a.feed_type_id = b.id
                LEFT OUTER JOIN feed_brand c        ON a.feed_brand_id = c.id
                WHERE a.pig_farm_feed_buy_id = %s
                ORDER BY a.id ASC
        
                """ % (feed_buy_id)
        
        
            
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
                cur_id                  = row[0]
                
                cur_feed_type_id        = row[1]
                cur_feed_brand_id       = row[2]

                cur_quantity            = row[3]
                cur_kg_per_unit         = row[4]
                cur_kg_total            = row[5]
            
                cur_unit_cost           = float(row[6]) if row[6] is not None else None
                cur_total_cost          = float(row[7]) if row[7] is not None else None
                
                cur_feed_type_name      = row[8]
                cur_feed_brand_name     = row[9]
                
                
                cur_entry = {
                    
                    'feed_item':{
                        'id':           cur_id,
                        'quantity':     cur_quantity,
                        'kg_per_unit':  cur_kg_per_unit,
                        'kg_total':     cur_kg_total,
                        
                        'unit_cost':    cur_unit_cost,
                        'total_cost':   cur_total_cost,
                    },
                    
                    
                    'feed_type':{
                        'id':           cur_feed_type_id,
                        'name':         cur_feed_type_name 
                    },
                    
                    'feed_brand':{
                        'id':           cur_feed_brand_id,
                        'name':         cur_feed_brand_name
                    }
                    
                }
                
                result.append(cur_entry)
                
              
        return result
    
    
