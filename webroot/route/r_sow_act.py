# December 16, 2024
# Jack Wong

import os
import sys
import pprint

from datetime               import datetime, timedelta 
from pydantic               import BaseModel
    
from common_constants       import *
from common_app             import *
from common_fast_api        import *

from fastapi.responses      import PlainTextResponse


RES_NUM_SUCCESS                         = 0



MONDAY                          = 0
TUESDAY                         = 1
WEDNESDAY                       = 2
THURSDAY                        = 3
FRIDAY                          = 4
SATURDAY                        = 5
SUNDAY                          = 6

s_day_week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']



DAY_1_STARTS_AT_BIRTH           = 1
NUMDAYS_SINCE_BIRTH_WEANING             = 45


@app.get("/sow_act/activities", response_class=PlainTextResponse)
async def sow_activities(ins_id:str = None, full_info: int = 0):
    """
    Will get latest coming sow activities.
    
    Parameters
    ----------
    ins_id:str
        comma separated string of ins_id(insemination_id); example 1,2
    
    full_info:int
        0 = will return minimum info older dates not return; 
        1 = will return full info

        
    """
    
    list_ins_id = []
    
    if ins_id is not None:
        items = ins_id.split(',')
        
        # reject invalid ins_id
        for cur_entry in items:
            try:
                cur_ins_id = int(cur_entry)
                list_ins_id.append(str(cur_ins_id)) # need to convert back to str
            except:
                test = 1
        
        if len(list_ins_id) == 0:
            res = model['sow_act'].get_latest_sow_activities(full_info)
        else:
            res = model['sow_act'].get_latest_sow_activities(full_info, 
                list_ins_id)
        
    else:
        res = model['sow_act'].get_latest_sow_activities(full_info)
    
    s = DB_INFO + '\n\n'
    
    s += 'INS_ID      Sow   Act_ID   Date             Num_Days  Activity               Description\n'
    
    last_ins_id = None
    
    
    for cur_entry in res:
        cur_ins_id = cur_entry['ins_id']
        
        line_count = 0
        for cur_act in cur_entry['activities']:
            
            cur_date    = datetime.strptime(cur_act['date'], '%Y-%m-%d')
            cur_day     = cur_date.weekday()
        
            if line_count == 0:
                s_temp      = str(cur_ins_id)
                num_chars   = len(s_temp)
                num_space   = 5 - num_chars
                s           += ' ' * num_space + s_temp
                s           += '   '
                
                
                s_temp      = str(cur_entry['sow_number'])
                num_chars   = len(s_temp)
                num_space   = 7 - num_chars
                s           += ' ' * num_space + s_temp
                s           += '   '
            
            else:
                s           += ' ' * 18
            
            
            s_temp      = str(cur_act['id'])
            num_chars   = len(s_temp)
            num_space   = 6 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '   '
            
            
            s_temp      = cur_act['date']
            s           += s_temp
            s           += '(' + s_day_week[cur_day] +')'
            s           += '   '
            
            
            
            if cur_act['days_ins'] is not None:
                s_temp      = str(cur_act['days_ins'])
                num_chars   = len(s_temp)
                num_space   = 6 - num_chars
                s           += ' ' * num_space + s_temp
                s           += '   '
            else:
                s           += '         '
            
            s_temp      = cur_act['activity']
            num_chars   = len(s_temp)
            num_space   = 20 - num_chars
            s           += s_temp + ' ' * num_space
            s           += '   '
            
            cur_date_2  = cur_act['date_2']
            
            if cur_date_2 is None:
                s_temp  = cur_act['desc']
            else:
                s_temp  = 'until ' + cur_date_2 + '; ' + cur_act['desc']
            s           += s_temp
            s           += '\n'
            
            line_count  += 1
        
        s           += '\n'
        
    return s
    
    
