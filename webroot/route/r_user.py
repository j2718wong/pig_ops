# August 8, 2025
# Jack Wong

import os
import sys
import random
import pprint
import json
import httpx


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse
from fastapi                import BackgroundTasks


from google.oauth2          import id_token
from google.auth.transport  import requests

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *





import data_model           as dm



# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_utils                import (remove_database_null_description,
                                    replace_plain_ids_user_account,
                                    get_browser_info)


from r_a0_security_checks   import (check_if_valid_user_account,
                                    get_user_account_info)
                                    
from email_templates        import *




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



def create_access_token(data: dict):
    to_encode   = data.copy()
    expire      = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt




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
    


@app.get("/user/verify_token", tags=["User"])
async def user_verify_token(request: Request):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    data_user_account = get_user_account_info(user_id)
            
            
    # With this block
    replace_plain_ids_user_account(data_user_account)

    return {
        'result':{
            'num':  0
        },
        
        'user_account': data_user_account
    }

    




@app.post("/user/register_or_login", tags=["User"])
async def user_register_or_login(request: Request,
        background_tasks: BackgroundTasks, 
        user_data: dm.DataUserLogin):

    access_code_id = None
    
    access_code_hid        = user_data.access_code_hid

    if access_code_hid is not None:
        res = hashids_access_code.decrypt(access_code_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_USER_REQUEST_INVALID_ACCESS_CODE,
                    'code': 'ERROR_USER_REQUEST_INVALID_ACCESS_CODE'
                }
            }
        
        access_code_id = res[0]
        
        user_data.access_code_id = access_code_id
         
         
    # Get browser info 
    browser_info                = get_browser_info(request)
    
    user_data.is_mobile         = 1 if browser_info['is_mobile'] else 0
    user_data.is_webview        = 1 if browser_info['is_webview'] else 0
    user_data.browser           = browser_info['browser']
    user_data.browser_version   = browser_info['browser_version']
    user_data.webview_platform  = browser_info['webview_platform']
    
    user_data.os                = browser_info['os']
    user_data.os_version        = browser_info['os_version']
    user_data.device            = browser_info['device']
    user_data.device_type       = browser_info['device_type'] 
    user_data.ip_address        = browser_info['ip_address']
    
    
    res_register =  model['user'].register_or_login(user_data)
    
    
    if res_register is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # No token yet at this time; user must address the 
    # non-zero res_register['result']['num']
    if res_register['result']['num'] > 0:
        return res_register
    
    
    
    # Get user_id is there is any
    user_id = None
    if 'user' in res_register:
        user_id = res_register['user']['id']
    
    
    
    # Check if user is unverified
    if 'user_unverified' in res_register:
        user_unverified = res_register['user_unverified']

        
        # Replace plain_id
        cur_id     = user_unverified['id']
        
        # The user is not in the system and unverified.
        if cur_id is not None and cur_id > 0:
            cur_hid    = hashids_common.encrypt(cur_id)
        
            del user_unverified['id']
            user_unverified['hid']   = cur_hid
        
        
        # The user already in the system but needs code authentication, 
        if user_id is not None:
            cur_id      = user_id  
            cur_hid     = hashids_user.encrypt(cur_id)
            
            # Need to add this 
            user_unverified['uhid'] = cur_hid
            
            
        """
        So two possible keys of user_unverified
        res_register['user_unverified']['hid']  -> user not in the system yet
        res_register['user_unverified']['uhid'] -> needs to authenticate user
        """
        
        
        
        del user_unverified['verify_id']
        
        verification_code   = user_unverified['verify_code']
        expiry_minutes      = user_unverified['expiry_minutes']
        
        del user_unverified['verify_code']

        
        # Send verification code email to user
        template    = EmailVerificationCode()
        subject     = template.get_email_subject()
        msg_body    = template.get_email_body(verification_code, expiry_minutes)
        
        user_email  = user_data.email
        print('\n\nAbout to send verification email to: %s' % user_email)
        
        background_tasks.add_task(send_email, [user_email], subject, msg_body)
        
        return res_register
        
        
    # At this point user is verified    
    
    
    # Get user_id and account info
    user_id = res_register['user']['id']
    data_user_account = get_user_account_info(user_id)
            
            
    # Replace the user block
    del res_register['user']
    
    
    # With this block
    res_register['user_account'] = data_user_account
    replace_plain_ids_user_account(data_user_account)

    
    # Create JWT token
    user_hid = data_user_account['user']['user']['hid']
    access_token = create_access_token(data={"uhid": user_hid})
    
    
    res_register['bearer_token'] = access_token
    
    return res_register
    
    
