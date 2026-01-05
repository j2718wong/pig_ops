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


def get_user_account_info(user_id):
    data_user = model['user'].get_user_info(user_id)
    if data_user == None:
        # TODO what to do in case no result
        print('Error 1')
        return None
        
        
    # Get user.account_id 
    account_id = data_user['user']['account_id']
    
    
    
    
    # Get account info
    data_account = model['account'].get_info(account_id)
    if data_account == None:
        # TODO what to do in case no result
        print('Error 2')
        return None
        
        
    # TODO Check account free trial period
        
    # TODO check account for not paid bill
    
    result = {
        'user':     data_user,
        'account':  data_account
    }
    
    return result


def clean_data_user_account(user_account):
    # Clean user
    cur_id      = user_account['user']['user']['id']
    cur_hid     = hashids_user.encrypt(cur_id)
    
    del user_account['user']['user']['id']
    user_account['user']['user']['hid']   = cur_hid

    del user_account['user']['user']['account_id']
    
    user_pig_farms = user_account['user']['pig_farms']
    
    farm_hash_ids = [hashids_user.encrypt(cur_id) for cur_id in user_pig_farms]
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


