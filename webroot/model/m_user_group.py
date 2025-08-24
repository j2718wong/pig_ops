# January 3, 2024
# Jack Wong

from common_constants       import *


class UserGroup:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'UserGroup'
    
    
    def get_user_group_list_by_account(self, account_id):
        sql =   """
                SELECT 
                    id,
                    account_id,
                    group_num,
                    flag_business_obj,
                    name,
                    
                    flag_priv_user,
                    flag_priv_account,
                    flag_priv_account_request,
                    flag_priv_pig_farm,
                    
                    flag_priv_sow_boar,
                    flag_priv_semen_source,
                    flag_priv_pig_prod,
                    
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
            msg = 'get_user_group_list_by_account(); error in executing query[] = ' + sql
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
                    'id':                   row[0],
                    'account_id':           row[1],
                    'group_num':            row[2],
                    'flag_business_obj':    row[3],
                    'flag_business_obj_h':  f"0x{row[3]:08x}",
                    'name':                 row[4],
                    
                    'flag_priv_user':       row[5],
                    'flag_priv_user_h':     f"0x{row[5]:02x}",
                    
                    'flag_priv_account':    row[6],
                    'flag_priv_account_h':  f"0x{row[6]:02x}",
                    
                    'flag_priv_acc_req':    row[7],
                    'flag_priv_acc_req_h':  f"0x{row[7]:02x}",
                    
                    
                    'flag_priv_pig_farm':   row[8],
                    'flag_priv_pig_farm_h': f"0x{row[8]:02x}",
                    
                    'flag_priv_sow_boar':   row[9],
                    'flag_priv_sow_boar_h': f"0x{row[9]:02x}",
                    
                    'flag_priv_semen_source':   row[10],
                    'flag_priv_semen_source_h': f"0x{row[10]:02x}",
                    
                    'flag_priv_pig_prod':   row[11],
                    'flag_priv_pig_prod_h': f"0x{row[11]:02x}",
                    
                    'dt_entry':             row[12]
                    
                }
                    
                result.append(cur_entry)
        
        return result
    