@app.get("/sow_act/pig_prod/list", response_class=PlainTextResponse)
async def sow_act_pig_prod_list(full_info: int = 0, is_active = 1, is_growing:int = 0, 
        is_harvested =0, year:int = None, sow = None):
    """
    Will get pig production list.

    Parameters
    ----------
    full_info : int
        if > 0, will include historical data per production cycle
        
    is_active : int
        if > 0, pig production with status gestating, lactating and weaning 
           will be returned
        
    is_growing : int
        if > 0, pig production with status growing, fattening, finishing will be returned

    is_harvested : int
        if > 0, pig production with status harvested will be returned
        
    
        
    """
    
    

    if full_info > 0:
        is_active = 0
    
    res = model['sow_act'].get_pig_prod_list(is_active, int(is_growing), 
            int(is_harvested), year, sow)
            
    
    culled_sows = []
    
    for cur_entry in res:
        if cur_entry['status_id'] == INS_STATUS_ID_TERMINATED:
            culled_sows.append(cur_entry['sow_number'])
            
    if len(culled_sows) > 0:
        res_sows = model['sow_act'].get_sow_list(culled_sows)
        
        for cur_entry in res:
            if cur_entry['status_id'] == INS_STATUS_ID_TERMINATED:
                for cur_sow in res_sows:
                    if cur_entry['sow_number'] == cur_sow['sow_number']:
                        cur_entry['date_culled'] = cur_sow['date_culled']
                        break
    
    s = DB_INFO + '\n\n'
    
    s += '       PIG PRODUCTION                                                                   Num baktin birth  Num baktin lutas\n'
    s += '=============================                                                           ----------------  ----------------\n'
    s += '    Sow  PROD_ID  PROD_Status   Date_TAKAL  Expected    Date_Birth  NumDays  Birth+45D   Dead    M    F    Dead    M    F   Date_Lutas  Baktin  Semilya\n'
    
    
    last_sow_number = None
    for cur_entry in res:
        
        date_birth  = cur_entry['date_actual_birth']
        
        
        if last_sow_number and last_sow_number != cur_entry['sow_number']:
            s           += '\n'
        
        s_temp      = str(cur_entry['sow_number'])
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        s_temp      = str(cur_entry['id'])
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        
        s_temp      = cur_entry['status']
        num_chars   = len(s_temp)
        num_space   = 12 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        s_temp      = cur_entry['date_ins']
        s           += s_temp 
        s           += '  '
        
        s_temp      = cur_entry['date_expected']
        s           += s_temp 
        s           += '  '
        
        
        if cur_entry['status_id'] == INS_STATUS_ID_TERMINATED:
            s_temp = 'girasyon or namatay'
            s           += s_temp 
            s           += '\n'
        
            last_sow_number = cur_entry['sow_number']
            continue
            
        
        if date_birth is not None:
            s_temp      = date_birth
            s           += s_temp 
            s           += '  '
        else:
            s           += ' ' * 12
        
        cur_days_actual = cur_entry['days_actual']
        if cur_days_actual is not None and cur_days_actual > 0:
            s_temp      = str(cur_days_actual)
            num_chars   = len(s_temp)
            num_space   = 7 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
        else:
            s           += ' ' * 10
            
            
        if date_birth is not None:
            
            dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')
            dt_birth_45 = dt_birth + timedelta(days=NUMDAYS_SINCE_BIRTH_WEANING- DAY_1_STARTS_AT_BIRTH) 
            
            s_temp      = dt_birth_45.strftime('%Y-%m-%d')
            s           += s_temp 
            s           += '  '
        else:
            s           += ' ' * 12
            
            
        num_piglets_birth = cur_entry['num_piglets_birth']
        num_dead        = num_piglets_birth['dead']
        num_male        = num_piglets_birth['male']
        num_female      = num_piglets_birth['female']
        
        if num_dead is not None:
            s_temp      = str(num_dead)
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
        else:
            s           += ' ' * 5
        
        if num_male is not None:
            s_temp      = str(num_male)
            num_chars   = len(s_temp)
            num_space   = 3 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
        else:
            s           += ' ' * 5
        
        if num_female is not None:
            s_temp      = str(num_female)
            num_chars   = len(s_temp)
            num_space   = 3 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
        else:
            s           += ' ' * 5
        
        
        num_piglets_birth = cur_entry['num_piglets_birth']
        num_dead        = num_piglets_birth['dead']
        num_male        = num_piglets_birth['male']
        num_female      = num_piglets_birth['female']
        
        num_piglets     = None
        if num_male is not None and num_female is not None:
            num_piglets = num_male + num_female
        
        
        s           += '  '
        
        if num_dead is not None:
            s_temp      = str(num_dead)
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
        else:
            s           += ' ' * 3
            
        if num_male is not None:
            s_temp      = str(num_male)
            num_chars   = len(s_temp)
            num_space   = 3 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
        else:
            s           += ' ' * 3
        
        if num_female is not None:
            s_temp      = str(num_female)
            num_chars   = len(s_temp)
            num_space   = 3 - num_chars
            s           += ' ' * num_space + s_temp
            s           += ' '
        else:
            s           += ' ' * 3
            
        s           += '  '
            
        if cur_entry['date_weaning'] is not None:
            s_temp      = cur_entry['date_weaning']
            s           += s_temp 
            s           += '  '
        else:
            s           += ' ' * 12
            
        
        s           += '  '
        
        if num_piglets is not None:
            s_temp      = str(num_piglets)
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
        
        else:
            s           += ' ' * 12
        
        
        s           += cur_entry['semen_desc']
            
        s           += '\n'
        
        last_sow_number = cur_entry['sow_number']
        
    return s

# Day 1 starts at date of birth

NUMDAYS_SINCE_BIRTH_INJECT_IRON_1       = 3
NUMDAYS_SINCE_BIRTH_INJECT_IRON_2       = 13
NUMDAYS_SINCE_BIRTH_INJECT_VITAMINS_1   = 14
NUMDAYS_SINCE_BIRTH_INJECT_VITAMINS_2   = 21
NUMDAYS_SINCE_BIRTH_KAPON               = 22
NUMDAYS_SINCE_BIRTH_INJECT_DEWORM_1     = 25
  
    
NUMDAYS_SINCE_BIRTH_BOOSTER             = 7
NUMDAYS_SINCE_BIRTH_PRESTARTER          = 30
NUMDAYS_SINCE_BIRTH_STARTER             = 50
NUMDAYS_SINCE_BIRTH_GROWER              = 90


