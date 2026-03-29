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

from fastapi.middleware.trustedhost     import TrustedHostMiddleware
from fastapi.middleware.httpsredirect   import HTTPSRedirectMiddleware



import mimetypes
import jwt
import secrets




# Add JavaScript MIME type if not already registered
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/javascript', '.js')



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
    



# Application secret key 
JWT_SECRET = 'MIdkgAL5GXSQO7D6nG9rYV9Xg3TQkQ4tkSlRn5V3gfT4yZF1-JWQO_-WXUVK_R7W'



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
    
    
    {"name": "Report",          "description": "Report generation"},
    
    {"name": "HashIds",         "description": "HashIds Testing"}
]


# Get APP_ENVI
app_envi = os.getenv('APP_ENVI', 'development')

app = FastAPI(
    openapi_tags    = tags_metadata,
    docs_url        = "/docs"           if app_envi == "development" else None,
    redoc_url       = "/redoc"          if app_envi == "development" else None,
    openapi_url     = "/openapi.json"   if app_envi == "development" else None
)





# Add this middleware to trust proxy headers
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Tell FastAPI to trust X-Forwarded-* headers from your proxy
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["jsysdev.com", "*.jsysdev.com", "localhost"]  # Add your domains
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Add this exemption
# Your OAuth paths that should bypass security checks
OAUTH_PATHS = [
    "/auth/google/callback",
    "/auth/google/login",
    "/api/auth/google"  # If this endpoint receives callbacks
]



# Security Guard
"""
# Disabled until potential warning IP spoof messages is solved

config_security = SecurityConfig(
    # Manually block known bad IPs
    blacklist=["82.197.71.28"],  # Add that annoying bot
    
    # Auto-ban after suspicious behavior
    auto_ban_threshold=5,        # Ban after 5 suspicious requests
    auto_ban_duration=86400,      # Ban for 24 hours
    
    
    
    # Trusted proxies (add your proxy IPs)
    trusted_proxies=[
        "127.0.0.1",
        "::1",
        "10.0.0.0/8",      # If using internal network
        "172.16.0.0/12",
        "192.168.0.0/16",
        "68.183.225.10",    # Your DigitalOcean IP (if needed)
    ],
    
    # Disable IP spoof detection entirely 
    disable_ip_spoof_detection=True,  # 
    

    
    
    # ✅ Explicitly disable IP security checks
    disable_checks=[
        "ip_security",
        "cloud_provider",
        "suspicious_activity",  # Might also include IP checks
    ],
    
    # ✅ Keep log level high
    log_level="CRITICAL",
    
    
    
    # ✅ ADD THIS: Disable spoof detection for trusted proxies
    disable_spoof_detection_for_trusted_proxies=True,
    
    
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


#app.add_middleware(SecurityMiddleware, config=config_security)
"""






JWT_ALGORITHM = "HS256"




# Signin Using Google configuration 

# This is the first Google Client ID used; working but the problem is cannot
# create token for sending email using port 443
# This project is from jsysdev.contact@gmail.com, SuperPig project 
# GOOGLE_CLIENT_ID        = "466858490005-irmhmqrbnmtkmah0baa27sgorivueu6g.apps.googleusercontent.com"


# 2026-03-20: New project created from jsysdev.contact@gmail.com, SuperPig2 project
GOOGLE_CLIENT_ID        = "528524387884-cgehid63a3k9813421ajctmf280p2o7c.apps.googleusercontent.com"
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
    times=12,        # 6 requests
    seconds=60,      # per minute
    trust_proxy=True, # Use X-Forwarded-For if behind proxy
    add_headers=True  # Show rate limit info in response headers
)


# More restrictive endpoint for sensitive operations
strict_limit = RateLimiter(
    times=8,
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






import asyncio

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
        subtype=MessageType.html,
        reply_to=["no-reply@jsysdev.com"] 
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



def get_application_data():
    return {
        "product_name":     "SuperPig",
        "contact_whatsapp": "+85260615575",
        "contact_email":    "jsysdev.contact@gmail.com",
        "privacy_officer":  "Jack Wong",
        "privacy_email":    "privacy@jsysdev.com",
        "website":          "https://superpig.jsysdev.com",
        
        
        "eu_privacy_officer":   "Richard Lee",
        "eu_privacy_email":     "eu-privacy@jsysdev.com",
        "eu_representrative":   "eu-rep-superpig@jsysdev.com",
        
        "rt_updates_enabled": 0
    }




import logging
import logging.handlers
import os
from pathlib import Path

# Setup logging with rotation
def setup_logging():
    # Create logs directory
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "superpig.log"
    
    # Rotating file handler - 10MB per file, keep 5 backups
    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,  # 10MB
        backupCount=5
    )
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    # Also log to console if needed
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger
    


"""
Note: There are two loggers
1.) The logger_main below is for the FastAPI logging.
2.) The common_app.logger is application logger only. will only log application
errors particulary database calls.

3.) The structure of the application logs is 

is like this

root@prod-pig-ops:~/projects/jsys/pig_ops/webroot/data/logs# ls -lt
total 20
drwxr-xr-x 2 root root 4096 Mar 18 01:32 2026-03-18
drwxr-xr-x 2 root root 4096 Mar 17 22:34 2026-03-16
drwxr-xr-x 2 root root 4096 Mar 17 01:33 2026-03-17
drwxr-xr-x 2 root root 4096 Mar 15 03:30 2026-03-15
drwxr-xr-x 2 root root 4096 Mar 14 03:09 2026-03-14



"""


    
    
# Call this at the start of your app
logger_main = setup_logging()
logger_main.info("SuperPig starting up...")

