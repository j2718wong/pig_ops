# September 18, 2025
# Jack Wong

from common_constants       import *


class ProductionHarvest:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'ProductionHarvest'


    def get_harvest_type(self):
        


    def add(self, data = None):
        """
        PROCEDURE production_harvest_add(
            in_user_id              INT,
            in_pig_prod_id          INT,
            in_production_group_id  INT,
            in_acc_pig_buyer_id     INT,
            
            in_date_harvest         VARCHAR(10),
            
            in_num_pigs_harvest     INT,
            in_harvest_type_id      INT,
            
            in_live_weight          INT,
            in_slaughter_weight     DECIMAL(6,1),
            in_slaughter_net_weight DECIMAL(6,1),
            
            in_live_price_per_unit          DECIMAL(6,1),
            in_slaughther_price_per_unit    DECIMAL(6,1),
            
            in_net_sales            DECIMAL(8,1),
            in_harvest_cost         DECIMAL(5,1),
            in_comments             VARCHAR(160)
        )  
        """
        
        sql =  'CALL production_harvest_add('
        sql += '%s,'    % data.user_id
        
        
        if data.pig_prod_id is not None and data.pig_prod_id > 0:
            sql += '%s,'    % data.pig_prod_id
        else:
            sql += 'NULL,'
        
        if data.pig_prod_group_id is not None and data.pig_prod_group_id > 0:
            sql += '%s,'    % data.pig_prod_group_id
        else:
            sql += 'NULL,'
            
        sql += '%s,'    % data.acc_pig_buyer_id
        
        sql += '"%s",'  % data.date_harvest
        sql += '%s,'    % data.num_pigs_harvest
        sql += '%s,'    % data.harvest_type_id
        
        if data.live_weight is not None:
            sql += '%s,'    % data.live_weight
        else:
            sql += 'NULL,'
        
        if data.slaughter_weight is not None:
            sql += '%s,'    % data.slaughter_weight
        else:
            sql += 'NULL,'
            
        if data.slaughter_net_weight is not None:
            sql += '%s,'    % data.slaughter_net_weight
        else:
            sql += 'NULL,'
        
        if data.live_price_per_unit is not None:
            sql += '%s,'    % data.live_price_per_unit
        else:
            sql += 'NULL,'
        
        if data.slaughter_price_per_unit is not None:
            sql += '%s,'    % data.slaughter_price_per_unit
        else:
            sql += 'NULL,'
        
        if data.net_sales is not None:
            sql += '%s,'    % data.net_sales
        else:
            sql += 'NULL,'
            
        if data.harvest_cost is not None:
            sql += '%s,'    % data.harvest_cost
        else:
            sql += 'NULL,'
        
        
        if data.comments is not None:
            sql += '"%s");'  % data.comments
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
            in_harvest_type_id      INT,
            
            in_live_weight          DECIMAL(6,1),
            in_slaughter_weight     DECIMAL(6,1),
            in_slaughter_net_weight DECIMAL(6,1),
            
            in_live_price_per_unit          DECIMAL(6,1),
            in_slaughther_price_per_unit    DECIMAL(6,1),
            
            in_net_sales            DECIMAL(8,1),
            in_harvest_cost         DECIMAL(5,1),
            in_comments             VARCHAR(160)
        )
        """
       
        sql =  'CALL production_harvest_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.production_harvest_id
        
        sql += '"%s",'  % data.date_harvest
        sql += '%s,'    % data.num_pigs_harvest
        sql += '%s,'    % data.harvest_type_id
        
        if data.live_weight is not None:
            sql += '%s,'    % data.live_weight
        else:
            sql += 'NULL,'
        
        if data.slaughter_weight is not None:
            sql += '%s,'    % data.slaughter_weight
        else:
            sql += 'NULL,'
            
        if data.slaughter_net_weight is not None:
            sql += '%s,'    % data.slaughter_net_weight
        else:
            sql += 'NULL,'
        
        if data.live_price_per_unit is not None:
            sql += '%s,'    % data.live_price_per_unit
        else:
            sql += 'NULL,'
        
        if data.slaughter_price_per_unit is not None:
            sql += '%s,'    % data.slaughter_price_per_unit
        else:
            sql += 'NULL,'
        

        sql += '%s,'    % data.net_sales
        sql += '%s,'    % data.harvest_cost
        
        if data.comments is not None:
            sql += '"%s");'  % data.comments
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
        
        if pig_prod_id > 0:
            where_clause = 'WHERE a.pig_prod_id = %s ' % pig_prod_id
        
        if production_group_id > 0:
            where_clause = 'WHERE a.production_group_id = %s ' % production_group_id
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.date_harvest,
                        a.num_pigs_harvest,
                        
                        a.live_weight,
                        a.live_weight_ave,
                        a.live_price_per_unit,
                        
                        a.slaugther_weight,
                        a.slaughter_weight_ave,
                        a.slaughter_net_weight,
                        a.slaughter_price_per_unit,
                        
                        a.sales,
                        a.harvest_cost,
                        a.comments,
                        
                        a.acc_pig_buyer_id,
                        b.name AS acc_pig_buyer_name
                    
                    FROM production_harvest a 
                    LEFT OUTER JOIN acc_pig_buyer b ON a.acc_pig_buyer_id = b.id
                    %s
                    ORDER BY a.id DESC
                    """ % where_clause
                    
        else:
            sql =   """
                    SELECT 
                        a.id,
                        
                        a.date_harvest,
                        a.num_pigs_harvest,
                        
                        a.live_weight,
                        a.live_weight_ave,
                        a.live_price_per_unit,
                        
                        a.slaugther_weight,
                        a.slaughter_weight_ave,
                        a.slaughter_net_weight,
                        a.slaughter_price_per_unit,
                        
                        a.sales,
                        a.harvest_cost,
                        a.comments,
                        
                        a.acc_pig_buyer_id,
                        b.name AS acc_pig_buyer_name,
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                    
                    FROM production_harvest a 
                    LEFT OUTER JOIN acc_pig_buyer b ON a.acc_pig_buyer_id = b.id
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    ORDER BY a.id DESC
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
                        'num_pigs':         row[2],
                        
                        'live_weight':      float(row[3])   if row[3] is not None else None,
                        'live_weight_ave':  float(row[4])   if row[4] is not None else None, 
                        'live_ppu':         float(row[5])   if row[5] is not None else None,
                        
                        'slaugther_weight': float(row[6])   if row[6] is not None else None,
                        'slaughter_weight_ave':float(row[7])if row[7] is not None else None,
                        'slaughter_net_weight':float(row[8])if row[8] is not None else None,
                        'slaughter_ppu':    float(row[9])   if row[9] is not None else None,
                        
                        'sales':            float(row[10])   if row[10] is not None else None,
                        'harvest_cost':     float(row[11])   if row[11] is not None else None,
                        'comments':,
                        
                        
                    }
                   
                }
                
                result.append(cur_entry)
        
        return result
    
    