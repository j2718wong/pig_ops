# August 10, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel
from fastapi.responses      import HTMLResponse

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


from fastapi.responses      import PlainTextResponse


import data_model           as dm


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description

from r_pig_medvac           import get_data_pig_medvac
from r_pig_prod_notes       import get_data_pig_prod_notes 
from r_sow_boar_mate        import get_data_sow_boar_mate_list


@app.get("/sow_boar", response_class = HTMLResponse, tags=["Sow Boar"])
async def sow_boar(pfhid:str = None):
    # Get the current logged in user;
    
    pig_farm_id = None
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            # Just proceed if it is invalid; will get default 
            # account farm_id if not given
            test = 1
            
            """
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID',
                    'desc': ''
                }
            }
            """
        else:
            pig_farm_id = res[0]
            
    
    # temporary
    user_id = 1
   
    res_user = model['user'].get_user_info(user_id)
    if res_user == None:
        # TODO what to do in case no result
        return None
        
        
    # Get user.account_id 
    account_id = res_user['user']['account_id']
    
    # Get account info
    data_account = model['account'].get_info(account_id)
    if data_account == None:
        # TODO what to do in case no result
        return None
        
        
    # TODO Check account free trial period
        
    # TODO check account for not paid bill
    
        
    # Check if there is a farm_id list
    account_farm_ids = data_account['farm_ids']
    len_items = len(account_farm_ids)
    if len_items == 0:
        # TODO what to do in case no farm set
        return None
        
    if pig_farm_id is not None:
        # This is given by user 
        
        if pig_farm_id not in account_farm_ids:
            # TODO what to do in case farm_id given is not in account list
            return None
    
    else:
        # select the first farm_id
        pig_farm_id = account_farm_ids[0]
        
    
    
    # Get pig_farm sow list
    list_sow_list = model['sow_boar'].get_list(pig_farm_id, 'F', 
        is_disposed = 0, inc_external = 0, inc_user_audit = 1, 
        minimum_info = 0, order_by = 0)
    if list_sow_list == None:
        # TODO what to do in case no result
        return None
    
    
    # Get pig_farm boar list
    list_boar_list = model['sow_boar'].get_list(pig_farm_id, 'M', 
        is_disposed = 0, inc_external = 1, inc_user_audit = 1, 
        minimum_info = 0, order_by = 0)
    if list_boar_list == None:
        # TODO what to do in case no result
        return None
    

    for cur_entry in list_sow_list:
        cur_id      = cur_entry['sow_boar']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['sow_boar']['id']
        cur_entry['sow_boar']['hid']   = cur_hid
    
    
    for cur_entry in list_boar_list:
        cur_id      = cur_entry['sow_boar']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['sow_boar']['id']
        cur_entry['sow_boar']['hid']   = cur_hid

    
    page_data = {
        'account':                  data_account,
        
        'sow_list':                 list_sow_list,
        'boar_list':                list_boar_list
      
    }
    

    page = controller.view['sow_boar'].render(page_data = json.dumps(page_data, indent=4))
    
    return page
    

    
    
    
@app.get("/sow_status/list", tags=["Sow Boar"])
async def sow_status_list(is_dispose: int = 0):
    """
    Will get sow status list.
    
    Parameters
    ----------

    """
    
    res = model['sow_boar'].get_sow_status_list()
    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    
