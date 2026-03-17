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
                    a.name,
                    a.name_last,
                    a.name_first,
                    
                    a.user_group_id,
                    b.group_num,
                    b.flag_business_obj_1,
                    b.flag_business_obj_2,
                    b.name AS group_name,
                    
                    a.user_req_join_acc_id,
                    c.account_id,
                    c.status_id,
                    c.dt_entry,
                    d.name AS account_name
                    
                FROM user a
                LEFT OUTER JOIN user_group b    ON a.user_group_id = b.id
                LEFT OUTER JOIN user_request c  ON a.user_req_join_acc_id = c.id
                LEFT OUTER JOIN account d       ON c.account_id = d.id 
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
                cur_user_id                         = row[0]
                cur_user_account_id                 = row[1]
                cur_user_flag                       = row[2]
                cur_user_email                      = row[3]
                cur_user_mobile_num                 = row[4]
                cur_user_name                       = row[5]
                cur_user_name_last                  = row[6]
                cur_user_name_first                 = row[7]
                
                cur_user_group_id                   = row[8]
                cur_user_group_num                  = row[9]
                cur_user_group_flag_business_obj_1  = row[10]
                cur_user_group_flag_business_obj_2  = row[11]
                cur_user_group_name                 = row[12]
                
                cur_user_req_join_acc_id            = row[13]
                cur_user_req_account_id             = row[14]
                cur_user_req_status_id              = row[15]
                cur_user_req_dt_entry               = str(row[16])[0:10] # extract date only
                cur_user_req_account_name           = row[17]
                
                
                
                                
                cur_entry = {
                    'user': {
                        'id':               cur_user_id,
                        'account_id':       cur_user_account_id,
                        'flag':             cur_user_flag,
                        'email':            cur_user_email,
                        'mobile_num':       cur_user_mobile_num,
                        'name':             cur_user_name,
                        'name_last':        cur_user_name_last,
                        'name_first':       cur_user_name_first
                    },
                    
                    'user_group': {
                        'id':               cur_user_group_id,
                        'group_num':        cur_user_group_num,
                        'flag_business_obj_1': cur_user_group_flag_business_obj_1,
                        'flag_business_obj_2': cur_user_group_flag_business_obj_2,
                        'name':             cur_user_group_name
                    }
                }
                
                
                if cur_user_req_join_acc_id is not None:
                    user_request = {
                        'id':               cur_user_req_join_acc_id,
                        'account_id':       cur_user_req_account_id,
                        'account_name':     cur_user_req_account_name,
                        'status_id':        cur_user_req_status_id,
                        'date_req_sent':    cur_user_req_dt_entry
                    }
                    
                    cur_entry['user_request'] = user_request
                
                
                user_pig_farm_ids = self.model['user_farm'].get_list(user_id = user_id)
                
                if user_pig_farm_ids:
                    cur_entry['pig_farms'] = user_pig_farm_ids
                    
                return cur_entry
                

        
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
                    
                    a.email,
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
                cur_group_name          = row[4]
                
                cur_email               = row[5]
                cur_name_last           = row[6]
                cur_name_first          = row[7]
                
                
                cur_entry = {
                    'user': {
                        'id':           cur_id,
                        'email':        cur_email,
                        'name_last':    cur_name_last,
                        'name_first':   cur_name_first,
                        'flag':         cur_flag
                    },
                    
                    'user_group': {
                        'id':           cur_user_group_id,
                        'group_num':    cur_group_num,
                        'name':         cur_group_name
                    }
                    
                }
                
                    
                result.append(cur_entry)
        
        return result
    
    
    def register_or_login(self, data = None):
        """
        PROCEDURE user_register_or_login(
            in_login_social_media_id INT,

            in_name                 VARCHAR(80),
            in_name_last            VARCHAR(50),
            in_name_first           VARCHAR(50),
            
            in_email                VARCHAR(50),
            
            in_login_country_code   VARCHAR(3);  /* This should be in upper case*/
            in_login_country_name   VARCHAR(50);
            in_login_city           VARCHAR(50); /* This should be in upper case*/
            in_login_region         VARCHAR(50); /* This should be in upper case*/
            
            
            in_viewport_width       INT,
            in_viewport_height      INT,
            in_ip_address           VARCHAR(24)            
        )    
        """
        
        
        
        sql =  'CALL user_register_or_login('
        
        if data.login_social_media_id and data.login_social_media_id > 0:
            sql += '%s,'  % data.login_social_media_id
        else:
            sql += 'NULL,'
        
        
        if data.name and len(data.name) > 0:
            sql += '"%s",'  % data.name
        else:
            sql += 'NULL,'
        
        
        if data.name_last and len(data.name_last) > 0:
            sql += '"%s",'  % data.name_last
        else:
            sql += 'NULL,'
        
        
        if data.name_first and len(data.name_first) > 0:
            sql += '"%s",'  % data.name_first
        else:
            sql += 'NULL,'
        
        
        sql += '"%s",'  % data.email
        
        
        if data.login_country_code is not None:
            sql += '"%s",'  % data.login_country_code
        else:
            sql += 'NULL,'
            
        if data.login_country_name is not None:
            sql += '"%s",'  % data.login_country_name
        else:
            sql += 'NULL,'
        
        if data.login_city is not None:
            sql += '"%s",'  % data.login_city
        else:
            sql += 'NULL,'
        
        
        if data.login_region is not None:
            sql += '"%s",'  % data.login_region
        else:
            sql += 'NULL,'
        
        
        if data.viewport_width and data.viewport_width > 0:
            sql += '%s,'  % data.viewport_width
        else:
            sql += 'NULL,'
        
        if data.viewport_height and data.viewport_height > 0:
            sql += '%s,'  % data.viewport_height
        else:
            sql += 'NULL,'
        
        
            
        if data.ip_address and len(data.ip_address) > 0:
            sql += '"%s");'  % data.ip_address
        else:
            sql += 'NULL);'
        
            
        print('\n\nsql')
        print(sql)
        
        
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
            msg = 'register_or_login(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            cur_user_id                 = row[3]
            cur_user_unverified_id      = row[6]
            
            cur_entry =  {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'user': {
                    'id':               cur_user_id,
                    'account_id':       row[4],
                    'flag':             row[5]
                },
                
                'user_unverified': {
                    'id':               cur_user_unverified_id,
                    'verify_id':        row[7],
                    'verify_code':      str(row[8]),
                    'verify_ts_expiry': row[9],
                    'verify_dt_expiry': str(row[10]) if row[10] else None,
                    'expiry_minutes':   row[11]
                }
            }


            if cur_user_id == 0:
                del cur_entry['user']

            if cur_user_unverified_id is None or cur_user_unverified_id == 0:
                del cur_entry['user_unverified']

            
            
            
            return cur_entry


        return None


    def user_verify_email(self, data = None):
        """
        PROCEDURE user_verify_email(
            in_unverified_user_id   INT,
            in_auth_code            INT,
            
            in_viewport_width       INT,
            in_viewport_height      INT,
            
            in_ip_address           VARCHAR(24)
            
        )    
        """
        
        
        
        sql =  'CALL user_verify_email('
        
        sql += '%s,'  % data.unverified_user_id
        sql += '%s,'  % data.auth_code
        
        if data.viewport_width and data.viewport_width > 0:
            sql += '%s,'  % data.viewport_width
        else:
            sql += 'NULL,'
        
        if data.viewport_height and data.viewport_height > 0:
            sql += '%s,'  % data.viewport_height
        else:
            sql += 'NULL,'
        
        
            
        if data.ip_address and len(data.ip_address) > 0:
            sql += '"%s");'  % data.ip_address
        else:
            sql += 'NULL);'
        
        
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
            msg = 'user_verify_email(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            
            cur_entry =  {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'user': {
                    'id':               cur_user_id,
                    'flag':             row[5]
                }
            }


            return cur_entry


        return None



