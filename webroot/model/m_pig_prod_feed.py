# February 13, 2026
# Jack Wong

from common_constants       import *


class PigProdFeed:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProdFeed'


    def add(self, data = None):
        """
        PROCEDURE pig_prod_feed_add(
            in_user_id              INT,
            
            in_pig_prod_id          INT,
            in_pig_farm_feed_buy_id INT,
            
            in_date_add             VARCHAR(10),
            
            
            in_num_gesta            INT, /** must be > 0; can be NULL; */
            in_num_lacta            INT, /** must be > 0; can be NULL; */   
            in_num_booster          INT, /** must be > 0; can be NULL; */
            in_num_prestarter       INT, /** must be > 0; can be NULL; */
            in_num_starter          INT, /** must be > 0; can be NULL; */
            in_num_grower           INT, /** must be > 0; can be NULL; */
            in_num_finisher         INT  /** must be > 0; can be NULL; */
        )  
        """
        
        sql =  'CALL pig_prod_feed_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        sql += '%s,'    % data.pig_farm_feed_buy_id
        
        sql += '"%s",'  % data.date_add
        
        
        if data.num_gesta is not None and data.num_gesta > 0:
            sql += '%s,'    % data.num_gesta
        else:
            sql += 'NULL,'
        
        
        if data.num_lacta is not None and data.num_lacta > 0:
            sql += '%s,'    % data.num_lacta
        else:
            sql += 'NULL,'
        
        
        if data.num_booster is not None and data.num_booster > 0:
            sql += '%s,'    % data.num_booster
        else:
            sql += 'NULL,'
        
        
        if data.num_prestarter is not None and data.num_prestarter > 0:
            sql += '%s,'    % data.num_prestarter
        else:
            sql += 'NULL,'
        
        
        if data.num_starter is not None and data.num_starter > 0:
            sql += '%s,'    % data.num_starter
        else:
            sql += 'NULL,'
        
        
        if data.num_grower is not None and data.num_grower > 0:
            sql += '%s,'    % data.num_grower
        else:
            sql += 'NULL,'
        
        
        if data.num_finisher is not None and data.num_finisher > 0:
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
                
                'pig_prod_feed': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_prod_feed_update(
            in_user_id              INT,
            
            in_pig_prod_feed_id     INT,
    
    
            in_date_add             VARCHAR(10),
            
            
            in_num_gesta            INT, /** can be >= 0; cannot be NULL*/
            in_num_lacta            INT, /** can be >= 0; cannot be NULL*/   
            in_num_booster          INT, /** can be >= 0; cannot be NULL*/
            in_num_prestarter       INT, /** can be >= 0; cannot be NULL*/
            in_num_starter          INT, /** can be >= 0; cannot be NULL*/
            in_num_grower           INT, /** can be >= 0; cannot be NULL*/
            in_num_finisher         INT  /** can be >= 0; cannot be NULL*/
        )  
        """
        
        sql =  'CALL pig_prod_feed_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_prod_feed_id
        
        sql += '"%s",'  % data.date_add
        
        
        sql += '%s,'    % data.num_gesta
        sql += '%s,'    % data.num_lacta
        sql += '%s,'    % data.num_booster
        sql += '%s,'    % data.num_prestarter
        sql += '%s,'    % data.num_starter
        sql += '%s,'    % data.num_grower
        sql += '%s);'   % data.num_finisher
        
        
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
                
                'pig_prod_feed': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id):
        
        
        sql =   """
                SELECT 
                    a.id,
                    a.pig_farm_feed_buy_id,
                    b.feed_supplier_id,
                    c.name AS supplier_name,
                    a.date_add        
                    
                FROM pig_prod_feed a
                LEFT OUTER JOIN pig_farm_feed_buy b ON a.pig_farm_feed_buy_id = b.id
                LEFT OUTER JOIN common_supplier c   ON b.feed_supplier_id = c.id
                WHERE a.pig_prod_id = %s
                ORDER BY a.date_add DESC
                """ % (pig_prod_id)
        
            
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
                cur_id                      = row[0]
                cur_pig_farm_feed_buy_id    = row[1]
                cur_feed_supplier_id        = row[2]
                cur_feed_supplier_name      = row[3]
                cur_date_add                = str(row[4])
                
               
                cur_entry = {
                    'pig_prod_feed': {
                        'id':               cur_id,
                        'pf_feed_buy_id':   cur_pig_farm_feed_buy_id,
                        'date_add':         cur_date_add
                    },
                    
                    'feed_supplier': {
                        'id':           cur_feed_supplier_id,
                        'name':         cur_feed_supplier_name
                    } 
                }
                
                feed_items = self.get_list_items(cur_id)
                cur_entry['feed_items'] = feed_items
                
                result.append(cur_entry)
                    

        return result
    
    
    
    def get_list_items(self, pig_prod_feed_id):
        
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
                    
                FROM feed_buy a 
                LEFT OUTER JOIN feed_type b         ON a.feed_type_id = b.id
                LEFT OUTER JOIN feed_brand c        ON a.feed_brand_id = c.id
                WHERE a.pig_prod_feed_id = %s
                ORDER BY a.id ASC
        
                """ % (pig_prod_feed_id)
        
        
            
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
    
