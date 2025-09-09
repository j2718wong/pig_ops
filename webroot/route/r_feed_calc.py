# December 16, 2024
# Jack Wong

import os
import sys
import pprint

from datetime               import datetime, timedelta 

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *

from fastapi.responses      import PlainTextResponse



    
@app.get("/feed_calc/consumption/list", response_class=PlainTextResponse)
async def feed_calc_consumption_list(pig_farm_hid:str, num_per_prod:int = None):
    """
    Will feed consumption list.

    Parameters
    ==========
       
    pig_farm_hid : str
        pig_farm hashed id
    
    num_per_prod : int
        if > 0, will include feeds cost
        
        
    """
    
    if num_per_prod is not None:
        if num_per_prod < 3: # set lower limit
            num_per_prod = 3
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    pig_farm_id = res[0]
    
    
    df_consume  = model['feed_calc'].get_feed_consumed_list(pig_farm_id)
    
    df_consume['con_num_LAC'] = df_consume['con_kg_LAC'] / DEFAULT_KG_PER_UNIT['LACTATING']
    df_consume['con_num_BOS'] = df_consume['con_kg_BOS'] / DEFAULT_KG_PER_UNIT['BOOSTER']
    df_consume['con_num_PRE'] = df_consume['con_kg_PRE'] / DEFAULT_KG_PER_UNIT['PRESTARTER']
    df_consume['con_num_STR'] = df_consume['con_kg_STR'] / DEFAULT_KG_PER_UNIT['STARTER']
    df_consume['con_num_GRO'] = df_consume['con_kg_GRO'] / DEFAULT_KG_PER_UNIT['GROWER']
    df_consume['con_num_FIN'] = df_consume['con_kg_FIN'] / DEFAULT_KG_PER_UNIT['FINISHER']
    
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
    
    
    
    dt_now      = datetime.now()
    dt_now_s    = datetime.strftime(dt_now, '%Y-%m-%d')
    
    s = DB_INFO + '  ' + dt_now_s + '\n\n'
        
    s += write_feed_consumed(df_filtered, num_per_prod)
    
    return s
    
    
def write_feed_consumed(df, num_per_prod):
    dt_now      = datetime.now()
    
    
    s += 'FEED_CONSUMPTON                                        Consumed (NUMBER OF SACKS)        Consumed (KG)\n'
    s += '===============                                   ==================================  ====================\n'
    s += ' P_ID  DATE_BIRTH  DATE_BAL    DAYS  WEKS  PIGS   LACT  BOST  PRES  STAR  GROW  FINS  TOTAL  DIFF  DIFF_PP\n'
    
    """
             14  2025-05-03  2025-08-14   123    23    16    2.0    20   2.0  12.5                250    50     3.13
                             2025-08-07   123    23    16    2.0    20   2.0  12.5                250    50     3.13
    """
    
    last_prod_id        = None
    count_row_per_prod  = 0
    
    for row in df.itertuples():
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
            
            s           += row.date_bal
            s           += '  '
            
        else:
            s           += ' ' * 19
            
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
        
        s_temp      = str(row.con_kg_diff)
        num_chars   = len(s_temp)
        num_space   = 4 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '  '
        
        s_temp      = f"{row.con_kg_diff_pp:.1f}"
        num_chars   = len(s_temp)
        num_space   = 5 - num_chars
        s           += ' ' * num_space + s_temp
        
        s += '\n'
        
        
    return s
        