@app.post("/sow_boar/add", tags=["Sow Boar"])
async def sow_boar_add(sow_boar_data: dm.DataSowBoar):
    uhid        = sow_boar_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_USER_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    pfhid       = sow_boar_data.pfhid
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID'
            }
        }
    
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
    
        return result
    
    pig_farm_id = res[0]
    
    
    number  = None
    name    = None
    
    sow_boar_number     = sow_boar_data.number
    if sow_boar_number is not None:
        number      = sow_boar_number.strip()
       
            
            
    sow_boar_name       = sow_boar_data.name
    if sow_boar_name is not None:
        name        = sow_boar_name.strip()
        
    
    if name is None and number is None:
        result = {
            'result':{
                'num':  ERROR_SOW_BOAR_NO_SOW_BOAR_NUMBER_OR_NAME,
                'code': 'ERROR_SOW_BOAR_NO_SOW_BOAR_NUMBER_OR_NAME'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
    
        return result
    
    
    parent_sow_id       = 0
    parent_sow_hid      = sow_boar_data.parent_sow_hid
    
    if parent_sow_hid is not None:
        res = hashids_common.decrypt(parent_sow_hid)
        
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_PARENT_SOW_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_PARENT_SOW_HASHID'
                }
            }
        
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
        
            return result
        
        parent_sow_id = res[0]
        
    
    parent_boar_id      = 0
    parent_boar_hid     = sow_boar_data.parent_boar_hid
    
    if parent_boar_hid is not None:
        res = hashids_common.decrypt(parent_boar_hid)
        
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_PARENT_BOAR_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_PARENT_BOAR_HASHID'
                }
            }
        
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
        
            return result
        
        parent_boar_id = res[0]
        
    
    
    sow_boar_data.user_id       = user_id
    sow_boar_data.pig_farm_id   = pig_farm_id
    sow_boar_data.parent_sow_id = parent_sow_id
    sow_boar_data.parent_boar_id= parent_boar_id
    sow_boar_data.number        = number
    sow_boar_data.name          = name
    
    
    res_add    =  model['sow_boar'].add(sow_boar_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    sow_boar_id     = res_add['sow_boar']['id']
    sow_boar_hid    = hashids_common.encrypt(sow_boar_id)
    
    del res_add['sow_boar']['id']
    res_add['sow_boar']['hid'] = sow_boar_hid
    
    
    # Add new_bill_hid
    if new_bill_hid is not None:
        res_add['result']['new_bill_hid'] = new_bill_hid
        
        
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
        
    return res_add
    

@app.post("/sow_boar/update", tags=["Sow Boar"])
async def sow_boar_update(sow_boar_data: dm.DataSowBoar):
    uhid        = sow_boar_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)
    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    sow_boar_hid    = sow_boar_data.sow_boar_hid
    res = hashids_common.decrypt(sow_boar_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_HASHID'
            }
        }
    
    sow_boar_id = res[0]
    
    
    
    parent_sow_id       = 0
    parent_sow_hid      = sow_boar_data.parent_sow_hid
    
    if parent_sow_hid is not None:
        res = hashids_common.decrypt(parent_sow_hid)
        
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_PARENT_SOW_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_PARENT_SOW_HASHID'
                }
            }
        
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
        
            return result
        
        parent_sow_id = res[0]
        
    
    parent_boar_id      = 0
    parent_boar_hid     = sow_boar_data.parent_boar_hid
    
    if parent_boar_hid is not None:
        res = hashids_common.decrypt(parent_boar_hid)
        
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_PARENT_BOAR_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_PARENT_BOAR_HASHID'
                }
            }
        
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
        
            return result
        
        parent_boar_id = res[0]
        
    
    
    
    sow_boar_data.user_id       = user_id
    sow_boar_data.sow_boar_id   = sow_boar_id
    sow_boar_data.parent_sow_id = parent_sow_id
    sow_boar_data.parent_boar_id= parent_boar_id
    
    
    
    res_update  =  model['sow_boar'].update(sow_boar_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
    
    # remove plain id
    clean_sow_boar_entry(res_update)
    
    
    # Add new_bill_hid
    if new_bill_hid is not None:
        res_update['result']['new_bill_hid'] = new_bill_hid
        
        
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    
    return res_update
    

@app.post("/sow_boar/dispose", tags=["Sow Boar"])
async def sow_boar_dispose(sow_boar_data: dm.DataSowBoarDispose):
    uhid        = sow_boar_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_USER_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)
    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    sow_boar_hid    = sow_boar_data.sow_boar_hid
    res = hashids_common.decrypt(sow_boar_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_HASHID'
            }
        }
    
    sow_boar_id = res[0]
    
    
    sow_boar_data.user_id       = user_id
    sow_boar_data.sow_boar_id   = sow_boar_id
    
    res_dispose     =  model['sow_boar'].dispose(sow_boar_data)
    
    if res_dispose is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
    
    # remove plain id
    sow_boar_id     = res_dispose['sow_boar']['id']
    sow_boar_hid    = hashids_common.encrypt(sow_boar_id)
    
    del res_dispose['sow_boar']['id']
    res_dispose['sow_boar']['hid'] = sow_boar_hid
        
    
    # Add new_bill_hid
    if new_bill_hid is not None:
        res_dispose['result']['new_bill_hid'] = new_bill_hid
        
        
    # Remove optional desc coming from database
    remove_database_null_description(res_dispose)
    
    
    
    return res_dispose


