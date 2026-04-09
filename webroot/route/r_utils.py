# December 17, 2025
# Jack Wong

import os
import sys
import pprint


from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


# utils/browser_detector.py
import re
from typing import Dict, Tuple, Optional


class BrowserDetector:
    """Detect browser, OS, device and webview from User-Agent"""
    
    @staticmethod
    def parse_user_agent(user_agent: str) -> Dict:
        """Parse User-Agent string to get browser, OS, device info"""
        ua = user_agent.lower()
        result = {
            'browser':          'unknown',
            'browser_version':  None,
            'os':               'unknown',
            'os_version':       None,
            'device':           'unknown',
            'device_type':      'desktop',
            'is_mobile':        False,
            'is_webview':       False,
            'webview_platform': None,
            'user_agent':       user_agent[:500]  # Truncate for storage
        }
        
        # Detect browser
        if 'firefox' in ua:
            result['browser'] = 'firefox'
            version = re.search(r'firefox/(\d+)', ua)
            if version:
                result['browser_version'] = version.group(1)
        elif 'edg' in ua:
            result['browser'] = 'edge'
            version = re.search(r'edg/(\d+)', ua)
            if version:
                result['browser_version'] = version.group(1)
        elif 'chrome' in ua and not 'edg' in ua:
            result['browser'] = 'chrome'
            version = re.search(r'chrome/(\d+)', ua)
            if version:
                result['browser_version'] = version.group(1)
        elif 'safari' in ua and not 'chrome' in ua:
            result['browser'] = 'safari'
            version = re.search(r'safari/(\d+)', ua)
            if version:
                result['browser_version'] = version.group(1)
        
        # Detect OS
        if 'windows' in ua:
            result['os'] = 'windows'
            version = re.search(r'windows nt (\d+\.\d+)', ua)
            if version:
                result['os_version'] = version.group(1)
        elif 'mac os' in ua:
            result['os'] = 'macos'
            version = re.search(r'mac os x (\d+[._]\d+)', ua)
            if version:
                result['os_version'] = version.group(1).replace('_', '.')
        elif 'android' in ua:
            result['os'] = 'android'
            result['is_mobile'] = True
            version = re.search(r'android (\d+\.?\d*)', ua)
            if version:
                result['os_version'] = version.group(1)
        elif 'ios' in ua or 'iphone' in ua or 'ipad' in ua:
            result['os'] = 'ios'
            result['is_mobile'] = True
            version = re.search(r'os (\d+[._]\d+)', ua)
            if version:
                result['os_version'] = version.group(1).replace('_', '.')
        
        # Detect device type
        if 'mobile' in ua:
            result['device_type'] = 'mobile'
        elif 'tablet' in ua or 'ipad' in ua:
            result['device_type'] = 'tablet'
        
        # Detect specific device
        if 'iphone' in ua:
            result['device'] = 'iphone'
        elif 'ipad' in ua:
            result['device'] = 'ipad'
        elif 'android' in ua:
            if 'mobile' in ua:
                result['device'] = 'android_phone'
            else:
                result['device'] = 'android_tablet'
        
        # WebView detection
        webview_patterns = {
            'facebook': ['fban', 'fbav', 'fbsv', 'fb_iab', 'fb4a'],
            'instagram': ['instagram', 'ig_iab'],
            'twitter': ['twitter', 'tweet', 'tw_iab'],
            'tiktok': ['tiktok', 'musically'],
            'snapchat': ['snapchat'],
            'line': ['line', 'line/'],
            'wechat': ['wechat', 'micromessenger'],
            'messenger': ['messenger']
        }
        
        for platform, patterns in webview_patterns.items():
            for pattern in patterns:
                if pattern in ua:
                    result['is_webview'] = True
                    result['webview_platform'] = platform
                    break
        
        # Generic webview indicators
        if not result['is_webview']:
            generic = ['webview', 'wv', 'appbrowser']
            for g in generic:
                if g in ua:
                    result['is_webview'] = True
                    result['webview_platform'] = 'generic'
                    break
        
        
        # Set string limits
        if len(result['browser']) > 50:
            result['browser'] = result['browser'][0:50]
        
        if result['browser_version'] is not None and len(result['browser_version']) > 20:
            result['browser_version'] = result['browser_version'][0:20]
        
        if result['webview_platform'] is not None and len(result['webview_platform']) > 30:
            result['webview_platform'] = result['webview_platform'][0:30]
        
        if len(result['os']) > 50:
            result['os'] = result['os'][0:50]
        
        if result['os_version'] is not None and len(result['os_version']) > 20:
            result['os_version'] = result['os_version'][0:20]
        
        if len(result['device']) > 50:
            result['device'] = result['device'][0:50]
        
        if len(result['device_type']) > 20:
            result['device_type'] = result['device_type'][0:20]
        
        
        return result



