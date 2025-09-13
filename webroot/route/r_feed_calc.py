# December 16, 2024
# Jack Wong

import os
import sys
import pprint

import pandas               as pd 
import numpy                as np

from datetime               import datetime, timedelta 

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *

from fastapi.responses      import PlainTextResponse



    
@app.get("/feed_calc/consumption/report", response_class=PlainTextResponse)
async def feed_calc_consumption_report(uhid:str, pfhid:str, num_per_prod:int = 5, 
        inc_historical: int =0):
    """
    Will feed consumption list.

    Parameters
    ==========
       
    pfhid : str
        pig_farm hashed id
    
    num_per_prod : int
        if > 0, will include feeds cost
        
        
    """
    
    if num_per_prod is not None:
        if num_per_prod < 3: # set lower limit
            num_per_prod = 3
    
    
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
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID',
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
    
    rep_gen = ReportGenFeedConsumption()
    s = rep_gen.write_report(account_id, pig_farm_id, num_per_prod, inc_historical)
    
    return s 
    
    
    
class ReportGenFeedConsumption:
    
    def write_report(self, account_id, pig_farm_id, num_per_prod, inc_historical):
        id_list     = [pig_farm_id]
        
        res_list    = model['pig_farm'].get_list(id_list = id_list)
        farm_info   = res_list[0]
        
        
        s  = self._write_report_header(farm_info)
        s += self._write_feed_consumed_list(pig_farm_id, num_per_prod, 
                inc_historical)
        
        return s
    
    
    def _write_report_header(self, farm_info):
        farm_name   = farm_info['pig_farm']['name']
        
        dt_now      = datetime.now()
        dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
        
        values = (farm_name, dt_now_s)
        s = 'Pig Production Feed Consumption Report for %s on %s\n\n' % values 
        return s
        

    def _write_feed_consumed_list(self, pig_farm_id, num_per_prod, inc_historical):
    
        df_consume  = model['feed_calc'].get_feed_consumed_list(pig_farm_id)
        

        df_consume['con_num_LAC'] = df_consume['con_kg_LAC'] / DEFAULT_KG_PER_FEED_UNIT['LACTATING']
        df_consume['con_num_BOS'] = df_consume['con_kg_BOS'] / DEFAULT_KG_PER_FEED_UNIT['BOOSTER']
        df_consume['con_num_PRE'] = df_consume['con_kg_PRE'] / DEFAULT_KG_PER_FEED_UNIT['PRESTARTER']
        df_consume['con_num_STR'] = df_consume['con_kg_STR'] / DEFAULT_KG_PER_FEED_UNIT['STARTER']
        df_consume['con_num_GRO'] = df_consume['con_kg_GRO'] / DEFAULT_KG_PER_FEED_UNIT['GROWER']
        df_consume['con_num_FIN'] = df_consume['con_kg_FIN'] / DEFAULT_KG_PER_FEED_UNIT['FINISHER']
        
        
        # remove unwanted columns
        df_filtered = df_consume[[
            'p_id',      
            'sow_number',
            'sow_name',  
            'date_birth',
                
            'date_bal',  
            'days_b',    
            'weeks_b',   
            'num_pigs',  
            
            'con_num_LAC',
            'con_num_BOS',
            'con_num_PRE',
            'con_num_STR',
            'con_num_GRO',
            'con_num_FIN',
            
            'con_kg_tot',    
            'con_kg_diff',   
            'con_kg_diff_pp'
            
        ]]
        
        df_filtered = df_filtered.replace(np.nan, None)
        
        
        dt_now      = datetime.now()
        dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
        
        s = DB_INFO + '  ' + dt_now_s + '\n\n'
            
        s += self._write_feed_consumed(df_filtered, num_per_prod)
        
        return s
        
        
    def _write_feed_consumed(self, df, num_per_prod):
        dt_now      = datetime.now()
        
        
        s  = 'FEED_CONSUMPTON                                        Consumed (NUMBER OF SACKS)        Consumed (KG)\n'
        s += '===============                                   ==================================  ====================\n'
        s += ' P_ID  DATE_BIRTH  DATE_BAL    DAYS  WEKS  PIGS   LACT  BOST  PRES  STAR  GROW  FINS  TOTAL  DIFF  DIFF_PP\n'
        
        """
                 14  2025-05-03  2025-08-14   123    23    16    2.0    20   2.0  12.5                250    50     3.13
                                 2025-08-07   123    23    16    2.0    20   2.0  12.5                250    50     3.13
        """
        
        last_prod_id        = None
        count_row_per_prod  = 0
        
        for row in df.itertuples():
            if num_per_prod is not None:
                if count_row_per_prod >= num_per_prod:
                    if last_prod_id == row.p_id:
                        continue
            
            if last_prod_id != row.p_id:
                last_prod_id = row.p_id
                
                count_row_per_prod = 0
                
                s += '\n'
                
                s_temp      = str(row.p_id)
                num_chars   = len(s_temp)
                num_space   = 5 - num_chars
                s           += ' ' * num_space + s_temp
                s           += '  '
                
                s           += row.date_birth
                s           += '  '
                
                
            else:
                s           += ' ' * 19
                
            s           += row.date_bal
            s           += '  '
                
            s_temp      = str(row.days_b)
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
            
            s_temp      = str(row.weeks_b)
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
            
            s_temp      = str(row.num_pigs)
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '   '
            
            
            if row.con_num_LAC is not None:
                s_temp      = f"{row.con_num_LAC:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
                
            else:
                s           += ' ' * 4
                
            s           += '  '
            
            
            if row.con_num_BOS is not None:
                s_temp      = f"{row.con_num_BOS:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
                
            else:
                s           += ' ' * 4
                
            s           += '  '
            
            
            if row.con_num_PRE is not None:
                s_temp      = f"{row.con_num_PRE:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
                
            else:
                s           += ' ' * 4
                
            s           += '  '
            
            
            if row.con_num_STR is not None:
                s_temp      = f"{row.con_num_STR:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
                
            else:
                s           += ' ' * 4
                
            s           += '  '
            
            
            if row.con_num_GRO is not None:
                s_temp      = f"{row.con_num_GRO:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
                
            else:
                s           += ' ' * 4
                
            s           += '  '
            
            
            if row.con_num_FIN is not None:
                s_temp      = f"{row.con_num_FIN:.1f}"
                num_chars   = len(s_temp)
                num_space   = 4 - num_chars
                s           += ' ' * num_space + s_temp
                
            else:
                s           += ' ' * 4
                
            s           += '  '
            
            
            s_temp      = str(row.con_kg_tot)
            num_chars   = len(s_temp)
            num_space   = 5 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
            
            s_temp      = str(int(row.con_kg_diff)) if row.con_kg_diff else ''
            num_chars   = len(s_temp)
            num_space   = 4 - num_chars
            s           += ' ' * num_space + s_temp
            s           += '  '
            
            if row.con_kg_diff_pp is not None:
                s_temp      = f"{row.con_kg_diff_pp:.1f}"
                num_chars   = len(s_temp)
                num_space   = 5 - num_chars
                s           += ' ' * num_space + s_temp
            else:
                s           += ' ' * 5
            
            count_row_per_prod += 1
            s += '\n'
            
            
        return s
            