@app.get("/sow/pt_list", response_class=PlainTextResponse, tags=["Sow Boar"])
async def sow_pt_list(pfhid, full_info: int = 0):
    """
    Will get sow list.
    
    Parameters
    ----------
    
    full_info:int
        0 = will return active sows only; 
        1 = will return including culled sows

        
    """
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]
    
    res = model['sow_boar'].get_sow_list(pig_farm_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    s = DB_INFO + '\n\n'
        
    s += 'Sow_Num   Sow_Name     Date of Birth   SOW_Status   Date Culled   Notes\n'
    
   
    
    for cur_entry in res:
        
        if full_info == 0:
            if cur_entry['date_culled'] is not None:
                continue
        
        s_temp      = cur_entry['sow_number']
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '   '
    
    
        s_temp      = cur_entry['sow_name']
        num_chars   = len(s_temp)
        num_space   = 10 - num_chars
        s           += s_temp + ' ' * num_space
        s           += '   '
    
    
        s_temp      = cur_entry['date_of_birth']
        s           += s_temp
        s           += '      '
        
        
        s_temp      = cur_entry['status']
        num_chars   = len(s_temp)
        num_space   = 10 - num_chars
        s           +=  s_temp + ' ' * num_space
        s           += '   '
    
        
        s_temp      = '          '   
        if cur_entry['date_culled'] is not None:
            s_temp  = cur_entry['date_culled']
        s           += s_temp
        s           += '    '
        
        s_temp      = '          '
        if cur_entry['notes'] is not None:
            s_temp  = cur_entry['notes']
        s           += s_temp
        s           += '    '
        
        
        s           += '\n'
        
    return s
    


def clean_sow_boar_entry(cur_sow_boar_entry):
    cur_entry = cur_sow_boar_entry['sow_boar']
    
    cur_id  = cur_entry['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['id']
    cur_entry['hid']   = cur_hid


    if 'parent_sow_id' in cur_entry:
        cur_id  = cur_entry['parent_sow_id']
        if cur_id != None:
            cur_hid = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
        
        del cur_entry['parent_sow_id']
        cur_entry['parent_sow_hid']   = cur_hid

    
    if 'parent_boar_id' in cur_entry:
        cur_id  = cur_entry['parent_boar_id']
        if cur_id != None:
            cur_hid = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
        
        del cur_entry['parent_boar_id']
        cur_entry['parent_boar_hid']   = cur_hid


    if 'last_mate_sow_boar_id' in cur_entry:
        cur_id      = cur_entry['last_mate_sow_boar_id']
        if cur_id is not None:
            cur_hid     = hashids_common.encrypt(cur_id)
        else:
            cur_hid     = None
        
        del cur_entry['last_mate_sow_boar_id']
        cur_entry['last_mate_sow_boar_hid']   = cur_hid
            

            
def clean_sow_production_list(production_list):
    for cur_entry in production_list:
        cur_id  = cur_entry['pig_production']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_production']['id']
        cur_entry['pig_production']['hid']   = cur_hid

        
        if 'boar' in cur_entry['insemination']:
            cur_id  = cur_entry['insemination']['boar']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['insemination']['boar']['id']
            cur_entry['insemination']['boar']['hid']   = cur_hid

        
        if 'ai' in cur_entry['insemination']:
            if 'semen_supplier' in cur_entry['insemination']['ai']:
                cur_id  = cur_entry['insemination']['ai']['semen_supplier']['id']
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_entry['insemination']['ai']['semen_supplier']['id']
                cur_entry['insemination']['ai']['semen_supplier']['hid']   = cur_hid
            
                
                cur_id  = cur_entry['insemination']['ai']['semen_supplier']['semen']['id']
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_entry['insemination']['ai']['semen_supplier']['semen']['id']
                cur_entry['insemination']['ai']['semen_supplier']['semen']['hid']   = cur_hid
            
            
            else:
                cur_id  = cur_entry['insemination']['ai']['internal_boar']['id']
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_entry['insemination']['ai']['internal_boar']['id']
                cur_entry['insemination']['ai']['internal_boar']['hid']   = cur_hid




@app.get("/sow_boar/data_details", tags=["Sow Boar"])
async def sow_boar_data_details(sow_boar_hid, inc_user_audit:int = 0):
    res = hashids_common.decrypt(sow_boar_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_HASHID'
            }
        }
    
    sow_boar_id = res[0]
    
    # Get quick sow_boar data
    cur_sow_boar_data   = model['sow_boar'].get_entry(sow_boar_id)
    
    
    data_pig_medvac     = get_data_pig_medvac(sow_boar_id, 0, 0, 0)
    data_pig_prod_notes = get_data_pig_prod_notes(0, sow_boar_id, 0, 0, 0)
    
    
    data_health_issues  = []
    data_notes          = []
    
    for cur_entry in data_pig_prod_notes:
        if 'is_health_issue' in cur_entry['prod_notes']:
            data_health_issues.append(cur_entry)
        else:
            data_notes.append(cur_entry)
    
    
    
    data_output         = []
    data_gilt_ops       = []
    
    if cur_sow_boar_data['sex'] == 'F':
        # This will return a list
        res_sow_production = model['pig_prod'].get_production_output(
                sow_id = sow_boar_id)
        
        if res_sow_production and len(res_sow_production) == 1:
            production_list = res_sow_production[0]['production']
            clean_sow_production_list(production_list)
            data_output = production_list
            
            
        
        # Check if Gilt
        # Gilt if sow_status = SOW_STATUS_GROWING
        # get Gilt pig_prod_pig_ops
        operation_type = PIG_OPERATION_TYPE_GILT
        if cur_sow_boar_data['sow_status_id'] == SOW_STATUS_GROWING:
            res_gilt_ops = model['pig_prod_pig_ops'].get_list(operation_type, 
                sow_boar_id = sow_boar_id,
                inc_user_audit = 1, order_by = 0)
            
            data_gilt_ops = res_gilt_ops
    
    
    data_mates          = get_data_sow_boar_mate_list(sow_boar_id)
    
    
    data_mates_ext  = None
    if cur_sow_boar_data['sex'] == 'M':
        data_mates_ext  = get_data_sow_boar_mate_list(sow_boar_id, is_external = 1)
    
    
    data = {
        'sow_boar':         cur_sow_boar_data,
        'list_medvac':      data_pig_medvac,
        'list_health_issues': data_health_issues,
        'list_notes':       data_notes,
        'list_output':      data_output,
        'list_mates':       data_mates
    }
    
    if cur_sow_boar_data['sex'] == 'M':
        data['list_mates_ext'] = data_mates_ext
    
    
    if cur_sow_boar_data['sex'] == 'F':
        if cur_sow_boar_data['sow_status_id'] == SOW_STATUS_GROWING:
            data['list_gilt_ops'] = data_gilt_ops
    
    
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': data
    }

    


