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

NUMDAYS_SINCE_BIRTH_TARGET_HARVEST      = 150


PRODUCTION_FEEDS = [
    FEED_TYPE_ID_LACTATING,
    FEED_TYPE_ID_BOOSTER,
    FEED_TYPE_ID_PRESTARTER,
    FEED_TYPE_ID_STARTER,
    FEED_TYPE_ID_GROWER,
    FEED_TYPE_ID_FINISHER
]

    
@app.get("/pig_prod/ops/report", response_class=PlainTextResponse)
async def pig_prod_ops_report(uhid:str, pfhid:str, inc_historical: int =0, 
        inc_cost: int = 0, inc_target_harvest: int= 0, year:int = None):
    """
    Will generate pig_prod operations report.

    Parameters
    ==========
    
    uhid : str
        user hash id
        
    pfhid : str
        pig farm hash id
       
    inc_historical : int
        if > 0, pig production with status lactating, growing, harvested, 
        close will be returned
    
    inc_cost : int
        if > 0, will include feeds cost
        
    inc_target_harvest : int
        if > 0, will compute target harvest date
        
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
    
    rep_gen = ReportGenPigProdOps()
    s = rep_gen.write_report(account_id, pig_farm_id, inc_historical, inc_cost,
                inc_target_harvest)
        
    
    # Record analytics
    data = {
        'user_id': user_id,
        'app_function_id': APP_ANALYTICS_ID_REPORT_PIG_PROD_OPERATIONS
    }
    model['app_analytics'].add(data)
    
    return s
    
    
@app.get("/pig_prod/weaning/report", response_class=PlainTextResponse)
async def pig_prod_weaning_report(uhid:str, pfhid:str, inc_historical: int =0):
    """
    Will generate pig_prod weaning report.

    Parameters
    ==========
    
    uhid : str
        user hash id
        
    pfhid : str
        pig farm hash id
       
    inc_historical : int
        if > 0, pig production with status lactating, growing, harvested, 
        close will be returned
    
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
    
    rep_gen = ReportGenPigWeaning()
    s = rep_gen.write_report(account_id, pig_farm_id, inc_historical)
    
        
    # Record analytics
    data = {
        'user_id': user_id,
        'app_function_id': APP_ANALYTICS_ID_REPORT_PIG_PROD_WEANING
    }
    model['app_analytics'].add(data)

    return s

    
    
