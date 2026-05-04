# January 3, 2025
# Jack Wong
import os
import sys

from common_constants       import *


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)

from base_model             import BaseModel




"""
account.flag bits

bit 0: FLAG_BIT_ACCOUNT_ENABLE
bit 1: FLAG_BIT_FREE_TRIAL_FINISHED
bit 2:
bit 3:  

bit 4:  FLAG_BIT_ACCOUNT_IS_BILL_EXEMPTED
0 = not exempted has to pay bill
1 = exempted



bit 16: COMPANY_OWNED ACCOUNT
"""

FLAG_BIT_ACCOUNT_ENABLE                 = 1
FLAG_BIT_FREE_TRIAL_FINISHED            = 2

FLAG_BIT_ACCOUNT_IS_BILL_EXEMPTED       = 1<<4
            

FLAG_BIT_ACCOUNT_IS_COMPANY_OWNED       = 1<<16





FLAG_BIT_USER_IS_ACTIVE                 = 1
FLAG_BIT_USER_EMAIL_VERIFIED            = 2
FLAG_BIT_USER_MOBILE_NUM_VERIFIED       = 4
FLAG_BIT_USER_IS_DELETED                = 8
                                        
FLAG_BIT_USER_IS_ACCOUNT_ADMIN          = 16



# The account.flag_settings will be broken down so that
# it will be easier to read in the application level.
# See account_register.sql for updated flag bits definition.

"""
/* account.flag_setting bits
bit 0: FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
0 = Date of birth is counted as DAY 0
1 = Date of birth is counted as DAY 1; default

bit 1: FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
0 = Date of insemination is counted as DAY 0; default
1 = Date of insemination is counted as DAY 1;


*/

"""

FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH     = 1
FLAG_BIT_DAY_1_ON_DATE_OF_INSEM     = 2
            