@app.get("/sow_boar/list", tags=["Sow Boar"])
async def sow_boar_list(pfhid:str, sex:str = None,
        is_disposed: int = 0, inc_user_audit:int = 0, order_by:int = 0):
    """
    Will get sow boar list.
    
    Parameters
    ----------
    pfhid:str
        pig farm hid; 
    
    
    sex: str
        F = sow entries
        M = boar entries
    
    is_disposed:int
        0 = will return active sows, boars only; 
        1 = will return disposed sows, boars
        

    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    order_by : int
            0 = ORDER BY date_of_birth DESC
            1 = ORDER BY name ASC

    """
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID'
            }
        }
    
    pig_farm_id = res[0]
    
    

    if is_disposed > 0:
        res = model['sow_boar'].get_list(pig_farm_id = pig_farm_id, is_disposed = 1)
    else:
        res = model['sow_boar'].get_list(pig_farm_id = pig_farm_id,
                sex = sex, inc_user_audit = inc_user_audit, order_by = order_by)
    
        if pig_farm_id > 0 and sex == 'F':
            list_sow_output_list = model['pig_prod'].get_production_output_group_per_sow(
                pig_farm_id);
    
            
            for cur_sow in res:
                cur_sow_id = cur_sow['sow_boar']['id']
                
                for cur_sow_output in list_sow_output_list:
                    if cur_sow_output['sow_id'] == cur_sow_id:
                        cur_sow['sow_boar']['num_births']       = cur_sow_output['num_births']
                        cur_sow['sow_boar']['num_pig_wean']     = cur_sow_output['num_pig_wean']
                        
                        break
                    
            
            
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # Replace plain id
    for cur_entry in res:
        clean_sow_boar_entry(cur_entry)

        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }


@app.get("/sow/piglets_output", tags=["Sow Boar"])
async def sow_production_output(sow_hid:str = None):
    """
    This will return number of piglets at weaning + currently lactating for a 
    given sow_hid.
    
    Parameters
    ----------
    sow_hid: str
        sow hash id
    
   

    """
    sow_id      = 0
    
    if sow_hid is not None:
        res = hashids_common.decrypt(sow_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_SOW_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_SOW_HASHID'
                }
            }
        
        sow_id = res[0]
    
    
    res = model['pig_prod'].get_production_output(sow_id = sow_id)
    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    production_list = []
    
    if len(res_sow_production) == 1:
        production_list = res[0]['production']
        clean_sow_production_list(production_list)    
    
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': production_list
    }
    

