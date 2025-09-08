# September 8, 2025
# Jack Wong

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
                    
                    a.num_pigs_current,
                    
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
                    d.num_days_since_birth,
                    d.num_weeks_since_birth,
                    
                    d.num_lactating,
                    d.num_booster,
                    d.num_prestarter,
                    d.num_starter,
                    d.num_grower,
                    d.num_finisher,
                    
                    
                    d.cons_kg_lactating,
                    d.cons_kg_booster,
                    d.cons_kg_prestarter,
                    d.cons_kg_starter,
                    d.cons_kg_grower,
                    d.cons_kg_finisher,
                    
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher,
                    
                    
                FROM pig_production a
                LEFT OUTER JOIN sow_boar b          ON a.sow_id = b.id
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
        

        result = []
        if rows is not None:
            
            for row in rows:
                cur_farm_prod_id        = row[0]
                cur_sow_number          = row[1]
                cur_sow_name            = row[2]
                
                cur_status_id           = row[3]
                
                cur_num_pigs_current    = row[4]
               
                cur_date_actual         = str(row[5])   if row[5]  else None
                
                cur_num_b_lactating     = row[6]
                cur_num_b_booster       = row[7]
                cur_num_b_prestarter    = row[8]
                cur_num_b_starter       = row[9]
                cur_num_b_grower        = row[10]
                cur_num_b_finisher      = row[11]
                
                cur_num_b_kg_lactating  = row[12]
                cur_num_b_kg_booster    = row[13]
                cur_num_b_kg_prestarter = row[14]
                cur_num_b_kg_starter    = row[15]
                cur_num_b_kg_grower     = row[16]
                cur_num_b_kg_finisher   = row[17]
                
                
                cur_bal_date_balance            = row[18]
                cur_bal_num_days_since_birth    = row[19]
                cur_bal_num_weeks_since_birth   = row[20]
                
                cur_bal_num_lactating   = float(row[21]) if row[21] is not None else None
                cur_bal_num_booster     = float(row[22]) if row[22] is not None else None
                cur_bal_num_prestarter  = float(row[23]) if row[23] is not None else None
                cur_bal_num_starter     = float(row[24]) if row[24] is not None else None
                cur_bal_num_grower      = float(row[25]) if row[25] is not None else None
                cur_bal_num_finisher    = float(row[26]) if row[26] is not None else None
                
                
                cur_cons_kg_lactating   = float(row[27]) if row[21] is not None else None
                cur_cons_kg_booster     = float(row[28]) if row[22] is not None else None
                cur_cons_kg_prestarter  = float(row[29]) if row[23] is not None else None
                cur_cons_kg_starter     = float(row[30]) if row[24] is not None else None
                cur_cons_kg_grower      = float(row[31]) if row[25] is not None else None
                cur_cons_kg_finisher    = float(row[32]) if row[26] is not None else None
                
                
                cur_cost_lactating      = float(row[33]) if row[27] is not None else None
                cur_cost_booster        = float(row[34]) if row[28] is not None else None
                cur_cost_prestarter     = float(row[35]) if row[29] is not None else None
                cur_cost_starter        = float(row[30]) if row[30] is not None else None
                cur_cost_grower         = float(row[31]) if row[31] is not None else None
                cur_cost_finisher       = float(row[32]) if row[32] is not None else None
                
                
                cur_cons_num_lactating  = None
                cur_cons_num_booster    = None
                cur_cons_num_prestarter = None
                cur_cons_num_starter    = None
                cur_cons_num_grower     = None
                cur_cons_num_finisher   = None
                
                cur_kg_cons_lactating   = None
                cur_kg_cons_booster     = None
                cur_kg_cons_prestarter  = None
                cur_kg_cons_starter     = None
                cur_kg_cons_grower      = None
                cur_kg_cons_finisher    = None
                
                
            
                if cur_num_b_lactating is not None and cur_cons_num_lactating is not None:
                    cur_cons_num_lactating  = float(cur_num_b_lactating) - cur_cons_num_lactating
                    cur_kg_cons_lactating   = cur_num_b_kg_lactating - 
                
                if cur_num_b_booster is not None and cur_cons_num_booster is not None:
                    cur_cons_num_booster = float(cur_num_b_booster) - cur_cons_num_booster
                
                if cur_num_b_prestarter is not None and cur_cons_num_prestarter is not None:
                    cur_cons_num_prestarter = float(cur_num_b_prestarter) - cur_cons_num_prestarter
                
                if cur_num_b_starter is not None and cur_cons_num_starter is not None:
                    cur_cons_num_starter = float(cur_num_b_starter) - cur_cons_num_starter
                
                if cur_num_b_grower is not None and cur_cons_num_grower is not None:
                    cur_cons_num_grower = float(cur_num_b_grower) - cur_cons_num_grower
                
                if cur_num_b_finisher is not None and cur_cons_num_finisher is not None:
                    cur_cons_num_finisher = float(cur_num_b_finisher) - cur_cons_num_finisher
                
                
                cur_entry = {
                    'farm_prod_id':     cur_farm_prod_id,
                    
                    'sow': {
                        'number':       cur_sow_number,
                        'name':         cur_sow_name,
                    },
                    
                    'status_id':        cur_status_id, 
                    'status':           cur_status_name,
                    
                    'num_pigs_current': cur_num_pigs_current,
                    
                    'dates':{
                        'birth':        cur_date_actual,
                        
                        'iron_1':       cur_date_iron_1,
                        'iron_2':       cur_date_iron_2,
                        'vitamins_1':   cur_date_vitamins_1,
                        'kapon':        cur_date_kapon,
                        'vitamins_2':   cur_date_vitamins_2,
                        'deworm_1':     cur_date_deworm_1,
                        
                        'booster':      cur_date_booster,
                        'prestarter':   cur_date_prestarter,
                        'weaning':      cur_date_weaning,
                        'starter':      cur_date_starter,
                        'grower':       cur_date_grower,
                        'finisher':     cur_date_finisher,
                        
                        'harvest':      cur_date_harvest
                    },
                    
                    'num_feeds': {
                        'lactating': {
                            'bought':   cur_num_b_lactating,
                            'consumed': cur_cons_num_lactating,
                            'left':     cur_cons_num_lactating
                        },
                        
                        'booster': {
                            'bought':   cur_num_b_booster,
                            'consumed': cur_cons_num_booster,
                            'left':     cur_cons_num_booster
                        },
                            
                        'prestarter': {
                            'bought':   cur_num_b_prestarter,
                            'consumed': cur_cons_num_prestarter,
                            'left':     cur_cons_num_prestarter
                        },
                            
                        'starter': {     
                            'bought':   cur_num_b_starter,
                            'consumed': cur_cons_num_starter,
                            'left':     cur_cons_num_starter
                        },
                        
                        'grower': {
                            'bought':   cur_num_b_grower,
                            'consumed': cur_cons_num_grower,
                            'left':     cur_cons_num_grower
                        },
                        
                        'finisher': {    
                            'bought':   cur_num_b_finisher,
                            'consumed': cur_cons_num_finisher,
                            'left':     cur_cons_num_finisher
                        }
                    },
                    
                    'cost_feeds': {
                        'lactating':    cur_cost_lactating,
                        'booster':      cur_cost_booster,
                        'prestarter':   cur_cost_prestarter,
                        'starter':      cur_cost_starter,
                        'grower':       cur_cost_grower,
                        'finisher':     cur_cost_finisher
                    }
                   
                }
                result.append(cur_entry)

        
        return result
        
    
      
    def get_list(self, pig_prod_id = 0, pig_prod_group_id = 0, inc_user_audit = 0):
        

        if inc_user_audit == 0: 
            if pig_prod_id > 0:
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
                            
                        FROM pig_prod_feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        WHERE a.pig_prod_id = %s
                        ORDER BY a.id
                        """ % pig_prod_id
                        
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
                            
                        FROM pig_prod_feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        WHERE a.pig_prod_group_id = %s
                        ORDER BY a.id
                        """ % pig_prod_group_id
                
                
        else:
            
            if pig_prod_id > 0:
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
                            
                            
                            e.username,
                            e.name_last,
                            e.name_first,
                            a.dt_entry,
                            
                            
                            f.username,
                            f.name_last,
                            f.name_first,
                            a.dt_last_update
                            
                        FROM pig_prod_feed_buy a 
                        LEFT OUTER JOIN feed_type b     ON a.feed_type_id = b.id
                        LEFT OUTER JOIN feed_brand c    ON a.feed_brand_id = c.id
                        LEFT OUTER JOIN feed_supplier d ON a.feed_supplier_id = d.id
                        LEFT OUTER JOIN user e          ON a.added_by_user_id = e.id
                        LEFT OUTER JOIN user f          ON a.last_update_user_id = f.id
                        WHERE a.pig_prod_id = %s
                        ORDER BY a.id
                        """ % pig_prod_id
                        
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
                            
                            
                            e.username,
                            e.name_last,
                            e.name_first,
                            a.dt_entry,
                            
                            
                            f.username,
                            f.name_last,
                            f.name_first,
                            a.dt_last_update
                            
                        FROM pig_prod_feed_buy a 
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
                            'username':         row[14],
                            'name_last':        row[15],
                            'name_first':       row[16],
                            'dt_entry':         row[17]
                        },
                        
                        'last_update':{
                            'username':         row[18],
                            'name_last':        row[19],
                            'name_first':       row[20],
                            'dt_update':        str(row[21]) if row[21] else None
                        }
                    }
                
                    
                result.append(cur_entry)
        
        return result
    
    