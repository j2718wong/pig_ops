# December 17, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


def remove_database_null_description(database_result):
    if 'desc' in database_result['result']:
        if database_result['result']['desc'] is not None:
            if len(database_result['result']['desc']) == 0:
                del database_result['result']['desc']
        else:
            del database_result['result']['desc']


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
    
    

def clean_data_user_account(user_account):
    # Clean user
    cur_id      = user_account['user']['user']['id']
    cur_hid     = hashids_user.encrypt(cur_id)
    
    del user_account['user']['user']['id']
    user_account['user']['user']['hid']   = cur_hid

    del user_account['user']['user']['account_id']
    
    user_pig_farms = user_account['user']['pig_farms']
    
    farm_hash_ids = [hashids_common.encrypt(cur_id) for cur_id in user_pig_farms]
    user_account['user']['pig_farms'] = farm_hash_ids
    
    
    # Clean account
    cur_id      = user_account['account']['account']['id']
    cur_hid     = hashids_account.encrypt(cur_id)
    
    del user_account['account']['account']['id']
    user_account['account']['account']['hid']   = cur_hid
    
    
    account_pig_farms = user_account['account']['pig_farms']
    
    
    for cur_entry in account_pig_farms:
        cur_id      = cur_entry['pig_farm']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_farm']['id']
        cur_entry['pig_farm']['hid']   = cur_hid
    
        get_location_address_names_and_replace_ids(cur_entry)
        
    return user_account


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
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del data['location']['address']['level_1']['id']
    data['location']['address']['level_1']['hid']   = cur_hid

    
    cur_id      = data['location']['address']['level_2']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del data['location']['address']['level_2']['id']
    data['location']['address']['level_2']['hid']   = cur_hid


    cur_id      = data['location']['address']['level_3']['id']
    if cur_id is not None and cur_id > 0:
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del data['location']['address']['level_3']['id']
        data['location']['address']['level_3']['hid']   = cur_hid