PRODUCTION_FEEDS = [
    FEED_TYPE_ID_LACTATING,
    FEED_TYPE_ID_BOOSTER,
    FEED_TYPE_ID_PRESTARTER,
    FEED_TYPE_ID_STARTER,
    FEED_TYPE_ID_GROWER,
    FEED_TYPE_ID_FINISHER
]

    
@app.get("/pig_prod_ops/report", response_class=PlainTextResponse)
async def pig_prod_ops_report(uhid:str, pfhid:str, inc_historical: int =0, 
        inc_cost : int = 0, year:int = None):
    """
    Will generate pig_prod_ops report.

    Parameters
    ==========
       
    inc_historical : int
        if > 0, pig production with status lactating, growing, harvested, 
        close will be returned
    
    inc_cost : int
        if > 0, will include feeds cost
        
        
    """
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_OPS_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_PROD_OPS_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]
    
    
    res_get = model['user'].get_user_info(user_id)
    
    if res_get is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    account_id      = res_get['user']['account_id']
   
        
    res = model['sow_act'].get_pig_prod_ops_list(pig_farm_id, inc_historical)
    
    dt_now      = datetime.now()
    dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
    
    s = DB_INFO + '  ' + dt_now_s + '\n\n'
        
    s += write_gestating_operations(account_id, pig_farm_id)
    s += write_lactating_operations(res, inc_historical)
    s += write_feeding_guide(res, inc_historical)
    s += write_feeds_consumed(res, inc_historical)
    
    s += write_sow_boar_balance(pig_farm_id)
    
    if inc_cost > 0:
        s += write_feeds_cost(res, inc_historical)
    
    # Record analytics
    data = {
        'user_id': user_id,
        'app_function_id': APP_ANALYTICS_ID_REPORT_PIG_OPS
    }
    model['app_analytics'].add(data)
    
    return s
    
    
def write_gestating_operations(account_id, pig_farm_id):
    acc_pig_ops = model['account_pig_ops'].get_list(account_id, 
            PIG_OPERATION_TYPE_GESTATING)
    
    list_gestating  = model['sow_act'].get_gestating_operations_list(pig_farm_id)
    
    for cur_entry in list_gestating:
        cur_pig_prod_id = cur_entry['id']
        
        list_pig_ops  = model['pig_prod_pig_ops'].get_list(
            cur_pig_prod_id, PIG_OPERATION_TYPE_GESTATING
        )
        
        cur_entry['gestating_ops'] = list_pig_ops
        
        
    dt_now      = datetime.now()
        
    s  = 'GESTA OPERATIONS\n' 
    s += '=================\n'    
    s += 'PROD_ID  Sow           Date_TAKAL       Type  '
    
    
    max_chars_per_date_col = 15
    
    for cur_entry in acc_pig_ops:
        s_temp      = cur_entry['name']
        
        num_chars   = len(s_temp)
        if num_chars > max_chars_per_date_col:
            s_temp      = s_temp[0:max_chars_per_date_col]
            num_chars   = max_chars_per_date_col
            
        num_space   = max_chars_per_date_col - num_chars
        
        s += s_temp
        if num_space > 0:
            s += ' ' * num_space
            
        s += '  '
        
        
    s_temp      = 'DATE_Expected'
    num_chars   = len(s_temp)
    #num_space   = 12 - num_chars
    
    s +=        s_temp
    s += '\n'
    
    
    for cur_entry in list_gestating:
        
        s_temp      = str(cur_entry['farm_prod_id'])
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        
        sow_number  = cur_entry['sow_number']
        sow_name    = cur_entry['sow_name']
        s_temp      = sow_name if sow_name else sow_number 
        num_chars   = len(s_temp)
        num_space   = 12 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        
        date_insem  = cur_entry['date_insemination']
        dt_insem    = datetime.strptime(date_insem, '%Y-%m-%d')
        delta_d_now = (dt_now - dt_insem).days 
        
        if delta_d_now < 10: 
            num_space = 2
        elif delta_d_now < 100:
            num_space = 1
        else:
            num_space = 0
        
        spaces = num_space * ' '
        
        s_temp      = f'{date_insem}({spaces}{delta_d_now})'
        s           += s_temp 
        s           += '  '
        
        
        s_temp      = cur_entry['insem_type']
        num_chars   = len(s_temp)
        num_space   = 4 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        cur_gestating_ops = cur_entry['gestating_ops']
        
        for cur_gest_ops in cur_gestating_ops:
            cur_pig_prod_pig_ops = cur_gest_ops['pig_prod_pig_ops']
            
            cur_date_target = cur_pig_prod_pig_ops['date_target']
            cur_date_actual = cur_pig_prod_pig_ops['date_actual']
            
            if cur_date_actual is not None:
                
                dt_actual   = datetime.strptime(cur_date_actual, '%Y-%m-%d')
                delta_d     = (dt_actual - dt_insem).days 
                
                if delta_d < 10: 
                    num_space = 2
                elif delta_d < 100:
                    num_space = 1
                else:
                    num_space = 0
                
                spaces = num_space * ' '
                
                s_temp      = f'{cur_date_actual}({spaces}{delta_d})'
                s           += s_temp 
                s           += '  '
            
            else:
                s_temp      = f'{cur_date_target}(P)'
                num_chars   = len(s_temp)
                num_space   = max_chars_per_date_col - num_chars
                s           += s_temp + ' ' * num_space 
                s           += '  '
        
        
        s_temp      = cur_entry['date_expected']
        num_chars   = len(s_temp)
        num_space   = max_chars_per_date_col - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        s           += '\n'
        
        
        
    
    s += '\n\n'
    
    return s 
    
    
