# January 3, 2024
# Jack Wong

from common_constants       import *

"""
/* user.flag bits*/
DECLARE FLAG_BIT_USER_IS_ACTIVE                 INT             DEFAULT 1;
DECLARE FLAG_BIT_USER_EMAIL_VERIFIED            INT             DEFAULT 2;
DECLARE FLAG_BIT_USER_MOBILE_NUM_VERIFIED       INT             DEFAULT 4;
DECLARE FLAG_BIT_USER_IS_DELETED                INT             DEFAULT 8;

DECLARE FLAG_BIT_USER_IS_ACCOUNT_ADMIN          INT             DEFAULT 16;
"""

FLAG_BIT_USER_IS_ACTIVE             = 1
FLAG_BIT_USER_EMAIL_VERIFIED        = 2
FLAG_BIT_USER_MOBILE_NUM_VERIFIED   = 4
FLAG_BIT_USER_IS_DELETED            = 8

FLAG_BIT_USER_IS_ACCOUNT_ADMIN      = 16


"""
/* account.flag bits
bit 0: FLAG_BIT_ACCOUNT_ENABLE
bit 1:
bit 2:
bit 3:  

bit 4:  FLAG_BIT_ACCOUNT_IS_BILL_EXEMPTED
0 = not exempted has to pay bill
1 = exempted



bit 16: FLAG_BIT_COMPANY_OWNED_ACCOUNT

*/
"""
FLAG_BIT_ACCOUNT_ENABLE             = 1
FLAG_BIT_FLAG_BIT_COMPANY_OWNED_ACCOUNT = 16



