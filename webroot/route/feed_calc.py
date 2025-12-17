# September 9, 2025
# Jack Wong

import os
import sys
import pprint

import pandas               as pd

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *

DAYS_ESTIMATE_MINIMUM       = 7
DAYS_ESTIMATE_MAXIMUM       = 35

class FeedCalculator:
    def __init__(self, pig_farm_id):
        self.model          = model
        self.logger         = logger
        self.pig_farm_id    = pig_farm_id
        
        
    def estimate_consumption_by_date(self, date_estimate):
        dt_estimate     = datetime.strptime(date_estimate, '%Y-%m-%d')
        
        dt_now          = datetime.now()
        
        delta_days  = (dt_estimate - dt_now).days
        
        if delta_days < DAYS_ESTIMATE_MINIMUM and delta_days > DAYS_ESTIMATE_MAXIMUM:
            return {
                values = (DAYS_ESTIMATE_MINIMUM, DAYS_ESTIMATE_MAXIMUM)
                msg = 'Please enter between %s and %s days.' % values
                
                'result': {
                    'num':  ERROR_FEED_ESTIMATE_OUTSIDE_RANGE
                    'code': 'ERROR_FEED_ESTIMATE_OUTSIDE_RANGE'
                    'desc': 
                }
            
            }
        
        
        # Check if there is a sow or boar list
        list_sows       = self.model['sow_boar'].get_list(self.pig_farm_id, 'F')
        list_boars      = self.model['sow_boar'].get_list(self.pig_farm_id, 'M')
        
        len_sows        = len(list_sows)
        len_boars       = len(list_boars)
        
        
        # Get production list
        df_prod         = self.model['feed_calc'].get_pig_prod_list(self.pig_farm_id)
        
        len_prod        = len(df_prod)
        
        
        
        
        df_prod['con_num_LAC']  = df_prod['buy_num_LAC']    - df_prod['bal_num_LAC']
        df_prod['bal_kg_LAC']   = df_prod['buy_kg_LAC']     - df_prod['con_kg_LAC']
        
        
        df_prod['con_num_BOS']  = df_prod['buy_num_BOS']    - df_prod['bal_num_BOS']
        df_prod['bal_kg_BOS']   = df_prod['buy_kg_BOS']     - df_prod['con_kg_BOS']
        
        
        df_prod['con_num_PRE']  = df_prod['buy_num_PRE']    - df_prod['bal_num_PRE']
        df_prod['bal_kg_PRE']   = df_prod['buy_kg_PRE']     - df_prod['con_kg_PRE']
        
        
        df_prod['con_num_STR']  = df_prod['buy_num_STR']    - df_prod['bal_num_STR']
        df_prod['bal_kg_STR']   = df_prod['buy_kg_STR']     - df_prod['con_kg_STR']
        
        
        df_prod['con_num_GRO']  = df_prod['buy_num_GRO']    - df_prod['bal_num_GRO']
        df_prod['bal_kg_GRO']   = df_prod['buy_kg_GRO']     - df_prod['con_kg_GRO']
        
        
        df_prod['con_num_FIN']  = df_prod['buy_num_FIN']    - df_prod['bal_num_FIN']
        df_prod['bal_kg_FIN']   = df_prod['buy_kg_FIN']     - df_prod['con_kg_FIN']
        
        
        date_birth_list = df_prod['date_birth'].tolist()
        
        
        # Compute the number of weeks from date_birth to date_estimate
        max_week_num_list = [int((dt_estimate - cur_date).days/7)  for cur_date in date_birth_list]
        
        
        # Get feed_consumed list 
        df_feed_consumed = self.model['feed_calc'].get_feed_consumed_list(
            self.pig_farm_id)
        
        # Get historical consumption per pig from last feed_balance weeknum + 1
        # until max_week_num per production
        
        for cur_entry in date_birth_list.itertuple():
            
            # 
            last_feed_balance_weeknum = cur_entry.weeks_since_b

        
        
        
        return df_prod
        
        
    def _get_average_consumption_per_pig(self, df_feed_consumed, week_num):
        filtered_df = df.loc[df_feed_consumed['weeks_b'] = week_num, ['p_id', 'con_kg_diff_pp']]
        num_data = len(filtered_df)
        
        
        