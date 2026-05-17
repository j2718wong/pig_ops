# January 5, 2026
# Jack Wong

import os
import sys
import time
import pprint

import aiohttp

import jwt

from fastapi                import Request, HTTPException, status, Depends, Response
from fastapi                import BackgroundTasks
from fastapi.responses      import HTMLResponse, RedirectResponse, FileResponse
from pydantic               import BaseModel


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


from r_utils                import (replace_plain_ids_user_account,
                                    get_browser_info)


from r_a0_security_checks   import get_user_account_info

from r_pig_production_get   import get_initial_farm_data_by_pig_farm_id


PIG_FARM_ADD_RES_NUM_SUCCESS        = 0

COMBINED_LACTATING_PIG_OPS  = (PIG_OPERATION_TYPE_LACTATING_PIGLETS, 
                                PIG_OPERATION_TYPE_LACTATING_SOW)


@app.get("/test123", response_class=HTMLResponse)
async def test_route(request: Request):
    print("=== TEST ROUTE CALLED ===")
    return HTMLResponse(content="<h1>TEST WORKS!</h1>")
    

@app.get("/manifest.json")
async def manifest():
    return FileResponse("manifest.json", media_type="application/json")



@app.get("/service_worker.js")
async def service_worker():
    return FileResponse("service_worker.js", media_type="application/javascript")


@app.get("/signup", response_class = HTMLResponse, dependencies=[Depends(strict_limit)])
@app.get("/login", response_class = HTMLResponse, dependencies=[Depends(strict_limit)])
async def signup_or_login(request: Request, response: Response):
    """
    Unified authentication page for both signup and login.
    The ManagerLogin JS class determines which mode to show based on URL path.
    """
    
    # Add cache control headers to prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    # Get current path (signup or login)
    current_path = request.url.path
    
    # Get language from query parameter first, then cookie, then default
    lang = request.query_params.get("lang")
    
    # If explicit language in URL, use it
    if lang:
        # Map to internal language code
        internal_lang = LANGUAGE_MAPPING.get(lang.lower(), 'en')
        
        # Set cookie
        response.set_cookie(key="user_lang", value=internal_lang, max_age=31536000, path="/")
    else:    
        # No explicit language - detect from cookie, browser, or country
        internal_lang = None
        
        # 1. Check cookie first
        cookie_lang = request.cookies.get("user_lang")
        if cookie_lang and cookie_lang in ['en', 'fil', 'ceb', 'zh']:
            internal_lang = cookie_lang
        
        # 2. Detect from browser Accept-Language header
        if not internal_lang:
            browser_lang = detect_browser_language(request)
            if browser_lang:
                internal_lang = browser_lang
        
        # 3. Detect from GeoIP country
        if not internal_lang:
            country_lang = await detect_country_language(request)
            if country_lang:
                internal_lang = country_lang
        
        # 4. Fallback to English
        if not internal_lang:
            internal_lang = 'en'
        
        
        # Map internal language to URL-friendly code
        url_lang_map = {
            'en': 'en',
            'fil': 'tag',
            'ceb': 'bis',
            'zh': 'zh'
        }
        url_lang = url_lang_map.get(internal_lang, 'en')
        
        
        # Redirect to language-specific URL (preserving signup/login path)
        # This ensures the URL reflects the detected language
        redirect_url = f"{current_path}?lang={url_lang}"
        return RedirectResponse(url=redirect_url, status_code=302)
    
    
    # Get translations
    translations = controller.get_public_pages_translations(internal_lang)
    
    # Remove page_home as this is not needed
    del translations['page_home']
    
    # Get available languages for dropdown
    available_languages = await get_available_languages(request, internal_lang)
    
    page = controller.view['signup'].render(
        lang=internal_lang,
        translations=translations,
        available_languages=available_languages
    )
    
    return page
    
    

@app.get("/logout", response_class = HTMLResponse, dependencies=[Depends(strict_limit)])
async def logout(response: Response):
    # Add cache control headers to prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    
    page = controller.view['signup'].render()
    
    return page
    


@app.get("/pig_farm/data")
async def pig_farm_data(request: Request):
    """
    2026-03-05 Notes:
    
    """
    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        # redirect to PAGE_NOT_FOUND
        raise HTTPException(status_code=401, detail="Invalid token")
        
    user_id = res[0]
    
    
    pig_farm_data = get_initial_farm_data_by_user_id(user_id)
    return pig_farm_data
    
    
