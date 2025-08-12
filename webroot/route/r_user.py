# August 8, 2025
# Jack Wong

import os
import sys
import random
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *
from server_messages        import *


import data_model           as dm


FLAG_BIT_USER_IS_ACTIVE                 = 1
FLAG_BIT_USER_EMAIL_VERIFIED            = 2
FLAG_BIT_USER_MOBILE_NUM_VERIFIED       = 4
FLAG_BIT_USER_IS_DELETED                = 8

FLAG_BIT_USER_IS_ACCOUNT_ADMIN          = 16


USER_REGISTER_RES_NUM_SUCCESS           = 0


def write_user_flag_bits(user, user_flag):
    # Break down flags for easier reading
        
    if user_flag & FLAG_BIT_USER_IS_ACTIVE > 0:
        user['is_active'] = 1
    else:
        user['is_active'] = 0
    
    
    if user_flag & FLAG_BIT_USER_EMAIL_VERIFIED > 0:
        user['is_email_verified'] = 1
    else:
        user['is_email_verified'] = 0
    
        
    if user_flag & FLAG_BIT_USER_MOBILE_NUM_VERIFIED > 0:
        user['is_mobile_num_verified'] = 1
    else:
        user['is_mobile_num_verified'] = 0
    
    
    if user_flag & FLAG_BIT_USER_IS_DELETED > 0:
        user['is_deleted'] = 1
    else:
        user['is_deleted'] = 0
    
    
    if user_flag & FLAG_BIT_USER_IS_ACCOUNT_ADMIN > 0:
        user['is_account_admin'] = 1
    else:
        user['is_account_admin'] = 0
    
    

@app.post("/user/register")
async def user_register(user_data: dm.DataUser):
    data = {
        'username':         user_data.username,
        'email':            user_data.email,
        'password':         user_data.password,
        'mobile_num':       user_data.mobile_num
    }
    
    
    res_register    =  model['user'].register(data)
    
    if res_register is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    # Check for email verification flag
    
    user_id         = res_register['user']['id']
    user_flag       = res_register['user']['flag']
        
    user_hashid     = hashids_user.encrypt(user_id)
    
    # remove plain id
    del res_register['user']['id']
    res_register['user']['h_id'] = user_hashid

    result_num      = res_register['result']['num']

    if result_num == USER_REGISTER_RES_NUM_SUCCESS:
        
        verify_code = random.randint(MFA_VERIFICATION_CODE_MIN,
                        MFA_VERIFICATION_CODE_MAX)
        
        now         = datetime.now()
        expiry      = now + timedelta(
                        minutes = NUM_MINUTES_EXPIRE_USER_REG_EMAIL_VERIFY)
        
        expiry_ts   = int(datetime.timestamp(expiry))
        expiry_str  = expiry.strftime('%Y-%m-%d %H:%M:%S')
        
        
        # TODO: send verification code
        res_send_code   = MFA_SEND_SUCCESS
        
        
        if res_send_code  == MFA_SEND_SUCCESS:
            res_register['mfa']  = {}
            
            data = {
                'business_obj_id':  BUSINESS_OBJ_ID_USER_REGISTER,
                'b_table_row_id':   user_id,
                'channel_id':       MFA_CHANNEL_ID_EMAIL,
                'country_code':     None,
                'mobile_num':       None,
                'email':            user_data.email,
                
                'auth_code':        verify_code,
                'ts_expiry':        expiry_ts,
                'dt_expiry':        expiry_str
            }
            
            
            res_mfa_add     = model['mfa'].add(data)
            mfa_id          = res_mfa_add['id']
            
            
            # Update user.last_mfa_id_email_verify
            data = {
                'user_id':          user_id,
                'mfa_id':           mfa_id
            }
            model['user'].update_mfa_id_email_verify(data)
            
            
            mfa_hashid      = hashids_common.encrypt(mfa_id)
            
            res_register['mfa']['h_id'] = mfa_hashid

        
        write_user_flag_bits(res_register['user'], user_flag)

    return res_register
    
    
MFA_EMAIL_RES_NUM_VERIFIED                          = 0 
MFA_EMAIL_RES_NUM_EMAIL_ALREADY_VERIFIED            = 1
MFA_EMAIL_RES_NUM_MFA_INVALID_CODE                  = 2
MFA_EMAIL_RES_NUM_MFA_EXPIRED                       = 3


