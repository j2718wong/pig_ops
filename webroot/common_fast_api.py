# December 13, 2024
# Jack Wong (zhaoshan99@gmail.com)

from fastapi_offline            import FastAPIOffline
from fastapi                    import FastAPI, Depends, HTTPException, status
from fastapi.security           import HTTPBasicCredentials, HTTPBearer

from fastapi.staticfiles        import StaticFiles


# Application secret key 
APP_SECRET_KEY = b'\xf2Pu\xcf\xbe\x88\x80\xac\x8e\xf1\xc6\xa7\xa4`Ae\x84\x10f\x9a|\xff\xe1r'

RELEASE_MODE_DEVELOPMENT    = 0
RELEASE_MODE_PRODUCTION     = 1


# If this is set to RELEASE_MODE_PRODUCTION authentication is needed in the API.
release_mode                = RELEASE_MODE_PRODUCTION

tags_metadata = [
    {"name": "User",            "description": "User related operations"},

    {"name": "Common Lookup",   "description": "Common data related operations"},

    {"name": "Account",         "description": "Account related operations"},
    {"name": "Account Details", "description": "Account Details related operations"},
    {"name": "Location Address","description": "Location Address related operations"},
    
    {"name": "Pig Farm",        "description": "Pig Farm related operations"},
    
    {"name": "Sow Boar",        "description": "Sow Boar related operation"},
    
    {"name": "Pig Production",  "description": "Pig Production related operations"},
    {"name": "Production Details",  "description": "Pig Production Details related operations"},
    
    {"name": "HashIds",         "description": "HashIds Testing"}
]

app = FastAPIOffline(openapi_tags = tags_metadata)


dir_static = 'C:\\Users\\JackWong\\Downloads\\p\\pig_ops_ui\\pig_ops_app\\src\\static'
app.mount('/static', StaticFiles(directory=dir_static), name='static')




JWT_TOKEN_AUTHENTICATED             = 0
JWT_TOKEN_EXPIRED                   = 1
JWT_TOKEN_INVALID                   = 2
JWT_TOKEN_OTHER_ERROR               = 3
JWT_TOKEN_USER_UNAUTHORIZED         = 4
JWT_TOKEN_USER_INVALID              = 5



HTTP_RESPONSE_UNAUTHORIZED          = 401
HTTP_RESPONSE_METHOD_NOT_ALLOWED    = 405


