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

PROD_STATUS_LACTATING           = 4


DAY_1_STARTS_AT_BIRTH           = 1
NUMDAYS_SINCE_BIRTH_WEANING             = 45


@app.get("/sow/list", response_class=PlainTextResponse)
async def sow_list(full_info: int = 0):
    """
    Will get sow list.
    
    Parameters
    ----------
    
    full_info:int
        0 = will return active sows only; 
        1 = will return including culled sows

        
    """
    
    res = model['sow_act'].get_sow_list()
        
    
    
        
    s = '    Sow   Date of Birth   SOW_Status   Date Culled   Comment\n'
    
   
    
    for cur_entry in res:
        
        if full_info == 0:
            if cur_entry['date_culled'] is not None:
                continue
        
        s_temp      = cur_entry['sow_number']
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
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
        if cur_entry['comment'] is not None:
            s_temp  = cur_entry['comment']
        s           += s_temp
        s           += '    '
        
        
        s           += '\n'
        
    return s
    
    
@app.get("/sow/operations", response_class=PlainTextResponse)
async def sow_operations(format= 0):
    res = model['sow_act'].get_sow_operations_list()
        
    
    
        
    s = '    Sow  SOW_Status  PROD_ID  Date_TAKAL   NormalKaon   CheckBuntis1    CheckBuntis2   BalhinDako   BalhinFarrow    Inject_IRON   Inject_PURGA \n'
    
   
    
    for cur_entry in res:
        
        
        s_temp      = cur_entry['sow_number']
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
    
        s_temp      = cur_entry['status_name']
        num_chars   = len(s_temp)
        num_space   = 10 - num_chars
        s           += s_temp
        s           += ' ' * num_space 
        s           += '  '
        
        if cur_entry['last_prod_id']: 
            s_temp      = str(cur_entry['last_prod_id'])
            num_chars   = len(s_temp)
            num_space   = 7 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
        else:
            num_sapce = 7
            s           += ' ' * num_space
            s           += '  '
        
        
        if cur_entry['date_insemination']: 
            s_temp      = cur_entry['date_insemination']
            num_chars   = len(s_temp)
            num_space   = 10 - num_chars
            s           += ' ' * num_space + s_temp
            s           += ' '
        else:
            num_sapce = 10
            s           += ' ' * num_space
            s           += ' '
        
        
        s           += '\n'
        
    return s
    
    