@app.post("/user/email/verify_code", tags=["User"])
async def user_email_verify_code(request: Request, data: dm.DataUserEmailVerify):
    """
    After the user registers, a verification code is sent to the user's email.
    The user should then input this code and send to server for verification.

    
    """
    
    uvuhid = data.uvuhid
    unverified_user_id = 0
    
    if uvuhid is not None:
        # Note: Since user is not yet verified, the hashids used is hashids_common;
        # after verified, use hashids_user  
        res = hashids_common.decrypt(uvuhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_USER_INVALID_USER_HASHID,
                    'code': 'ERROR_USER_INVALID_USER_HASHID'
                }
            }
        
        
        unverified_user_id = res[0]
        
    
    uhid = data.uhid
    user_id = 0
    
    if uhid is not None:
        res = hashids_user.decrypt(uhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_USER_INVALID_USER_HASHID,
                    'code': 'ERROR_USER_INVALID_USER_HASHID'
                }
            }
        
        
        user_id = res[0]
        
    
    
    
    
    client_host         = request.client.host
    
    data.unverified_user_id  = unverified_user_id
    data.user_id        = user_id
    data.ip_address     = client_host
    
    
    res_verify = model['user'].user_verify_email(data)
    
    if res_verify is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    if res_verify['user']['id'] > 0:
        # User is registered and email verified at this point
        
         # Get user_account info
        user_id = res_verify['user']['id']
        data_user_account = get_user_account_info(user_id)
            
            
        # Replace the user block
        del res_verify['user']
        
        
        # With this block
        res_verify['user_account'] = data_user_account
        replace_plain_ids_user_account(data_user_account)

        
        # Create JWT token
        user_hid = data_user_account['user']['user']['hid']
        access_token = create_access_token(data={"uhid": user_hid})
        
        
        res_verify['bearer_token'] = access_token
        
        return res_verify
    
    
    del res_verify['user']
    
    
    return res_verify
    
    
@app.get("/user/email/verify_code/resend", tags=["User"])
async def user_email_verify_resend(request: Request,
    background_tasks: BackgroundTasks,
    uvuhid:str = None, uhid:str = None):
    
    unverified_user_id = 0
    
    if uvuhid is not None:
        # Note: Since user is not yet verified, the hashids used is hashids_common;
        # after verified, use hashids_user  
        res = hashids_common.decrypt(uvuhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_USER_INVALID_USER_HASHID,
                    'code': 'ERROR_USER_INVALID_USER_HASHID'
                }
            }
        
        
        unverified_user_id = res[0]
        
    

    user_id = 0
    
    if uhid is not None:
        res = hashids_user.decrypt(uhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_USER_INVALID_USER_HASHID,
                    'code': 'ERROR_USER_INVALID_USER_HASHID'
                }
            }
        
        
        user_id = res[0]
    
    
    res = model['user'].user_resend_verify_code(unverified_user_id, user_id)
    
    
    user_unverified = res['user_unverified']
    user_email      = res['user_email']
        
        
    # Replace plain_id
    user_unverified['hid']   = uvuhid
    
    
    del user_unverified['verify_id']
    
    verification_code   = user_unverified['verify_code']
    expiry_minutes      = user_unverified['expiry_minutes']
    
    del user_unverified['verify_code']

    
    # Send verification code email to user
    template    = EmailVerificationCode()
    subject     = template.get_email_subject()
    msg_body    = template.get_email_body(verification_code, expiry_minutes)
    
    
    background_tasks.add_task(send_email, [user_email], subject, msg_body)
    
    return res
    
    
    
@app.post("/user/track_app_install", tags=["User"])
async def user_track_app_install(request: Request, data: dm.DataUserTrackAppInstall):
    """
    This is used to track user app install
    """
    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    data.user_id        = user_id
    
    res_add = model['user'].add_track_app_install(data)
    
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id    = res_add['track_install']['id']
    cur_hid   = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_add['track_install']['id']
    res_add['track_install']['hid'] = cur_hid
    
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    return res_add
    
    
    
