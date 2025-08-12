# January 3, 2024
# Jack Wong

from common_constants       import *


class User:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'User'
    
    
    def get_user_info(self, user_id):
        sql =   """
                SELECT 
                    a.account_id,
                    a.flag,
                    a.email,
                    a.mobile_num
                FROM user a
                WHERE id = %s
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
            conn.close()
            
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
                cur_user_account_id     = row[0]
                cur_user_flag           = row[1]
                cur_user_email          = row[2]
                cur_user_mobile_num     = row[3]
                
                cur_entry = {
                    'id':               user_id,
                    'account_id':       cur_user_account_id,
                    'flag':             cur_user_flag,
                    'email':            cur_user_email,
                    'mobile_num':       cur_user_mobile_num
                }
                    
                return cur_entry
                

        
        return None
    
    
    def register(self, data = None):
        """
        PROCEDURE user_register(
            in_username             VARCHAR(50),
            in_name_last            VARCHAR(50),
            in_name_first           VARCHAR(50),
    
            in_email                VARCHAR(50),
            in_mobile_num           VARCHAR(50),
            in_password             VARCHAR(200)
        )  
        """
        
        username        = data['username']
        name_last       = data['name_last'].upper()
        name_first      = data['name_first'].upper()
        
        email           = data['email'].lower()
        mobile_num      = data['mobile_num']
        password        = data['password']
        
        
        sql =  'CALL user_register('
        sql += '"%s",'  % username
        sql += '"%s",'  % name_last
        sql += '"%s",'  % name_first
        
        
        sql += '"%s",'  % email
        sql += '"%s",'  % mobile_num
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
    
        
    
    
    
    
    
    def login(self, data = None):
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

    
    
    
    