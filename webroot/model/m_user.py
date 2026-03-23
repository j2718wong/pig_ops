# January 3, 2025
# Jack Wong
import os
import sys

from common_constants       import *


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)

from base_model             import BaseModel


#/* user.flag bits*/
FLAG_BIT_USER_IS_ACTIVE                 = 1
FLAG_BIT_USER_EMAIL_VERIFIED            = 2
FLAG_BIT_USER_MOBILE_NUM_VERIFIED       = 4
FLAG_BIT_USER_IS_DELETED                = 8
FLAG_BIT_USER_IS_ACCOUNT_ADMIN          = 16

#/* account.flag bits */
FLAG_BIT_ACCOUNT_ENABLE                 = 1
FLAG_BIT_FLAG_BIT_COMPANY_OWNED_ACCOUNT = 16



class User(BaseModel):
    def __init__(self, model):
        super().__init__(model)  # Inherit from BaseModel
    
    
    def get_user_account_info(self, user_id):
        """
        Get user and account information
        """
        sql = """
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
        """
        
        rows = self._execute_query(sql, [user_id])
        
        if rows is None:
            return None
        
        
        for row in rows:
            cur_user_account_id         = row[0]
            cur_user_flag               = row[1]
            cur_account_flag            = row[2]
            cur_account_bill_id         = row[3]
            cur_account_bill_status_id  = row[4]
            
            user_is_active              = 1 if cur_user_flag & FLAG_BIT_USER_IS_ACTIVE > 0 else 0
            user_is_email_verified      = 1 if cur_user_flag & FLAG_BIT_USER_EMAIL_VERIFIED > 0 else 0
            user_is_mobile_verified     = 1 if cur_user_flag & FLAG_BIT_USER_MOBILE_NUM_VERIFIED > 0 else 0
            user_is_deleted             = 1 if cur_user_flag & FLAG_BIT_USER_IS_DELETED > 0 else 0
            user_is_account_admin       = 1 if cur_user_flag & FLAG_BIT_USER_IS_ACCOUNT_ADMIN > 0 else 0
            
            acc_is_enabled              = 1 if cur_account_flag & FLAG_BIT_ACCOUNT_ENABLE > 0 else 0
            acc_is_company_owned        = 1 if cur_account_flag & FLAG_BIT_FLAG_BIT_COMPANY_OWNED_ACCOUNT > 0 else 0
            
            cur_entry = {
                'user': {
                    'id':               user_id,
                    'is_active':        user_is_active,
                    'is_email_verified': user_is_email_verified,
                    'is_mobile_verified': user_is_mobile_verified
                },
                
                'account': {
                    'id':               cur_user_account_id,
                    'is_enabled':       acc_is_enabled,
                    'is_company_owned': acc_is_company_owned,
                    'cur_bill_id':      cur_account_bill_id,
                    'cur_bill_status_id': cur_account_bill_status_id
                }
            }
            return cur_entry
        
        return None
    
    
    def get_user_info(self, user_id):
        """
        Get complete user information
        """
        sql = """
            SELECT 
                a.id,
                a.account_id,
                a.flag,
                a.email,
                a.signup_social_media_id,
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
        """
        
        rows = self._execute_query(sql, [user_id])
        
        if rows is None:
            return None
        
        for row in rows:
            cur_user_id                         = row[0]
            cur_user_account_id                 = row[1]
            cur_user_flag                       = row[2]
            cur_user_email                      = row[3]
            cur_user_signup_social_media_id     = row[4]
            cur_user_mobile_num                 = row[5]
            cur_user_name                       = row[6]
            cur_user_name_last                  = row[7]
            cur_user_name_first                 = row[8]
            
            cur_user_group_id                   = row[9]
            cur_user_group_num                  = row[10]
            cur_user_group_flag_business_obj_1  = row[11]
            cur_user_group_flag_business_obj_2  = row[12]
            cur_user_group_name                 = row[13]
            
            cur_user_req_join_acc_id            = row[14]
            cur_user_req_account_id             = row[15]
            cur_user_req_status_id              = row[16]
            cur_user_req_dt_entry               = str(row[17])[0:10] if row[17] else None
            cur_user_req_account_name           = row[18]
            
            cur_entry = {
                'user': {
                    'id':               cur_user_id,
                    'account_id':       cur_user_account_id,
                    'flag':             cur_user_flag,
                    'email':            cur_user_email,
                    'social_media_id':  cur_user_signup_social_media_id,
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
            
            
            # Get pig farms for this user
            user_pig_farm_ids = self.model['user_farm'].get_list(user_id=user_id)
            if user_pig_farm_ids:
                cur_entry['pig_farms'] = user_pig_farm_ids
            
                
            return cur_entry
        
        return None
    
    
    def get_list(self, account_id, inc_deleted=0):
        """
        Get user list for an account
        """
        sql = """
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
            LEFT OUTER JOIN user_group b ON a.user_group_id = b.id
            WHERE a.account_id = %s
        """
        
        params = [account_id]
        
        if inc_deleted == 0:
            sql += " AND (a.flag & 8) = 0"
        
        sql += " ORDER BY a.name_first"
        
        rows = self._execute_query(sql, params)
        
        if rows is None:
            return []
        
        result = []
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
    
    
    def register_or_login(self, data=None):
        """
        PROCEDURE user_register_or_login(
            in_login_social_media_id INT,
            in_social_media_user_id VARCHAR(120),
            
            in_acc_access_code_id  INT,
            in_acc_access_code      VARCHAR(10),


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
            in_ip_address           VARCHAR(24),
            
            in_is_mobile            INT,
            in_is_webview           INT,
            
            in_browser              VARCHAR(50),
            in_browser_version      VARCHAR(20),
            in_webview_platform     VARCHAR(30),
            in_os                   VARCHAR(50),
            in_os_version           VARCHAR(20),
            in_device               VARCHAR(50),
            in_device_type          VARCHAR(20)            
        )    
        """
        
        params = [
            data.login_social_media_id  if data.login_social_media_id and data.login_social_media_id > 0 else None,
            data.social_media_user_id   if data.social_media_user_id else None,
                
            data.access_code_id         if data.access_code_id and data.access_code_id > 0 else None,
            data.access_code_hid        if data.access_code_hid else None,
                
                
            data.name                   if data.name and data.name.strip() else None,
            data.name_last              if data.name_last and data.name_last.strip() else None,
            data.name_first             if data.name_first and data.name_first.strip() else None,
                
            data.email, 
                
            data.login_country_code     if data.login_country_code and data.login_country_code.strip() else None,
            data.login_country_name     if data.login_country_name and data.login_country_name.strip() else None,
            data.login_city             if data.login_city and data.login_city.strip() else None,
            data.login_region           if data.login_region and data.login_region.strip() else None,
            
                
            data.viewport_width         if data.viewport_width and data.viewport_width > 0 else None,
            data.viewport_height        if data.viewport_height and data.viewport_height > 0 else None,
            data.ip_address,    
                
            data.is_mobile              if data.is_mobile is not None else None,
            data.is_webview             if data.is_webview is not None else None,
                
            data.browser                if data.browser and data.browser.strip() else None,
            data.browser_version        if data.browser_version and data.browser_version.strip() else None,
            data.webview_platform       if data.webview_platform and data.webview_platform.strip() else None,
            data.os                     if data.os and data.os.strip() else None,
            data.os_version             if data.os_version and data.os_version.strip() else None,
            data.device                 if data.device and data.device.strip() else None,
            data.device_type            if data.device_type and data.device_type.strip() else None
        ]
        
        rows = self._call_procedure('user_register_or_login', params)
        
        if rows is None:
            return None
        
        
        row = rows[0]
        
        
        cur_result_num              = row[0]
        cur_result_code             = row[1]
        cur_result_desc             = row[2]
        
        cur_user_id                 = row[3]
        cur_user_account_id         = row[4]
        cur_user_flag               = row[5]
        cur_user_unverified_id      = row[6]
        cur_verify_id               = row[7]
        cur_verify_code             = row[8]
        cur_verify_ts_expiry        = row[9]
        cur_verify_dt_expiry        = str(row[10]) if row[10] else None
        cur_expiry_minutes          = row[11]
        
        cur_entry = {
            'result': {
                'num':              cur_result_num,
                'code':             cur_result_code,
                'desc':             cur_result_desc,
            },
            
            'user': {
                'id':               cur_user_id,
                'account_id':       cur_user_account_id,
                'flag':             cur_user_flag
            },
            
            'user_unverified': {
                'id':               cur_user_unverified_id,
                'verify_id':        cur_verify_id,
                'verify_code':      str(cur_verify_code),
                'verify_ts_expiry': cur_verify_ts_expiry,
                'verify_dt_expiry': cur_verify_dt_expiry,
                'expiry_minutes':   cur_expiry_minutes
            }
        }
        
        if cur_user_id == 0:
            del cur_entry['user']
        
        if cur_user_account_id and cur_user_account_id > 0 and cur_user_id > 0:
            del cur_entry['user_unverified']
        
        return cur_entry
    
    
    def update_login(self, user_id, data=None):
        """
        PROCEDURE user_update_login(
            in_user_id              INT,
            
            
            in_login_country_code   VARCHAR(3),  /* This should be in upper case*/
            in_login_country_name   VARCHAR(50),
            in_login_city           VARCHAR(50), /* This should be in upper case*/
            in_login_region         VARCHAR(50), /* This should be in upper case*/
            
            
            in_viewport_width       INT,
            in_viewport_height      INT,
            in_ip_address           VARCHAR(24),
            
            in_is_mobile            INT,
            in_is_webview           INT,
            
            in_browser              VARCHAR(50),
            in_browser_version      VARCHAR(20),
            in_webview_platform     VARCHAR(30),
            in_os                   VARCHAR(50),
            in_os_version           VARCHAR(20),
            in_device               VARCHAR(50),
            in_device_type          VARCHAR(20)
                
        )    
        """
        
        params = [
            user_id,
            
            
            data.login_country_code     if data.login_country_code and data.login_country_code.strip() else None,
            data.login_country_name     if data.login_country_name and data.login_country_name.strip() else None,
            data.login_city             if data.login_city and data.login_city.strip() else None,
            data.login_region           if data.login_region and data.login_region.strip() else None,
            
            
            data.viewport_width         if data.viewport_width and data.viewport_width > 0 else None,
            data.viewport_height        if data.viewport_height and data.viewport_height > 0 else None,
            data.ip_address,
            
            data.is_mobile              if data.is_mobile is not None else None,
            data.is_webview             if data.is_webview is not None else None,
                
            data.browser                if data.browser and data.browser.strip() else None,
            data.browser_version        if data.browser_version and data.browser_version.strip() else None,
            data.webview_platform       if data.webview_platform and data.webview_platform.strip() else None,
            data.os                     if data.os and data.os.strip() else None,
            data.os_version             if data.os_version and data.os_version.strip() else None,
            data.device                 if data.device and data.device.strip() else None,
            data.device_type            if data.device_type and data.device_type.strip() else None
        ]
        
        rows = self._call_procedure('user_update_login', params)
        
        if rows is None:
            return None
        
        row = rows[0]
        
        cur_user_login_id           = row[0]
        
        return {
            'user_login_id':        cur_user_login_id
        }
    
    
    def user_verify_email(self, data=None):
        """
        PROCEDURE user_verify_email(
            in_unverified_user_id   INT, /* Only one of this is not NULL and > 0. */
            in_user_id              INT, /* Only one of this is not NULL and > 0. */
    
            in_auth_code            INT,
            
            in_viewport_width       INT,
            in_viewport_height      INT,
            
            in_ip_address           VARCHAR(24)
            
        )    
        """
        
        params = [
            data.unverified_user_id     if data.unverified_user_id and data.unverified_user_id > 0 else None,
            data.user_id                if data.user_id and data.user_id > 0 else None,
            
            data.auth_code,
            
            data.viewport_width         if data.viewport_width and data.viewport_width > 0 else None,
            data.viewport_height        if data.viewport_height and data.viewport_height > 0 else None,
            
            data.ip_address
        ]
        
        rows = self._call_procedure('user_verify_email', params)
        
        if rows is None:
            return None
        
        row = rows[0]
        
        cur_result_num              = row[0]
        cur_result_code             = row[1]
        cur_result_desc             = row[2]
        cur_user_id                 = row[3]
        cur_user_flag               = row[4]
        
        cur_entry = {
            'result': {
                'num':              cur_result_num,
                'code':             cur_result_code,
                'desc':             cur_result_desc,
            },
            
            'user': {
                'id':               cur_user_id,
                'flag':             cur_user_flag
            }
        }
        
        return cur_entry
    
    
    def user_resend_verify_code(self, unverified_user_id, user_id):
        """
        PROCEDURE user_resend_verify_code(
            in_unverified_user_id   INT, /* Only one of this is not NULL and > 0. */
            in_user_id              INT /* Only one of this is not NULL and > 0. */

            
        )    
        """
        
        params = [
            unverified_user_id if unverified_user_id and unverified_user_id > 0 else None,
            user_id if user_id and user_id > 0 else None
        ]
        
        rows = self._call_procedure('user_resend_verify_code', params)
        
        if rows is None:
            return None
        
        row = rows[0]
        
        cur_result_num              = row[0]
        cur_result_code             = row[1]
        cur_result_desc             = row[2]
        
        cur_user_id                 = row[3]
        cur_user_account_id         = row[4]
        cur_user_flag               = row[5]
        cur_user_unverified_id      = row[6]
        
        cur_verify_id               = row[7]
        cur_verify_code             = row[8]
        cur_verify_ts_expiry        = row[9]
        cur_verify_dt_expiry        = str(row[10]) if row[10] else None
        cur_expiry_minutes          = row[11]
        cur_user_email              = row[12]
        
        cur_entry = {
            'result': {
                'num':              cur_result_num,
                'code':             cur_result_code,
                'desc':             cur_result_desc,
            },
            
            'user': {
                'id':               cur_user_id,
                'account_id':       cur_user_account_id,
                'flag':             cur_user_flag
            },
            
            'user_unverified': {
                'id':               cur_user_unverified_id,
                'verify_id':        cur_verify_id,
                'verify_code':      str(cur_verify_code),
                'verify_ts_expiry': cur_verify_ts_expiry,
                'verify_dt_expiry': cur_verify_dt_expiry,
                'expiry_minutes':   cur_expiry_minutes
            },
            
            'user_email':           cur_user_email
        }
        
        if cur_user_id == 0:
            del cur_entry['user']
        
        if cur_user_unverified_id is None or cur_user_unverified_id == 0:
            del cur_entry['user_unverified']
        
        return cur_entry