def write_lactating_operations(data, inc_historical):
    dt_now      = datetime.now()
    
    s  = 'BAKTIN OPERATIONS                        IRON_1   IRON_2   VITA_1   VITA_2    KAPON    PURGA_1   LUTAS\n'
    s += '=================      ADLAW GIKAN ANAK  '
    
    s_temp      = str(NUMDAYS_SINCE_BIRTH_INJECT_IRON_1)
    num_chars   = len(s_temp)
    num_space   = 6 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '

    s_temp      = str(NUMDAYS_SINCE_BIRTH_INJECT_IRON_2)
    num_chars   = len(s_temp)
    num_space   = 6 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '
    
    s_temp      = str(NUMDAYS_SINCE_BIRTH_INJECT_VITAMINS_1)
    num_chars   = len(s_temp)
    num_space   = 6 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '
    
    s_temp      = str(NUMDAYS_SINCE_BIRTH_INJECT_VITAMINS_2)
    num_chars   = len(s_temp)
    num_space   = 6 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '

    s_temp      = str(NUMDAYS_SINCE_BIRTH_KAPON)
    num_chars   = len(s_temp)
    num_space   = 6 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '

    
    s_temp      = str(NUMDAYS_SINCE_BIRTH_INJECT_DEWORM_1)
    num_chars   = len(s_temp)
    num_space   = 7 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '

    
    s_temp      = str(NUMDAYS_SINCE_BIRTH_WEANING)
    num_chars   = len(s_temp)
    num_space   = 6 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '

    
    s           += "\n\n"
    
    
    
    s += 'PROD_ID  Sow           Date_Birth       Baktin  Inject_IRON1   Inject_IRON2    InjVitamins1    InjVitamins2    Kapon           Purga           Date_Lutas \n'
     
    for cur_entry in data:
        pig_prod    = cur_entry['pig_prod']
        status_id   = pig_prod['status_id']
        
        if inc_historical == 0:
            if status_id != PROD_STATUS_ID_LACTATING:
                continue
        
        s_temp      = str(pig_prod['farm_prod_id'])
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        sow_number  = cur_entry['sow']['number']
        sow_name    = cur_entry['sow']['name']
        s_temp      = sow_name if sow_name else sow_number 
        num_chars   = len(s_temp)
        num_space   = 12 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        date_birth  = cur_entry['dates']['birth']
        dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')
        delta_d_now = (dt_now - dt_birth).days + DAY_1_STARTS_AT_BIRTH
        
        if delta_d_now < 10: 
            num_space = 2
        elif delta_d_now < 100:
            num_space = 1
        else:
            num_space = 0
        
        spaces = num_space * ' '
        
        s_temp      = f'{date_birth}({spaces}{delta_d_now})'
        s           += s_temp 
        s           += '  '
        
        num_pigs_current = pig_prod['num_pigs_current']
        
        s_temp      = str(num_pigs_current)
        num_chars   = len(s_temp)
        num_space   = 6 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        date_iron_1  = cur_entry['dates']['iron_1']
        delta_d_iron_1 = None
        if date_iron_1 is not None:
            dt_iron_1  = datetime.strptime(date_iron_1, '%Y-%m-%d')
            delta_d_iron_1 = (dt_iron_1 - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = f"{date_iron_1}({delta_d_iron_1})" 
            
        else:
            dt_iron_1  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_INJECT_IRON_1 - DAY_1_STARTS_AT_BIRTH)
            date_iron_1 = datetime.strftime(dt_iron_1, '%Y-%m-%d')
           
            s_temp      = f"{date_iron_1}(P)"
        
        num_chars   = len(s_temp)
        num_space   = 13 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        
        date_iron_2  = cur_entry['dates']['iron_2']
        delta_d_iron_2 = None
        if date_iron_2 is not None:
            dt_iron_2  = datetime.strptime(date_iron_2, '%Y-%m-%d')
            delta_d_iron_2 = (dt_iron_2 - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = f"{date_iron_2}({delta_d_iron_2})" 
            
        else:
            dt_iron_2  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_INJECT_IRON_2 - DAY_1_STARTS_AT_BIRTH)
            date_iron_2 = datetime.strftime(dt_iron_2, '%Y-%m-%d')
           
            s_temp      = f"{date_iron_2}(P)"
        
        num_chars   = len(s_temp)
        num_space   = 14 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        
        date_vitamins_1  = cur_entry['dates']['vitamins_1']
        delta_d_vitamins_1 = None
        if date_vitamins_1 is not None:
            dt_vitamins_1  = datetime.strptime(date_vitamins_1, '%Y-%m-%d')
            delta_d_vitamins_1 = (dt_vitamins_1 - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = f"{date_vitamins_1}({delta_d_vitamins_1})" 
            
        else:
            dt_vitamins_1  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_INJECT_VITAMINS_1 - DAY_1_STARTS_AT_BIRTH)
            date_vitamins_1 = datetime.strftime(dt_vitamins_1, '%Y-%m-%d')
           
            s_temp      = f"{date_vitamins_1}(P)"
        
        num_chars   = len(s_temp)
        num_space   = 14 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        
        date_vitamins_2  = cur_entry['dates']['vitamins_2']
        delta_d_vitamins_2 = None
        if date_vitamins_2 is not None:
            dt_vitamins_2  = datetime.strptime(date_vitamins_2, '%Y-%m-%d')
            delta_d_vitamins_2 = (dt_vitamins_2 - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = f"{date_vitamins_2}({delta_d_vitamins_2})" 
            
        else:
            dt_vitamins_2  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_INJECT_VITAMINS_2 - DAY_1_STARTS_AT_BIRTH)
            date_vitamins_2 = datetime.strftime(dt_vitamins_2, '%Y-%m-%d')
           
            s_temp      = f"{date_vitamins_2}(P)"
        
        num_chars   = len(s_temp)
        num_space   = 14 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        
        date_kapon  = cur_entry['dates']['kapon']
        delta_d_kapon = None
        if date_kapon is not None:
            dt_kapon  = datetime.strptime(date_kapon, '%Y-%m-%d')
            delta_d_kapon = (dt_kapon - dt_birth).days  + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = f"{date_kapon}({delta_d_kapon})"
            
        else:
            dt_kapon  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_KAPON - DAY_1_STARTS_AT_BIRTH)
            date_kapon = datetime.strftime(dt_kapon, '%Y-%m-%d')
           
            s_temp      = f"{date_kapon}(P)"
        
        num_chars   = len(s_temp)
        num_space   = 14 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        
        date_deworm_1  = cur_entry['dates']['deworm_1']
        delta_d_deworm_1 = None
        if date_deworm_1 is not None:
            dt_deworm_1  = datetime.strptime(date_deworm_1, '%Y-%m-%d')
            delta_d_deworm_1 = (dt_deworm_1 - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = f"{date_deworm_1}({delta_d_deworm_1})" 
            
        else:
            dt_deworm_1  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_INJECT_DEWORM_1 - DAY_1_STARTS_AT_BIRTH)
            date_deworm_1 = datetime.strftime(dt_deworm_1, '%Y-%m-%d')
           
            s_temp      = f"{date_deworm_1}(P)"
        
        num_chars   = len(s_temp)
        num_space   = 14 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        
        date_weaning  = cur_entry['dates']['weaning']
        delta_d_weaning = None
        if date_weaning is not None:
            dt_weaning  = datetime.strptime(date_weaning, '%Y-%m-%d')
            delta_d_weaning = (dt_weaning - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = f"{date_weaning}({delta_d_weaning})" 
            
        else:
            dt_weaning  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_WEANING - DAY_1_STARTS_AT_BIRTH)
            date_weaning = datetime.strftime(dt_weaning, '%Y-%m-%d')
           
            s_temp      = f"{date_weaning}(P)"
        
        num_chars   = len(s_temp)
        num_space   = 14 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        s+= '\n'
        
    
    s+= '\n\n'
    
    return s

    