class User:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'User'
    
    
    def get_user_account_info(self, user_id):
        sql =   """
                SELECT 
                    a.account_id,
                    a.flag AS user_flag,
                    b.flag AS account_flag,
                    b.current_bill_id,
                    c.status_id 
               
                FROM user a
                LEFT OUTER JOIN account b ON a.account_id = b.id
                LEFT OUTER JOIN account_bill c ON b.current_bill_id = c.id
                WHERE a.id = %s
                """ % user_id
        
        
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
            msg = 'get_user_account_info(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        if rows is not None:
            
            for row in rows:
                cur_user_account_id         = row[0]
                cur_user_flag               = row[1]
                cur_account_flag            = row[2]
                cur_account_bill_id         = row[3]
                cur_account_bill_status_id  = row[4]
                
                
                user_is_active              = 1 if cur_user_flag & FLAG_BIT_USER_IS_ACTIVE > 0 else 0
                user_is_email_verified      = 1 if cur_user_flag & FLAG_BIT_USER_EMAIL_VERIFIED  > 0 else 0
                user_is_mobile_verified     = 1 if cur_user_flag & FLAG_BIT_USER_MOBILE_NUM_VERIFIED  > 0 else 0
                
                user_is_deleted             = 1 if cur_user_flag & FLAG_BIT_USER_IS_DELETED  > 0 else 0
                user_is_account_admin       = 1 if cur_user_flag & FLAG_BIT_USER_IS_ACCOUNT_ADMIN  > 0 else 0
                
                
                acc_is_enabled              = 1 if cur_account_flag & FLAG_BIT_ACCOUNT_ENABLE  > 0 else 0
                         
                acc_is_company_owned        = 1 if cur_account_flag & FLAG_BIT_FLAG_BIT_COMPANY_OWNED_ACCOUNT  > 0 else 0
                   
                
                cur_entry = {
                    'user': {
                        'id':               user_id,
                        'is_active':        user_is_active,
                        'is_email_verified':  user_is_email_verified,
                        'is_mobile_verified': user_is_mobile_verified
                    },
                    
                    'account': {
                        'id':               cur_user_account_id,
                        'is_enabled':       acc_is_enabled,
                        'is_company_owned': acc_is_company_owned,
                        
                        'cur_bill_id':      cur_account_bill_id,
                        'cur_bill_status_id':  cur_account_bill_status_id
                    }
                }
                    
                return cur_entry
                

        
        return None
    
    
    
    
    
    def get_user_info(self, user_id):
        sql =   """
                SELECT 
                    a.id,
                    a.account_id,
                    a.flag,
                    a.email,
                    a.mobile_num,
                    a.name_last,
                    a.name_first,
                    
                    a.user_group_id,
                    b.group_num,
                    b.flag_business_obj_1,
                    b.flag_business_obj_2,
                    b.name AS group_name
                FROM user a
                LEFT OUTER JOIN user_group b ON a.user_group_id = b.id
                WHERE a.id = %s
                """ % user_id
        
        
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
            msg = 'get_user_info(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        if rows is not None:
            
            for row in rows:
                                
                cur_entry = {
                    'user': {
                        'id':               row[0],
                        'account_id':       row[1],
                        'flag':             row[2],
                        'email':            row[3],
                        'mobile_num':       row[4],
                        'name_last':        row[5],
                        'name_first':       row[6]
                    },
                    
                    'user_group': {
                        'id':               row[7],
                        'group_num':        row[8],
                        'flag_business_obj_1': row[9],
                        'flag_business_obj_2': row[10],
                        'name':             row[11]
                    }
                }
                
                user_pig_farm_ids = self.model['user_farm'].get_list(user_id = user_id)
                
                if user_pig_farm_ids:
                    cur_entry['pig_farms'] = user_pig_farm_ids
                    
                return cur_entry
                

        
        return None
    
    
    def register(self, data = None):
        """
        PROCEDURE user_register(
            in_social_channel_id    INT,
            
            in_name_last            VARCHAR(50),
            in_name_first           VARCHAR(50),
    
            in_email                VARCHAR(50)
        )  
        """
        

        email           = data.email.lower()
        
        
        sql =  'CALL user_register('
        
        
        if data.social_channel_id is not None and data.social_channel_id > 0:
             sql += '%s,'  % data.social_channel_id
        else:
            sql += 'NULL,'
        
        if data.name_last is not None:
            sql += '"%s",'  % data.name_last
        else:
            sql += 'NULL,'
            
        if data.name_first is not None:
            sql += '"%s",'  % name_first
        else:
            sql += 'NULL,'
        
        
        sql += '"%s");'  % email

        
        
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
                
                'user': {
                    'id':               row[3],
                    'flag':             row[4]
                }
            }

        return None


    def update_hashid(self, data = None):
        user_id         = data['user_id']
        hashid          = data['hashid']
        
        values = (hashid, user_id)
        
        sql =   """
                UPDATE user SET
                    hashid    = "%s"
                WHERE id = %s;
                """ % values
        
        return self.model.execute_sql(sql)


    def update_mfa_id_email_verify(self, data = None):
        user_id         = data['user_id']
        mfa_id          = data['mfa_id']
        
        values = (mfa_id, user_id)
        
        sql =   """
                UPDATE user SET
                    last_mfa_id_email_verify    = %s
                WHERE id = %s;
                """ % values
        
        return self.model.execute_sql(sql)
    
        
    def get_list(self, account_id, inc_deleted = 0 ):
        
        if inc_deleted > 0:
            where_clause = 'WHERE a.account_id = %s' % account_id 
        else:
            where_clause = 'WHERE a.account_id = %s AND (a.flag & 8) = 0' % account_id 
        
    
        sql =   """
                SELECT 
                    a.id,
                    a.flag,
                    a.user_group_id,
                    b.group_num,
                    b.name,
                    
                    a.name_last,
                    a.name_first
                    
                FROM user a 
                LEFT OUTER JOIN user_group b        ON a.user_group_id   = b.id
                
                %s
                ORDER BY a.name_first
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
                cur_flag                = row[1]
                cur_user_group_id       = row[2]
                cur_group_num           = row[3]
                cur_name                = row[4]
                
                cur_name_last           = row[5]
                cur_name_first          = row[6]
                
                
                cur_entry = {
                    'user': {
                        'id':           cur_id,
                        'name_last':    cur_name_last,
                        'name_first':   cur_name_first,
                        'flag':         cur_flag
                    },
                    
                    'user_group': {
                        'id':           cur_user_group_id,
                        'group_num':    cur_group_num,
                        'name':         cur_name
                    }
                    
                }
                
                    
                result.append(cur_entry)
        
        return result
    
    

    
    def login_social(self, data = None):
        """
        PROCEDURE `booking`.`user_login`(
            in_email                    VARCHAR(30),
            in_password                 VARCHAR(255)
        )  
        """
        
        
        email           = data['email'].lower()
        password        = data['password']
       
        
        sql =  'CALL user_login('
        sql += '"%s",'  % email
        sql += '"%s");' % password
        
        
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
            msg = 'login(); error in executing query[] = ' + sql
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
                
                'user': {
                    'id':               row[3],
                    'flag':             row[4]
                }
            }

        return None


    def update_phone(self, data = None):
        """
        PROCEDURE `booking`.`user_phone_update`(
            in_user_id              INT,
            in_country_code_id      INT,
            in_phone_number         VARCHAR(15)
        )  
        """
        
        user_id         = data['user_id']
        country_code_id = data['country_code_id']
        phone_number    = data['phone_number']
        
        sql =  'CALL user_phone_update('
        sql += '%s,'    % user_id
        sql += '%s,'    % country_code_id
        sql += '"%s");' % phone_number
        
        
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
            msg = 'update_phone(); error in executing query[] = ' + sql
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
                
                'user': {
                    'id':               row[3],
                    'flag':             row[4]
                }
            }

        return None

    
    def add_phone_mfa(self, data = None):
        """
        PROCEDURE `booking`.`user_mfa_phone_add`(
            in_user_id                  INT,
            
            in_auth_code                INT,
            
            in_ts_expiry                BIGINT,
            in_dt_expiry                VARCHAR(20)
        )  
        """
        
        
        user_id         = data['user_id']
        auth_code       = data['auth_code']
        ts_expiry       = data['ts_expiry']
        dt_expiry       = data['dt_expiry']
        
        sql =  'CALL user_mfa_phone_add('
        sql += '%s,'    % user_id
        sql += '%s,'    % auth_code
        sql += '%s,'    % ts_expiry
        sql += '"%s");' % dt_expiry
        
        
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
            msg = 'add_phone_mfa(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            return {
                'id':               row[0]
            }

        return None

    
    def verify_email_mfa(self, data = None):
        """
        PROCEDURE user_verify_mfa_email(
            in_user_id                  INT,
            in_auth_code                INT
        )  
        """
        
        user_id         = data['user_id']
        auth_code       = data['auth_code']
        
        sql =  'CALL user_verify_mfa_email('
        sql += '%s,'    % user_id
        sql += '%s);'   % auth_code
        
        
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
            msg = 'verify_email_mfa(); error in executing query[] = ' + sql
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
                
                'user': {
                    'id':               row[3],
                    'flag':             row[4]
                }
            }

        return None

    
    def verify_phone_mfa(self, data = None):
        """
        PROCEDURE `booking`.`user_mfa_phone_verify`(
            in_user_id                  INT,
            
            in_auth_code                INT
        )  
        """
        
        user_id         = data['user_id']
        auth_code       = data['auth_code']
        
        sql =  'CALL user_mfa_phone_verify('
        sql += '%s,'    % user_id
        sql += '%s);'   % auth_code
        
        
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
            msg = 'verify_phone_mfa(); error in executing query[] = ' + sql
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
                
                'user': {
                    'id':               row[3],
                    'flag':             row[4]
                }
            }

        return None

    
    def app_install(self, data = None):
        """
        PROCEDURE `booking`.`app_install_register`(
            in_email                    VARCHAR(255),
            in_password                 VARCHAR(255),
            in_name_first               VARCHAR(50),
            in_name_last                VARCHAR(50),
            in_sex                      VARCHAR(3),
            
            in_country_code_id          INT,
            in_phone_number             VARCHAR(15)
        )  
        """
        
        
        email           = data['email'].lower()
        password        = data['password']
        name_first      = data['name_first']
        name_last       = data['name_last']
        sex             = data['sex']
        
        country_code_id = data['country_code_id']
        phone_number    = data['phone_number']
        
        sql =  'CALL user_register('
        sql += '"%s",'  % email
        sql += '"%s",'  % password
        sql += '"%s",'  % name_first
        sql += '"%s",'  % name_last
        sql += '"%s",'  % sex
        sql += '%s,'    % country_code_id
        sql += '"%s");' % phone_number
        
        
        
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
                'result_num':           row[0],
                'result_code':          row[1],
                'result_desc':          row[2],
                
                'user_id':              row[3],
                'user_flag':            row[4]

            }

        return None


    def add_user_location(self, data = None):
        """
        PROCEDURE `booking`.`user_location_add`(
            in_user_id              INT,
            in_location_type        INT,
            in_location_adrs_id     INT
        )  
        """
        
        
        user_id             = data['user_id']
        location_type       = data['location_type']
        location_adrs_id    = data['location_adrs_id']
       
        sql =  'CALL user_location_add('
        sql += '%s,'    % user_id
        sql += '%s,'    % location_type
        sql += '%s);'   % location_adrs_id
        
        
        
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
            msg = 'add_user_location(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            return {'id': row[0]}

        return None

    
    
    
    
