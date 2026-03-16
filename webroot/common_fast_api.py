# December 13, 2024
# Jack Wong (zhaoshan99@gmail.com)

import os
from pathlib                    import Path
from dotenv                     import load_dotenv


from fastapi                    import FastAPI, Request, Depends, HTTPException, status
from fastapi.security           import HTTPBasicCredentials, HTTPBearer
from fastapi.responses          import RedirectResponse
from typing                     import Union

from fastapi.staticfiles        import StaticFiles

from fastapi.middleware.cors    import CORSMiddleware

from fastapi_throttle           import RateLimiter

from guard.middleware           import SecurityMiddleware
from guard.models               import SecurityConfig

from fastapi_mail               import FastMail, ConnectionConfig, MessageSchema, MessageType


from starlette.middleware.base  import BaseHTTPMiddleware



import mimetypes
import jwt
import secrets




# Add JavaScript MIME type if not already registered
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/javascript', '.js')



# Application secret key 
JWT_SECRET = 'MIdkgAL5GXSQO7D6nG9rYV9Xg3TQkQ4tkSlRn5V3gfT4yZF1-JWQO_-WXUVK_R7W'

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
    {"name": "Pig Details",     "description": "Pig Details related operation"},
    
    {"name": "Pig Production",  "description": "Pig Production related operations"},
    {"name": "Production Details",  "description": "Pig Production Details related operations"},
    
    {"name": "HashIds",         "description": "HashIds Testing"}
]

app = FastAPI(openapi_tags = tags_metadata)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
class CORPHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # These headers tell the browser to allow cross-origin resources
        response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        response.headers["Cross-Origin-Opener-Policy"] = "unsafe-none"
        return response

app.add_middleware(CORPHeaderMiddleware)
"""

# Add this exemption
# Your OAuth paths that should bypass security checks
OAUTH_PATHS = [
    "/auth/google/callback",
    "/auth/google/login",
    "/api/auth/google"  # If this endpoint receives callbacks
]

# 
config_security = SecurityConfig(
    # Manually block known bad IPs
    blacklist=["82.197.71.28"],  # Add that annoying bot
    
    # Auto-ban after suspicious behavior
    auto_ban_threshold=5,        # Ban after 5 suspicious requests
    auto_ban_duration=86400,      # Ban for 24 hours
    
    # Block common attack patterns
    enable_penetration_detection=False,
    
    # ✅ CRITICAL: Exempt OAuth paths from all security checks
    exempt_paths=OAUTH_PATHS,
    
    # ✅ Whitelist Google's user agents
    whitelist_user_agents=[
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Google-Cloud-Scheduler",
        "APIs-Google",
        "GoogleHC",
        "Google-OAuth-Client",
    ],
    
    # ✅ FIXED: Removed "Go-http-client" from blocked list
    blocked_user_agents=[
        "curl", 
        "wget", 
        "python-requests",
        # "Go-http-client"  ← REMOVED - Google uses this
    ],
    
    # Rate limiting
    rate_limit=100,
    
    # ❌ REMOVED ENTIRELY: block_cloud_providers
    # This was blocking all GCP IPs (including Google's callback servers)
    # block_cloud_providers={"AWS", "GCP", "Azure"},  ← DELETE THIS LINE
)

app.add_middleware(SecurityMiddleware, config=config_security)







JWT_ALGORITHM = "HS256"


# Try multiple possible locations for .env file
env_paths = [
    Path('.env'),  # current directory
    Path(__file__).parent / '.env',  # same as this file
    Path.home() / '.pig_ops_env' / '.env',  # user home directory
    Path('/etc/pig_ops/.env'),  # system config (for production)
]



# Load .env
env_loaded = False
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from: {env_path}")
        env_loaded = True
        break

if not env_loaded:
    print("Warning: No .env file found, using system environment variables")
    


# Signin Using Google configuration 
GOOGLE_CLIENT_ID        = "466858490005-irmhmqrbnmtkmah0baa27sgorivueu6g.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET    = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI     = '/auth/google/callback'


# This is in separate directory
FRONT_END_DIRECTORY = os.getenv('FRONT_END_DIRECTORY')


# JS bundles
dir_static = '%s/static' % FRONT_END_DIRECTORY
app.mount('/static', StaticFiles(directory=dir_static), name='static')


# New mobile first static directory
dir_static_m = '%s/src/static' % FRONT_END_DIRECTORY
app.mount('/static_m', StaticFiles(directory=dir_static_m), name='static_m')




# Public endpoint: 10 requests per minute per IP
public_limit = RateLimiter(
    times=10,        # 6 requests
    seconds=60,      # per minute
    trust_proxy=True, # Use X-Forwarded-For if behind proxy
    add_headers=True  # Show rate limit info in response headers
)


# More restrictive endpoint for sensitive operations
strict_limit = RateLimiter(
    times=4,
    seconds=60,
    add_headers=True
)



# Dependency function
def get_current_uhid(request: Request) -> str:
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        uhid = payload.get("uhid")
        
        if uhid is None:
            return None
            
        return uhid
        
    except jwt.ExpiredSignatureError:
        # You might want different behavior for API vs web endpoints
        return RedirectResponse(url="/login", status_code=302)
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )



def get_uhid_or_redirect(request: Request) -> Union[str, RedirectResponse]:
    """
    Returns uhid string if valid token, otherwise returns RedirectResponse to login.
    """
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Token"
        )
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        uhid = payload.get("uhid")
        
        if uhid is None:
            return RedirectResponse(url="/login", status_code=302)
            
        return uhid
        
    except jwt.ExpiredSignatureError:
        return RedirectResponse(url="/login", status_code=302)
        
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Token"
        )







ACCESS_TOKEN_EXPIRE_DAYS        = 300


def generate_csrf_token(data) -> str:
    """Generate a CSRF token"""
    # Create a unique token
    random_string = secrets.token_urlsafe(32)
    
    
    days_expiry = ACCESS_TOKEN_EXPIRE_DAYS
    
    if data:
        if 'days_expiry' in data:
            days_expiry = data['days_expiry']
    
    
    # Create JWT token
    payload = {
        "csrf_token": random_string,
        "exp": datetime.utcnow() + timedelta(days=days_expiry)
    }
    
    return jwt.encode(payload, APP_SECRET_KEY, algorithm=JWT_ALGORITHM)



def validate_csrf_token(token: str) -> bool:
    """Validate CSRF token"""
    try:
        # Decode and verify JWT
        payload = jwt.decode(token, APP_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return bool(payload.get("csrf_token"))
    except jwt.InvalidTokenError:
        return False






"""

# Email configuration
config_email = ConnectionConfig(
    MAIL_USERNAME="jsysdev.contact@gmail.com",
    MAIL_PASSWORD="ndjt lxmz dmby meip",  # Use app password for Gmail
    MAIL_FROM="no-reply@jsysdev.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Equivalent to MAIL_TLS=True in some versions
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

"""






# This is your required function signature
def send_email(recipient: str, subject: str, body: str):
    """
    Synchronous function that sends email to a single recipient
    This matches your required signature
    """
    # Create message
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],  # Single recipient as list
        body=body,
        subtype=MessageType.html
    )
    
    # Send email using FastMail (async) but run it synchronously
    fm = FastMail(config_email)
    
    # Run the async send_message in a synchronous context
    # Using asyncio.run() for a standalone async call
    try:
        # Get or create an event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # No event loop in current thread, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async function
        loop.run_until_complete(fm.send_message(message))
    except Exception as e:
        print(f"Error sending email: {e}")
        raise


