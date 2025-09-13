# January 3, 2024
# Jack Wong

from common_constants       import *


class Account:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'Account'

    
    def get_info(self, id):
        
        sql =   """
                SELECT 
                    a.id,
                    a.flag,
                    a.status_id, 
                    b.name AS status_name,
                    a.hashid,
                    a.name,
                    a.date_trial_start,
                    a.date_trial_end,
                    a.flag_settings,
                    
                    a.farm_id_01,
                    a.farm_id_02,
                    a.farm_id_03,
                    a.farm_id_04,
                    a.farm_id_05,
                    
                    a.num_bills_paid,
                    a.last_acc_paid_bill_id,
                    a.dt_entry
                FROM account a
                LEFT OUTER JOIN account_status b ON a.status_id = b.id
                WHERE a.id = 
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
            in_user_id              INT,
    
            in_day_1_on_dob         INT
        )  
        """
        
        sql =  'CALL account_update_settings('
        sql += '%s,'    % data.user_id
        sql += '%s);'   % data.in_day_1_on_dob
        
        
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
                    'id':               row[3]
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
                    a.flag,
                    a.name,
                    
                    a.added_by_user_id,
                    b.name_last,
                    b.name_first,
                    
                    a.country_id,
                    a.adrs_level_1_id,
                    a.adrs_level_2_id,
                    a.adrs_level_3_id,
                    a.latitude,
                    a.longitude
                FROM pig_farm a
                LEFT OUTER JOIN user b ON a.added_by_user_id = b.id
                WHERE a.account_id = %s &  flag = %s
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
    
    
    def get_business_obj_selection(self, account_id, business_obj_id):
        
        if business_obj_id == BUSINESS_OBJ_ID_SEMEN_SUPPLIER:
            sql =   """
                    SELECT semen_supplier_id
                    FROM account_selection
                    WHERE account_id = %s AND semen_supplier_id > 0
                    """ % account_id
                    
        if business_obj_id == BUSINESS_OBJ_ID_FEED_SUPPLIER:
            sql =   """
                    SELECT feed_supplier_id
                    FROM account_selection
                    WHERE account_id = %s AND feed_supplier_id > 0
                    """ % account_id
            
        if business_obj_id == BUSINESS_OBJ_ID_FEED_BRAND:
            sql =   """
                    SELECT feed_brand_id
                    FROM account_selection
                    WHERE account_id = %s AND feed_brand_id > 0
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
            msg = 'get_business_obj_selection(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        result = []
        if rows is not None:
            
            for row in rows:
                result.append(row[0])
        
        return result
    
    