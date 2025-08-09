# January 3, 2024
# Jack Wong

from common_constants       import *


class Mfa:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'Mfa'
    
    
    def add(self, data = None):
        """
        PROCEDURE app_mfa_add(
            in_business_obj_id          INT,
            in_b_table_row_id           INT,
            in_channel_id               INT,
            in_country_code             INT,
            in_mobile_num               VARCHAR(15),
            in_email                    VARCHAR(100),
            
            in_auth_code                INT,
            
            in_ts_expiry                BIGINT,
            in_dt_expiry                VARCHAR(20)
        )  
        """
        
        
        business_obj_id = data['business_obj_id']
        b_table_row_id  = data['b_table_row_id']
        channel_id      = data['channel_id']
        country_code    = data['country_code']
        mobile_num      = data['mobile_num']
        email           = data['email']
        
        auth_code       = data['auth_code']
        ts_expiry       = data['ts_expiry']
        dt_expiry       = data['dt_expiry']
        
        
        sql =  'CALL app_mfa_add('
        sql += '%s,'    % business_obj_id
        sql += '%s,'    % b_table_row_id
        sql += '%s,'    % channel_id
        
        if mobile_num is not None:
            sql += '%s,'    % country_code
            sql += '"%s",'  % mobile_num
        else:
            sql += 'NULL,NULL,'
            
        if email is not None:
            sql += '"%s",'  % email
        else:
            sql += 'NULL,'
            
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
            msg = 'add(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            return {'id': row[0]}

        return None

    
    