class Account(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        
    
    def get_info(self, account_id):
        
        sql =   """
                SELECT 
                    a.id,
                    a.flag,
                    a.status_id, 
                    
                    a.country_id,
                    b.name AS country_name,
                    b.flag,
                    
                    a.name AS account_name,
                    a.date_trial_start,
                    a.date_trial_end,
                    
                    a.count_sow_boar,
                    a.count_pig_prod,
                    
                    a.current_bill_id,
                    c.status_id,
                    c.flag,
                    c.bill_reference,
                    c.date_issue,
                    c.date_due,
                    
                    c.num_sow_boar_billed,
                    d.num_sow,
                    d.num_boar,
                    
                    c.currency_code,
                    c.tax_rate,
                    
                    c.charge_per_pig,
                    c.amount,
                    c.deduction,
                    c.taxable_amount,
                    c.taxes,
                    c.total_amount_due,
                    
                    a.weight_unit,
                    a.currency,
                    a.flag_settings,
                    a.num_days_move_to_farrow,
                    a.num_days_wean,
                    a.num_days_harvest_from_birth,
                    a.num_days_harvest_from_wean,
                    
                    
                    e.name_last,
                    e.name_first,
                    a.dt_last_update_settings,
                    
                    
                    a.ver_num_gestating_ops,
                    a.ver_num_lactating_piglets_ops, 
                    a.ver_num_lactating_sow_ops,     
                    a.ver_num_gilt_ops,              
                    a.ver_num_weaning_sow_ops,       
                    
                    a.data_ver_num_account
                    
                FROM account a
                LEFT OUTER JOIN app_country b   ON a.country_id = b.id
                LEFT OUTER JOIN account_bill c  ON a.current_bill_id = c.id
                LEFT OUTER JOIN sow_boar_head_count d  ON c.sow_boar_head_count_id = d.id
                LEFT OUTER JOIN user e          ON a.last_update_settings_user_id = e.id
                
                WHERE a.id = %s
                """ % account_id
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        

        for row in rows:
            cur_acc_id                  = row[0]
            cur_acc_flag                = row[1]
            cur_acc_status_id           = row[2]
            
            cur_acc_country_id          = row[3]
            cur_acc_country_name        = row[4]
            cur_acc_country_flag        = row[5]
        
            cur_acc_account_name        = row[6]
            cur_acc_date_trial_start    = str(row[7]) if row[7] else None
            cur_acc_date_trial_end      = str(row[8]) if row[8] else None
            
            # Accumlated count for account
            cur_acc_count_sow_boar      = row[9] 
            cur_acc_count_pig_prod      = row[10]
            
            
            cur_acc_current_bill_id             = row[11]
            cur_acc_bill_status                 = row[12]
            cur_acc_bill_flag                   = row[13]
            cur_acc_bill_reference              = row[14]
            cur_acc_bill_date_issue             = row[15]
            cur_acc_bill_date_due               = row[16]

            cur_acc_bill_num_sow_boar_billed    = row[17]
            cur_acc_bill_num_sow                = row[18]
            cur_acc_bill_num_boar               = row[19]

            cur_acc_bill_currency_code          = row[20]
            cur_acc_bill_tax_rate               = row[21]

            cur_acc_bill_charge_per_pig         = row[22]
            cur_acc_bill_amount                 = row[23]
            cur_acc_bill_deduction              = row[24]
            cur_acc_bill_taxable_amount         = row[25]
            cur_acc_bill_taxes                  = row[26]
            cur_acc_bill_total_amount_due       = row[27]

            cur_acc_weight_unit                 = row[28]
            cur_acc_currency                    = row[29]
            cur_acc_settings_flag               = row[30]
            cur_acc_num_days_move_to_farrow     = row[31]
            cur_acc_num_days_wean               = row[32]
            cur_acc_num_days_harvest_from_birth = row[33]
            cur_acc_num_days_harvest_from_wean  = row[34]

            cur_user_name_last                  = row[35]
            cur_user_name_first                 = row[36]
            cur_settings_last_update            = str(row[37]) if row[37] else None

            cur_ver_num_gestating_ops           = row[38]
            cur_ver_num_lactating_piglets_ops   = row[39]
            cur_ver_num_lactating_sow_ops       = row[40]
            cur_ver_num_gilt_ops                = row[41]
            cur_ver_num_weaning_sow_ops         = row[42]

            cur_data_ver_num_account            = row[43]

            
            temp = cur_acc_flag & FLAG_BIT_ACCOUNT_ENABLE
            cur_flag_acc_is_enabled = 1 if temp > 0 else 0
            
            
            temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
            cur_flag_day_1_on_dob   = 1 if temp > 0 else 0
            
            temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
            cur_flag_day_1_on_doi   = 1 if temp > 0 else 0
            
            
            cur_entry = {
                'account': {
                    'id':                   cur_acc_id,
                    'name':                 cur_acc_account_name,
                    'flag':                 cur_acc_flag,
                    'status_id':            cur_acc_status_id,
                    
                        
                    'is_enabled':           cur_flag_acc_is_enabled,
                        
                        
                    'count_sow_boar':       cur_acc_count_sow_boar,
                    'count_pig_prod':       cur_acc_count_pig_prod,
                        
                    'date_trial_start':     cur_acc_date_trial_start,
                    'date_trial_end':       cur_acc_date_trial_end,
                    
                    'country':  {
                        'id':               cur_acc_country_id,
                        'name':             cur_acc_country_name,
                        'flag':             cur_acc_country_flag
                    },
                    
                    
                    'current_bill':{
                        'id':               cur_acc_current_bill_id,
                        'status_id':        cur_acc_bill_status,
                        
                        'flag':             cur_acc_bill_flag,
                        'bill_reference':   cur_acc_bill_reference,
                        'date_issue':       cur_acc_bill_date_issue,
                        'date_due':         cur_acc_bill_date_due,
                        
                        'num_billed':       cur_acc_bill_num_sow_boar_billed,
                        'num_sow':          cur_acc_bill_num_sow,
                        'num_boar':         cur_acc_bill_num_boar,
                        
                        'currency_code':    cur_acc_bill_currency_code,
                        'tax_rate':         cur_acc_bill_tax_rate,
                        
                        'charge_per_pig':   cur_acc_bill_charge_per_pig,
                        'amount':           cur_acc_bill_amount,
                        'deduction':        cur_acc_bill_deduction,
                        'taxes':            cur_acc_bill_taxes,
                        'taxable_amount':   cur_acc_bill_taxable_amount,
                        'total_amount_due': cur_acc_bill_total_amount_due
                    }
                },
                
                'settings_operations': {
                    'weight_unit':                  cur_acc_weight_unit,
                    'currency':                     cur_acc_currency,
                    'day_1_on_date_of_birth':       cur_flag_day_1_on_dob,
                    'day_1_on_date_of_insem':       cur_flag_day_1_on_doi,
                    'num_days_move_to_farrow':      cur_acc_num_days_move_to_farrow,
                    'num_days_wean':                cur_acc_num_days_wean,
                    'num_days_harvest_from_birth':  cur_acc_num_days_harvest_from_birth,
                    'num_days_harvest_from_wean':   cur_acc_num_days_harvest_from_wean,
                
                    'last_update':{
                        'name_last':    cur_user_name_last,
                        'name_first':   cur_user_name_first,
                        'dt_update':    cur_settings_last_update
                    }
                },
                
                'data_ver_num':[
                    cur_ver_num_gestating_ops,        
                    cur_ver_num_lactating_piglets_ops,
                    cur_ver_num_lactating_sow_ops,    
                    cur_ver_num_gilt_ops,             
                    cur_ver_num_weaning_sow_ops,      
                    
                    cur_data_ver_num_account
                ]
            }
            

            if cur_acc_current_bill_id == 0:
                del cur_entry['account']['current_bill']


            
            # Get Farm List
            account_farms = self.model['pig_farm'].get_list(account_id)
            
            if account_farms:
                cur_entry['pig_farms'] = account_farms
            
                
            return cur_entry
        
        return None
    
    
    def register(self, data = None):
        """
        PROCEDURE account_register(
            in_user_id              INT,
    
            in_country_id           INT,
            
            in_referred_by_account_id INT,  
            
            in_name                 VARCHAR(100)
        )  
        """
        
        params = [
            data.user_id,
            data.country_id,
            data.referred_by_account_id    if data.referred_by_account_id > 0 else None,
            data.name               if data.name and data.name.strip() else None
        ]
        
        rows = self._call_procedure('account_register', params)
        
        if rows is None:
            return None
        
        
        row = rows[0]


        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'account': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5],
                    'status_id':        row[6],
                    'status_name':      row[7],
                    'dt_trial_start':   row[8],
                    'dt_trial_end':     row[9]
                }
            }

        return None

    
    def update_hashid(self, data = None):
        account_id      = data['account_id']
        hashid          = data['hashid']
        
        values = (hashid, account_id)
        
        sql =   """
                UPDATE account SET
                    hashid    = "%s"
                WHERE id = %s;
                """ % values
        
        return self.model.execute_sql(sql)
    
    
    def update(self, data = None):
        """
        PROCEDURE account_update(
            in_user_id              INT,
    
            in_name                 VARCHAR(100)
        )  
        """
        
        params = [
            data.user_id,
            data.name if data.name and data.name.strip() else None
        ]
        
        rows = self._call_procedure('account_update', params)
        
        if rows is None:
            return None
        
        
        row = rows[0]
    

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'account': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5],
                    'status_id':        row[6],
                    'status_name':      row[7],
                    'dt_trial_start':   row[8],
                    'dt_trial_end':     row[9]
                }
            }

        return None
    
    
    def update_settings(self, data = None):
        """
        PROCEDURE account_update_settings(
            in_user_id                  INT,
    
            in_day_1_on_dob             INT,
            in_day_1_on_insem           INT,
            
            in_days_move_to_farrow      INT,
            in_days_wean                INT,
            
            in_days_harvest_from_birth  INT,
            in_days_harvest_from_wean   INT,
            
            in_weight_unit              VARCHAR(4)
        )  
        """
        
        params = [
            data.user_id,
            data.day_1_on_date_of_birth,
            data.day_1_on_date_insem,
            
            data.days_move_farrow,
            data.days_wean,
            
            data.days_harvest_from_birth,
            data.days_harvest_from_wean,
            data.weight_unit                if data.weight_unit and data.weight_unit.strip() else None
        ]
        
        rows = self._call_procedure('account_update_settings', params)
        
        if rows is None:
            return None

        
        row = rows[0]
    

        if row is not None:
            cur_res_num                 = row[0]
            cur_res_code                = row[1]
            cur_res_desc                = row[2]
            
            cur_acc_settings_flag       = row[3]
             
            temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
            cur_flag_day_1_on_dob   = 1 if temp > 0 else 0
            
            temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
            cur_flag_day_1_on_doi   = 1 if temp > 0 else 0
            
            
            cur_acc_num_days_wean       = row[4]
            cur_acc_num_days_harvest_from_birth = row[5]
            cur_acc_num_days_harvest_from_wean  = row[6]
            
            cur_acc_weight_unit         = row[7]
            cur_acc_currency            = row[8]
            
            
            result =  {
                'result':{
                    'num':              cur_res_num,
                    'code':             cur_res_code,
                    'desc':             cur_res_desc
                },
                
                'settings_operations': {
                    'day_1_on_date_of_birth':       cur_flag_day_1_on_dob,
                    'day_1_on_date_of_insem':       cur_flag_day_1_on_doi,
                    'num_days_wean':                cur_acc_num_days_wean,
                    'num_days_harvest_from_birth':  cur_acc_num_days_harvest_from_birth,
                    'num_days_harvest_from_wean':   cur_acc_num_days_harvest_from_wean,
                    
                    'acc_weight_unit':  cur_acc_weight_unit,
                    'currency':         cur_acc_currency
                }
            }

            return result 

        return None
    
    
    def get_list_account_admin(self, account_id):
        user_flag = FLAG_BIT_USER_IS_ACTIVE | FLAG_BIT_USER_EMAIL_VERIFIED 
        user_flag |= FLAG_BIT_USER_IS_ACCOUNT_ADMIN
        
        values = (account_id, user_flag)
        
        sql =   """
                SELECT 
                    id,
                    flag,
                    email,
                    mobile_num
                FROM user 
                WHERE account_id = %s &  flag = %s
                """ % values
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
            
            
        result = []
        if rows is not None:
            
            for row in rows:
                cur_user_account_id     = row[0]
                cur_user_flag           = row[1]
                cur_user_email          = row[2]
                cur_user_mobile_num     = row[3]
                
                cur_entry = {
                    'id':               user_id,
                    'flag':             cur_user_flag,
                    'email':            cur_user_email,
                    'mobile_num':       cur_user_mobile_num
                }
                    
                result.append(cur_entry)
        
        return result
    
    
    def get_list_pig_farm(self, account_id):
        
        sql =   """
                SELECT 
                    a.id,
                    a.name,
                    
                    a.added_by_user_id,
                    b.name_last,
                    b.name_first,
                    a.dt_entry,
                    
                    a.country_id,
                    c.name AS country_name,
                    a.address_level_1_id,
                    a.address_level_2_id,
                    a.address_level_3_id,
                    a.latitude,
                    a.longitude
                FROM pig_farm a
                LEFT OUTER JOIN user b ON a.added_by_user_id = b.id
                LEFT OUTER JOIN app_country c   ON a.country_id = c.id
                WHERE a.account_id = %s 
                """ % account_id
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
        if rows is not None:
            
            for row in rows:
                cur_entry = {
                    'pig_farm': {
                        'id':               row[0],
                        'name':             row[1],
                        
                        'added_by_user':{
                            'id':           row[2],
                            'name_last':    row[3],
                            'name_first':   row[4]
                        },
                        
                        'dt_entry':         str(row[5])
                    },
                    
                    'location':{
                        
                        'country': {
                            'id':           row[6],
                            'name':         row[7]
                        },
                        
                        'address': {
                            'level_1':{
                                'id':       row[8]
                            },
                        
                            'level_2':{
                                'id':       row[9]
                            },
                            
                            'level_3':{
                                'id':       row[10]
                            }
                            
                        },
                        
                        'geoloc':{
                            'latitude':     float(row[11]) if row[11] else None,
                            'longitude':    float(row[12]) if row[12] else None
                        }
                    }
                }
                    
                result.append(cur_entry)
        
        return result
    
    
    def get_data_ver_num(self, account_id, return_array = 0):
        sql =   """
                SELECT 
                    ver_num_gestating_ops,
                    ver_num_lactating_piglets_ops,
                    ver_num_lactating_sow_ops,    
                    ver_num_gilt_ops,             
                    ver_num_weaning_sow_ops,      
                    
                    data_ver_num_account,
                    data_ver_num_pig_buyer
                    
                FROM account 
                WHERE id = %s
                """ % account_id
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        

        for row in rows:
            cur_ver_num_gestating_ops           = row[0]
            cur_ver_num_lactating_piglets_ops   = row[1]
            cur_ver_num_lactating_sow_ops       = row[2]    
            cur_ver_num_gilt_ops                = row[3]             
            cur_ver_num_weaning_sow_ops         = row[4]      
            
            cur_ver_num_account                 = row[5]
            cur_ver_num_pig_buyer               = row[6]
            
            
            if return_array == 0:
                cur_entry = {
                    'data_ver_num': {
                        'gesta_ops':            cur_ver_num_gestating_ops,       
                        'lacta_piglets_ops':    cur_ver_num_lactating_piglets_ops,    
                        'lacta_sow_ops':        cur_ver_num_lactating_sow_ops,
                        'gilt_ops':             cur_ver_num_gilt_ops,   
                        'weaning_sow_ops':      cur_ver_num_weaning_sow_ops,
                        
                        'account':              cur_ver_num_account,
                        'pig_buyer':            cur_ver_num_pig_buyer
                    }
                }
                
                return cur_entry
            
            else:
                return [
                    cur_ver_num_gestating_ops,        
                    cur_ver_num_lactating_piglets_ops,
                    cur_ver_num_lactating_sow_ops,    
                    cur_ver_num_gilt_ops,             
                    cur_ver_num_weaning_sow_ops,      
                    
                    cur_ver_num_account,
                    cur_ver_num_pig_buyer              
                ]

        return None

