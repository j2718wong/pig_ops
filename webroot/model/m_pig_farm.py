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



# The account.flag_settings will be broken down so that
# it will be easier to read in the application level.
# See account_register.sql for updated flag bits definition.

"""
/* account.flag_setting bits
FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
0 = Date of birth is counted as DAY 0
1 = Date of birth is counted as DAY 1; default

FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
0 = Date of insemination is counted as DAY 0; default
1 = Date of insemination is counted as DAY 1;


*/

"""

FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH     = 1
FLAG_BIT_DAY_1_ON_DATE_OF_INSEM     = 2
            

class PigFarm(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        
        
    def add(self, data = None):
        """
        PROCEDURE pig_farm_add(
            in_user_id              INT,

            in_name                 VARCHAR(50),
            
            in_new_country_code     VARCHAR(5),
            in_new_country_name     VARCHAR(50),
            
            
            in_country_id           INT, 
            in_address_level_1_id   INT,
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5),
            
            in_num_farrowing_crates INT
    
        )  
        """
        
        params = [
            data.user_id,
            data.name               if data.name and data.name.strip() else None,
            
            data.new_country_code   if data.new_country_code else None,
            data.new_country_name   if data.new_country_name else None,
            
            data.country_id,
            data.level_1_id,
            data.level_2_id,
            data.level_3_id,
            
            data.latitude           if data.latitude is not None else None,
            data.longitude          if data.longitude is not None else None,
            
            data.num_farrowing_crates
        ]
        
        # DEBUG: Print the procedure call string 
        # debug_sql = self._generate_debug_procedure('pig_farm_add', params)
        
        rows = self._call_procedure('pig_farm_add', params)
        
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
                
                'pig_farm': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None

    
    def update_hashid(self, data = None):
        pig_farm_id     = data['pig_farm_id']
        hashid          = data['hashid']
        
        values = (hashid, pig_farm_id)
        
        sql =   """
                UPDATE pig_farm SET
                    hashid    = "%s"
                WHERE id = %s;
                """ % values
        
        return self.model.execute_sql(sql)
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_farm_update(
            in_user_id              INT,
            in_pig_farm_id          INT,

            in_name                 VARCHAR(50),
            
            in_address_level_1_id   INT,
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5),
            
            in_num_farrowing_crates INT
        )
        """
       
        params = [
            data.user_id,
            data.pig_farm_id,
            data.name               if data.name and data.name.strip() else None,
            
            data.level_1_id,
            data.level_2_id,
            data.level_3_id,
            
            data.latitude           if data.latitude is not None else None,
            data.longitude          if data.longitude is not None else None,
            
            data.num_farrowing_crates
        ]
        
        rows = self._call_procedure('pig_farm_update', params)
        
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
                
                'pig_farm': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }
                
            
        return None
    
    
    def update_fixed_expenses(self, data = None):
        """
        PROCEDURE pig_farm_update_fixed_expense(
            in_user_id              INT,
            in_pig_farm_id          INT,
            
            
            in_budget_electric      DECIMAL(8,2),
            in_budget_water         DECIMAL(8,2),
            in_budget_internet      DECIMAL(8,2),
            in_budget_staff         DECIMAL(8,2),
            in_budget_fuel          DECIMAL(8,2),
            in_budget_supplies      DECIMAL(8,2),
            in_budget_other         DECIMAL(8,2)
        )
        """
       
        params = [
            data.user_id,
            data.pig_farm_id,
            
            data.budget_electric    if data.budget_electric  else None,
            data.budget_water       if data.budget_water  else None,
            data.budget_internet    if data.budget_internet  else None,
            data.budget_staff       if data.budget_staff  else None,
            data.budget_fuel        if data.budget_fuel  else None,
            data.budget_supplies    if data.budget_supplies else None,
            data.budget_other       if data.budget_other else None
        ]
        
        rows = self._call_procedure('pig_farm_update_fixed_expense', params)
        
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
                
                'pig_farm': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }
                
            
        return None

    
    def get_pig_farm_info(self, pig_farm_id):
        """
        Get pig farm information with associated account and country details.
        
        Parameters
        ==========
        pig_farm_id : int
            The ID of the pig farm to retrieve
        
        Returns
        -------
        dict
            Dictionary containing farm, account, and country information
        """
        
        sql = """
            SELECT 
                a.id,
                a.name,
                
                a.account_id,
                b.name,
                
                a.country_id,
                c.name,
                c.flag,
                
                a.address_level_1_id,
                a.address_level_2_id,
                a.address_level_3_id,
                a.latitude,
                a.longitude,
                
                a.num_farrowing_crates
                
            FROM pig_farm a
            LEFT OUTER JOIN account b       ON a.account_id = b.id
            LEFT OUTER JOIN app_country c   ON a.country_id = c.id
            WHERE a.id = %s
        """ % pig_farm_id

        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
        
        
        for row in rows:
            # Farm basic info
            cur_farm_id                     = row[0]
            cur_farm_name                   = row[1]
            
            # Account info
            cur_account_id                  = row[2]
            cur_account_name                = row[3]
            
            # Country info
            cur_country_id                  = row[4]
            cur_country_name                = row[5]
            cur_country_flag                = row[6]
            
            # Address levels
            cur_address_level_1_id          = row[7]  
            cur_address_level_2_id          = row[8]  
            cur_address_level_3_id          = row[9]  

            # Location
            cur_farm_latitude               = row[10] 
            cur_farm_longitude              = row[11] 

            cur_num_farrowing_crates        = row[12] 
            
            
            # Build the result dictionary
            cur_entry = {
                'pig_farm': {
                    'id':           cur_farm_id, 
                    'name':         cur_farm_name,
                    'num_farrow_crates': cur_num_farrowing_crates
                },
                
                'account': {
                    'id':           cur_account_id,
                    'name':         cur_account_name
                },
                
                'location':{
                    'country': {
                        'id':       cur_country_id,
                        'name':     cur_country_name,
                        'flag':     cur_country_flag
                    },
                    
                    'address':{
                        'level_1':  {
                            'id':   cur_address_level_1_id
                        },
                        
                        'level_2':  {
                            'id':   cur_address_level_2_id
                        },
                        
                        'level_3': {
                            'id':   cur_address_level_3_id
                        }
                    },
                    
                    'geoloc':{
                        'latitude':  cur_farm_latitude,
                        'longitude': cur_farm_longitude,
                    }
                }
            }
            
            return cur_entry
    
        return None
    
    
    def get_pig_farm_account_info(self, pig_farm_id):
        sql =   """
                SELECT 
                    a.account_id,
                    b.name,
                    
                    b.current_bill_id,
                    c.status_id,
                    c.bill_reference,
                    c.date_bill_start,
                    c.date_bill_end,
                    c.date_issue,
                    c.date_due,
                    c.currency_code,
                    c.amount,
                    
                    b.weight_unit,
                    b.currency,
                    b.flag_settings,
                    b.num_days_move_to_farrow,
                    b.num_days_wean,
                    b.num_days_harvest_from_birth,
                    b.num_days_harvest_from_wean,
                    
                    d.name_last,
                    d.name_first,
                    b.dt_last_update_settings
                FROM pig_farm a
                LEFT OUTER JOIN account b       ON a.account_id = b.id
                LEFT OUTER JOIN account_bill c  ON b.current_bill_id = c.id
                LEFT OUTER JOIN user d          ON b.last_update_settings_user_id = d.id
                WHERE a.id = %s
                """ % pig_farm_id
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
            
        for row in rows:
            cur_acc_id                  = row[0]
            cur_acc_name                = row[1]
                
                
            cur_bill_id                 = row[2]
            cur_bill_status_id          = row[3]
            cur_bill_reference          = row[4]
            cur_bill_date_bill_start    = str(row[5]) if row[5] else None
            cur_bill_date_bill_end      = str(row[6]) if row[6] else None
            cur_bill_date_issue         = str(row[7]) if row[7] else None
            cur_bill_date_due           = str(row[8]) if row[8] else None
            cur_bill_currency_code      = row[9]
            cur_bill_amount             = float(row[10]) if row[10] is not None else None
            
            cur_acc_weight_unit         = row[11]
            cur_acc_currency            = row[12]
            cur_acc_settings_flag       = row[13]
            cur_acc_num_days_move_to_farrow     = row[14]
            cur_acc_num_days_wean               = row[15]
            cur_acc_num_days_harvest_from_birth = row[16]
            cur_acc_num_days_harvest_from_wean  = row[17]
            
                           
            cur_user_name_last          = row[18]
            cur_user_name_first         = row[19]
            cur_settings_last_update    = str(row[20]) if row[20] else None
            
            
            
            
            temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_BIRTH
            cur_flag_day_1_on_dob   = 1 if temp > 0 else 0
            
            temp = cur_acc_settings_flag & FLAG_BIT_DAY_1_ON_DATE_OF_INSEM
            cur_flag_day_1_on_doi   = 1 if temp > 0 else 0
            
            
            
            cur_entry = {
                'account': {
                    'id':               cur_acc_id,
                    'name':             cur_acc_name
                },
                
                'account_bill':{
                    'id':               cur_bill_id,
                    'status_id':        cur_bill_status_id,
                    'reference':        cur_bill_reference,
                    'date_bill_start':  cur_bill_date_bill_start,
                    'date_bill_end':    cur_bill_date_bill_end,
                    'date_issue':       cur_bill_date_issue,
                    'date_due':         cur_bill_date_due,
                    'currency_code':    cur_bill_currency_code,
                    'amount':           cur_bill_amount
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
                }
            }
            
            return cur_entry
    
        return None
        
    
    def get_pig_farm_fixed_expenses(self, pig_farm_id):
        """
        Get pig farm fixed expenses.
        
        Parameters
        ==========
        pig_farm_id : int
            The ID of the pig farm to retrieve
        
        Returns
        -------
        dict
            
        """
        
        sql = """
            SELECT 
                fixed_expense_electric,    
                fixed_expense_water,       
                fixed_expense_internet,    
                fixed_expense_staff,       
                fixed_expense_fuel,        
                fixed_expense_supplies,    
                fixed_expense_other,
                
                data_ver_num_fixed_expense
                
            FROM pig_farm
            WHERE id = %s
        """ % pig_farm_id

        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
        
        
        for row in rows:
            cur_expense_electric            = float(row[0]) if row[0] else 0.0    
            cur_expense_water               = float(row[1]) if row[1] else 0.0      
            cur_expense_internet            = float(row[2]) if row[2] else 0.0   
            cur_expense_staff               = float(row[3]) if row[3] else 0.0      
            cur_expense_fuel                = float(row[4]) if row[4] else 0.0       
            cur_expense_supplies            = float(row[5]) if row[5] else 0.0   
            cur_expense_other               = float(row[6]) if row[6] else 0.0
            
            cur_ver_num_fixed_expense       = row[7]
            
            
            # Build the result dictionary
            cur_entry = {
                'fixed_expense': {
                    'electric':     cur_expense_electric,
                    'water':        cur_expense_water,   
                    'internet':     cur_expense_internet,
                    'staff':        cur_expense_staff,   
                    'fuel':         cur_expense_fuel,    
                    'supplies':     cur_expense_supplies,
                    'other':        cur_expense_other
                },
                
                'data_ver_num': {
                    'fixed_expenses': cur_ver_num_fixed_expense
                }
            }
            
            return cur_entry
    
        return None
    
    
    def get_list(self, account_id = 0, id_list = None):
        """
        Will get pig farm list.
        
        
        Returns
        -------
        list of dictionary

        """
        
        if account_id > 0:
            where_clause = 'account_id = %s' % account_id
        else:
            s = ''
            index = 0
            for cur_entry in id_list:
                if index > 0: s += ','
                s += str(cur_entry)
                index += 1
                
        
            
            where_clause = 'a.id IN (%s)' % s
            
        sql =   """
                SELECT 
                    a.id,
                    a.flag,
                    a.name,
                    
                    a.country_id,
                    b.name AS country_name,
                    b.flag AS country_flag,
                    
                    a.address_level_1_id,
                    a.address_level_2_id,
                    a.address_level_3_id,
                    a.latitude,
                    a.longitude,
                    
                    a.num_farrowing_crates,
                    
                    a.data_ver_num_sow,
                    a.data_ver_num_boar,     
                    a.data_ver_num_pig_prod, 
                    a.data_ver_num_prod_history, 
                    a.data_ver_num_staff,    
                    
                    a.data_ver_num_feed_buy,
                    a.data_ver_num_feed_balance,
                    a.data_ver_num_not_pregnant,
                    a.data_ver_num_boar_ext_mate,
                    a.data_ver_num_pig_dead,
                    
                    a.data_ver_num_sd_chklst,
                    a.data_ver_num_sb_disposed,
                    a.data_ver_num_prod_gesta, 
                    a.data_ver_num_prod_lacta,  
                    a.data_ver_num_prod_fatten,
                    
                    a.data_ver_num_fixed_expense
                    
                FROM pig_farm a
                LEFT OUTER JOIN app_country b ON a.country_id = b.id
                WHERE %s
                """ % where_clause
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        

        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_farm_id                     = row[0]
                cur_farm_flag                   = row[1]
                cur_farm_name                   = row[2]
                        
                cur_country_id                  = row[3]
                cur_country_name                = row[4]
                cur_country_flag                = row[5]

                cur_farm_address_level_1_id     = row[6]
                cur_farm_address_level_2_id     = row[7]
                cur_farm_address_level_3_id     = row[8]
                cur_farm_latitude               = float(row[9]) if row[9] else None
                cur_farm_longitude              = float(row[10]) if row[10] else None

                cur_num_farrowing_crates        = row[11]

                cur_data_ver_num_sow            = row[12]
                cur_data_ver_num_boar           = row[13]
                cur_data_ver_num_pig_prod       = row[14]
                cur_data_ver_num_prod_history   = row[15]
                cur_data_ver_num_staff          = row[16]
                
                cur_data_ver_num_feed_buy       = row[17]
                cur_data_ver_num_feed_balance   = row[18]
                cur_data_ver_num_not_pregnant   = row[19]
                cur_data_ver_num_boar_ext_mate  = row[20]
                cur_data_ver_num_pig_dead       = row[21]
                
                cur_data_ver_num_sd_chklst      = row[22]
                cur_data_ver_num_sb_disposed    = row[23]
                cur_data_ver_num_prod_gesta     = row[24]
                cur_data_ver_num_prod_lacta     = row[25]
                cur_data_ver_num_prod_fatten    = row[26]
                
                cur_data_ver_num_fixed_expense  = row[27]
                
                
                
                cur_entry = {
                    'pig_farm': {
                        'id':           cur_farm_id, 
                        'flag':         cur_farm_flag,
                        'name':         cur_farm_name,
                        'num_farrow_crates': cur_num_farrowing_crates
                    },
                    
                    'location':{
                        'country': {
                            'id':       cur_country_id,
                            'name':     cur_country_name,
                            'flag':     cur_country_flag
                        },
                        
                        'address':{
                            'level_1':  {
                                'id':   cur_farm_address_level_1_id
                            },
                            
                            'level_2':  {
                                'id':   cur_farm_address_level_2_id
                            },
                            
                            'level_3': {
                                'id':   cur_farm_address_level_3_id
                            }
                        },
                        
                        'geoloc':{
                            'latitude':  cur_farm_latitude,
                            'longitude': cur_farm_longitude,
                        }
                    },
                    
                    'data_ver_num':{
                        'sow':              cur_data_ver_num_sow,       
                        'boar':             cur_data_ver_num_boar,    
                        'pig_prod':         cur_data_ver_num_pig_prod,
                        'prod_history':     cur_data_ver_num_prod_history,
                        'staff':            cur_data_ver_num_staff,   
                        
                        'feed_buy':         cur_data_ver_num_feed_buy,
                        'feed_balance':     cur_data_ver_num_feed_balance,
                        'not_pregnant':     cur_data_ver_num_not_pregnant,
                        'boar_ext_mate':    cur_data_ver_num_boar_ext_mate,
                        'pig_dead':         cur_data_ver_num_pig_dead,
                        
                        'checklist':        cur_data_ver_num_sd_chklst,  
                        'sb_disposed':      cur_data_ver_num_sb_disposed,
                        'prod_gesta':       cur_data_ver_num_prod_gesta, 
                        'prod_lacta':       cur_data_ver_num_prod_lacta, 
                        'prod_fatten':      cur_data_ver_num_prod_fatten,
                        
                        'fixed_expense':    cur_data_ver_num_fixed_expense
                            
                    }
                    
                }
                
                result.append(cur_entry)

        return result
    
    
    def get_sow_boar_balance(self, pig_farm_id):
        sql =   """
                SELECT 
                    b.date_balance,
                    b.num_sows,
                    b.num_sows_gestating,
                    b.num_sows_lactating,
                    
                    b.num_boars,
                    b.num_gestating,
                    b.num_finisher
                FROM pig_farm a
                LEFT OUTER JOIN sow_boar_balance b ON a.last_sow_boar_balance_id = b.id
                WHERE pig_farm_id = %s
                """ % pig_farm_id
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None
        
            
        for row in rows:
           
            cur_entry = {
                'date_balance':         str(row[0]), 
                
                'sows': {
                    'total':            row[1],
                    'num_gestating':    row[2],
                    'num_lactating':    row[3],
                },
                
                'boars':                row[4],
                
                'feed_balance': {
                    'num_gestating':    float(row[5]) if row[5] else None,
                    'num_finisher':     float(row[6]) if row[6] else None
                }
                
                
            }
            
            return cur_entry
        
        return None
        
    
    def get_data_ver_num(self, pig_farm_id, return_array = 0):
        sql =   """
                SELECT
                    data_ver_num_sow,
                    data_ver_num_boar,     
                    data_ver_num_pig_prod,
                    data_ver_num_prod_history,
                    data_ver_num_staff, 
                       
                    data_ver_num_feed_buy,
                    data_ver_num_feed_balance,
                    data_ver_num_not_pregnant,
                    data_ver_num_boar_ext_mate,
                    data_ver_num_pig_dead,
                    
                    data_ver_num_sd_chklst,
                    data_ver_num_sb_disposed,
                    data_ver_num_prod_gesta, 
                    data_ver_num_prod_lacta,  
                    data_ver_num_prod_fatten,
                    
                    data_ver_num_fixed_expense
                    
                FROM pig_farm 
                WHERE id = %s
                """ % pig_farm_id
        
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return None

            
        for row in rows:
            cur_data_ver_num_sow            = row[0]
            cur_data_ver_num_boar           = row[1]   
            cur_data_ver_num_pig_prod       = row[2]
            cur_data_ver_num_prod_history   = row[3]
            cur_data_ver_num_staff          = row[4]
              
            cur_data_ver_num_feed_buy       = row[5]
            cur_data_ver_num_feed_balance   = row[6]
            cur_data_ver_num_not_pregnant   = row[7]
            cur_data_ver_num_boar_ext_mate  = row[8]
            cur_data_ver_num_pig_dead       = row[9]
            
            cur_data_ver_num_sd_chklst      = row[10]
            cur_data_ver_num_sb_disposed    = row[11]
            cur_data_ver_num_prod_gesta     = row[12]
            cur_data_ver_num_prod_lacta     = row[13]
            cur_data_ver_num_prod_fatten    = row[14]
            
            cur_data_ver_num_fixed_expense  = row[15]

            
            if return_array == 0:
                cur_entry = {
                    'data_ver_num': {
                        'sow':              cur_data_ver_num_sow,       
                        'boar':             cur_data_ver_num_boar,    
                        'pig_prod':         cur_data_ver_num_pig_prod,
                        'prod_history':     cur_data_ver_num_prod_history,
                        'staff':            cur_data_ver_num_staff,   
                        
                        'feed_buy':         cur_data_ver_num_feed_buy,
                        'feed_balance':     cur_data_ver_num_feed_balance,
                        'not_pregnant':     cur_data_ver_num_not_pregnant,
                        'boar_ext_mate':    cur_data_ver_num_boar_ext_mate,
                        'pig_dead':         cur_data_ver_num_pig_dead,
                        
                        'sow_due_checklist':cur_data_ver_num_sd_chklst,
                        'sow_boar_disposed':cur_data_ver_num_sb_disposed,
                        'prod_gesta':       cur_data_ver_num_prod_gesta, 
                        'prod_lacta':       cur_data_ver_num_prod_lacta, 
                        'prod_fatten':      cur_data_ver_num_prod_fatten,
                        
                        'fixed_expense':    cur_data_ver_num_fixed_expense     
                        
                    }
                }
                
                return cur_entry
            
            else:
                return [
                    cur_data_ver_num_sow,        
                    cur_data_ver_num_boar,       
                    cur_data_ver_num_pig_prod,
                    cur_data_ver_num_prod_history,   
                    cur_data_ver_num_staff,
                          
                    cur_data_ver_num_feed_buy,
                    cur_data_ver_num_feed_balance,   
                    cur_data_ver_num_not_pregnant,
                    cur_data_ver_num_boar_ext_mate,
                    cur_data_ver_num_pig_dead,
                    
                    cur_data_ver_num_sd_chklst,
                    cur_data_ver_num_sb_disposed,
                    cur_data_ver_num_prod_gesta, 
                    cur_data_ver_num_prod_lacta, 
                    cur_data_ver_num_prod_fatten,
                    
                    cur_data_ver_num_fixed_expense 
                ]

        return None