from fastapi                import Request


def get_browser_info(request: Request) -> dict:
    """FastAPI dependency to get browser info from request"""
    
    # Get User-Agent
    user_agent = request.headers.get('user-agent', '')
    
    # Parse browser info
    browser_info = BrowserDetector.parse_user_agent(user_agent)
    
    # Add request-specific info
    browser_info['ip_address'] = request.client.host
    
    # Get forwarded IP if behind proxy
    forwarded = request.headers.get('x-forwarded-for')
    if forwarded:
        browser_info['ip_address'] = forwarded.split(',')[0].strip()
    
    
    return browser_info



def remove_database_null_description(database_result):
    if 'desc' in database_result['result']:
        if database_result['result']['desc'] is not None:
            if len(database_result['result']['desc']) == 0:
                del database_result['result']['desc']
        else:
            del database_result['result']['desc']


    if controller.is_prod_envi == True:
        if database_result['result']['num'] == 0:
            del database_result['result']['code']



def check_if_valid_user_account(user_id):
    res_user = model['user'].get_user_account_info(user_id)
    
    if res_user is None:
        inv_result = {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        return {
            'new_bill_hid': None,
            'inv_result':   inv_result
        }
        
        
        
    if res_user['user']['is_active'] == 0:
        inv_result = {
            'result':{
                'num':  ERROR_USER_INACTIVE,
                'code': 'ERROR_USER_INACTIVE'
            }
        }
        
        return {
            'new_bill_hid': None,
            'inv_result':   inv_result
        }
        
    
    if res_user['account']['is_enabled'] == 0:
        inv_result = {
            'result':{
                'num':  ERROR_ACCOUNT_DISABLED,
                'code': 'ERROR_ACCOUNT_DISABLED'
            }
        }
        
        return {
            'new_bill_hid': None,
            'inv_result':   inv_result
        }
    
    
    if res_user['account']['cur_bill_status_id'] == ACC_BILL_STATUS.OVERDUE:
        # remove plain id
        cur_id          = res_user['account']['cur_bill_id']
        cur_bill_hid    = hashids_common.encrypt(cur_id)
        
        
        inv_result = {
            'result':{
                'num':  ERROR_ACCOUNT_BILL_OVERDUE,
                'code': 'ERROR_ACCOUNT_BILL_OVERDUE',
                
                'due_bill_hid': cur_hid
            }
        }
    
        
        return {
            'new_bill_hid': None,
            'inv_result':   inv_result
        }
    
    
    
    new_bill_hid = None 
    
    if res_user['account']['cur_bill_status_id'] == ACC_BILL_STATUS.NEW:
        # remove plain id
        cur_id          = res_user['account']['cur_bill_id']
        new_bill_hid    = hashids_common.encrypt(cur_id)
    
    
    return {
        'new_bill_hid': new_bill_hid,
        'inv_result':   None
    }
    
    

def get_location_address_names_and_replace_ids(data):
    # Get location address names from a different database
    location_address = data['location']['address']
        
    level_1_id = location_address['level_1']['id']
    level_2_id = location_address['level_2']['id']
    level_3_id = location_address['level_3']['id']
    
    if level_3_id is None:
        level_3_id = 0
    
    
    cur_id      = data['location']['country']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del data['location']['country']['id']
    data['location']['country']['hid']   = cur_hid
    
    
    if 'geoloc' in data['location']:
        geoloc = data['location']['geoloc']
        if geoloc['latitude'] is None:
            del data['location']['geoloc']
        
    
    # Nothing to request; nothing to change
    if level_1_id == 0 and level_2_id == 0 and level_3_id == 0:
        return
    
    
    
    address_names = model_la['address_level'].get_address_level_names(
        address_level_1_id = level_1_id, 
        address_level_2_id = level_2_id,
        address_level_3_id = level_3_id
    )
    
    
    if address_names is not None:
        location_address['level_1']['name'] = address_names['level_1_name']
        location_address['level_2']['name'] = address_names['level_2_name']
        location_address['level_3']['name'] = address_names['level_3_name']
        
    
    
    
    cur_id      = data['location']['address']['level_1']['id']
    if cur_id == 0: 
        # No address at all; delete address 
        del  data['location']['address']['level_1']
        del  data['location']['address']['level_2']
        del  data['location']['address']['level_3']
        
        return
        
    
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del data['location']['address']['level_1']['id']
    data['location']['address']['level_1']['hid']   = cur_hid

    
    cur_id      = data['location']['address']['level_2']['id']
    if cur_id == 0:
        # No level 2 address
        del  data['location']['address']['level_2']
        del  data['location']['address']['level_3']
        
        return
        

    cur_hid     = hashids_common.encrypt(cur_id)
    
    del data['location']['address']['level_2']['id']
    data['location']['address']['level_2']['hid']   = cur_hid



    cur_id      = data['location']['address']['level_3']['id']
    if cur_id == 0:
        # No level 3 address
        del  data['location']['address']['level_3']
        
        return
        
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del data['location']['address']['level_3']['id']
    data['location']['address']['level_3']['hid']   = cur_hid

    
    
    

    


def replace_plain_ids_account(data):
    cur_id  = data['account']['id']
    cur_hid = hashids_account.encrypt(cur_id)
    
    del data['account']['id']
    data['account']['hid']   = cur_hid
    
    
    if 'pig_farms' in data:
        pig_farms = data['pig_farms']
        
        for cur_entry in pig_farms:
            cur_id  = cur_entry['pig_farm']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['pig_farm']['id']
            cur_entry['pig_farm']['hid']   = cur_hid
            
            
            get_location_address_names_and_replace_ids(cur_entry)
        

def replace_plain_ids_user_account(user_account):
    # Clean user
    cur_id      = user_account['user']['user']['id']
    cur_hid     = hashids_user.encrypt(cur_id)
    
    del user_account['user']['user']['id']
    user_account['user']['user']['hid']   = cur_hid

    del user_account['user']['user']['account_id']
    
    
    if 'user_request' in user_account['user']:
        cur_id      = user_account['user']['user_request']['id']
        cur_hid     = hashids_user.encrypt(cur_id)
    
        del user_account['user']['user_request']['id']
        user_account['user']['user_request']['hid'] = cur_hid
        
        
        cur_id      = user_account['user']['user_request']['account_id']
        cur_hid     = hashids_account.encrypt(cur_id)
    
        del user_account['user']['user_request']['account_id']
        user_account['user']['user_request']['account_hid'] = cur_hid
        
        
        
    
    if 'pig_farms' in user_account['user']:
        user_pig_farms = user_account['user']['pig_farms']
        
        farm_hash_ids = [hashids_common.encrypt(cur_id) for cur_id in user_pig_farms]
        user_account['user']['pig_farms'] = farm_hash_ids
        
    
    # Clean account
    if 'account' in user_account and user_account['account'] is not None:
        replace_plain_ids_account(user_account['account'])
        
    return user_account



PIG_PROD_FLAG_BIT_IS_A_GROUP        = 2


def replace_plain_ids_pig_production(cur_entry):
    # Replace plain_id
        
    cur_id  = cur_entry['pig_production']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['pig_production']['id']
    cur_entry['pig_production']['hid']   = cur_hid
    
    
    # 2026-04-09; it is possible to have a production with no sow;
    # - production entries combined to group
    # - piglets bought externally
    
    # Check if a Production Group
    cur_flag = 0
    
    if 'flag' in cur_entry['pig_production']:
        cur_flag = cur_entry['pig_production']['flag']


    if cur_flag & PIG_PROD_FLAG_BIT_IS_A_GROUP > 0:
        # Delete sow information at all;
        del cur_entry['sow']
        
        # Delete insemination info at all
        del cur_entry['insemination']
        
        return
        
        
    
    cur_id  = cur_entry['sow']['id']     
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['sow']['id']
    cur_entry['sow']['hid']   = cur_hid
    
    
    # If boar_id is None, delete whole boar block
    cur_id  = cur_entry['insemination']['boar']['id']
    if cur_id is None:
        del cur_entry['insemination']['boar']
        
        
        # If semen_supplier_id is None, delete whole semen_supplier block
        cur_id  = cur_entry['insemination']['ai']['semen_supplier']['id']
        if cur_id is None:
            del cur_entry['insemination']['ai']['semen_supplier']
        
            cur_id  = cur_entry['insemination']['ai']['internal_boar']['id']
            if cur_id is None:
                del cur_entry['insemination']['ai']['internal_boar']
            else:
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_entry['insemination']['ai']['internal_boar']['id']
                cur_entry['insemination']['ai']['internal_boar']['hid'] = cur_hid
        else:
            # encrypt semen_supplier.id
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['insemination']['ai']['semen_supplier']['id']
            cur_entry['insemination']['ai']['semen_supplier']['hid']   = cur_hid
            
            # encrypt semen_supplier.semen.id
            cur_id  = cur_entry['insemination']['ai']['semen_supplier']['semen']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['insemination']['ai']['semen_supplier']['semen']['id']
            cur_entry['insemination']['ai']['semen_supplier']['semen']['hid']   = cur_hid
            
            
        
    else:
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['insemination']['boar']['id']
        cur_entry['insemination']['boar']['hid']   = cur_hid
        
        
        # delete whole ai block
        del cur_entry['insemination']['ai']

    
    if 'insem_staff_id' in cur_entry['insemination']:
    
        cur_id  = cur_entry['insemination']['insem_staff_id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['insemination']['insem_staff_id']
        cur_entry['insemination']['insem_staff_hid']   = cur_hid


