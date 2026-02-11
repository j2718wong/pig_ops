# February 2, 2026
# Jack Wong

from common_constants       import *


class PigFarmFeedBuyItem:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigFarmFeedBuyItem'


    def add(self, data = None):
        """
        PROCEDURE pig_farm_feed_buy_item_add(
            in_user_id              INT,
            
            in_pig_farm_feed_buy_id INT,
            
            in_feed_type_id         INT,
            in_feed_brand_id        INT,
            in_quantity             INT,
            in_kg_per_unit          DECIMAL(5,1),
            
            in_unit_cost            DECIMAL(8,2),
            in_total_cost           DECIMAL(8,2)
        )  
        """
        
        sql =  'CALL pig_farm_feed_buy_item_add('
        sql += '%s,'    % data.user_id
        
       
        sql += '%s,'    % data.pig_farm_feed_buy_id
                
        
        sql += '%s,'    % data.feed_type_id
        sql += '%s,'    % data.feed_brand_id
        sql += '%s,'    % data.quantity
        sql += '%s,'    % data.unit_weight
       
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
                
                'feed_buy_item': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_farm_feed_buy_item_update(
            in_user_id              INT,
    
            in_feed_buy_item_id     INT,
            
            in_feed_type_id         INT,
            in_feed_brand_id        INT,
            in_quantity             INT,
            in_kg_per_unit          DECIMAL(5,1),
            
            in_unit_cost            DECIMAL(8,2),
            in_total_cost           DECIMAL(8,2)
        )  
        """
        
        sql =  'CALL pig_farm_feed_buy_item_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pf_feed_buy_item_id
        
        sql += '%s,'    % data.feed_type_id
        sql += '%s,'    % data.feed_brand_id
        sql += '%s,'    % data.quantity
        sql += '%s,'    % data.unit_weight
       
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
                
                'feed_buy_item': {
                    'id':               row[3]
                }
            }

        return None
    
      
    
