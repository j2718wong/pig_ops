# August 8, 2025
# Jack Wong

import os
import sys
import random
import pprint
import json


from fastapi                import HTTPException, status
from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
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


SOCIAL_MEDIA_GOOGLE             = 1
SOCIAL_MEDIA_FACEBOOK           = 2
SOCIAL_MEDIA_TIKTOK             = 3

ALLOWED_SOCIAL_MEDIA_LOGIN = [
    SOCIAL_MEDIA_GOOGLE,  
    SOCIAL_MEDIA_FACEBOOK,
    SOCIAL_MEDIA_TIKTOK  

]





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
    
    

@app.post("/user/register", tags=["User"])
async def user_register(user_data: dm.DataUser):
    # TODO preprocess 
    # checking token
    
    

    res_register    =  model['user'].register(user_data)
    
    if res_register is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Check for email verification flag
    user_id         = res_register['user']['id']
    user_flag       = res_register['user']['flag']
        
    user_hashid     = hashids_user.encrypt(user_id)
    
    # remove plain id
    del res_register['user']['id']
    res_register['user']['hid'] = user_hashid

    result_num      = res_register['result']['num']

    if result_num == 0:
        verify_code = random.randint(MFA_VERIFICATION_CODE_MIN,
                        MFA_VERIFICATION_CODE_MAX)
        
        dt_now      = datetime.now()
        dt_expiry   = dt_now + timedelta(
                        minutes = NUM_MINUTES_EXPIRE_USER_REG_EMAIL_VERIFY)
        
        expiry_ts   = int(datetime.timestamp(dt_expiry))
        expiry_str  = dt_expiry.strftime('%Y-%m-%d %H:%M:%S')
        
        
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
            
            res_register['mfa']['hid'] = mfa_hashid

        
        # No more more flag decomposition on transit; for security reasons;
        # Should be decomposed at JS side
        # write_user_flag_bits(res_register['user'], user_flag)

    return res_register
    
    
MFA_EMAIL_RES_NUM_VERIFIED                          = 0 
MFA_EMAIL_RES_NUM_EMAIL_ALREADY_VERIFIED            = 1
MFA_EMAIL_RES_NUM_MFA_INVALID_CODE                  = 2
MFA_EMAIL_RES_NUM_MFA_EXPIRED                       = 3


@app.get("/user/email/verify_code", tags=["User"])
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
                'code': 'ERROR_USER_INVALID_USER_HASHID'
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
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_verify['user']['id']
    res_verify['user']['hid'] = uhid
    
    user_flag = res_verify['user']['flag']
    
    
    return res_verify
    
    
@app.get("/user/email/verify_code/resend", tags=["User"])
async def user_email_verify_resend(uhid:str):
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    
    user_id = res[0]
    
    
    
    verify_code = random.randint(MFA_VERIFICATION_CODE_MIN,
                            MFA_VERIFICATION_CODE_MAX)
            
    dt_now      = datetime.now()
    dt_expiry   = dt_now + timedelta(
                    minutes = NUM_MINUTES_EXPIRE_USER_REG_EMAIL_VERIFY)
    
    expiry_ts   = int(datetime.timestamp(dt_expiry))
    expiry_str  = dt_expiry.strftime('%Y-%m-%d %H:%M:%S')
    
    
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
                'code': 'SUCCESS'
            }
        }
        
    return {
        'result':{
            'num':  ERROR_DATABASE_ERROR,
            'code': 'ERROR_DATABASE_ERROR'
        }
    }
    
    
@app.get("/user/login_social", tags=["User"])
async def user_info(request: Request):
     # Get raw JSON body
    body = await request.body()
    
    # Parse JSON manually
    data = json.loads(body)
    
    
    if 'social_media_id' not in data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = REQUEST_ACCESS_DENIED
        )
    
    
    social_media_id = data.get('social_media_id')
    if social_media_id not in ALLOWED_SOCIAL_MEDIA_LOGIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = REQUEST_ACCESS_DENIED
        )

    
    
    if 'email' not in data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = REQUEST_ACCESS_DENIED
        )
    
    
    email = data['email']
    len_email = len(email)
    if  len_email == 0 or len_email > 50:
        return {
            'result':{
                'num':  ERROR_USER_EMAIL,
                'code': 'ERROR_USER_EMAIL'
                'desc': 'Invalid email lenght.'
            }
        }
    
    
    # there should be at least a user.name_first;
    
    if 'name_first' not in data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = REQUEST_ACCESS_DENIED
        )
    
    
    name_first = data['name_first']
    len_name_first = len(name_first)
    if  len_name_first == 0 or len_name_first > 50:
        return {
            'result':{
                'num':  ERROR_USER_EMAIL,
                'code': 'ERROR_USER_EMAIL'
                'desc': 'Invalid email lenght.'
            }
        }
    
    model['user']
    
    
    
@app.get("/user/info", tags=["User"])
async def user_info(uhid:str):
    """
    
    Parameters
    ----------
    uhid : str
        user hashid
    
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
    
        
    res_get = model['user'].get_user_info(user_id)
    
    if res_get is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_get['user']['id']
    res_get['user']['hid'] = uhid
    
    account_id          = res_get['user']['account_id']
    account_hashid      = hashids_account.encrypt(account_id)
    
    del res_get['user']['account_id']
    res_get['user']['account_hid'] = account_hashid
    
    user_group_id       = res_get['user_group']['id']
    user_group_hashid   = hashids_common.encrypt(user_group_id)
    res_get['user_group']['hid'] = user_group_hashid
    
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res_get
    }
    

@app.get("/user/list", tags=["User"])
async def pig_farm_staff_list(ahid: str, inc_deleted : int = 0):
    """
    Will get user list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    
    """
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID'
            }
        }
    
    
    account_id = res[0]
        
        
    res = model['user'].get_list(account_id, inc_deleted)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'    
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['user']['id']
        cur_hid = hashids_user.encrypt(cur_id)
        
        del cur_entry['user']['id']
        cur_entry['user']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['user_group']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['user_group']['id']
        cur_entry['user_group']['hid']   = cur_hid
        
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    

    