@app.get("/user/email/verify_code")
async def user_email_verify_code(uhid:str, code: int):
    """
    After the user registers, a verification code is sent to the user's email.
    The user should then input this code and send to server for verification.

    Parameters
    ----------
    uhid : str
        user hashid
    
    code : int
        verification code
    
    """

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    
    user_id = res[0]
    
    data = {
        'user_id':      user_id,
        'auth_code':    code
    }
    
    
    res_verify = model['user'].verify_email_mfa(data)
    
    if res_verify is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_verify['user']['id']
    res_verify['user']['h_id'] = uhid
    
    user_flag = res_verify['user']['flag']
    
    write_user_flag_bits(res_verify['user'], user_flag)
    
    return res_verify
    
    
@app.get("/user/email/verify_code/resend")
async def user_email_verify_resend(uhid:str):
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    
    user_id = res[0]
    
    
    
    verify_code = random.randint(MFA_VERIFICATION_CODE_MIN,
                            MFA_VERIFICATION_CODE_MAX)
            
    now         = datetime.now()
    expiry      = now + timedelta(
                    minutes = NUM_MINUTES_EXPIRE_USER_REG_EMAIL_VERIFY)
    
    expiry_ts   = int(datetime.timestamp(expiry))
    expiry_str  = expiry.strftime('%Y-%m-%d %H:%M:%S')
    
    
    user_info = model['user'].get_user_info(user_id)
    
    # TODO: send verification code
    res_send_code   = MFA_SEND_SUCCESS
    
    if res_send_code  == MFA_SEND_SUCCESS:
    
        data = {
            'business_obj_id':  BUSINESS_OBJ_ID_USER_REGISTER,
            'b_table_row_id':   user_id,
            'channel_id':       MFA_CHANNEL_ID_EMAIL,
            'country_code':     None,
            'mobile_num':       None,
            'email':            None,
            
            'auth_code':        verify_code,
            'ts_expiry':        expiry_ts,
            'dt_expiry':        expiry_str
        }
    

        res_mfa_add     = model['mfa'].add(data)
        mfa_id          = res_mfa_add['id']
        
        
        # Update user.last_mfa_id_email_verify
        data = {
            'user_id':          user_id,
            'mfa_id':           mfa_id
        }
        model['user'].update_mfa_id_email_verify(data)


        return {
            'result':{
                'num':  0,
                'code': 'SUCCESS',
                'desc': ''
            }
        }
        
    return {
        'result':{
            'num':  ERROR_DATABASE_ERROR,
            'code': 'ERROR_DATABASE_ERROR',
            'desc': ''
        }
    }
    
    
RES_NUM_SUCCESS_SEND_EMAIL_TO_ACCOUNT_ADMIN_TO_ADD_USER_TO_ACCOUNT = 0
    
@app.get("/user/request/add_to_account")
async def user_request_add_to_account(uhid:str, ahid:str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    
    user_id = res[0]
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
    
    data = {
        'user_id':      user_id,
        'account_id':   account_id,
        'user_hashid':  uhid
    }
   
    res_add = model['account'].add_account_request_add_user(data)
        
    # TODO; send an email to account admins to grant this user to be added to this 
    # account
    
    res_send = RES_NUM_SUCCESS_SEND_EMAIL_TO_ACCOUNT_ADMIN_TO_ADD_USER_TO_ACCOUNT
    
    if res_send == RES_NUM_SUCCESS_SEND_EMAIL_TO_ACCOUNT_ADMIN_TO_ADD_USER_TO_ACCOUNT:
        
        key = SUCCESS_SEND_EMAIL_TO_ACCOUNT_ADMIN_TO_ADD_USER_TO_ACCOUNT
        msg = SERVER_MESSAGES[key]['en']
        msg = msg.replace('{ACCOUNT_HID}', ahid)
        
        return {
            'result':{
                'num':  0,
                'code': 'SUCCESS',
                'desc': '',
                'msg':  msg
            }
        }
    
    

    
    return  {
        'result':{
            'num':  ERROR_SERVER_ERROR,
            'code': 'ERROR_SERVER_ERROR',
            'desc': ''
        }
    }