def get_initial_farm_data_by_user_id(user_id):
    time_init = time.time()
    
    data_app = get_application_data()
    
    user_account = get_user_account_info(user_id)
    
    
    if user_account is None:
        data = {
            'application':          data_app,
            'user_account':         None,
            'initial_farm_data':    None
        }
        
        return {
            'result':{
                'num':  0
            },
            
            'data': data
        }
       
    

    
    account = user_account['account']
    user    = user_account['user']
    
    
    
    if account is None:
        
        data = {
            'application':          data_app,
            'user_account':         user_account,
            'initial_farm_data':    None
        }
        
        return {
            'result':{
                'num':  0
            },
            
            'data': data
        }
    
    
    
    pig_farm_id = 0
    
    # Get user assigned farm id
    # This is the first pig_farm id in user.pig_farms
    #
    # It is possible that the user has user_id, account_id but no farm_ids.
    # This is because the user did not finish adding a pig farm
    # in the Add Pig Farm page. Users can do this.
    user_pig_farms = None
    
    if 'pig_farms' in user:
        user_pig_farms =  user['pig_farms']
    else:
        print('\n\nuser has no pig farms; user_id = %s\n\n' % user_id)
    
    if user_pig_farms is not None and len(user_pig_farms) > 0:
        pig_farm_id = user_pig_farms[0]
    
    
    initial_farm_data = None

    if pig_farm_id > 0:  
        initial_farm_data = get_initial_farm_data_by_pig_farm_id(
            pig_farm_id, inc_pig_prod = 0, inc_user_audit = 1)
        
    
    data = {
        'application':          data_app,
        'user_account':         replace_plain_ids_user_account(user_account),
        'initial_farm_data':    initial_farm_data
    }
    
    
    time_final  = time.time()
    delta_secs  = time_final - time_init
    s_time      = '%.2f' % delta_secs
    
    
    return {
        'result':{
            'num':  0
        },
        
        'data': data
    }
    

@app.post("/pig_farm/data")
async def pig_farm_data_post(request: Request, user_data: dm.DataUserLogin):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        # redirect to PAGE_NOT_FOUND
        raise HTTPException(status_code=401, detail="Invalid token")
        
    user_id = res[0]
    

    
    pig_farm_data = get_initial_farm_data_by_user_id(user_id)
    

    
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
    
    
    # Update user_login
    model['user'].update_login(user_id, user_data)
    
    
    return pig_farm_data
    


@app.get("/app", response_class=HTMLResponse)
async def spa_dashboard(request: Request, lang: str = None):
    """
    SPA Dashboard - requires authentication
    Supports language parameter: /app?lang=bis
    """
    
    uhid = get_current_uhid(request)
    
    if not uhid:
        # No token, redirect to login with language
        redirect_lang = lang or request.cookies.get("user_lang", "en")
        url_lang_map = {'en': 'en', 'fil': 'tag', 'ceb': 'bis', 'zh': 'zh'}
        url_lang = url_lang_map.get(redirect_lang, 'en')
        return RedirectResponse(url=f"/login?lang={url_lang}", status_code=302)
    
    # Determine language (priority: URL param > cookie > default)
    if not lang:
        lang = request.cookies.get("user_lang", "en")
    
    # Map to internal language code
    internal_lang = LANGUAGE_MAPPING.get(lang.lower(), 'en')
    
    # Set cookie for future visits
    response = None
    
    # Get translation for SPA
    translation = controller.get_translation(internal_lang)
    
    # Get available languages for dropdown
    available_languages = await get_available_languages(request, internal_lang)
    
    # Render SPA
    page = controller.view['root'].render(
        uhid=uhid,
        translation=translation,
        lang=internal_lang,
        available_languages=available_languages
    )
    
    # Set language cookie if we have a response object
    if isinstance(page, HTMLResponse):
        page.set_cookie(key="user_lang", value=internal_lang, max_age=31536000, path="/")
    
    return page




