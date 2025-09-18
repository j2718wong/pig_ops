# September 18, 2025
# Jack Wong

from common_constants       import *


class ProductionHarvest:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'ProductionHarvest'


    def add(self, data = None):
        """
        PROCEDURE production_harvest_add(
            in_user_id              INT,
            in_pig_prod_id          INT,
            in_production_group_id  INT,
            in_acc_pig_buyer_id     INT,
            
            in_date_harvest         VARCHAR(10),
            
            in_num_pigs_harvest     INT,
            in_live_weight          INT,
            in_slaugther_weight     INT,
            
            in_sales                DECIMAL(8,1),
            in_harvest_cost         DECIMAL(5,1),
            in_cost_comments        VARCHAR(160)
        )  
        """
        
        sql =  'CALL production_harvest_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        sql += '%s,'    % data.pig_prod_group_id
        sql += '%s,'    % data.acc_pig_buyer_id
        
        sql += '"%s",'  % data.date_harvest
        sql += '%s,'    % data.num_pigs_harvest
        
        if data.live_weight is not None:
            sql += '%s,'    % data.live_weight
        else:
            sql += 'NULL,'
        
        if data.slaughter_weight is not None:
            sql += '%s,'    % data.slaughter_weight
        else:
            sql += 'NULL,'
        
        sql += '%s,'    % data.sales
        sql += '%s,'    % data.harvest_cost
        
        if cost_comments is not None:
            sql += '"%s");'  % data.cost_comments
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
                
                'production_harvest': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE production_harvest_update(
            in_user_id              INT,
            
            in_production_harvest_id INT,
            
            in_date_harvest         VARCHAR(10),
            
            in_num_pigs_harvest     INT,
            in_live_weight          INT,
            in_slaugther_weight     INT,
            
            in_sales                DECIMAL(8,1),
            in_harvest_cost         DECIMAL(5,1),
            in_cost_comments        VARCHAR(160)
        )
        """
       
        sql =  'CALL production_harvest_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.production_harvest_id
        
        sql += '"%s",'  % data.date_harvest
        sql += '%s,'    % data.num_pigs_harvest
        
        if data.live_weight is not None:
            sql += '%s,'    % data.live_weight
        else:
            sql += 'NULL,'
        
        if data.slaughter_weight is not None:
            sql += '%s,'    % data.slaughter_weight
        else:
            sql += 'NULL,'
        
        sql += '%s,'    % data.sales
        sql += '%s,'    % data.harvest_cost
        
        if cost_comments is not None:
            sql += '"%s");'  % data.cost_comments
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
                
                'pig_prod_notes': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id = 0, production_group_id = 0,  inc_user_audit = 0):
        
        where_clause = 'WHERE a.pig_prod_id = %s ' % pig_prod_id
        
        if pig_prod_id > 0:
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.date_harvest,
                        a.num_pigs_harvest,
                        
                        a.live_weight,
                        a.slaugther_weight,
                        
                        a.sales,
                        a.harvest_cost,
                        a.cost_comments,
                        
                        a.acc_pig_buyer_id
                        b.name
                    
                    FROM production_harvest a 
                    LEFT OUTER JOIN acc_pig_buyer b ON a.acc_pig_buyer_id = b.id
                    WHERE a.pig_prod_id = %s
                    ORDER BY a.id DESC
                    """ % pig_prod_id
                    
        else:
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.date_harvest,
                        a.num_pigs_harvest,
                        
                        a.live_weight,
                        a.slaugther_weight,
                        
                        a.sales,
                        a.harvest_cost,
                        a.cost_comments,
                        
                        a.acc_pig_buyer_id
                        b.name
                    
                    FROM production_harvest a 
                    LEFT OUTER JOIN acc_pig_buyer b ON a.acc_pig_buyer_id = b.id
                    WHERE a.production_group_id = %s
                    ORDER BY a.id DESC
                    """ % production_group_id
            
           
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
                cur_entry = {
                    'pig_harvest'{
                        'id':               row[0],
                        'date_harvest':     str(row[1]),
                        'num_pigs':         row[1]
                    }
                   
                }
                
                result.append(cur_entry)
        
        return result
    
    