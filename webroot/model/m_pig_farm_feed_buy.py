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
            
            cur_pf_feed_buy_id = None
            
            for row in rows:
                cur_id                  = row[0]
                    
                cur_date_buy            = str(row[1])

                cur_total_feed_cost     = float(row[2]) if row[2] is not None else None
                cur_other_cost          = float(row[3]) if row[3] is not None else None

                cur_feed_supplier_id    = row[4]
                cur_feed_supplier_name  = row[5]


                if cur_pf_feed_buy_id is None or cur_pf_feed_buy_id != cur_id:
                    cur_pf_feed_buy_id  = cur_id
                    
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
                        },
                        
                        'buy_items':[]
                    }
                    result.append(cur_entry)
                    


                cur_feed_buy_item_id    = row[6]

                cur_feed_type_id        = row[7]
                cur_feed_brand_id       = row[8]

                cur_quantity            = row[9]
                cur_kg_per_unit         = row[10]
                cur_kg_total            = row[11]
            
                cur_unit_cost           = float(row[12]) if row[12] is not None else None
                cur_total_cost          = float(row[13]) if row[13] is not None else None
                
                cur_feed_type_name      = row[14]
                cur_feed_brand_name     = row[15]
                
                
                cur_buy_item = {
                    'id':               cur_feed_buy_item_id,
                    
                    'feed':{
                        'quantity':     cur_quantity,
                        'kg_per_unit':  cur_kg_per_unit,
                        'kg_total':     cur_kg_total,
                        
                        'unit_cost':    cur_unit_cost,
                        'total_cost':   cur_total_cost,
                    },
                    
                    
                    'feed_type':{
                        'id':       cur_feed_type_id,
                        'name':     cur_feed_type_name 
                    },
                    
                    'feed_brand':{
                        'id':       cur_feed_brand_id,
                        'name':     cur_feed_brand_id
                    }
                    
                }
                
                cur_entry['buy_items'].append(cur_buy_item)
                
              
        return result
    
    