@app.get("/{lang}", response_class=HTMLResponse, dependencies=[Depends(public_limit)])
async def root_with_lang(request: Request, lang: str):
    """
    Marketing homepage with language - always shows marketing content
    
    Handle homepage with language support
    
    Language codes supported:
    - English: en, english
    - Tagalog: fil, tag, tagalog, tl
    - Cebuano: ceb, bis, bisaya, cebuano
    - Chinese: zh, chinese # not yet implemented
    
    Handle homepage with language support
    
    SEO-friendly URLs:
    - /en - English
    - /tag - Tagalog  
    - /bis - Bisaya
    - /zh - Chinese
    
    Also supports ?lang= for backwards compatibility with SPA
    
    Language detection priority:
    1. Explicit URL language (/en, /tag, /bis, /zh)
    2. Cookie (user's saved preference)
    3. Browser Accept-Language header
    4. GeoIP country detection
    5. Fallback to English
    """
    
    print('went root_with_lang')

    
    # Map URL lang to internal language
    internal_lang = LANGUAGE_MAPPING.get(lang.lower(), 'en')
    
    # Set cookie
    response = None
    
    # Get available languages
    available_languages = await get_available_languages(request, internal_lang)
    
    # Always render marketing page (ignore token)
    page = controller.view['root'].render(
        uhid=None,  # Force no user
        translation=None,
        lang=internal_lang,
        available_languages=available_languages
    )
    
    # If we have a response object, set cookie
    if isinstance(page, HTMLResponse):
        page.set_cookie(key="user_lang", value=internal_lang, max_age=31536000, path="/")
    
    return page



@app.get("/", response_class=HTMLResponse, dependencies=[Depends(public_limit)])
async def root(request: Request):
    """Marketing homepage - always shows marketing content, never SPA"""
    
    print('went root')
    
    # Get language from cookie or detect
    internal_lang = request.cookies.get("user_lang", "en")
    
    # Get available languages
    available_languages = await get_available_languages(request, internal_lang)
    
    # Always render marketing page (ignore token)
    page = controller.view['root'].render(
        uhid=None,  # Force no user
        translation=None,
        lang=internal_lang,
        available_languages=available_languages
    )
    
    return page



def detect_browser_language(request: Request) -> str:
    """Detect language from browser Accept-Language header"""
    accept_lang = request.headers.get("Accept-Language", "")
    if not accept_lang:
        return None
    
    # Get primary language (e.g., "en-US,en;q=0.9" -> "en")
    primary = accept_lang.split(',')[0].split('-')[0].lower()
    
    # Map to supported languages
    lang_map = {
        'tl': 'fil',    # Tagalog
        'fil': 'fil',
        'ceb': 'ceb',
        'zh': 'zh',
        'en': 'en'
    }
    
    return lang_map.get(primary)



async def detect_country_language(request: Request) -> str:
    """Detect language from GeoIP country code"""
    # Get client IP (handle proxy headers)
    client_ip = request.headers.get("X-Forwarded-For")
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.client.host if request.client else None
    
    if not client_ip or client_ip.startswith('127.') or client_ip.startswith('192.168.'):
        return None  # Localhost or private IP
    
    try:
        # Use free API (consider caching results)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ipapi.co/{client_ip}/country/", timeout=aiohttp.ClientTimeout(total=2)) as resp:
                if resp.status == 200:
                    country_code = await resp.text()
                    country_code = country_code.strip()
                    
                    # Map country to language
                    country_map = {
                        'PH': 'fil',    # Philippines -> Tagalog
                        'CN': 'zh',     # China -> Chinese
                        'TW': 'zh',     # Taiwan -> Chinese
                        'HK': 'zh',     # Hong Kong -> Chinese
                        'SG': 'en',     # Singapore -> English
                        'MY': 'en',     # Malaysia -> English
                        'US': 'en',
                        'GB': 'en',
                        'AU': 'en',
                        'CA': 'en'
                    }
                    return country_map.get(country_code)
    except Exception as e:
        print(f"GeoIP detection failed: {e}")
        return None


# Define all possible languages
all_languages = [
    {'code': 'en', 'url': '/en', 'name': 'English', 'local_name': 'English'},
    {'code': 'fil', 'url': '/tag', 'name': 'Tagalog', 'local_name': 'Tagalog'},
    {'code': 'ceb', 'url': '/bis', 'name': 'Bisaya', 'local_name': 'Bisdak'}
]


    

default_languages =[
    {'code': 'en', 'url': '/en', 'name': 'English', 'local_name': 'English'}
]


# Optional: Add Chinese for international visitors
# default_languages = [
#     {'code': 'en', 'url': '/en', 'name': 'English', 'local_name': 'English'},
#     {'code': 'zh', 'url': '/zh', 'name': 'Chinese', 'local_name': '中文'}
# ]