@app.post("/user/push_susbcription_add", tags=["User"])
async def user_push_susbcription_add(request: Request, data: dm.DataUserPushSubscription):
    """
    This is used to track user app install
    """
    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    data.user_id        = user_id
    
    res_add = model['user'].add_push_subscription(data)
    
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id    = res_add['push_susbcription']['id']
    cur_hid   = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_add['push_susbcription']['id']
    res_add['push_susbcription']['hid'] = cur_hid
    
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    return res_add
    
    


    
    
    
@app.post("/user/login_social", tags=["User"])
async def user_login_social(request: Request, user_data: dm.DataUserLogin):
    """
    This is signup or login using scoial media.
    """
    
    
    social_media_id = user_data.social_media_id
    if social_media_id == 0 or social_media_id not in ALLOWED_SOCIAL_MEDIA_LOGIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = REQUEST_ACCESS_DENIED
        )
    
    
    
    email = user_data.email
    len_email = len(email)
    if  len_email == 0 or len_email > 50:
        return {
            'result':{
                'num':  ERROR_USER_EMAIL,
                'code': 'ERROR_USER_EMAIL',
                'desc': 'Invalid email lenght.'
            }
        }
    
    
    # there should be at least a user.name_first;
    name_first = user_data.name_first
    len_name_first = len(name_first)
    if len_name_first == 0 or len_name_first > 50:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = REQUEST_ACCESS_DENIED
        )
    
    
    if user_data.viewport_width is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = REQUEST_ACCESS_DENIED
        )
    
    
    if user_data.viewport_height is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = REQUEST_ACCESS_DENIED
        )
    
    
    
    # Get browser info 
    browser_info                = get_browser_info(request)
    
    user_data.is_mobile         = 1 if browser_info['is_mobile'] else 0
    user_data.is_webview        = 1 if browser_info['is_webview'] else 0
    user_data.browser           = browser_info['browser']
    user_data.browser_version   = browser_info['browser_version']
    user_data.webview_platform  = browser_info['webview_platform']
    
    user_data.os                = browser_info['os']
    user_data.os_version        = browser_info['os_version']
    user_data.device            = browser_info['device']
    user_data.device_type       = browser_info['device_type'] 
    user_data.ip_address        = browser_info['ip_address']
    
    
    res_login = model['user'].register_or_login(user_data)
    if res_login == None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    

    # Get user_id
    user_id = res_login['user']['id']
    
    
    # Get user_account info
    data_user_account = get_user_account_info(user_id)
    
    
    # Replace the user block
    del res_login['user']
    
    
    # With this block
    res_login['user_account'] = data_user_account


    replace_plain_ids_user_account(data_user_account)

    
    return res_login
    
    
    
    
    
    
    
    
@app.get("/user/info", tags=["User"])
async def user_info(uhid:str):
    """
    
    Parameters
    ----------
    uhid : str
        user hashid
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    

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
                'code': 'ERROR_DATABASE_ERROR'
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
            'num':  0
        },
        
        'data': res_get
    }
    


@app.get("/user/list", tags=["User"])
async def user_list(request: Request, ahid: str, inc_deleted : int = 0):
    """
    Will get user list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
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
            'num':  0
        },
        
        'data': res
    }
    


