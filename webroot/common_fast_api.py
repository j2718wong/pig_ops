# December 13, 2024
# Jack Wong (zhaoshan99@gmail.com)

from fastapi_offline            import FastAPIOffline
from fastapi                    import FastAPI, Depends, HTTPException, status
from fastapi.security           import HTTPBasicCredentials, HTTPBearer
from jose                       import jwt, JWTError


# Application secret key 
APP_SECRET_KEY = b'\xf2Pu\xcf\xbe\x88\x80\xac\x8e\xf1\xc6\xa7\xa4`Ae\x84\x10f\x9a|\xff\xe1r'

RELEASE_MODE_DEVELOPMENT    = 0
RELEASE_MODE_PRODUCTION     = 1


# If this is set to RELEASE_MODE_PRODUCTION authentication is needed in the API.
release_mode                = RELEASE_MODE_PRODUCTION



app = FastAPIOffline()


JWT_TOKEN_AUTHENTICATED             = 0
JWT_TOKEN_EXPIRED                   = 1
JWT_TOKEN_INVALID                   = 2
JWT_TOKEN_OTHER_ERROR               = 3
JWT_TOKEN_USER_UNAUTHORIZED         = 4
JWT_TOKEN_USER_INVALID              = 5



HTTP_RESPONSE_UNAUTHORIZED          = 401
HTTP_RESPONSE_METHOD_NOT_ALLOWED    = 405




def decode_auth_token(auth_token):
    """
    Decodes auth_token JWT token.
    
    Parameters
    ----------
    auth_token : str
        JWT token

    Returns
    -------
    tuple 
        Will return (user_data, JWT_TOKEN code)
    """
    try:
        payload = jwt.decode(auth_token, APP_SECRET_KEY)

        user = {
            'user_id':      payload['uid'],
            'user_flag':    -1,
            'login_id':     -1,
            'group_id':     -1,
            'group_flag':   -1,
        }

        key = 'uflg'
        if key in payload: user['user_flag']    = int(payload[key])

        key = 'ulid'
        if key in payload: user['login_id']     = int(payload[key])

        key = 'gid'
        if key in payload: user['group_id']     = int(payload[key])
        
        key = 'gflg'
        if key in payload: user['group_flag']   = int(payload[key])


        """
        user flags checking
        
        # User is using default password
        if user['user_flag'] & 1 != 0:
            return user, JWT_TOKEN_USER_UNAUTHORIZED
        
        # User is invalid
        if user['user_flag'] & 4 != 0:
            return user, JWT_TOKEN_USER_INVALID
        """
        return user, JWT_TOKEN_AUTHENTICATED


    except jwt.ExpiredSignatureError:
        return None, JWT_TOKEN_EXPIRED
    
    except jwt.InvalidTokenError:
        return None, JWT_TOKEN_INVALID
    
    return None, JWT_TOKEN_OTHER_ERROR



def check_authorization(bearer_token = None, request = None):
    """
    Will check authorization token; will return a tuple.

    if Authorization and Token are valid:
    
    """
    
    if request is not None:
        """
        This is provided in case request object is passed.
        """
    
        auth_header = request.headers.get('Authorization')
        
        if auth_header is None:
            # Optional authentication if is_development_mode > 0
            if release_mode == RELEASE_MODE_DEVELOPMENT:
                return None, JWT_TOKEN_AUTHENTICATED
                
            response = {'error': 'AUTHORIZATION_NONE'}
            return response, HTTP_RESPONSE_UNAUTHORIZED

        
        #  auth_header is not None here
        items       = auth_header.split(' ')
        if len(items) != 2:
            response = {'error': 'AUTHORIZATION_INVALID'}
            return response, HTTP_RESPONSE_UNAUTHORIZED


        token       = items[1]
    
    else:
        token       = bearer_token
        
        if token is None:
            # Optional authentication if is_development_mode > 0
            if release_mode == RELEASE_MODE_DEVELOPMENT:
                return None, JWT_TOKEN_AUTHENTICATED
                
            response = {'error': 'AUTHORIZATION_NONE'}
            return response, HTTP_RESPONSE_UNAUTHORIZED
    
    
    result      = decode_auth_token(token)

    if result[1] == JWT_TOKEN_AUTHENTICATED:
        return result[0], JWT_TOKEN_AUTHENTICATED
    
    
    response = {'error': ''}
    if result[1] == JWT_TOKEN_EXPIRED:
        response = {'error': 'JWT_TOKEN_EXPIRED'}


    if result[1] == JWT_TOKEN_INVALID:
        response = {'error': 'JWT_TOKEN_INVALID'}

    if result[1] == JWT_TOKEN_OTHER_ERROR:
        response = {'error': 'JWT_TOKEN_OTHER_ERROR'}

    if result[1] == JWT_TOKEN_USER_UNAUTHORIZED:
        response = {'error': 'JWT_TOKEN_USER_UNAUTHORIZED'}

    if result[1] == JWT_TOKEN_USER_INVALID:
        response = {'error': 'JWT_TOKEN_USER_INVALID'}

    return response, HTTP_RESPONSE_UNAUTHORIZED


