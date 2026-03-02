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
    
    
    if res_user['account']['cur_bill_status_id'] == ACC_BILL_STATUS['OVERDUE']:
        # remove plain id
        cur_id          = res_user['account']['cur_bill_id']
        cur_hid         = hashids_common.encrypt(cur_id)
        
        
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
    
    if res_user['account']['cur_bill_status_id'] == ACC_BILL_STATUS['NEW']:
        # remove plain id
        cur_id          = res_user['account']['cur_bill_id']
        new_bill_hid    = hashids_common.encrypt(cur_id)
    
    
    return {
        'new_bill_hid': new_bill_hid,
        'inv_result':   None
    }
    
    

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