@app.get("/sow/activities", response_class=PlainTextResponse)
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
    
        
    s = 'INS_ID      Sow   Act_ID   Date             Num_Days  Activity               Description\n'
    
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
    
    
@app.get("/pig_prod/list", response_class=PlainTextResponse)
async def pig_prod_list(full_info: int = 0, is_active = 1, is_growing:int = 0, 
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
    
    s  = '       PIG PRODUCTION                                                                   Num baktin birth  Num baktin lutas\n'
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
        
        
        num_piglets_weaning = cur_entry['num_piglets_weaning']
        num_dead        = num_piglets_weaning['dead']
        num_male        = num_piglets_weaning['male']
        num_female      = num_piglets_weaning['female']
        
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

    
@app.get("/pig_prod/feeding", response_class=PlainTextResponse)
async def pig_prod_feeding(full_info: int = 0,   is_growing:int = 0, 
        is_harvested =0, inc_cost = 0, year:int = None):
    """
    Will get pig feeding list.

    Parameters
    ==========
    full_info : int
        if > 0, will include historical data per production cycle
    
       
    is_growing : int
        if > 0, pig production with status growing, fattening, finishing will be returned
    
    inc_cost : int
        if > 0, will include feeds cost
        
     is_harvested : int
        if > 0, pig production with status harvested will be returned
        
    """
    
    is_growing = int(is_growing)
        
    res = model['sow_act'].get_pig_prod_feeding_list(is_growing)
    
    s  = write_baktin_operations(res, is_growing)
    s += write_feeding_guide(res)
    s += write_feeds_consumed(res, inc_cost)
    
    return s
    
    
    
def write_baktin_operations(data, is_growing):
    dt_now      = datetime.now()
    dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
    
    
    s  = f'BAKTIN OPERATIONS      {dt_now_s}\n'
    s += '=================      IRON_1   IRON_2   VITA_1   VITA_2    KAPON   PURGA_1 \n'
    s += 'ADLAW GIKAN ANAK       '
    
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
    num_space   = 6 - num_chars
    s           += ' ' * num_space + s_temp
    s           += '   '
    
    s           += "\n\n"
    
    
    
    s += 'PROD_ID  Sow           Date_Birth       Baktin  Inject_IRON1   Inject_IRON2    InjVitamins1    InjVitamins2    Kapon           Purga           Date_Lutas \n'
     
    for cur_entry in data:
        if is_growing == 0:
            if cur_entry['status_id'] != PROD_STATUS_LACTATING:
                continue
        
        s_temp      = str(cur_entry['id'])
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
        
        num_piglets_weaning = cur_entry['num_piglets_weaning']
        num_piglets = num_piglets_weaning['male'] + num_piglets_weaning['female']
        
        s_temp      = str(num_piglets)
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

    
def write_feeding_guide(data):
    dt_now      = datetime.now()
    dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
    
    
    s  = f'FEEDING GUIDE          {dt_now_s}\n'
    s += '=================      BOOSTER   PSTARTER     LUTAS   STARTER    GROWER   FINISHER\n'
    s += 'ADLAW GIKAN ANAK       '
    
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
    
    
    s += 'PROD_ID  PROD_Status   Date_Birth       Baktin  Date_Booster   Date_PreStarter  Date_Lutas      Date_Starter    Date Grower  Date_Finisher\n'
    
    for cur_entry in data:
        
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
        
        num_piglets_weaning = cur_entry['num_piglets_weaning']
        num_piglets = num_piglets_weaning['male'] + num_piglets_weaning['female']
        
        s_temp      = str(num_piglets)
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
            s           += '  '
        else:
            s           += ' ' * 12
            
        
        date_grower     = cur_entry['dates']['grower']
        if date_grower is not None:
            dt_grower   = datetime.strptime(date_grower, '%Y-%m-%d')
            numdays_delta = (dt_grower - dt_birth).days + DAY_1_STARTS_AT_BIRTH
            
            s_temp      = date_grower
            s           += s_temp
            s           += f"({numdays_delta})"
            s           += '  '
        else:
            s           += ' ' * 12
        
        s+= '\n'
    
    s += '\n\n'
    
    return s
    

def write_feeds_consumed(data, inc_cost):
    dt_now      = datetime.now()
    dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
    
    
    s  = 'FEEDS CONSUMED            %s                                                               NUM SACKS\n' % dt_now_s
    s += '=================                                ========================================================================================================\n'
    s += '                                                      LACTA            BOOSTER        PRE_STARTER         STARTER            GROWER          FINISHER   \n'
    s += '                                                 ===============   ===============   ===============   ===============   ===============  ===============\n'
    s += 'PROD_ID  PROD_Status   Date_Birth       Baktin   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT  BUY  CONS  LEFT\n'
    
    if inc_cost > 0:
        s += 'PROD_ID  PROD_Status   Date_Birth       Baktin  BOS  PRE  STR  GRO  FIN    BOOSTER  PRE  STR  GRO  FIN \n'
    
    
    count = 0
    
    for cur_entry in data:
        
        if count == 0:
            pprint.pprint(cur_entry)
            count = 1
        
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
        
        num_piglets_weaning = cur_entry['num_piglets_weaning']
        num_piglets = num_piglets_weaning['male'] + num_piglets_weaning['female']
        
        s_temp      = str(num_piglets)
        num_chars   = len(s_temp)
        num_space   = 6 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '   '
        
        
        num_lactating  = cur_entry['num_feeds']['lactating']
        if num_lactating is not None:
                
            num_bought  = num_lactating['bought']
            
            if num_bought is not None:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            s           += '  '
            
            num_consumed  = num_lactating['consumed']
            
            if num_consumed is not None:
                s_temp      = f"{num_consumed:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
            
            s           += '  '
                
            num_left        = num_lactating['left']
            
            if num_left is not None:
                s_temp      = f"{num_left:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
        
        else:
            s           += 15 * ' '
            
        s           += '   '
        
        
        num_booster  = cur_entry['num_feeds']['booster']
        if num_booster is not None:
            
            num_bought  = num_booster['bought']
            
            if num_bought is not None:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
                
            s           += '  '
            
            num_consumed  = num_booster['consumed']
            
            if num_consumed is not None:
                s_temp      = str(int(num_consumed))
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
                
            s           += '  '
                
            num_left        = num_booster['left']
            
            if num_left is not None:
                s_temp      = str(int(num_left))
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            
        else:
            s           += 15 * ' '
        
        s           += '   '
            
        
        num_prestarter  = cur_entry['num_feeds']['prestarter']
        if num_prestarter is not None:
                
            num_bought  = num_prestarter['bought']
            
            if num_bought is not None:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            s           += '  '
            
            num_consumed  = num_prestarter['consumed']
            
            if num_consumed is not None:
                s_temp      = f"{num_consumed:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
            
            s           += '  '
                
            num_left        = num_prestarter['left']
            
            if num_left is not None:
                s_temp      = f"{num_left:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
        
        else:
            s           += 15 * ' '
            
        s           += '   '
            
        
        num_starter  = cur_entry['num_feeds']['starter']
        if num_starter is not None:
                
            num_bought  = num_starter['bought']
            
            if num_bought is not None:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            
            s           += '  '
            
            num_consumed  = num_starter['consumed']
            
            if num_consumed is not None:
                s_temp      = f"{num_consumed:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
                
            s           += '  '
                
            num_left        = num_starter['left']
            
            if num_left is not None:
                s_temp      = f"{num_left:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
        
        else:
            s           += 15 * ' '
            
        s           += '   '
            
        
        num_grower  = cur_entry['num_feeds']['grower']
        if num_grower is not None:
                
            num_bought  = num_grower['bought']
            
            if num_bought is not None:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            
            s           += '  '
            
            num_consumed  = num_grower['consumed']
            
            if num_consumed is not None:
                s_temp      = f"{num_consumed:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
                
            s           += '  '
                
            num_left        = num_grower['left']
            
            if num_left is not None:
                s_temp      = f"{num_left:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '    '
        
        else:
            s           += 9 * ' '
        
        s           += '   '
            
        
        
        
        s+= '\n'

    return s
    

    
    
@app.get("/cal/activities", response_class=PlainTextResponse)
async def cal_activities(num_days: int = 30):
    """
    Will get latest coming calendar activities.
    
    Parameters
    ----------
    num_days:int
        number of days starting today

        
    """
    
    now             = datetime.now()
    date_start_str  = now.strftime('%Y-%m-%d')
    
    date_end        = now + timedelta(days=num_days) 
    date_end_str    = date_end.strftime('%Y-%m-%d')

    res = model['sow_act'].get_latest_calendar_activities(date_start_str, 
        date_end_str)
    
        
    s = 'Date                  Sow   Act_ID   Days_AI   Activity               Description\n'
    
    
    
    for cur_entry in res:
        cur_date = cur_entry['date']
        
        line_count = 0
        for cur_act in cur_entry['activities']:
        
            if line_count == 0:
                cur_date    = datetime.strptime(cur_entry['date'], '%Y-%m-%d')
                cur_day     = cur_date.weekday()
                
                s_temp      = cur_entry['date']
                s           += s_temp
                s           += '(' + s_day_week[cur_day] +')'
                s           += '    '
            else:
                s           += ' ' * 19

                
            s_temp      = str(cur_act['sow_number'])
            num_chars   = len(s_temp)
            num_space   = 6 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '   '
        
            
            s_temp      = str(cur_act['id'])
            num_chars   = len(s_temp)
            num_space   = 6 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '   '
            
            
            if cur_act['days_ins'] is not None:
                s_temp      = str(cur_act['days_ins'])
                num_chars   = len(s_temp)
                num_space   = 7 - num_chars
                s           += ' ' * num_space + s_temp
                s           += '   '
            else:
                s           += '          '
            
            s_temp      = cur_act['activity']
            num_chars   = len(s_temp)
            num_space   = 20 - num_chars
            s           += s_temp + ' ' * num_space
            s           += '   '
            
            s_temp      = cur_act['desc']
            s           += s_temp
            s           += '\n'
            
            line_count  += 1
        
        s           += '\n'
        
    return s