# September 8, 2025
# Jack Wong

import pandas       as pd 

from common_constants       import *


class FeedCalc:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'FeedCalc'


    def get_pig_prod_list(self, pig_farm_id):
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        
        
        where_clause = 'WHERE a.pig_farm_id = %s AND  a.prod_status_id IN (4, 5, 6) ' % pig_farm_id
             
        sql =   """
                SELECT 
                    a.farm_prod_id,
                    b.number,
                    b.name AS sow_name,
                    
                    a.prod_status_id,
                    c.name AS prod_status,
                    
                    
                    a.date_actual_birth,
                                        
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    a.num_b_kg_lactating,
                    a.num_b_kg_booster,
                    a.num_b_kg_prestarter,
                    a.num_b_kg_starter,
                    a.num_b_kg_grower,
                    a.num_b_kg_finisher,
                    
                    
                    d.date_balance,
                    d.num_pigs,
                    d.num_days_since_birth,
                    d.num_weeks_since_birth,
                    
                    d.num_lactating,
                    d.num_booster,
                    d.num_prestarter,
                    d.num_starter,
                    d.num_grower,
                    d.num_finisher,
                    
                    d.consumed_kg_lactating,
                    d.consumed_kg_booster,
                    d.consumed_kg_prestarter,
                    d.consumed_kg_starter,
                    d.consumed_kg_grower,
                    d.consumed_kg_finisher,
                    
                    d.consumed_kg_total,
                                       
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher
                    
                    
                FROM pig_production a
                LEFT OUTER JOIN sow_boar b          ON a.sow_id = b.id
                LEFT OUTER JOIN pig_prod_status c   ON a.prod_status_id = c.id
                LEFT OUTER JOIN feed_balance d      ON a.last_feed_balance_id = d.id
                %s
                ORDER BY a.date_actual_birth DESC
                """ % where_clause 
    
        rows = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()

        except Exception as e:
            msg = 'get_pig_prod_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        
        """
        Convert to pandas dataframe with these columns
        """
        

        prod_id         = []
        sow_number      = []
        sow_name        = []
        status_id       = []
        status_name     = []
        
        date_birth      = []
        
        date_balance    = []
        bal_num_pigs    = []
        days_since_b    = []
        weeks_since_b   = []
        
        buy_num_LAC     = []
        bal_num_LAC     = []
        con_num_LAC     = []
        
        buy_kg_LAC      = []
        bal_kg_LAC      = []
        con_kg_LAC      = []
        
        buy_num_BOS     = []
        bal_num_BOS     = []
        con_num_BOS     = []
        
        buy_kg_BOS      = []
        bal_kg_BOS      = []
        con_kg_BOS      = []
        
        buy_num_PRE     = []
        bal_num_PRE     = []
        con_num_PRE     = []
        
        buy_kg_PRE      = []
        bal_kg_PRE      = []
        con_kg_PRE      = []
        
        buy_num_STR     = []
        bal_num_STR     = []
        con_num_STR     = []
        
        buy_kg_STR      = []
        bal_kg_STR      = []
        con_kg_STR      = []
        
        buy_num_GRO     = []
        bal_num_GRO     = []
        con_num_GRO     = []
        
        buy_kg_GRO      = []
        bal_kg_GRO      = []
        con_kg_GRO      = []
        
        buy_num_FIN     = []
        bal_num_FIN     = []
        con_num_FIN     = []
        
        buy_kg_FIN      = []
        bal_kg_FIN      = []
        con_kg_FIN      = []
        
        
        con_kg_total    = []
      
        
        cost_LAC        = []
        cost_BOS        = []
        cost_PRE        = []
        cost_STR        = []
        cost_GRO        = []
        cost_FIN        = []
        
        
        if rows is not None:
            
            for row in rows:
                prod_id         .append(row[0])
                sow_number      .append(row[1])
                sow_name        .append(row[2])
                status_id       .append(row[3])
                status_name     .append(row[4])
                    
                    
                date_birth      .append(row[5])  # dont convert to string
                                            
                buy_num_LAC     .append(row[6])
                buy_num_BOS     .append(row[7])
                buy_num_PRE     .append(row[8])
                buy_num_STR     .append(row[9])
                buy_num_GRO     .append(row[10])
                buy_num_FIN     .append(row[11])
                    
                buy_kg_LAC      .append(row[12])
                buy_kg_BOS      .append(row[13])
                buy_kg_PRE      .append(row[14])
                buy_kg_STR      .append(row[15])
                buy_kg_GRO      .append(row[16])
                buy_kg_FIN      .append(row[17])
                    
                    
                date_balance    .append(row[18]) # dont convert to string
                bal_num_pigs    .append(row[19])
                days_since_b    .append(row[20])
                weeks_since_b   .append(row[21])
                
                bal_num_LAC     .append(float(row[22]) if row[22] is not None else None)
                bal_num_BOS     .append(float(row[23]) if row[23] is not None else None)
                bal_num_PRE     .append(float(row[24]) if row[24] is not None else None)
                bal_num_STR     .append(float(row[25]) if row[25] is not None else None)
                bal_num_GRO     .append(float(row[26]) if row[26] is not None else None)
                bal_num_FIN     .append(float(row[27]) if row[27] is not None else None)
                
                con_kg_LAC      .append(row[28])
                con_kg_BOS      .append(row[29])
                con_kg_PRE      .append(row[30])
                con_kg_STR      .append(row[31])
                con_kg_GRO      .append(row[32])
                con_kg_FIN      .append(row[33])
                
                con_kg_total    .append(row[34])
                diff_con_kg     .append(row[35])
                diff_con_pp     .append(row[36])
                
                cost_LAC        .append(float(row[37]) if row[37] is not None else None)
                cost_BOS        .append(float(row[38]) if row[38] is not None else None)
                cost_PRE        .append(float(row[39]) if row[39] is not None else None)
                cost_STR        .append(float(row[40]) if row[40] is not None else None)
                cost_GRO        .append(float(row[41]) if row[41] is not None else None)
                cost_FIN        .append(float(row[42]) if row[42] is not None else None)
        
        
        len_items = len(prod_id)
        
        data = {
            'p_id':             prod_id,
            'sow_number':       sow_number,
            'sow_name':         sow_name,
            'status_id':        status_id,
            'status_name':      status_name,
                
            'date_birth':       date_birth,
                
            'date_bal':         date_balance,
            'num_pigs':         bal_num_pigs,
            'days_b':           days_since_b,
            'weeks_b':          weeks_since_b,
            
            'buy_num_LAC':      buy_num_LAC,
            'bal_num_LAC':      bal_num_LAC,
            'con_num_LAC':      [None] * len_items,
            
            'buy_kg_LAC':       buy_kg_LAC,
            'bal_kg_LAC':       [None] * len_items,
            'con_kg_LAC':       con_kg_LAC,
            
            'buy_num_BOS':      buy_num_BOS,
            'bal_num_BOS':      bal_num_BOS,
            'con_num_BOS':      [None] * len_items,
            
            'buy_kg_BOS':       buy_kg_BOS,
            'bal_kg_BOS':       [None] * len_items,
            'con_kg_BOS':       con_kg_BOS,
           
            
            'buy_num_PRE':      buy_num_PRE,
            'bal_num_PRE':      bal_num_PRE,
            'con_num_PRE':      [None] * len_items,
            
            'buy_kg_PRE':       buy_kg_PRE,
            'bal_kg_PRE':       [None] * len_items,
            'con_kg_PRE':       con_kg_PRE,
            
            'buy_num_STR':      buy_num_STR,
            'bal_num_STR':      bal_num_STR,
            'con_num_STR':      [None] * len_items,
            
            'buy_kg_STR':       buy_kg_STR,
            'bal_kg_STR':       [None] * len_items,
            'con_kg_STR':       con_kg_STR,
            
            'buy_num_GRO':      buy_num_GRO,
            'bal_num_GRO':      bal_num_GRO,
            'con_num_GRO':      [None] * len_items,
            
            'buy_kg_GRO':       buy_kg_GRO,
            'bal_kg_GRO':       [None] * len_items,
            'con_kg_GRO':       con_kg_GRO,
            
            'buy_num_FIN':      buy_num_FIN,
            'bal_num_FIN':      bal_num_FIN,
            'con_num_FIN':      [None] * len_items,
            
            'buy_kg_FIN':       buy_kg_FIN,
            'bal_kg_FIN':       [None] * len_items,
            'con_kg_FIN':       con_kg_FIN,
                
                
            'con_kg_total':     con_kg_total,
            
            'cost_LAC':         cost_LAC,
            'cost_BOS':         cost_BOS,
            'cost_PRE':         cost_PRE,
            'cost_STR':         cost_STR,
            'cost_GRO':         cost_GRO,
            'cost_FIN':         cost_FIN
            
        }
        
        return pd.DataFrame(data)
        
        
    def get_feed_consumed_list(self, pig_farm_id, by_pig_prod = 1):
        
        if by_pig_prod > 0:
            sql =   """
                SELECT 
                    a.farm_prod_id,
                    
                    c.number,
                    c.name, 
                    
                    a.date_actual_birth,
                    
                    b.date_balance,
                    b.num_days_since_birth,
                    b.num_weeks_since_birth,
                    
                    b.num_pigs,
                    
                    b.consumed_kg_lactating,
                    b.consumed_kg_booster,
                    b.consumed_kg_prestarter,
                    b.consumed_kg_starter,
                    b.consumed_kg_grower,
                    b.consumed_kg_finisher,
                        
                        
                    b.consumed_kg_total,
                    b.diff_consumed_kg_total,
                    b.diff_consumption_per_pig
                    
                FROM pig_production a 
                RIGHT JOIN feed_balance b       ON a.id = b.pig_prod_id
                LEFT OUTER JOIN sow_boar c      ON a.sow_id  = c.id
                WHERE a.pig_farm_id = %s AND a.prod_status_id IN (4,5,6)
                ORDER BY a.date_actual_birth DESC, b.id DESC
                """ % pig_farm_id
                
        else:
            #TODO
            test = 1
            
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
            msg = 'get_feed_consumed_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        
        prod_id         = []
        sow_number      = []
        sow_name        = []
        
        date_birth      = []
        
        date_balance    = []
        days_since_b    = []
        weeks_since_b   = []
        bal_num_pigs    = []
        
        con_kg_LAC      = []
        con_kg_BOS      = []
        con_kg_PRE      = []
        con_kg_STR      = []
        con_kg_GRO      = []
        con_kg_FIN      = []
        
        con_kg_tot      = []
        con_kg_diff     = []
        con_kg_diff_pp  = []
        
        
        if rows is not None:
            
            for row in rows:
                prod_id         .append(row[0])
                sow_number      .append(row[1])
                sow_name        .append(row[2])
                    
                date_birth      .append(str(row[3])) 
                
                date_balance    .append(str(row[4]))
                days_since_b    .append(row[5])
                weeks_since_b   .append(row[6])
                bal_num_pigs    .append(row[7])
                
                con_kg_LAC      .append(row[8])
                con_kg_BOS      .append(row[9])
                con_kg_PRE      .append(row[10])
                con_kg_STR      .append(row[11])
                con_kg_GRO      .append(row[12])
                con_kg_FIN      .append(row[13])
                    
                con_kg_tot      .append(row[14])
                con_kg_diff     .append(row[15])
                con_kg_diff_pp  .append(float(row[16]) if row[16] is not None else None)
                
                
        len_items = len(prod_id)
        
        data = {
            'p_id':             prod_id,
            'sow_number':       sow_number,
            'sow_name':         sow_name,
            'date_birth':       date_birth,
                
            'date_bal':         date_balance,
            'days_b':           days_since_b,
            'weeks_b':          weeks_since_b,
            'num_pigs':         bal_num_pigs,
            
            'con_kg_LAC':       con_kg_LAC,
            'con_kg_BOS':       con_kg_BOS,
            'con_kg_PRE':       con_kg_PRE, 
            'con_kg_STR':       con_kg_STR,
            'con_kg_GRO':       con_kg_GRO,
            'con_kg_FIN':       con_kg_FIN,
            
            'con_num_LAC':      [None] * len_items,
            'con_num_BOS':      [None] * len_items,
            'con_num_PRE':      [None] * len_items,
            'con_num_STR':      [None] * len_items,
            'con_num_GRO':      [None] * len_items,
            'con_num_FIN':      [None] * len_items,
            
            'con_kg_tot':       con_kg_tot,
            'con_kg_diff':      con_kg_diff,
            'con_kg_diff_pp':   con_kg_diff_pp
        }
        
        return pd.DataFrame(data)
    
    