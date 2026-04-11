# September 18, 2025
# Jack Wong
import os
import sys

from common_constants       import *

# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)

from base_model             import BaseModel


class ProductionHarvest(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE production_harvest_add(
            in_user_id              INT,
            in_pig_prod_id          INT,
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
        
        params = [
            data.user_id,
            
            data.pig_prod_id,
            data.acc_pig_buyer_id           if data.acc_pig_buyer_id and data.acc_pig_buyer_id > 0 else None,
            
            data.date_harvest,
            
            data.num_pigs,
            data.harvest_type_id,
            
            data.live_weight                if data.live_weight is not None else None,
            data.live_price                 if data.live_price is not None else None,
            
            data.slaughter_weight           if data.slaughter_weight is not None else None,
            data.slaughter_minus_weight     if data.slaughter_minus_weight is not None else None,
            data.slaughter_price            if data.slaughter_price is not None else None,
            
            data.net_sales                  if data.net_sales is not None else None,
            data.harvest_cost               if data.harvest_cost is not None else None,
            
            data.comments                   if data.comments and data.comments.strip() else None,
            
            data.weight_pp_lw_csv           if data.weight_pp_lw_csv and data.weight_pp_lw_csv.strip() else None,
            data.weight_pp_sw_csv           if data.weight_pp_sw_csv and data.weight_pp_sw_csv.strip() else None
        ]
        
        rows = self._call_procedure('production_harvest_add', params)
        
        
        if rows is None:
            return None
    
        row = rows[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'prod_harvest': {
                    'id':               row[3],
                    'prod_status_id':   row[4]
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
       
        params = [
            data.user_id,
            
            data.prod_harvest_id,
            
            data.acc_pig_buyer_id           if data.acc_pig_buyer_id and data.acc_pig_buyer_id > 0 else None,
            
            data.date_harvest,
            
            data.num_pigs,
            data.harvest_type_id,
            
            data.live_weight                if data.live_weight is not None else None,
            data.live_price                 if data.live_price is not None else None,
            
            data.slaughter_weight           if data.slaughter_weight is not None else None,
            data.slaughter_minus_weight     if data.slaughter_minus_weight is not None else None,
            data.slaughter_price            if data.slaughter_price is not None else None,
            
            data.net_sales                  if data.net_sales is not None else None,
            data.harvest_cost               if data.harvest_cost is not None else None,
            
            data.comments                   if data.comments and data.comments.strip() else None,
            
            data.weight_pp_lw_csv           if data.weight_pp_lw_csv and data.weight_pp_lw_csv.strip() else None,
            data.weight_pp_sw_csv           if data.weight_pp_sw_csv and data.weight_pp_sw_csv.strip() else None
        ]
        
        rows = self._call_procedure('production_harvest_update', params)
        
        if rows is None:
            return None
        
        row = rows[0]

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'prod_harvest': {
                    'id':               row[3],
                    'prod_status_id':   row[4]
                }
            }

        return None
    
    
    def get_list(self, pig_farm_id = 0, pig_prod_id = 0, inc_user_audit = 0):
        
        """
        if pig_farm_id is given, the result structure will be different
        result = [
            {   'pig_prod_id': 1,
                'list_harvest':[]
            }
            
        ]
        
        if pig_farm_id is not given, the result is just plain array
        
        """
        
        
        if pig_farm_id > 0:
            where_clause = 'WHERE a.pig_farm_id = %s ' % pig_farm_id
        
        if pig_prod_id > 0:
            where_clause = 'WHERE a.pig_prod_id = %s ' % pig_prod_id
        
        
        order_clause = 'ORDER BY a.date_harvest DESC'
        
        if pig_farm_id > 0:
            order_clause = 'ORDER BY a.pig_prod_id DESC, a.date_harvest DESC'
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.pig_prod_id,
                        
                        a.date_harvest,
                        a.num_pigs_harvest,
                        a.num_days_since_birth,
                        
                        a.harvest_type_id,
                        
                        a.live_weight,
                        a.live_weight_ave,
                        a.live_price_per_unit,
                        
                        a.slaughter_weight,
                        a.slaughter_weight_ave,
                        a.slaughter_minus_weight,
                        a.slaughter_net_weight,
                        a.slaughter_price_per_unit,
                        
                        a.net_sales,
                        a.net_sales_pp,
                        a.harvest_cost,
                        a.comments,
                        
                        
                        a.weight_pp_lw_csv,
                        a.weight_pp_sw_csv,
                        
                        a.acc_pig_buyer_id,
                        b.name AS acc_pig_buyer_name
                    
                    FROM production_harvest a 
                    LEFT OUTER JOIN account_pig_buyer b ON a.acc_pig_buyer_id = b.id
                    %s
                    %s
                    """ % (where_clause, order_clause)
                    
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.pig_prod_id,
                        
                        a.date_harvest,
                        a.num_pigs_harvest,
                        a.num_days_since_birth,
                        
                        a.harvest_type_id,
                        
                        a.live_weight,
                        a.live_weight_ave,
                        a.live_price_per_unit,
                        
                        a.slaughter_weight,
                        a.slaughter_weight_ave,
                        a.slaughter_minus_weight,
                        a.slaughter_net_weight,
                        a.slaughter_price_per_unit,
                        
                        a.net_sales,
                        a.net_sales_pp,
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
                    LEFT OUTER JOIN account_pig_buyer b ON a.acc_pig_buyer_id = b.id
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    %s
                    """ % (where_clause, order_clause)
            
           
        rows = self._execute_query(sql)
        
        if rows is None:
            return None

        
        result = []
        if rows is not None:
            
            last_pig_prod_id = None
            
            for row in rows:
                cur_id                  = row[0]
                cur_pig_prod_id         = row[1]
                
                cur_date_harvest        = str(row[2])
                cur_num_pigs_harvest    = row[3]
                cur_num_days_since_birth= row[4]
                
                cur_harvest_type_id     = row[5]
                
                cur_live_weight         = float(row[6]) if row[6] else None
                cur_live_weight_ave     = float(row[7]) if row[7] else None 
                cur_live_price_per_unit = float(row[8]) if row[8] else None
                
                cur_slaughter_weight        = float(row[9]) if row[9] else None
                cur_slaughter_weight_ave    = float(row[10]) if row[10] else None
                cur_slaughter_minus_weight  = float(row[11]) if row[11] else None
                cur_slaughter_net_weight    = float(row[12]) if row[12] else None
                cur_slaughter_price_per_unit= float(row[13]) if row[13] else None
                
                cur_net_sales           = float(row[14]) if row[14] else None
                cur_net_sales_per_pig   = float(row[15]) if row[15] else None
                cur_harvest_cost        = float(row[16]) if row[16] else None
                cur_comments            = row[17]
                
                cur_weight_pp_lw_csv    = row[18]
                cur_weight_pp_sw_csv    = row[19]
                
                cur_acc_pig_buyer_id    = row[20]
                cur_acc_pig_buyer_name  = row[21]
                
                
                
                cur_entry = {
                    'prod_harvest': {
                        'id':               cur_id,
                        'pig_prod_id':      cur_pig_prod_id,
                        
                        'date_harvest':     cur_date_harvest,
                        'num_pigs':         cur_num_pigs_harvest,
                        'num_days':         cur_num_days_since_birth,
                        
                        'harvest_type_id':  cur_harvest_type_id,
                        
                        'live_weight': {
                            'weight':       cur_live_weight,
                            'average':      cur_live_weight_ave,
                            'price':        cur_live_price_per_unit,
                            'pp_csv':       cur_weight_pp_lw_csv
                        },
                            
                        
                        'slaughter_weight': {
                            'weight':       cur_slaughter_weight,
                            'minus':        cur_slaughter_minus_weight,
                            'net_weight':   cur_slaughter_net_weight,
                            'average':      cur_slaughter_weight_ave,
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
                
                
                
                
                
                # remove null data
                if cur_acc_pig_buyer_id is None:
                    del cur_entry['prod_harvest']['pig_buyer']  
                    
                    
                if cur_live_weight is None:
                    del cur_entry['prod_harvest']['live_weight']
                    
                    
                if cur_net_sales is None:
                    del cur_entry['prod_harvest']['sales']
                

                
                
                if pig_farm_id == 0:
                    # No need for this if not given
                    del cur_entry['prod_harvest']['pig_prod_id']  
                
                    result.append(cur_entry)
                    
                else:
                    
                    if last_pig_prod_id is None or last_pig_prod_id != cur_pig_prod_id:
                        last_pig_prod_id = cur_pig_prod_id
                        
                        cur_harvest = {
                            'pig_prod_id': cur_pig_prod_id,
                            'list_harvest': []
                        }
                        
                        result.append(cur_harvest)
                        
                    
                    cur_harvest['list_harvest'].append(cur_entry)
        
        return result
    
    
