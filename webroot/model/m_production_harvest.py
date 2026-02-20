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
            in_harvest_type_id      INT,
            
            in_live_weight                  DECIMAL(6,1),
            in_live_price_per_unit          DECIMAL(6,1),
            
            in_slaughter_weight             DECIMAL(6,1),
            in_slaughter_minus_weight       DECIMAL(6,1),
            in_slaughther_price_per_unit    DECIMAL(6,1),
            
            in_net_sales            DECIMAL(8,1),
            in_harvest_cost         DECIMAL(5,1),
            in_comments             VARCHAR(160),
            
            in_weight_pp_live       VARCHAR(400),
            in_weight_pp_slaughter  VARCHAR(400)
        )  
        """
        
        sql =  'CALL production_harvest_add('
        sql += '%s,'    % data.user_id
        
        
        if data.pig_prod_id is not None and data.pig_prod_id > 0:
            sql += '%s,'    % data.pig_prod_id
        else:
            sql += 'NULL,'
        
        if data.production_group_id is not None and data.production_group_id > 0:
            sql += '%s,'    % data.pig_prod_group_id
        else:
            sql += 'NULL,'
            
        if data.acc_pig_buyer_id is not None and data.acc_pig_buyer_id > 0: 
            sql += '%s,'    % data.acc_pig_buyer_id
        else:
            sql += 'NULL,'
        
        
        sql += '"%s",'  % data.date_harvest
        sql += '%s,'    % data.num_pigs
        sql += '%s,'    % data.harvest_type_id
        
        if data.live_weight is not None:
            sql += '%s,'    % data.live_weight
        else:
            sql += 'NULL,'
        
        if data.live_price is not None:
            sql += '%s,'    % data.live_price
        else:
            sql += 'NULL,'
        
        
        
        if data.slaughter_weight is not None:
            sql += '%s,'    % data.slaughter_weight
        else:
            sql += 'NULL,'
            
        if data.slaughter_minus_weight is not None:
            sql += '%s,'    % data.slaughter_minus_weight
        else:
            sql += 'NULL,'
          
        if data.slaughter_price is not None:
            sql += '%s,'    % data.slaughter_price
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
            sql += '"%s",'  % data.comments
        else:
            sql += 'NULL,'
        
        
        if data.weight_pp_lw_csv is not None:
            sql += '"%s",'  % data.weight_pp_lw_csv
        else:
            sql += 'NULL,'
        
        
        if data.weight_pp_sw_csv is not None:
            sql += '"%s");'  % data.weight_pp_sw_csv
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
                
                'prod_harvest': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE production_harvest_update(
            in_user_id              INT,
            
            in_acc_pig_buyer_id     INT,
            
            in_production_harvest_id INT,
            
            in_date_harvest         VARCHAR(10),
    
            in_num_pigs_harvest     INT,
            in_harvest_type_id      INT,
            
            in_live_weight                  DECIMAL(6,1),
            in_live_price_per_unit          DECIMAL(6,1),
            
            in_slaughter_weight             DECIMAL(6,1),
            in_slaughter_minus_weight       DECIMAL(6,1),
            in_slaughther_price_per_unit    DECIMAL(6,1),
            
            in_net_sales            DECIMAL(8,1),
            in_harvest_cost         DECIMAL(5,1),
            in_comments             VARCHAR(160),
            
            in_weight_pp_live       VARCHAR(400),
            in_weight_pp_slaughter  VARCHAR(400)
        )
        """
       
        sql =  'CALL production_harvest_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.prod_harvest_id
        
        if data.acc_pig_buyer_id is not None and data.acc_pig_buyer_id > 0: 
            sql += '%s,'    % data.acc_pig_buyer_id
        else:
            sql += 'NULL,'
        
        
        sql += '"%s",'  % data.date_harvest
        sql += '%s,'    % data.num_pigs
        sql += '%s,'    % data.harvest_type_id
        
        
        if data.live_weight is not None:
            sql += '%s,'    % data.live_weight
        else:
            sql += 'NULL,'
        
        if data.live_price is not None:
            sql += '%s,'    % data.live_price
        else:
            sql += 'NULL,'
        
        
        
        if data.slaughter_weight is not None:
            sql += '%s,'    % data.slaughter_weight
        else:
            sql += 'NULL,'
            
        if data.slaughter_minus_weight is not None:
            sql += '%s,'    % data.slaughter_minus_weight
        else:
            sql += 'NULL,'
          
        if data.slaughter_price is not None:
            sql += '%s,'    % data.slaughter_price
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
            sql += '"%s"'  % data.comments
        else:
            sql += 'NULL,'
        
        
        if data.weight_pp_lw_csv is not None:
            sql += '"%s",'  % data.weight_pp_lw_csv
        else:
            sql += 'NULL,'
        
        
        if data.weight_pp_sw_csv is not None:
            sql += '"%s");'  % data.weight_pp_sw_csv
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
                
                'prod_harvest': {
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
                        a.num_days_since_birth,
                        
                        a.harvest_type_id,
                        
                        a.live_weight,
                        a.live_weight_ave,
                        a.live_price_per_unit,
                        
                        a.slaugther_weight,
                        a.slaughter_weight_ave,
                        a.slaugther_minus_weight,
                        a.slaughter_net_weight,
                        a.slaughter_price_per_unit,
                        
                        a.net_sales,
                        a.net_sales_per_pig,
                        a.harvest_cost,
                        a.comments,
                        
                        
                        a.weight_pp_lw_csv,
                        a.weight_pp_sw_csv,
                        
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
                        a.num_days_since_birth,
                        
                        a.harvest_type_id,
                        
                        a.live_weight,
                        a.live_weight_ave,
                        a.live_price_per_unit,
                        
                        a.slaugther_weight,
                        a.slaughter_weight_ave,
                        a.slaugther_minus_weight,
                        a.slaughter_net_weight,
                        a.slaughter_price_per_unit,
                        
                        a.net_sales,
                        a.net_sales_per_pig,
                        a.harvest_cost,
                        a.comments,
                        
                        
                        a.weight_pp_lw_csv,
                        a.weight_pp_sw_csv,
                        
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
                cur_id                  = row[0]
                
                cur_date_harvest        = str(row[1])
                cur_num_pigs_harvest    = row[2]
                cur_num_days_since_birth= row[3]
                
                cur_harvest_type_id     = row[4]
                
                cur_live_weight         = float(row[5]) if row[5] else None
                cur_live_weight_ave     = float(row[6]) if row[6] else None 
                cur_live_price_per_unit = float(row[7]) if row[7] else None
                
                cur_slaugther_weight        = float(row[8]) if row[8] else None
                cur_slaughter_weight_ave    = float(row[9]) if row[9] else None
                cur_slaughter_minus_weight  = float(row[10]) if row[10] else None
                cur_slaughter_net_weight    = float(row[11]) if row[11] else None
                cur_slaughter_price_per_unit= float(row[12]) if row[12] else None
                
                cur_net_sales           = float(row[13]) if row[13] else None
                cur_net_sales_per_pig   = float(row[14]) if row[14] else None
                cur_harvest_cost        = float(row[15]) if row[15] else None
                cur_comments            = row[16]
                
                cur_weight_pp_lw_csv    = row[17]
                cur_weight_pp_sw_csv    = row[18]
                
                cur_acc_pig_buyer_id    = row[19]
                cur_acc_pig_buyer_name  = row[20]
                
                
                
                cur_entry = {
                    'prod_harvest': {
                        'id':               cur_id,
                        'date_harvest':     cur_date_harvest,
                        'num_pigs':         cur_num_pigs_harvest,
                        'num_days':         cur_num_days_since_birth,
                        
                        'harvest_type_id':  cur_harvest_type_id,
                        
                        'live_weight': {
                            'weight':       cur_live_weight,
                            'weight_ave':   cur_live_weight_ave,
                            'price':        cur_live_price_per_unit,
                            'pp_csv':       cur_weight_pp_lw_csv
                        },
                            
                        
                        'slaugther_weight': {
                            'weight':       cur_slaugther_weight,
                            'net_weight':   cur_slaughter_net_weight,
                            'weight_ave':   cur_slaughter_weight_ave,
                            'price':        cur_slaughter_price_per_unit,
                            'pp_csv':       cur_weight_pp_sw_csv
                        },
                        
                        
                        
                        'sales':           { 
                            'net_sales':    cur_net_sales,
                            'sales_pp':     cur_net_sales_per_pig,
                            'harvest_cost': cur_harvest_cost
                        
                        },
                        
                        'notes': cur_comments,
                        
                        'pig_buyer':{
                            'id':           cur_acc_pig_buyer_id,
                            'name':         cur_acc_pig_buyer_name,
                        }
                        
                    }
                   
                }
                
                result.append(cur_entry)
        
        return result
    
    
