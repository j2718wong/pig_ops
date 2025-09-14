# January 3, 2024
# Jack Wong

from common_constants       import *


class UserGroup:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'UserGroup'
    
    
    def get_list(self, account_id):
        sql =   """
                SELECT 
                    id,
                    account_id,
                    group_num,
                    flag_business_obj,
                    name,
                    
                    flag_priv_user,
                    flag_priv_account,
                    flag_priv_acc_request,
                    flag_priv_user_group,
                    
                    flag_priv_acc_translation,
                    flag_priv_acc_billing,
                    flag_priv_acc_pig_buyer,
                    flag_priv_acc_pig_ops,
                    
                    flag_priv_pig_farm,
                    flag_priv_pig_farm_staff,
                    flag_priv_pig_race,
                    flag_priv_pig_race_line,
                    
                    
                    flag_priv_semen_supplier,
                    flag_priv_feed_supplier,
                    flag_priv_feed_brand,
                    flag_priv_feed_type,
                    flag_priv_feed_buy,
                    flag_priv_feed_balance,
                    
                    flag_priv_sow_boar,
                    flag_priv_semen_source,
                    flag_priv_pig_production,
                    flag_priv_pig_prod_ai,
                    
                    
                    flag_priv_pig_prod_pig_ops,
                    flag_priv_pig_prod_pig_dead,
                    flag_priv_pig_prod_notes,
                    flag_priv_pig_prod_harvest,
                    
                    
                    flag_priv_sow_boar_balance,
                    
                    dt_entry
                FROM user_group
                WHERE account_id = %s
                ORDER BY group_num
                """ % account_id
        
        
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
                    'id':                       row[0],
                    'account_id':               row[1],
                    'group_num':                row[2],
                    'flag_business_obj':        row[3],
                    'flag_business_obj_h':      f"0x{row[3]:08x}",
                    'name':                     row[4],
                    
                    'flag_priv_user':           row[5],
                    'flag_priv_account':        row[6],
                    'flag_priv_acc_req':        row[7],
                    'flag_priv_user_group':     row[8],
                    
                    'flag_priv_acc_translation': row[9],
                    'flag_priv_acc_billing':    row[10],
                    'flag_priv_acc_pig_buyer':  row[11],
                    'flag_priv_acc_pig_ops':    row[12],
                    
                    'flag_priv_pig_farm':       row[13],
                    'flag_priv_pig_farm_staff': row[14], 
                    'flag_priv_pig_race':       row[15],
                    'flag_priv_pig_race_line':  row[16],
                    
                    'flag_priv_semen_supplier': row[17],
                    'flag_priv_feed_supplier':  row[18],
                    'flag_priv_feed_brand':     row[19],
                    'flag_priv_feed_type':      row[20],
                    'flag_priv_feed_buy':       row[21],
                    'flag_priv_feed_balance':   row[22],
                    
                    
                    'flag_priv_sow_boar':       row[23],
                    'flag_priv_semen_source':   row[24],
                    'flag_priv_pig_production': row[25],
                    'flag_priv_pig_prod_ai':    row[26],
                    
                    
                    'flag_priv_pig_prod_pig_ops':   row[27],
                    'flag_priv_pig_prod_pig_dead':  row[28],
                    'flag_priv_pig_prod_notes':     row[29],
                    'flag_priv_pig_prod_harvest':   row[30],
                    
                    'flag_priv_sow_boar_balance':   row[31],
                    
                    'dt_entry':                 row[32]
                    
                }
                    
                result.append(cur_entry)
        
        return result
    