@app.get("/pig_farm/piglets_output", tags=["Sow Boar"])
async def sow_production_output(pfhid:str = None):
    """
    Will get pig farm piglets output list.
    This will return number of piglets at weaning + currently lactating.
    This includes both active sows and disposed sows.
            
    
    Parameters
    ----------
    pfhid: str
        pig_farm id
    
   

    """
    pig_farm_id = 0
    
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID'
                }
            }
        
        pig_farm_id = res[0]
    
    
    res = model['pig_prod'].get_production_output_group_per_sow(pig_farm_id)

    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['sow_id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['sow_id']
        cur_entry['sow_hid']   = cur_hid
        
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }


    
@app.get("/sow_boar/get_parent_trace", tags=["Sow Boar"])
async def sow_boar_get_parent_trace(sow_hid:str = None, boar_hid: str = None, pfhid:str = None):
    """
    Will get sow and boar parent trace from their birth_pig_prod_id.
    
    Note:
    1.) sow_boar entries that have a specified birth_pig_prod_id cannot
        update the parent_sow_id and parent_boar_id because the parent
        details is taken from pig_production.
        
    2.) The user can set the parent_sow_id and parent_boar_id if only 
        sow_boar.birth_pig_prod_id is NULL;
        
    3.) If either the given sow_hid or boar_hid has a user specified
        parent_sow_id and parent_boar_id, this function will still read
        the parents details from birth_pig_prod_id.
    
    Parameters
    ----------
    sow_hid: str
        sow hash id
    
    boar_hid: str
        boar hash id
    
    pfhid:str
        it is possible to parent trace all not disposed pigs in the farm 
    """
    
    sow_id = 0
    
    if sow_hid is not None:
        res = hashids_common.decrypt(sow_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_SOW_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_SOW_HASHID'
                }
            }
        
        sow_id = res[0]
    
    
    boar_id = 0
    
    if boar_hid is not None:
        res = hashids_common.decrypt(boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_SOW_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_SOW_HASHID'
                }
            }
        
        boar_id = res[0]
        
    
    pig_farm_id = 0
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_SOW_HASHID,
                    'code': 'ERROR_SOW_BOAR_INVALID_SOW_HASHID'
                }
            }
        
        pig_farm_id = res[0]
        
    
    
    res = model['sow_boar'].get_parent_trace(sow_id, boar_id, pig_farm_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['sow_boar']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['sow_boar']['id']
        cur_entry['sow_boar']['hid']   = cur_hid
        

        
        cur_id  = cur_entry['parent_sow']['id']
        if cur_id is not None:
            cur_hid = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
            
        del cur_entry['parent_sow']['id']
        cur_entry['parent_sow']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['parent_boar']['id']
        if cur_id is not None:
            cur_hid = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
        
        del cur_entry['parent_boar']['id']
        cur_entry['parent_boar']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['insemination']['sow_id']
        if cur_id is not None:
            cur_hid = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
        
        del cur_entry['insemination']['sow_id']
        cur_entry['insemination']['sow_hid']   = cur_hid
        
        
        
        if 'boar_id' in cur_entry['insemination']:
            cur_id  = cur_entry['insemination']['boar_id']
            if cur_id is not None:
                cur_hid = hashids_common.encrypt(cur_id)
            else:
                cur_hid = None
            
            del cur_entry['insemination']['boar_id']
            cur_entry['insemination']['boar_hid']   = cur_hid
        
        
        if 'ai_boar_id' in cur_entry['insemination']:
            cur_id  = cur_entry['insemination']['ai_boar_id']
            if cur_id is not None:
                cur_hid = hashids_common.encrypt(cur_id)
            else:
                cur_hid = None
            
            del cur_entry['insemination']['ai_boar_id']
            cur_entry['insemination']['ai_boar_hid']   = cur_hid
        
        
        if 'semen_supplier' in cur_entry['insemination']:
        
            cur_id  = cur_entry['insemination']['semen_supplier']['id']
            if cur_id is not None:
                cur_hid = hashids_common.encrypt(cur_id)
            else:
                cur_hid = None
            
            del cur_entry['insemination']['semen_supplier']['id']
            cur_entry['insemination']['semen_supplier']['hid']   = cur_hid
            
            
            cur_id  = cur_entry['insemination']['semen_supplier']['semen']['id']
            if cur_id is not None:
                cur_hid = hashids_common.encrypt(cur_id)
            else:
                cur_hid = None
            
            del cur_entry['insemination']['semen_supplier']['semen']['id']
            cur_entry['insemination']['semen_supplier']['semen']['hid']   = cur_hid
            
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