def write_feeding_guide(data, inc_historical):
    dt_now      = datetime.now()
    
    
    s  = 'PROD FEEDING GUIDE                       BOOSTER   PSTARTER     LUTAS   STARTER    GROWER   FINISHER\n'
    s += '=====================   ADLAW GIKAN ANAK '
    
    s_temp      = str(NUMDAYS_SINCE_BIRTH_BOOSTER)
    num_chars   = len(s_temp)
    num_space   = 7 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '

    s_temp      = str(NUMDAYS_SINCE_BIRTH_PRESTARTER)
    num_chars   = len(s_temp)
    num_space   = 8 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '

    s_temp      = str(NUMDAYS_SINCE_BIRTH_WEANING)
    num_chars   = len(s_temp)
    num_space   = 7 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '
    
    s_temp      = str(NUMDAYS_SINCE_BIRTH_STARTER)
    num_chars   = len(s_temp)
    num_space   = 7 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '
    
    
    s_temp      = str(NUMDAYS_SINCE_BIRTH_GROWER)
    num_chars   = len(s_temp)
    num_space   = 7 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '

    s           += "\n\n"
    
    
    s += 'PROD_ID  PROD_Status   Date_Birth       Baktin  Date_Booster   Date_PreStarter  Date_Lutas      Date_Starter    Date_Grower     Date_Finisher   Date_Harvest\n'
    
    for cur_entry in data:
        pig_prod    = cur_entry['pig_prod']
        status_id   = pig_prod['status_id']
        
        if status_id == PROD_STATUS_ID_GESTATING:
            continue
        
        
        s_temp      = str(pig_prod['farm_prod_id'])
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        s_temp      = pig_prod['status']
        num_chars   = len(s_temp)
        num_space   = 12 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        date_birth  = cur_entry['dates']['birth']
        dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')


        # Dont compute pig numdays if already harvested or closed
        dt_final    = dt_now
        if status_id in (PROD_STATUS_ID_HARVESTED, PROD_STATUS_ID_CLOSED):
            date_harvest    = cur_entry['dates']['harvest']
            dt_harvest      = datetime.strptime(date_harvest, '%Y-%m-%d')
            dt_final        = dt_harvest
        
        delta_d = (dt_final - dt_birth).days + DAY_1_STARTS_AT_BIRTH
        
        if delta_d < 10: 
            num_space = 2
        elif delta_d < 100:
            num_space = 1
        else:
            num_space = 0
        
        spaces = num_space * ' '
        
        s_temp      = f'{date_birth}({spaces}{delta_d})'
        s           += s_temp 
        s           += '  '
        
        num_pigs_current = pig_prod['num_pigs_current']
        
        s_temp      = str(num_pigs_current)
        num_chars   = len(s_temp)
        num_space   = 6 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        date_booster  = cur_entry['dates']['booster']
        delta_d_booster = None
        if date_booster is not None:
            dt_booster  = datetime.strptime(date_booster, '%Y-%m-%d')
            delta_d_booster = (dt_booster - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = date_booster
            s           += s_temp
            s           += f"({delta_d_booster})"
            if delta_d_booster < 10:
                s       += '  '
            else:
                s       += ' '
        else:
            dt_booster  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_BOOSTER - DAY_1_STARTS_AT_BIRTH)
            date_booster = datetime.strftime(dt_booster, '%Y-%m-%d')
           
            s           += f"{date_booster}(P)"
            s           += '  '
            
            
        date_prestarter  = cur_entry['dates']['prestarter']
        if date_prestarter is not None:
            dt_prestarter  = datetime.strptime(date_prestarter, '%Y-%m-%d')
            numdays_delta = (dt_prestarter - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = date_prestarter
            s           += s_temp
            s           += f"({numdays_delta})"
            s           += '   '
        else:
            dt_prestarter  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_PRESTARTER - DAY_1_STARTS_AT_BIRTH)
            date_prestarter = datetime.strftime(dt_prestarter, '%Y-%m-%d')
           
            s           += f"{date_prestarter}(P)"
            s           += '    '
            
            
        date_weaning    = cur_entry['dates']['weaning']
        if date_weaning is not None:
            dt_weaning  = datetime.strptime(date_weaning, '%Y-%m-%d')
            numdays_delta = (dt_weaning - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = date_weaning
            s           += s_temp
            s           += f"({numdays_delta})"
            s           += '  '
        else:
            dt_weaning  = dt_birth + timedelta(days = NUMDAYS_SINCE_BIRTH_WEANING - DAY_1_STARTS_AT_BIRTH)
            date_weaning = datetime.strftime(dt_weaning, '%Y-%m-%d')
           
            s           += f"{date_weaning}(P)"
            s           += '  '
            
        
        date_starter    = cur_entry['dates']['starter']
        if date_starter is not None:
            dt_starter  = datetime.strptime(date_starter, '%Y-%m-%d')
            numdays_delta = (dt_starter - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = date_starter
            s           += s_temp
            s           += f"({numdays_delta})"
        else:
            s           += ' ' * 14
        
        s               += '  '
        
        date_grower     = cur_entry['dates']['grower']
        if date_grower is not None:
            dt_grower   = datetime.strptime(date_grower, '%Y-%m-%d')
            numdays_delta = (dt_grower - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = date_grower
            s           += s_temp
            s           += f"({numdays_delta})"
        else:
            s           += ' ' * 14
        s               += '  '
        
        
        date_finisher     = cur_entry['dates']['finisher']
        if date_finisher is not None:
            dt_finisher   = datetime.strptime(date_finisher, '%Y-%m-%d')
            numdays_delta = (dt_finisher - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = date_finisher
            s           += s_temp
            s           += f"({numdays_delta})"            
        else:
            s           += ' ' * 14
        s           += '  '
        
        date_harvest     = cur_entry['dates']['harvest']
        if date_harvest is not None:
            dt_harvest   = datetime.strptime(date_harvest, '%Y-%m-%d')
            numdays_delta = (dt_harvest - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = date_harvest
            s           += s_temp
            s           += f"({numdays_delta})"
            s           += '  '
        else:
            s           += ' ' * 14
        
        
        
        s+= '\n'
    
    s += '\n\n'
    
    return s
    
    
def _get_feed_buy(list_feed_buy, feed_type_id):
    """
    
    sample_list_feed_buy = 
    [{'feed_brand': {'id': 1, 'name': 'Promix'},
      'feed_buy': {'date_buy': '2025-09-10',
                   'dt_entry': '2025-09-10 20:05:49',
                   'id': 21,
                   'kg_per_unit': 50.0,
                   'kg_total': 250.0,
                   'quantity': 5,
                   'total_cost': 9250.0,
                   'unit_cost': 1850.0},
      'feed_supplier': {'id': 1, 'name': 'Arnel Sampan'},
      'feed_type': {'id': 5, 'name': 'STARTER'}}]
    """
    
    
    for cur_entry in list_feed_buy:
        if cur_entry['feed_type']['id'] == feed_type_id:
            return cur_entry
    
    return None
        
    

def write_feeds_consumed(data, inc_historical):
    dt_now      = datetime.now()
    
    s  = 'PROD FEEDS CONSUMED                                   LACTA            BOOSTER         PRE_STARTER         STARTER            GROWER          FINISHER    \n'
    s += '======================                           ===============   ===============   ===============   ===============   ===============   ===============\n'
    s += 'PROD_ID  PROD_Status   Date_Birth       Baktin   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT\n'
    
    
    total_num_piglets       = 0
    
    len_items   = len(PRODUCTION_FEEDS)
    feeds_left  = [0.0] * len_items
    
    
    for cur_entry in data:
        pig_prod    = cur_entry['pig_prod']
        status_id   = pig_prod['status_id']
        
        
        # Get feeds bought after last feed_balance
        
        pig_prod_id     = pig_prod['id']
        date_balance    = cur_entry['num_feeds']['date_balance']
        
        list_feed_bought = model['feed_buy'].get_list(pig_prod_id = pig_prod_id, 
                after_date = date_balance)
        

        s_temp      = str(pig_prod['farm_prod_id'])
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        s_temp      = pig_prod['status']
        num_chars   = len(s_temp)
        num_space   = 12 - num_chars
        s           += s_temp + ' ' * num_space 
        s           += '  '
        
        date_birth  = cur_entry['dates']['birth']
        
        
        if date_birth is not None:
            
            dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')
        
            # Dont compute pig numdays if already ahrvested or closed
            status_id   = pig_prod['status_id']
            dt_final    = dt_now
            if status_id in (PROD_STATUS_ID_HARVESTED, PROD_STATUS_ID_CLOSED):
                date_harvest    = cur_entry['dates']['harvest']
                dt_harvest      = datetime.strptime(date_harvest, '%Y-%m-%d')
                dt_final        = dt_harvest
            
            delta_d = (dt_final - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            if delta_d < 10: 
                num_space = 2
            elif delta_d < 100:
                num_space = 1
            else:
                num_space = 0
            
            spaces = num_space * ' '
            
            s_temp      = f'{date_birth}({spaces}{delta_d})'
            s           += s_temp         
            
        
        else:
            s += ' ' * 15

        s           += '  '
        
        
        if date_birth is not None:
            num_pigs_current = pig_prod['num_pigs_current']
             
            total_num_piglets += num_pigs_current
            
            s_temp      = str(num_pigs_current)
            num_chars   = len(s_temp)
            num_space   = 6 - num_chars
            s           += ' ' * num_space + s_temp
        
        else:
            s += ' ' * 6
        
        s           += '   '
        
        
        index = 0
        for cur_feed_type in PRODUCTION_FEEDS:
            res = _write_feed_consumed_type(cur_feed_type, 
                    cur_entry['num_feeds'], list_feed_bought)
            
            s += res[0]
            feeds_left[index] += res[1]
            index += 1
            
        
        s += '\n'
    
    s += '\n'
    
    
    s += '                              Nabilin'
    s += '   '
    
    s_temp      = str(total_num_piglets)
    num_chars   = len(s_temp)
    num_space   = 6 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '
    
    index = 0
    for cur_entry in feeds_left:
        if index != 1:
            s_temp   = f"{cur_entry:.1f}"
        else:
            s_temp  = str(cur_entry)
        num_chars   = len(s_temp)
        num_space   = 15 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '   '

    s += '\n\n'

    return s
    
        

def _write_feed_consumed_type(feed_type_id, data, list_feed_bought):
    s = ''
    
    if feed_type_id == FEED_TYPE_ID_LACTATING:
        data_feed_type = data['lactating']
    
    elif feed_type_id == FEED_TYPE_ID_BOOSTER:
        data_feed_type = data['booster']
        
    elif feed_type_id == FEED_TYPE_ID_PRESTARTER:
        data_feed_type = data['prestarter']
    
    elif feed_type_id == FEED_TYPE_ID_STARTER:
        data_feed_type = data['starter']
    
    elif feed_type_id == FEED_TYPE_ID_GROWER:
        data_feed_type = data['grower']
    
    elif feed_type_id == FEED_TYPE_ID_FINISHER:
        data_feed_type = data['finisher']
    
    
    balance_feeds = 0.0

    if data_feed_type is not None:
        num_bought  = data_feed_type['bought']
        
        if num_bought is not None and num_bought > 0:
            s_temp      = str(num_bought)
            num_chars   = len(s_temp)
            num_space   = 3 - num_chars
            s           += ' ' * num_space + s_temp
        else:
            # if num_bought is None, then consumed and left are also None; 
            # and not zero
            data_feed_type['consumed']  = None
            data_feed_type['left']      = None
            s       += '   '
            
        s           += '  '
        
        
        # New bought feeds after last feed balance date 
        new_bought_feeds = None
        feed_buy    = _get_feed_buy(list_feed_bought, feed_type_id)
        if feed_buy is not None:
            new_bought_feeds = feed_buy['feed_buy']['quantity']

                
        num_consumed  = data_feed_type['consumed']
        
        if num_consumed is not None and num_consumed > 0:
            if new_bought_feeds is not None:
                num_consumed = num_consumed - new_bought_feeds
                
            if feed_type_id != FEED_TYPE_ID_BOOSTER:
                s_temp      = f"{num_consumed:.1f}"
            else:
                s_temp      = str(num_consumed)
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
        else:
            s       += '    '
        
        s           += '  '
        
                    
        num_left        = data_feed_type['left']
        
        if new_bought_feeds is not None:
            if num_left is not None:
                num_left += new_bought_feeds
            else:
                num_left = new_bought_feeds
        
        if num_left is not None:
            balance_feeds    += num_left
            
            s_temp      = f"{num_left:.1f}"
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
        else:
            s       += '    '
            
    else:
        s           += 15 * ' '
        
    s           += '   '
        
        
    return s, balance_feeds
        

def write_feeds_cost(data, inc_historical):
    dt_now      = datetime.now()
    
    
    s  = 'FEEDS COST                                            LACTA            BOOSTER        PRE_STARTER         STARTER            GROWER          FINISHER    \n'
    s += '=================                                ===============   ===============   ===============   ===============   ===============  ===============\n'
    s += 'PROD_ID   Total_COST   Date_Birth       Baktin   BUY        COST   BUY        COST   BUY        COST   BUY        COST   BUY        COST  BUY        COST\n'
   
    
    for cur_entry in data:
            
        s_temp      = str(cur_entry['farm_prod_id'])
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        total_cost  = 0
        
        cost_feeds  = cur_entry['cost_feeds']
        
        cost_lactating  = cost_feeds['lactating']
        cost_booster    = cost_feeds['booster']
        cost_prestarter = cost_feeds['prestarter']
        cost_starter    = cost_feeds['starter']
        cost_grower     = cost_feeds['grower']
        cost_finisher   = cost_feeds['finisher']
        
        if cost_lactating is not None:
            total_cost  += cost_lactating
        
        if cost_booster is not None:
            total_cost  += cost_booster
        
        if cost_prestarter is not None:
            total_cost  += cost_prestarter
        
        if cost_starter is not None:
            total_cost  += cost_starter
        
        if cost_grower is not None:
            total_cost  += cost_grower
        
        if cost_finisher is not None:
            total_cost  += cost_finisher
            
        s_temp      = f"{total_cost:,.1f}"
        num_chars   = len(s_temp)
        num_space   = 11 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '   '
        
        
        date_birth  = cur_entry['dates']['birth']
        
        if date_birth is not None:
            dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')
            
            # Dont compute pig numdays if already ahrvested or closed
            status_id   = cur_entry['status_id']
            dt_final    = dt_now
            if status_id in (PROD_STATUS_ID_HARVESTED, PROD_STATUS_ID_CLOSED):
                date_harvest    = cur_entry['dates']['harvest']
                dt_harvest      = datetime.strptime(date_harvest, '%Y-%m-%d')
                dt_final        = dt_harvest
            
            delta_d = (dt_final - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            if delta_d < 10: 
                num_space = 2
            elif delta_d < 100:
                num_space = 1
            else:
                num_space = 0
            
            spaces = num_space * ' '
            
            s_temp      = f'{date_birth}({spaces}{delta_d})'
            s           += s_temp
            
        else:
            s += ' ' * 15
            
        s           += '  '
        
        
        if date_birth is not None:
            num_pigs_current = cur_entry['num_pigs_current']
            
            s_temp      = str(num_pigs_current)
            num_chars   = len(s_temp)
            num_space   = 6 - num_chars
            s           += ' ' * num_space + s_temp
            
        else:
            s += ' ' * 6
            
        s           += '   '
        
        
        num_lactating  = cur_entry['num_feeds']['lactating']
        if num_lactating is not None:
                
            num_bought  = num_lactating['bought']
            
            if num_bought is not None and num_bought > 0:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            s           += '  '
            
            if cost_lactating is not None:
                s_temp      = f"{cost_lactating:,.1f}"
                num_chars   = len(s_temp)
                num_space   = 10 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += ' ' * 10
        
        else:
            print(fid={cur_entry['id']})
            s           += 15 * ' '
            
        s           += '   '
        
        
        num_booster  = cur_entry['num_feeds']['booster']
        if num_booster is not None:
            
            num_bought  = num_booster['bought']
            
            if num_bought is not None and num_bought > 0:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
                
            s           += '  '
            
            if cost_booster is not None:
                s_temp      = f"{cost_booster:,.1f}"
                num_chars   = len(s_temp)
                num_space   = 10 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += ' ' * 10
            
        else:
            s           += 15 * ' '
        
        s           += '   '
            
        
        num_prestarter  = cur_entry['num_feeds']['prestarter']
        if num_prestarter is not None:
                
            num_bought  = num_prestarter['bought']
            
            if num_bought is not None and num_bought > 0:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            s           += '  '
            
            if cost_prestarter is not None:
                s_temp      = f"{cost_prestarter:,.1f}"
                num_chars   = len(s_temp)
                num_space   = 10 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += ' ' * 10
        
        else:
            s           += 15 * ' '
            
        s           += '   '
            
        
        num_starter  = cur_entry['num_feeds']['starter']
        if num_starter is not None:
                
            num_bought  = num_starter['bought']
            
            if num_bought is not None and num_bought > 0:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            
            s           += '  '
            
            if cost_starter is not None:
                s_temp      = f"{cost_starter:,.1f}"
                num_chars   = len(s_temp)
                num_space   = 10 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += ' ' * 10
        
        else:
            s           += 15 * ' '
            
        s           += '   '
            
        
        num_grower  = cur_entry['num_feeds']['grower']
        if num_grower is not None:
                
            num_bought  = num_grower['bought']
            
            if num_bought is not None and num_bought > 0:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            
            s           += '  '
            
            if cost_grower is not None:
                s_temp      = f"{cost_grower:,.1f}"
                num_chars   = len(s_temp)
                num_space   = 10 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += ' ' * 10
        
        else:
            s           += 9 * ' '
        
        s           += '   '
            
        
        num_finisher  = cur_entry['num_feeds']['finisher']
        if num_finisher is not None:
                
            num_bought  = num_finisher['bought']
            
            if num_bought is not None and num_bought > 0:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            
            s           += '  '
            
            if cost_finisher is not None:
                s_temp      = f"{cost_finisher:,.1f}"
                num_chars   = len(s_temp)
                num_space   = 10 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += ' ' * 10
        
        else:
            s           += 9 * ' '
        
        s           += '   '
        
        
        
        s+= '\n'

    return s
    


def write_sow_boar_balance(pig_farm_id):
    
    res = model['pig_farm'].get_sow_boar_balance(pig_farm_id)
    
    pprint.pprint(res)
    
    
    
    s  = 'SOW BOAR BALANCE       ===== SOW(ANAY) =====    BOAR     NON-PROD FEEDS\n'
    s += '                       GESTA   LACTA   TOTAL    TOTAL    GESTA  FINISHER\n'
    s += '==================     =====   =====   =====    =====    =====  =========\n'
    s += 'AS OF  '          
   
    
    s_temp      = res['date_balance']
    s           += s_temp
    s           += '      '
    
    
    s_temp      = str(res['sows']['num_gestating'])
    num_chars   = len(s_temp)
    num_space   = 5 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '
    
    s_temp      = str(res['sows']['num_lactating'])
    num_chars   = len(s_temp)
    num_space   = 5 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '
    
    
    s_temp      = str(res['sows']['total'])
    num_chars   = len(s_temp)
    num_space   = 5 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '    '
    
    
    s_temp      = str(res['boars'])
    num_chars   = len(s_temp)
    num_space   = 5 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '    '
    
    
    temp        = res['feed_balance']['num_gestating']
    s_temp      = f"{temp:.1f}"
    num_chars   = len(s_temp)
    num_space   = 5 - num_chars
    s           += ' ' * num_space + s_temp

    
    temp        = res['feed_balance']['num_finisher']
    if temp is not None:
        s_temp      = f"{temp:.1f}"
        num_chars   = len(s_temp)
        num_space   = 5 - num_chars
        s           += ' ' * num_space + s_temp
    
    s += '\n'
    
    return s