class ReportGenPigProdOps:
    
    
    def write_report(self, account_id, pig_farm_id, inc_historical, inc_cost,
            inc_target_harvest):
        id_list     = [pig_farm_id]
        
        res_list    = model['pig_farm'].get_list(id_list = id_list)
        farm_info   = res_list[0]
        
        res_prod_ops = model['pig_prod'].get_pig_prod_ops_list(pig_farm_id, 
                    inc_historical)
    
        
        
        s  = self._write_report_header(farm_info)
        s += self._write_gestating_operations(account_id, pig_farm_id, inc_historical)
        s += self._write_lactating_sows_operations(account_id)
        s += self._write_lactating_piglets_operations(res_prod_ops, inc_historical)
        s += self._write_feeding_guide(res_prod_ops, inc_target_harvest, inc_historical)
        s += self._write_feeds_consumed(res_prod_ops, inc_historical)
        
        if inc_cost > 0:
            s += self._write_feeds_cost(res_prod_ops, inc_historical)
        
        s += self._write_sow_boar_balance(pig_farm_id)
        
        
        return s
    
    
    def _write_report_header(self, farm_info):
        farm_name   = farm_info['pig_farm']['name']
        
        dt_now      = datetime.now()
        dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
        
        values = (farm_name, dt_now_s)
        s = 'Pig Production Operations Report for %s on %s\n\n' % values 
        return s
        
    
    def _write_gestating_operations(self, account_id, pig_farm_id, inc_historical):
        # This is the list of the gestating operations specified by the account
        # that needs to be done fos each gestating sow(already inseminated).
        acc_pig_ops = model['account_pig_ops'].get_list(account_id, 
                PIG_OPERATION_TYPE_GESTATING)
        
        len_acc_pig_ops     = len(acc_pig_ops)
        
        list_gestating_sows = model['sow_act'].get_production_sow_list(
                            pig_farm_id, 0, inc_historical)
        
        for cur_entry in list_gestating_sows:
            cur_pig_prod_id = cur_entry['pig_prod']['id']
            
            # This is the actual pig operations on the gestating sow.
            list_pig_ops  = model['pig_prod_pig_ops'].get_list(
                cur_pig_prod_id, PIG_OPERATION_TYPE_GESTATING
            )
            
            cur_entry['gestating_ops'] = list_pig_ops
            
            
        dt_now      = datetime.now()
            
        s  = 'GESTA OPERATIONS\n' 
        s += '=================\n'    
        s += ' P_ID  Sow           Date_TAKAL       Boar        '
        
        
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
        s += '  '
        
        
        
        s += '\n'
        
        
        
        for cur_entry in list_gestating_sows:
            
            s_temp      = str(cur_entry['pig_prod']['farm_prod_id'])
            num_chars   = len(s_temp)
            num_space   = 5 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
            
            
            sow_number  = cur_entry['sow']['number']
            sow_name    = cur_entry['sow']['name']
            s_temp      = sow_name if sow_name else sow_number 
            num_chars   = len(s_temp)
            num_space   = 12 - num_chars
            s           += s_temp + ' ' * num_space 
            s           += '  '
            
            
            date_insem  = cur_entry['insemination']['date']
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
            
            
            boar_id         = cur_entry['boar']['id']
            semen_source    = cur_entry['semen_source']
            semen_source_id = semen_source['id']
            
            if boar_id is None:
                s_temp      = cur_entry['insemination']['type']
            else:
                boar_number = cur_entry['boar']['number']
                boar_name   = cur_entry['boar']['name']
                s_temp      = boar_name if boar_name else boar_number
            
            num_chars   = len(s_temp)
            num_space   = 10 - num_chars
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
            
            
            len_items   = len(cur_gestating_ops)
            
            if len_items == 0 and len_acc_pig_ops > 0:
                num_space   = len_acc_pig_ops * (max_chars_per_date_col + 2)
                s           += ' ' * num_space 
                
            
            s_temp      = cur_entry['birth']['date_expected']
            num_chars   = len(s_temp)
            num_space   = max_chars_per_date_col - num_chars
            s           += s_temp + ' ' * num_space 
            s           += '  '
            
            
            # Add comments of the semen source if artificial insemination
            s_temp = ''
            if semen_source_id is not None:
                semen_is_external = semen_source['is_external']
                
                if semen_is_external > 0:
                    semen_source_name       = semen_source['name']
                    semen_source_supplier   = semen_source['supplier']['name']
                
                    s_temp = semen_source_name + ' from ' + semen_source_supplier
                else:
                    boar_number = semen_source['boar']['number']
                    boar_name = semen_source['boar']['name']
                    
                    s_temp = 'Internal semen from BOAR: '
                    
                    if boar_name is not None:
                        s_temp += boar_name
                    else:
                        s_temp += boar_number
            else:
                boar_notes = cur_entry['boar']['notes']
                if boar_notes is not None:
                    s_temp = boar_notes
                
            s += s_temp
            
            s           += '\n'
            
        
        s += '\n\n'
        
        return s 
         
        
    def _write_lactating_sows_operations(self, account_id):
        # Check first if there are lactating sow operations set by account
        
        acc_pig_ops = model['account_pig_ops'].get_list(account_id, 
                PIG_OPERATION_TYPE_LACTATING_SOW)
        
        if len(acc_pig_ops) == 0:
            return ''
        
        s = ''
        
        return s
        
        
    def _write_lactating_piglets_operations(self, data, inc_historical):
        dt_now      = datetime.now()
        
        s  = 'BAKTIN OPERATIONS\n'
        s += '=================\n'
        s += ' P_ID  Sow           Date_Birth       Pigs  InjIron1  (3)  InjIron2  (13)  InjVita1  (14)  InjVita2  (21)  Kapon     (22)  Purga     (25)  Date_Lutas(45)\n'
         
        for cur_entry in data:
            pig_prod    = cur_entry['pig_prod']
            status_id   = pig_prod['status_id']
            
            if inc_historical == 0:
                if status_id != PROD_STATUS_ID_LACTATING:
                    continue
            
            s_temp      = str(pig_prod['farm_prod_id'])
            num_chars   = len(s_temp)
            num_space   = 5 - num_chars
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
            num_space   = 4 - num_chars
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

        
    def _write_feeding_guide(self, data, inc_target_harvest, inc_historical):
        dt_now      = datetime.now()
        
        
        s  = 'PROD FEEDING GUIDE\n'
        s += '===================\n'
        s += ' P_ID  PROD_Status   Date_Birth       Pigs  Booster   (7)  PreStarter(30)   Date_Lutas(45)  Starter   (50)  Grower    (90)  Finisher         Date_Harvest\n'
        
        for     cur_entry in data:
            pig_prod    = cur_entry['pig_prod']
            status_id   = pig_prod['status_id']
            
            if status_id == PROD_STATUS_ID_GESTATING:
                continue
            
            
            s_temp      = str(pig_prod['farm_prod_id'])
            num_chars   = len(s_temp)
            num_space   = 5 - num_chars
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
            num_space   = 4 - num_chars
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
                num_days    = NUMDAYS_SINCE_BIRTH_BOOSTER - DAY_1_STARTS_AT_BIRTH
                dt_booster  = dt_birth + timedelta(days = num_days)
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
                num_days    = NUMDAYS_SINCE_BIRTH_PRESTARTER - DAY_1_STARTS_AT_BIRTH
                dt_prestarter  = dt_birth + timedelta(days = num_days)
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
                num_days    = NUMDAYS_SINCE_BIRTH_WEANING - DAY_1_STARTS_AT_BIRTH
                dt_weaning  = dt_birth + timedelta(days = num_days)
                date_weaning = datetime.strftime(dt_weaning, '%Y-%m-%d')
               
                s           += f"{date_weaning}(P)"
                s           += '   '
                
            
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
                s           += ' ' * 15
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
                
                if inc_target_harvest > 0:
                    num_days = NUMDAYS_SINCE_BIRTH_TARGET_HARVEST
                    dt_harvest = dt_birth + timedelta(days = num_days)
                    date_harvest = datetime.strftime(dt_harvest, '%Y-%m-%d')
                    
                    numdays_delta = num_days
                    
                    s_temp      = date_harvest
                    s           += s_temp
                    s           += f"({numdays_delta}T)"
                    s           += '  '
                else:
            
                    s           += ' ' * 14
            
            
            
            s+= '\n'
        
        s += '\n\n'
        
        return s
        
        
    def _get_feed_buy(self, list_feed_buy, feed_type_id):
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
            
        
    def _write_feeds_consumed(self, data, inc_historical):
        dt_now      = datetime.now()
        
        s  = 'PROD FEEDS CONSUMED                               LACTA            BOOSTER         PRE_STARTER         STARTER            GROWER          FINISHER    \n'
        s += '====================                         ===============   ===============   ===============   ===============   ===============   ===============\n'
        s += ' P_ID  PROD_Status   Date_Birth       Pigs   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT   BUY  CONS  LEFT\n'
        
        
        total_num_pigs       = 0
        
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
            num_space   = 5 - num_chars
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
                 
                total_num_pigs += num_pigs_current
                
                s_temp      = str(num_pigs_current)
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            
            else:
                s += ' ' * 4
            
            s           += '   '
            
            
            index = 0
            for cur_feed_type in PRODUCTION_FEEDS:
                res = self._write_feeds_consumed_type(cur_feed_type, 
                        cur_entry['num_feeds'], list_feed_bought)
                
                s += res[0]
                feeds_left[index] += res[1]
                index += 1
                
            
            s += '\n'
        
        s += '\n'
        
        
        s += '                          Balance  '
        s += '   '
        
        s_temp      = str(total_num_pigs)
        num_chars   = len(s_temp)
        num_space   = 4 - num_chars
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
        

    def _write_feeds_consumed_type(self, feed_type_id, data, list_feed_bought):
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
            feed_buy    = self._get_feed_buy(list_feed_bought, feed_type_id)
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
            

    def _write_feeds_cost(self, data, inc_historical):
        dt_now      = datetime.now()
        
        
        s  = 'FEEDS COST                                        LACTA            BOOSTER         PRE_STARTER         STARTER           GROWER           FINISHER    \n'
        s += '=================                            ===============   ===============   ===============   ===============   ===============   ===============\n'
        s += ' P_ID   Total_COST   Date_Birth       Pigs   BUY        COST   BUY        COST   BUY        COST   BUY        COST   BUY        COST   BUY        COST\n'
       
        
        for cur_entry in data:
            pig_prod    = cur_entry['pig_prod']
                
            s_temp      = str(pig_prod['farm_prod_id'])
            num_chars   = len(s_temp)
            num_space   = 5 - num_chars
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
                
                s_temp      = str(num_pigs_current)
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
                
            else:
                s += ' ' * 4
                
            s           += '   '
            
            
            
            index = 0
            for cur_feed_type in PRODUCTION_FEEDS:
                res = self._write_feeds_cost_type(cur_feed_type, 
                        cur_entry['num_feeds'], cost_feeds)
                
                s += res
                index += 1
            
            
            s+= '\n'
        
        s+= '\n\n'
        
        return s
            
            
    def _write_feeds_cost_type(self, feed_type_id, data, cost_feeds):
        s = ''
        
        if feed_type_id == FEED_TYPE_ID_LACTATING:
            data_feed_type = data['lactating']
            cost_feed_type = cost_feeds['lactating']
        
        elif feed_type_id == FEED_TYPE_ID_BOOSTER:
            data_feed_type = data['booster']
            cost_feed_type = cost_feeds['booster']
            
        elif feed_type_id == FEED_TYPE_ID_PRESTARTER:
            data_feed_type = data['prestarter']
            cost_feed_type = cost_feeds['prestarter']
        
        elif feed_type_id == FEED_TYPE_ID_STARTER:
            data_feed_type = data['starter']
            cost_feed_type = cost_feeds['starter']
        
        elif feed_type_id == FEED_TYPE_ID_GROWER:
            data_feed_type = data['grower']
            cost_feed_type = cost_feeds['grower']
        
        elif feed_type_id == FEED_TYPE_ID_FINISHER:
            data_feed_type = data['finisher']
            cost_feed_type = cost_feeds['finisher']
        
            
           
        if data_feed_type is not None:
                
            num_bought  = data_feed_type['bought']
            
            if num_bought is not None and num_bought > 0:
                s_temp      = str(num_bought)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += '   '
            s           += '  '
            
            if cost_feed_type is not None:
                s_temp      = f"{cost_feed_type:,.1f}"
                num_chars   = len(s_temp)
                num_space   = 10 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s       += ' ' * 10
        
        else:
            s           += 15 * ' '
            
        s           += '   '
        
            
        
        return s
        

    def _write_sow_boar_balance(self, pig_farm_id):
        
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
        
        
        
