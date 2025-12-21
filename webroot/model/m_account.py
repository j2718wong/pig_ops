# January 3, 2024
# Jack Wong

from common_constants       import *


# The account.flag_settings will be broken down so that
# it will be easier to read in the application level.
# See account_register.sql for updated flag bits definition.

"""
/* account.flag_setting bits
FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
0 = Date of birth is counted as DAY 0
1 = Date of birth is counted as DAY 1; default

FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
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
                    
                    a.flag_settings,
                    a.num_days_wean,
                    a.num_days_harvest_from_birth,
                    a.num_days_harvest_from_wean,
                    
                    a.num_bills_paid,
                    a.last_acc_paid_bill_id,
                    
                    a.farm_01_id,
                    a.farm_02_id,
                    a.farm_03_id,
                    a.farm_04_id,
                    a.farm_05_id,
                    
                    c.name_last,
                    c.name_first,
                    a.dt_last_update_settings
                FROM account a
                LEFT OUTER JOIN account_status b ON a.status_id = b.id
                LEFT OUTER JOIN user c          ON a.last_update_settings_user_id = c.id
                
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
                cur_acc_id              = row[0]
                cur_acc_flag            = row[1]
                cur_acc_status_id       = row[2]
                cur_acc_status_name     = row[3]
                cur_acc_account_name    = row[4]
                cur_acc_date_trial_start = row[5]
                cur_acc_date_trial_end  = row[6]
                
                
                cur_acc_settings_flag   = row[7]
                cur_acc_num_days_wean   = row[8]
                cur_acc_num_days_harvest_from_birth = row[9]
                cur_acc_num_days_harvest_from_wean  = row[10]
                
                cur_acc_farm_01_id      = row[13]
                cur_acc_farm_02_id      = row[14]
                cur_acc_farm_03_id      = row[15]
                cur_acc_farm_04_id      = row[16]
                cur_acc_farm_05_id      = row[17]
                
                cur_user_name_last      = row[18]
                cur_user_name_first     = row[19]
                cur_settings_last_update= str(row[20]) if row[20] else None
                
                
                
                
                temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
                cur_flag_day_1_on_dob   = 1 if temp > 0 else 0
                
                temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
                cur_flag_day_1_on_doi   = 1 if temp > 0 else 0
                
                farm_ids = []
                if cur_acc_farm_01_id > 0: farm_ids.append(cur_acc_farm_01_id)
                if cur_acc_farm_02_id > 0: farm_ids.append(cur_acc_farm_02_id)
                if cur_acc_farm_03_id > 0: farm_ids.append(cur_acc_farm_03_id)
                if cur_acc_farm_04_id > 0: farm_ids.append(cur_acc_farm_04_id)
                if cur_acc_farm_05_id > 0: farm_ids.append(cur_acc_farm_05_id)
                
                
                cur_entry = {
                    'account': {
                        'id':               cur_acc_id,
                        'flag':             cur_acc_flag,
                        'status_id':        cur_acc_status_id,
                        'status_name':      cur_acc_status_name
                    },
                    
                    'settings_operations': {
                        'day_1_on_date_of_birth': cur_flag_day_1_on_dob,
                        'day_1_on_date_of_insem': cur_flag_day_1_on_doi,
                        'num_days_wean':    cur_acc_num_days_wean,
                        'num_days_harvest_from_birth': cur_acc_num_days_harvest_from_birth,
                        'num_days_harvest_from_wean':  cur_acc_num_days_harvest_from_wean,
                    
                        'last_update':{
                            'name_last':    cur_user_name_last,
                            'name_first':   cur_user_name_first,
                            'dt_update':    cur_settings_last_update
                        }
                    },
                    
                    'farm_ids': farm_ids
                }
                    
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
            in_days_harvest_from_wean   INT
        )  
        """
        
        sql =  'CALL account_update_settings('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.day_1_on_date_of_birth
        sql += '%s,'    % data.day_1_on_date_insem
        sql += '%s,'    % data.days_wean
        sql += '%s,'    % data.days_harvest_from_birth
        sql += '%s);'   % data.days_harvest_from_wean
        
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
            
            
            cur_user_name_last          = row[7]
            cur_user_name_first         = row[8]
            cur_settings_last_update    = str(row[9]) if row[9] is not None else None
            
            
            return {
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
                
                    'last_update':{
                        'name_last':    cur_user_name_last,
                        'name_first':   cur_user_name_first,
                        'dt_update':    cur_settings_last_update
                    }
                }
            }

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
    
    