@app.get("/user/push_susbcription/list", tags=["User"])
async def user_push_susbcription_list(request: Request):
    """
    Will get user push subcription list.
    
    Parameters
    ----------
    
        
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
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
    
    
    res                 = model['user'].get_push_subscription_list(user_id)

    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    

    
    for cur_entry in res:
        
        cur_id      = cur_entry['push_subscription']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['push_subscription']['id']
        cur_entry['push_subscription']['hid'] = cur_hid
        
        
            
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }






# NEW CODE Using HTTPS

from fastapi import Request, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse, HTMLResponse
import httpx
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from urllib.parse import urlencode


@app.get("/auth/google/callback", response_class=HTMLResponse)
async def google_callback(
    request: Request, 
    background_tasks: BackgroundTasks,
    code: str = None, 
    state: str = None,
    error: str = None
):
    """
    Handle the Google OAuth redirect callback
    """
    # Check for error from Google
    if error:
        print(f"Google OAuth error: {error}")
        return RedirectResponse(url="/login?error=google_auth_failed")
    
    if not code:
        return RedirectResponse(url="/login?error=no_code")
    
    try:
        # Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        
        # Build the full redirect URI
        base_url = str(request.base_url).rstrip('/')
        redirect_uri = f"{base_url}{GOOGLE_REDIRECT_URI}"
        
        data = {
            "code":          code,
            "client_id":     GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri":  redirect_uri,
            "grant_type":    "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=data)
            
            if token_response.status_code != 200:
                print(f"Token exchange failed: {token_response.text}")
                return RedirectResponse(url="/login?error=token_exchange_failed")
            
            token_data = token_response.json()
            
            if "id_token" not in token_data:
                print(f"No ID token in response: {token_data}")
                return RedirectResponse(url="/login?error=no_id_token")
            
            # Verify the ID token
            try:
                user_info = id_token.verify_oauth2_token(
                    token_data["id_token"], 
                    requests.Request(), 
                    GOOGLE_CLIENT_ID
                )
            except ValueError as e:
                print(f"Token verification failed: {e}")
                return RedirectResponse(url="/login?error=invalid_token")
            
            
            # Extract user info
            user_email          = user_info['email']
            email_verified      = user_info.get('email_verified', False)
            user_name           = user_info.get('name')
            user_name_last      = user_info.get('family_name')
            user_name_first     = user_info.get('given_name')
            user_picture        = user_info.get('picture')
            
            
            # Get client info
            viewport_width              = request.cookies.get('viewport_width', 0)
            viewport_height             = request.cookies.get('viewport_height', 0)
            ip_address                  = request.client.host
            

            
            # Create user data
            user_data = dm.DataUserLogin(
                email                   = user_email,
                name                    = user_name,
                name_last               = user_name_last,
                name_first              = user_name_first,
                
                viewport_width          = viewport_width,
                viewport_height         = viewport_height,
                ip_address              = ip_address, 
                
                login_social_media_id   = SOCIAL_MEDIA_GOOGLE,
                login_country_code      = None,
                login_country_name      = None,
                login_city              = None,
                login_region            = None
            )
            
            
            # Login/create user
            res_login = model['user'].register_or_login(user_data)
            if res_login is None:
                return RedirectResponse(url="/login?error=login_failed")
            
            
            # Get user_id and account info
            user_id = res_login['user']['id']
            data_user_account = get_user_account_info(user_id)
            
            
            # Replace the user block
            del res_login['user']
            
            
            # With this block
            res_login['user_account'] = data_user_account
            replace_plain_ids_user_account(data_user_account)

            
            # Create JWT token
            user_hid = data_user_account['user']['user']['hid']
            access_token = create_access_token(data={"uhid": user_hid})
            
            
            
            # ✅ FIXED: Create HTML response with script
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Redirecting...</title>
            </head>
            <body>
                <script>
                    // Store tokens in localStorage
                    localStorage.setItem('access_token', '{access_token}');
                    localStorage.setItem('user_picture', '{user_picture}');
                    
                    // Also set cookie for server-side auth (optional, can be removed)
                    document.cookie = "access_token={access_token}; path=/; max-age=" + 60*60*24*7;
                    
                    // Redirect to home page
                    window.location.href = '/login';
                </script>
                <p>Redirecting to home page...</p>
            </body>
            </html>
            """
            
            # Return the HTML response
            return HTMLResponse(content=html_content)
    
    except Exception as e:
        print(f"Google callback error: {e}")
        import traceback
        traceback.print_exc()
        return RedirectResponse(url=f"/login?error={str(e)}")    




@app.get("/auth/google/login")
async def google_login(request: Request):
    """
    Initiate Google OAuth login flow
    """
    encoded = urlencode({
                'client_id': GOOGLE_CLIENT_ID,
                'redirect_uri': f"{str(request.base_url).rstrip('/')}{GOOGLE_REDIRECT_URI}",
                'response_type': 'code',
                'scope': 'email profile openid',
                'access_type': 'offline',
                'prompt': 'consent'
            })
            
    # Store viewport dimensions in cookies for later use
    response = RedirectResponse(
        url=f"https://accounts.google.com/o/oauth2/v2/auth?{encoded}"
    )
    
    # Store viewport dimensions if passed as query params
    if request.query_params.get('viewport_width'):
        response.set_cookie(
            key="viewport_width",
            value=request.query_params.get('viewport_width'),
            max_age=60,  # Short-lived, just for the callback
            httponly=True
        )
    if request.query_params.get('viewport_height'):
        response.set_cookie(
            key="viewport_height",
            value=request.query_params.get('viewport_height'),
            max_age=60,
            httponly=True
        )
    
    return response




# OLD CODE Before HTTPS
# DO NOT DELETE