class ReportGenPigWeaning:
    
    def write_report(self, account_id, pig_farm_id, inc_historical):
        id_list     = [pig_farm_id]
        
        res_list    = model['pig_farm'].get_list(id_list = id_list)
        farm_info   = res_list[0]
        
        
        s  = self._write_report_header(farm_info)
        s += self._write_weaning_list(pig_farm_id, inc_historical)
        
        return s
    
    
    def _write_report_header(self, farm_info):
        farm_name   = farm_info['pig_farm']['name']
        
        dt_now      = datetime.now()
        dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
        
        values = (farm_name, dt_now_s)
        s = 'Pig Production at Weaning Report for %s on %s\n\n' % values 
        return s
        
    
    
    def _write_weaning_list(self, pig_farm_id, inc_historical):
        list_weaning_sows = model['sow_act'].get_production_sow_list(
                            pig_farm_id, 1, inc_historical)
    
        
        s  = '       PIG PRODUCTION                                                                  Birth                    Wean\n'
        s += '=======================================                                            ============              ============\n'
        s += ' P_ID  Sow       Boar      PROD_Status   Date_TAKAL  Expected    Date_Birth  Days   D    M    F  Date_Lutas   D    M    F   Pigs  \n'
        
        

        for cur_entry in list_weaning_sows:
            s_temp      = str(cur_entry['pig_prod']['id'])
            num_chars   = len(s_temp)
            num_space   = 5 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '

            
            sow_number  = cur_entry['sow']['number']
            sow_name    = cur_entry['sow']['name']
            s_temp      = sow_name if sow_name else sow_number 
            s_temp      = s_temp[0:8]
            num_chars   = len(s_temp)
            num_space   = 8 - num_chars
            s           += s_temp + ' ' * num_space
            s           += '  '
            
            
            boar_id     = cur_entry['boar']['id']
            boar_number = cur_entry['boar']['number']
            boar_name   = cur_entry['boar']['name']
            
            if boar_id and boar_id > 0:
                s_temp  = boar_name if boar_name else boar_number
            else:
                s_temp  = cur_entry['insemination']['type']
                
            s_temp      = s_temp[0:8]
            num_chars   = len(s_temp)
            num_space   = 8 - num_chars
            s           += s_temp + ' ' * num_space
            s           += '  '
                
                
            s_temp      = cur_entry['pig_prod']['status_name']
            num_chars   = len(s_temp)
            num_space   = 12 - num_chars
            s           += s_temp + ' ' * num_space 
            s           += '  '
            
            
            s_temp      = cur_entry['insemination']['date']
            s           += s_temp 
            s           += '  '
            
            
            cur_entry_birth = cur_entry['birth']
            
            
            s_temp      = cur_entry_birth['date_expected']
            s           += s_temp 
            s           += '  '
            
                
            date_birth  = cur_entry_birth['date_actual']
            if date_birth is not None:
                s_temp      = date_birth
                s           += s_temp 
            else:
                s           += ' ' * 10
            s           += '  '
            
            
            cur_days_actual = cur_entry_birth['num_days_actual']
            if cur_days_actual is not None and cur_days_actual > 0:
                s_temp      = str(cur_days_actual)
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += s_temp + ' ' * num_space
                
            else:
                s           += ' ' * 4
            s           += '  '
            
                                      
            num_pigs_birth  = cur_entry_birth['num_pigs']
            num_dead        = num_pigs_birth['dead_at_birth']
            num_male        = num_pigs_birth['live_m']
            num_female      = num_pigs_birth['live_f']
            
            total_pigs_birth = None
            if num_male is not None and num_female is not None:
                total_pigs_birth = num_male + num_female
            
            if num_dead is not None:
                s_temp      = str(num_dead)
                num_chars   = len(s_temp)
                num_space   = 2 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s           += ' ' * 2
                
            s           += '  '
                
            
            if num_male is not None:
                s_temp      = str(num_male)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s           += ' ' * 3
            
            s           += '  '
                
            
            if num_female is not None:
                s_temp      = str(num_female)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s           += ' ' * 3

            s           += '  '
            
            
            weaning         = cur_entry['weaning']
            num_dead        = None
            num_male        = weaning['num_pigs_m']
            num_female      = weaning['num_pigs_f']
            
            total_pigs_wean = None
            if num_male is not None and num_female is not None:
                total_pigs_wean = num_male + num_female
                
            if total_pigs_birth is not None and total_pigs_wean is not None:
                num_dead = total_pigs_birth - total_pigs_wean
                
            if weaning['date'] is not None:
                s_temp      = weaning['date']
                s           += s_temp 
            else:
                s           += ' ' * 10
                
            s           += '  '
            
            
            if num_dead is not None:
                s_temp      = str(num_dead)
                num_chars   = len(s_temp)
                num_space   = 2 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s           += ' ' * 2
            
            s           += '  '
            
            
            if num_male is not None:
                s_temp      = str(num_male)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s           += ' ' * 3
            
            s           += '  '
            
            
            if num_female is not None:
                s_temp      = str(num_female)
                num_chars   = len(s_temp)
                num_space   = 3 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s           += ' ' * 3

            s           += '   '
            
            
            if total_pigs_wean is not None:
                s_temp      = str(total_pigs_wean)
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s           += ' ' * 4
            
            s           += '  '
            
            
            boar_id         = cur_entry['boar']['id']
            semen_source    = cur_entry['semen_source']
            semen_source_id = semen_source['id']
            
            # Add comments of the semen source if artificial insemination
            s_temp = ''
            if semen_source_id is not None:
                semen_is_external = semen_source['is_external']
                
                if semen_is_external > 0:
                    semen_source_name       = semen_source['name']
                    semen_source_supplier   = semen_source['supplier']['name']
                
                    s_temp = semen_source_name + ' from ' + semen_source_supplier
                else:
                    boar_number = semen_source['boar']['number']
                    boar_name = semen_source['boar']['name']
                    
                    s_temp = 'Internal semen from BOAR: '
                    
                    if boar_name is not None:
                        s_temp += boar_name
                    else:
                        s_temp += boar_number
            else:
                boar_notes = cur_entry['boar']['notes']
                if boar_notes is not None:
                    s_temp = boar_notes
                
            s += s_temp
            
            
            s           += '\n'
            
            
        return s
