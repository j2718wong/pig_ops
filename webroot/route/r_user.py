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
from server_messages        import *


import data_model           as dm



# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_utils                import replace_plain_ids_user_account

from r_a0_security_checks   import (check_if_valid_user_account,
                                    get_user_account_info)
                                    


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
async def user_register(user_data: dm.DataUserLogin):

    

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
    
    
@app.post("/user/login_social", tags=["User"])
async def user_login_social(request: Request, user_data: dm.DataUserLogin):
    
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
    
    
    # record client ip
    client_host = request.client.host
    
    # should port also be recorded?
    
    user_data.ip_address = client_host 
    
    
    
    res_login = model['user'].login_social(user_data)
    if res_login == None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Temporary encode user.id and user.account_id
    # Will put later in tokens
    
    user_id = res_login['user']['id']
    
    
    # Get user_account info
    data_user_account = get_user_account_info(user_id)
    
    
    pprint.pprint('login social data_user_account')
    pprint.pprint(data_user_account)
    
    # replace the user block
    del res_login['user']
    
    
    # with this block
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
            'num':  0,
            'code': 'SUCCESS'
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
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    




def create_access_token(data: dict):
    to_encode   = data.copy()
    expire      = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt





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
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
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
            client_host         = request.client.host
            viewport_width      = request.cookies.get('viewport_width', 0)
            viewport_height     = request.cookies.get('viewport_height', 0)
            
            # Create user data
            user_data = dm.DataUserLogin(
                email           = user_email,
                name            = user_name,
                name_last       = user_name_last,
                name_first      = user_name_first,
                viewport_width  = viewport_width,
                viewport_height = viewport_height,
                ip_address      = client_host,
                login_social_media_id   = SOCIAL_MEDIA_GOOGLE,
                login_country_code      = None,
                login_country_name      = None,
                login_city              = None,
                login_region            = None
            )
            
            # Login/create user
            res_login = model['user'].login_social(user_data)
            if res_login is None:
                return RedirectResponse(url="/login?error=login_failed")
            
            # Get user_id and account info
            user_id = res_login['user']['id']
            data_user_account = get_user_account_info(user_id)
            
            print('\n\nuser_id = %s' % user_id)
            
            # replace the user block
            del res_login['user']
            
            # with this block
            res_login['user_account'] = data_user_account
            replace_plain_ids_user_account(data_user_account)

            print('data_user_account')
            pprint.pprint(data_user_account)
            
            # Create JWT token
            user_hid = data_user_account['user']['user']['hid']
            print('user_hid = %s ' % user_hid)
            
            access_token = create_access_token(data={"uhid": user_hid})
            print('access_token = %s' % access_token)
            print('\n\n\n')
            
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
                    window.location.href = '/';
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


# NEW CODE Using HTTPS

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

@app.post("/api/auth/google")
async def google_auth(request: Request, token_data: dm.GoogleToken):
    
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
    
    # record client ip
    client_host = request.client.host
    
    # should port also be recorded?
    
    
    # This will create account or login
    user_data = dm.DataUserLogin(
        email                   = user_email,
                
        name                    = user_name,         
        name_last               = user_name_last,      
        name_first              = user_name_first,    
        
        viewport_width          = token_data.viewport_width, 
        viewport_height         = token_data.viewport_height,
        ip_address              = client_host,     
    
        login_social_media_id   = SOCIAL_MEDIA_GOOGLE,
        
        login_country_code      = token_data.login_country_code,
        login_country_name      = token_data.login_country_name,
        login_city              = token_data.login_city,
        login_region            = token_data.login_region      
    )
    
    
    
    res_login = model['user'].login_social(user_data)
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
    #background_tasks.add_task(send_email, 'j2718wong@gmail.com','login in app', 'Test message')
    
    return res_login
    