async def get_available_languages(request: Request, internal_lang: str):
    """
    Return available language options based on user's country
    
    Parameters
    ----------
    internal_lang : string
        must be already normalized, via 
        internal_lang = LANGUAGE_MAPPING.get(lang.lower(), 'en')
    
    Returns
    -------
    list : Available language options with 'active' flag
    
    """
    
    country_code = None
    
    # Detect country from route, if user selected local language previously.
    # Hardcoded known local only in PH; 
    # will improve later for other countries with known multiple languages 
    if internal_lang in ('fil', 'ceb'):
        country_code = 'PH'
    
    
    # Detect country from other methods
    if country_code is None:
        country_code = await detect_country(request)
        
        print('detect_country(request) = %s' %country_code)
    
    
    # 2026-04-03; At this date, the marketing focus is in PH;
    # This may change in the future, when more countries are targeted. 
    #

    # Filter based on country - CREATE A NEW LIST (not a reference)
    if country_code == 'PH':
        # Philippines: Show all languages - create new dicts
        available_langs = []
        for lang in all_languages:
            available_langs.append({
                'code': lang['code'],
                'url': lang['url'],
                'name': lang['name'],
                'local_name': lang['local_name'],
                'active': False  # Start with False
            })
    else:
        # Other countries: Show only default languages - create new dicts
        available_langs = []
        for lang in default_languages:
            available_langs.append({
                'code': lang['code'],
                'url': lang['url'],
                'name': lang['name'],
                'local_name': lang['local_name'],
                'active': False
            })
    
    # Mark active language
    for lang in available_langs:
        if lang['code'] == internal_lang:
            lang['active'] = True
    
    
    return available_langs


async def detect_country(request: Request) -> str:
    # 1. Check CloudFlare header first (this is the fastest and most reliable)
    cf_country = request.headers.get("CF-IPCountry")
    if cf_country and cf_country != "XX":
        print(f'Country detected via CF header: {cf_country}')
        return cf_country

    # 2. Fallback to external API (only if CF header is missing or "XX")
    client_ip = request.headers.get("X-Forwarded-For")
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.client.host if request.client else None

    print(f'Falling back to API for IP: {client_ip}')

    if client_ip and not client_ip.startswith(('127.', '192.168.', '10.', '172.')):
        try:
            async with aiohttp.ClientSession() as session:
                # Use ipapi.co to get just the country code
                api_url = f"https://ipapi.co/{client_ip}/country/"
                async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=2)) as resp:
                    if resp.status == 200:
                        country = (await resp.text()).strip()
                        if country:
                            print(f'Country detected via API: {country}')
                            return country
        except Exception as e:
            print(f"API call failed: {e}")

    # 3. Ultimate fallback for local testing
    if client_ip and client_ip.startswith('127.'):
        print('Localhost detected, returning test country PH')
        return "PH"

    # 4. If everything fails
    print('Could not detect country, returning default XX')
    return "XX"





# List of suspicious patterns that should return 404
SUSPICIOUS_PATHS = [
    '.env', '.git', 'config', 'secret', 'backup', '.sql', '.ini',
    '.yml', '.yaml', '.xml', '.json', 'wp-admin', 'phpmyadmin',
    'api/.env', 'app/.env', 'admin', 'login', 'cgi-bin'
]


    
@app.get("/{full_path:path}", response_class=HTMLResponse, dependencies=[Depends(strict_limit)])
async def catch_all_frontend(request: Request, full_path: str = None):
    """
    This catches any route not matched above and serves the frontend
    """
    
    return HTMLResponse(content="<h1>404 - Page Not Found</h1>", status_code=404)
    
    # Check for suspicious paths that should not serve the app
    if full_path:
        full_path_lower = full_path.lower()
        for pattern in SUSPICIOUS_PATHS:
            if pattern in full_path_lower:
                # Return 404 for security scanners
                raise HTTPException(status_code=404, detail="Not found")
    
    # Also block dot files and hidden directories
    if full_path and full_path.startswith('.'):
        raise HTTPException(status_code=404, detail="Not found")
    
    
    result = get_current_uhid(request)
    if isinstance(result, RedirectResponse):
        return result
    
    uhid = result
    page = controller.view['root'].render(uhid)
    return page