@app.post("/api/auth/google")
async def google_auth(request: Request, token_data: dm.GoogleToken):
    print('\n\ngoogle_auth')
    
    user_info = None
    
    try:
        # Specify the CLIENT_ID of the app that accesses the backend
        # The id_token.verify_oauth2_token method verifies the token's signature, 
        # issuer, and audience (client_id)
        user_info = id_token.verify_oauth2_token(
            token_data.token, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        
        # Get user info from token
        
        """
        print(str(user_info))
        

        {'iss': 'https://accounts.google.com', 
        'azp': '466858490005-irmhmqrbnmtkmah0baa27sgorivueu6g.apps.googleusercontent.com', 
        'aud': '466858490005-irmhmqrbnmtkmah0baa27sgorivueu6g.apps.googleusercontent.com',
        'sub': '117290373613803383814', 
        'email': 'j2718wong@gmail.com', 
        'email_verified': True, 
        'nbf': 1772621501, 
        
        'name': 'Jack Wong', 
        'picture': 'https://lh3.googleusercontent.com/a/ACg8ocJZJVZm7hWU9R7IaVXPDedhyyx2C8wJz6AMZNDWXpT0CEU9cw=s96-c', 
        
        'given_name': 'Jack', 
        'family_name': 'Wong', 
        'iat': 1772621801, 
        'exp': 1772625401, 
        
        'jti': 'd3d598e78c4bad85419b46839b4d728da66facc4'}
        """
        
    except ValueError as e:
        # Invalid token
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception as e:
        print('google error = ' + str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    
    # Get User data
    user_email      = user_info['email']
    email_verified  = user_info['email_verified']  
    user_name       = user_info['name']         if 'name' in user_info else None 
    user_name_last  = user_info['family_name']  if 'family_name' in user_info else None
    user_name_first = user_info['given_name']   if 'given_name' in user_info else None
    
    user_picture    = user_info['picture']
    
    
    # Get browser info 
    browser_info                = get_browser_info(request)
    
    user_data.is_mobile         = 1 if browser_info['is_mobile'] else 0
    user_data.is_webview        = 1 if browser_info['is_webview'] else 0
    user_data.browser           = browser_info['browser']
    user_data.browser_version   = browser_info['browser_version']
    user_data.webview_platform  = browser_info['webview_platform']
    
    user_data.os                = browser_info['os']
    user_data.os_version        = browser_info['os_version']
    user_data.device            = browser_info['device']
    user_data.device_type       = browser_info['device_type'] 
    user_data.ip_address        = browser_info['ip_address']

    
    
    
    # This will create account or login
    user_data = dm.DataUserLogin(
        email                   = user_email,
                
        name                    = user_name,         
        name_last               = user_name_last,      
        name_first              = user_name_first,    
        
        viewport_width          = token_data.viewport_width, 
        viewport_height         = token_data.viewport_height,
    
    
        login_social_media_id   = SOCIAL_MEDIA_GOOGLE,
        
        login_country_code      = token_data.login_country_code,
        login_country_name      = token_data.login_country_name,
        login_city              = token_data.login_city,
        login_region            = token_data.login_region,
                
                
        is_mobile               = user_data.is_mobile,
        is_webview              = user_data.is_webview,      
        browser                 = user_data.browser,         
        browser_version         = user_data.browser_version, 
        webview_platform        = user_data.webview_platform,
                                
        os                      = user_data.os,              
        os_version              = user_data.os_version,      
        device                  = user_data.device,          
        device_type             = user_data.device_type,     
        ip_address              = user_data.ip_address
    )
    
    
    
    res_login = model['user'].register_or_login(user_data)
    if res_login == None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    
    # Get user_id
    user_id = res_login['user']['id']
    
    
    # Get user_account info
    data_user_account = get_user_account_info(user_id)
    

    
    # replace the user block
    del res_login['user']
    
    
    # with this block
    res_login['user_account'] = data_user_account

    replace_plain_ids_user_account(data_user_account)

    
    # Get user_hid
    user_hid =  data_user_account['user']['user']['hid']
        
    
    
    
    # Create JWT token for the app
    access_token = create_access_token(
        data = {"uhid": user_hid}
    )
    
    
    # To be stored in client
    res_login['bearer_token'] = access_token
    res_login['user_picture'] = user_picture
    
    # tEST
    #background_tasks.add_task(send_email, ['j2718wong@gmail.com'],'login in app', 'Test message')
    
    return res_login
    


