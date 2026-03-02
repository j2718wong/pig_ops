# January 3, 2024
# Jack Wong

from common_constants       import *


FLAG_BIT_ACCOUNT_ENABLE                 = 1
FLAG_BIT_ACCOUNT_IS_BILL_EXEMPTED       = 1<<4


FLAG_BIT_ACCOUNT_IS_COMPANY_OWNED       = 1<<16


"""
account.flag bits

bit 0: FLAG_BIT_ACCOUNT_ENABLE
bit 1:
bit 2:
bit 3:  

bit 4:  FLAG_BIT_ACCOUNT_IS_BILL_EXEMPTED
0 = not exempted has to pay bill
1 = exempted



bit 16: COMPANY_OWNED ACCOUNT
"""


# The account.flag_settings will be broken down so that
# it will be easier to read in the application level.
# See account_register.sql for updated flag bits definition.

"""
/* account.flag_setting bits
bit 0: FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
0 = Date of birth is counted as DAY 0
1 = Date of birth is counted as DAY 1; default

bit 1: FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
0 = Date of insemination is counted as DAY 0; default
1 = Date of insemination is counted as DAY 1;


*/

"""

FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH     = 1
FLAG_BIT_DAY_1_ON_DATE_OF_INSEM     = 2
            

class Account:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'Account'

    
    def get_info(self, account_id):
        
        sql =   """
                SELECT 
                    a.id,
                    a.flag,
                    a.status_id, 
                    b.name AS status_name,
                    a.name AS account_name,
                    a.date_trial_start,
                    a.date_trial_end,
                    
                    a.current_bill_id,
                    c.status_id,
                    
                    a.weight_unit,
                    a.currency,
                    a.flag_settings,
                    a.num_days_wean,
                    a.num_days_harvest_from_birth,
                    a.num_days_harvest_from_wean,
                    
                    
                    d.name_last,
                    d.name_first,
                    a.dt_last_update_settings
                FROM account a
                LEFT OUTER JOIN account_status b ON a.status_id = b.id
                LEFT OUTER JOIN account_bill c ON a.current_bill_id = c.id
                LEFT OUTER JOIN user d          ON a.last_update_settings_user_id = d.id
                
                WHERE a.id = %s
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
            msg = 'get_account_admin(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        result = []
        if rows is not None:
            
            for row in rows:
                cur_acc_id                  = row[0]
                cur_acc_flag                = row[1]
                cur_acc_status_id           = row[2]
                cur_acc_status_name         = row[3]
                cur_acc_account_name        = row[4]
                cur_acc_date_trial_start    = row[5]
                cur_acc_date_trial_end      = row[6]
                
                cur_acc_current_bill_id     = row[7]
                cur_acc_current_bill_status = row[8]
                
                cur_acc_weight_unit         = row[9]
                cur_acc_currency            = row[10]
                cur_acc_settings_flag       = row[11]
                cur_acc_num_days_wean       = row[12]
                cur_acc_num_days_harvest_from_birth = row[13]
                cur_acc_num_days_harvest_from_wean  = row[14]
                
                               
                cur_user_name_last          = row[15]
                cur_user_name_first         = row[16]
                cur_settings_last_update    = str(row[17]) if row[17] else None
                
                
                temp = cur_acc_flag & FLAG_BIT_ACCOUNT_ENABLE
                cur_flag_acc_is_enabled = 1 if temp > 0 else 0
                
                
                temp = cur_acc_flag & FLAG_BIT_ACCOUNT_IS_BILL_EXEMPTED
                cur_flag_acc_is_bill_exempt = 1 if temp > 0 else 0
                
                
                temp = cur_acc_flag & FLAG_BIT_ACCOUNT_IS_COMPANY_OWNED
                cur_flag_acc_is_company_owned = 1 if temp > 0 else 0
                
                
                
                temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
                cur_flag_day_1_on_dob   = 1 if temp > 0 else 0
                
                temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
                cur_flag_day_1_on_doi   = 1 if temp > 0 else 0
                
                
                cur_entry = {
                    'account': {
                        'id':               cur_acc_id,
                        'account_name':     cur_acc_account_name,
                        'flag':             cur_acc_flag,
                        'status_id':        cur_acc_status_id,
                        'status_name':      cur_acc_status_name,
                        
                        'is_enabled':       cur_flag_acc_is_enabled,
                        'is_bill_exempt':   cur_flag_acc_is_bill_exempt,
                        'is_company_owned': cur_flag_acc_is_company_owned,
                        
                        'current_bill':{
                            'id':           cur_acc_current_bill_id,
                            'status_id':    cur_acc_current_bill_status
                        }
                    },
                    
                    'settings_operations': {
                        'weight_unit':                  cur_acc_weight_unit,
                        'currency':                     cur_acc_currency,
                        'day_1_on_date_of_birth':       cur_flag_day_1_on_dob,
                        'day_1_on_date_of_insem':       cur_flag_day_1_on_doi,
                        'num_days_wean':                cur_acc_num_days_wean,
                        'num_days_harvest_from_birth':  cur_acc_num_days_harvest_from_birth,
                        'num_days_harvest_from_wean':   cur_acc_num_days_harvest_from_wean,
                    
                        'last_update':{
                            'name_last':    cur_user_name_last,
                            'name_first':   cur_user_name_first,
                            'dt_update':    cur_settings_last_update
                        }
                    }
                }
                
                
                # Get Farm List
                account_farms = self.model['pig_farm'].get_list(account_id)
                
                if account_farms:
                    cur_entry['pig_farms'] = account_farms
                
                    
                return cur_entry
        
        return None
    
    
    def register(self, data = None):
        """
        PROCEDURE account_register(
            in_user_id              INT,
    
            in_country_id           INT,
            in_name                 VARCHAR(100)
        )  
        """
        
        sql =  'CALL account_register('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.country_id
        sql += '"%s");' % data.name
        
        
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
            msg = 'register(); error in executing query[] = ' + sql
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
                
                'account': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5],
                    'status_id':        row[6],
                    'status_name':      row[7],
                    'dt_trial_start':   row[8],
                    'dt_trial_end':     row[9]
                }
            }

        return None

    
    def update_hashid(self, data = None):
        account_id      = data['account_id']
        hashid          = data['hashid']
        
        values = (hashid, account_id)
        
        sql =   """
                UPDATE account SET
                    hashid    = "%s"
                WHERE id = %s;
                """ % values
        
        return self.model.execute_sql(sql)
    
    
    def update(self, data = None):
        """
        PROCEDURE account_update(
            in_user_id              INT,
    
            in_name                 VARCHAR(100)
        )  
        """
        
        sql =  'CALL account_update('
        sql += '%s,'    % data.user_id
        sql += '"%s");' % data.name
        
        
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
                
                'account': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5],
                    'status_id':        row[6],
                    'status_name':      row[7],
                    'dt_trial_start':   row[8],
                    'dt_trial_end':     row[9]
                }
            }

        return None
    
    
    def update_settings(self, data = None):
        """
        PROCEDURE account_update_settings(
            in_user_id                  INT,
    
            in_day_1_on_dob             INT,
            in_day_1_on_insem           INT,
            
            in_days_wean                INT,
            
            in_days_harvest_from_birth  INT,
            in_days_harvest_from_wean   INT,
            
            in_weight_unit              VARCHAR(4)
        )  
        """
        
        sql =  'CALL account_update_settings('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.day_1_on_date_of_birth
        sql += '%s,'    % data.day_1_on_date_insem
        sql += '%s,'    % data.days_wean
        sql += '%s,'    % data.days_harvest_from_birth
        sql += '%s,'    % data.days_harvest_from_wean
        sql += '"%s");' % data.weight_unit
        
        
        
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
            cur_res_num                 = row[0]
            cur_res_code                = row[1]
            cur_res_desc                = row[2]
            
            cur_acc_settings_flag       = row[3]
             
            temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
            cur_flag_day_1_on_dob   = 1 if temp > 0 else 0
            
            temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
            cur_flag_day_1_on_doi   = 1 if temp > 0 else 0
            
            
            cur_acc_num_days_wean       = row[4]
            cur_acc_num_days_harvest_from_birth = row[5]
            cur_acc_num_days_harvest_from_wean  = row[6]
            
            cur_acc_weight_unit         = row[7]
            cur_acc_currency            = row[8]
            
            
            result =  {
                'result':{
                    'num':              cur_res_num,
                    'code':             cur_res_code,
                    'desc':             cur_res_desc
                },
                
                'settings_operations': {
                    'day_1_on_date_of_birth':       cur_flag_day_1_on_dob,
                    'day_1_on_date_of_insem':       cur_flag_day_1_on_doi,
                    'num_days_wean':                cur_acc_num_days_wean,
                    'num_days_harvest_from_birth':  cur_acc_num_days_harvest_from_birth,
                    'num_days_harvest_from_wean':   cur_acc_num_days_harvest_from_wean,
                    
                    'acc_weight_unit':  cur_acc_weight_unit,
                    'currency':         cur_acc_currency
                }
            }

            return result 

        return None
    
    
    def get_list_account_admin(self, account_id):
        user_flag = FLAG_BIT_USER_IS_ACTIVE | FLAG_BIT_USER_EMAIL_VERIFIED 
        user_flag |= FLAG_BIT_USER_IS_ACCOUNT_ADMIN
        
        values = (account_id, user_flag)
        
        sql =   """
                SELECT 
                    id,
                    flag,
                    email,
                    mobile_num
                FROM user 
                WHERE account_id = %s &  flag = %s
                """ % values
        
        
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
            msg = 'get_account_admin(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        result = []
        if rows is not None:
            
            for row in rows:
                cur_user_account_id     = row[0]
                cur_user_flag           = row[1]
                cur_user_email          = row[2]
                cur_user_mobile_num     = row[3]
                
                cur_entry = {
                    'id':               user_id,
                    'flag':             cur_user_flag,
                    'email':            cur_user_email,
                    'mobile_num':       cur_user_mobile_num
                }
                    
                result.append(cur_entry)
        
        return result
    
    
    def get_list_pig_farm(self, account_id):
        
        sql =   """
                SELECT 
                    a.id,
                    a.name,
                    
                    a.added_by_user_id,
                    b.name_last,
                    b.name_first,
                    a.dt_entry,
                    
                    a.country_id,
                    c.name AS country_name,
                    a.address_level_1_id,
                    a.address_level_2_id,
                    a.address_level_3_id,
                    a.latitude,
                    a.longitude
                FROM pig_farm a
                LEFT OUTER JOIN user b ON a.added_by_user_id = b.id
                LEFT OUTER JOIN app_country c   ON a.country_id = c.id
                WHERE a.account_id = %s 
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
            msg = 'get_list_pig_farm(); error in executing query[] = ' + sql
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
                    'pig_farm': {
                        'id':               row[0],
                        'name':             row[1],
                        
                        'added_by_user':{
                            'id':           row[2],
                            'name_last':    row[3],
                            'name_first':   row[4]
                        },
                        
                        'dt_entry':         str(row[5])
                    },
                    
                    'location':{
                        
                        'country': {
                            'id':           row[6],
                            'name':         row[7]
                        },
                        
                        'address': {
                            'level_1':{
                                'id':       row[8]
                            },
                        
                            'level_2':{
                                'id':       row[9]
                            },
                            
                            'level_3':{
                                'id':       row[10]
                            }
                            
                        },
                        
                        'geoloc':{
                            'latitude':     float(row[11]) if row[11] else None,
                            'longitude':    float(row[12]) if row[12] else None
                        }
                    }
                }
                    
                result.append(cur_entry)
        
        return result
    
    
