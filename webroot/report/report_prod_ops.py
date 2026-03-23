# March 21, 2026
# Jack Wong

import os
import sys
import pprint

from datetime               import datetime, timedelta

from common_constants       import *
from common_app             import *
from common_fast_api        import *




# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)
webroot_directory           = os.path.dirname(module_directory)


# Add route directory to Python path
route_dir = os.path.join(module_directory, 'route')
if route_dir not in sys.path:
    sys.path.insert(0, route_dir)

# Add templates_report directory
templates_report_dir = os.path.join(webroot_directory, 'templates_report')
if templates_report_dir not in sys.path:
    sys.path.insert(0, templates_report_dir)



from r_utils                import get_location_address_names_and_replace_ids
from r_pig_production       import get_pig_prod_list
 


if module_directory not in sys.path:
    sys.path.append(module_directory)



class ReportBasic:
    def __init__(self):
        pass


"""

2026-03-22: Notes on feeds in general;
        
1.) The farm buys all feeds at once for production and non-production feeds.
    Usually for small farms, feeds are bought gradually, not all at once. 
    Not sure with how big farms work.
    
    Production feeds means for lactating sows, weaned piglets and fattening.
    
    Non-production feeds are for gestating sows and boars and other pigs not tracked;
    The gestating feeds per production are not tracked because it does not 
    make sense, unless somebody will really request this. The system is ready 
    for this. Currently it is not just accounted as production feeds.
    
    But lactating feeds are tracked per production feeds.  

2.) To track how much feed goes to each production entry somebody must record
    the feed allocation per batch. The  current piglet feed type system
    is a predictable system. This is the typical consumption per batch
    from pig birth to 140-142 days harvest (based on My current pig farm 
    records).
    
    
    For sow     for piglets
    lactating   booster-->prestarter-->starter-->grower-->finisher
    
    
    Feed Type       Typical consumption
    =========       ==========
    lactating       100kg to 150 kg     (2 to 3  50kg sacks)
    booster         <20kg               (20 1kg packs)
    prestarter      25kg to 50kg        (1 to 2  25 kg sacks)
    starter         50 kg per pig
    grower          100 kg per pig
    finisher        50 kg per pig
    
    
3.) When a feed is allocated to a production entry, it will add all 
    feeds quantities and cost of that type and will be saved in production.feeds.bought
    and feeds.cost
     
    
     
4.) Technical details

Database table      what is saved
=================   =================
pig_farm_feed_buy   feed supplier, when it was bought,
feed_buy            type of feeds, quantity, price, toal cost

pig_prod_feed       relates feed allocation per production and pig_farm_feed_buy.
                

feed_buy            feed details for pig_farm_feed_buy,  pig_prod_feed;
                    
                    it is related to multiple keys
                    
                    pig_farm_id         
                    pig_prod_id         
                    pig_prod_group_id   
                    pig_prod_feed_id    
                    pig_farm_feed_buy_id

     

mysql> DESCRIBE pig_farm_feed_buy;
+---------------------+---------------+------+-----+-------------------+-------------------+
| Field               | Type          | Null | Key | Default           | Extra             |
+---------------------+---------------+------+-----+-------------------+-------------------+
| id                  | int unsigned  | NO   | PRI | NULL              | auto_increment    |
| account_id          | int unsigned  | NO   |     | 0                 |                   |
| pig_farm_id         | int           | YES  | MUL | NULL              |                   |
| date_buy            | date          | YES  |     | NULL              |                   |
| feed_supplier_id    | int           | YES  |     | NULL              |                   |
| total_feed_cost     | decimal(10,2) | YES  |     | NULL              |                   |
| other_cost          | decimal(8,2)  | YES  |     | NULL              |                   |
| added_by_user_id    | int           | YES  |     | NULL              |                   |
| last_update_user_id | int           | YES  |     | NULL              |                   |
| dt_last_update      | datetime      | YES  |     | NULL              |                   |
| dt_entry            | datetime      | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+---------------------+---------------+------+-----+-------------------+-------------------+


mysql> DESCRIBE pig_prod_feed;
+----------------------+--------------+------+-----+-------------------+-------------------+
| Field                | Type         | Null | Key | Default           | Extra             |
+----------------------+--------------+------+-----+-------------------+-------------------+
| id                   | int unsigned | NO   | PRI | NULL              | auto_increment    |
| pig_prod_id          | int unsigned | NO   | MUL | 0                 |                   |
| pig_farm_feed_buy_id | int unsigned | YES  |     | NULL              |                   |
| date_add             | date         | YES  |     | NULL              |                   |
| added_by_user_id     | int          | YES  |     | NULL              |                   |
| last_update_user_id  | int          | YES  |     | NULL              |                   |
| dt_last_update       | datetime     | YES  |     | NULL              |                   |
| dt_entry             | datetime     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+----------------------+--------------+------+-----+-------------------+-------------------+



mysql> DESCRIBE feed_buy;
+----------------------+--------------+------+-----+-------------------+-------------------+
| Field                | Type         | Null | Key | Default           | Extra             |
+----------------------+--------------+------+-----+-------------------+-------------------+
| id                   | int unsigned | NO   | PRI | NULL              | auto_increment    |
| pig_farm_id          | int unsigned | YES  | MUL | NULL              |                   |
| pig_prod_id          | int unsigned | YES  | MUL | NULL              |                   |
| pig_prod_group_id    | int unsigned | YES  | MUL | NULL              |                   |
| pig_prod_feed_id     | int unsigned | YES  | MUL | NULL              |                   |
| pig_farm_feed_buy_id | int unsigned | YES  | MUL | NULL              |                   |
| flag                 | int unsigned | YES  |     | 0                 |                   |
| date_buy             | date         | YES  |     | NULL              |                   |
| feed_type_id         | int unsigned | YES  |     | NULL              |                   |
| feed_brand_id        | int unsigned | YES  |     | NULL              |                   |
| feed_supplier_id     | int unsigned | YES  |     | NULL              |                   |
| quantity             | int          | YES  |     | NULL              |                   |
| kg_per_unit          | decimal(5,1) | YES  |     | NULL              |                   |
| kg_total             | decimal(6,1) | YES  |     | NULL              |                   |
| unit_cost            | decimal(8,2) | YES  |     | NULL              |                   |
| total_cost           | decimal(8,2) | YES  |     | NULL              |                   |
| added_by_user_id     | int          | YES  |     | NULL              |                   |
| last_update_user_id  | int          | YES  |     | NULL              |                   |
| dt_last_update       | datetime     | YES  |     | NULL              |                   |
| dt_entry             | datetime     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+----------------------+--------------+------+-----+-------------------+-------------------+

Typical production_entry data:
{
 'pig_production': {},
 
 'insemination': {}, 
    
 'feeds': {'balance': {'booster': None,
               'date_balance': None,
               'finisher': None,
               'gestating': None,
               'grower': None,
               'lactating': None,
               'prestarter': None,
               'starter': None},
   'bought': {'booster': None,
              'finisher': None,
              'gestating': None,
              'grower': None,
              'lactating': None,
              'prestarter': None,
              'starter': None},
   'cost': {'booster': None,
            'finisher': None,
            'gestating': None,
            'grower': None,
            'lactating': None,
            'prestarter': None,
            'starter': None},
   'date_change_feed': {'booster': None,
                        'finisher': None,
                        'gestating': None,
                        'grower': None,
                        'lactating': None,
                        'prestarter': None,
                        'starter': None},
                        
                        
    'consumed': {'booster': None,
            'finisher': None,
            'gestating': None,
            'grower': None,
            'lactating': None,
            'prestarter': None,
            'starter': None},
                        
    }
}

"""
        




class ReportProdOps(ReportBasic):
    def __init__(self):
        super().__init__()
        
        
    def _calculate_feed_consumed(self, cur_entry):
        cur_feeds           = cur_entry['feeds']
        cur_feed_buy        = cur_feeds['bought']
        cur_feed_balance    = cur_feeds['balance']
        
        consumed = {
            'lactating':    None,
            'booster':      None,
            'prestarter':   None,
            'starter':      None,
            'grower':       None,
            'finisher':     None
        }
        
        if cur_feed_buy['lactating'] is not None:
            if cur_feed_balance['lactating'] is not None:
                consumed['lactating'] = cur_feed_buy['lactating']   - cur_feed_balance['lactating']
                
        if cur_feed_buy['booster'] is not None:
            if cur_feed_balance['booster'] is not None:
                consumed['booster'] = cur_feed_buy['booster']       - cur_feed_balance['booster']
                
        if cur_feed_buy['prestarter'] is not None:
            if cur_feed_balance['prestarter'] is not None:
                consumed['prestarter'] = cur_feed_buy['prestarter'] - cur_feed_balance['prestarter']
        
        if cur_feed_buy['starter'] is not None:
            if cur_feed_balance['starter'] is not None:
                consumed['starter'] = cur_feed_buy['starter']       - cur_feed_balance['starter']
        
        if cur_feed_buy['grower'] is not None:
            if cur_feed_balance['grower'] is not None:
                consumed['grower'] = cur_feed_buy['grower']         - cur_feed_balance['grower']
        
        if cur_feed_buy['finisher'] is not None:
            if cur_feed_balance['finisher'] is not None:
                consumed['finisher'] = cur_feed_buy['finisher']     - cur_feed_balance['finisher']
        
        cur_entry['consumed'] = consumed
        
        
    def _add_feed_balance(self, total, cur_entry):
        cur_feeds           = cur_entry['feeds']
        cur_feed_buy        = cur_feeds['bought']
        cur_feed_balance    = cur_feeds['balance']
        cur_feed_cost       = cur_feeds['cost']
        
        
        if cur_feed_balance['lactating'] is not None:
            if total['lactating'] is None:
                total['lactating'] = cur_feed_balance['lactating']
            else:
                total['lactating'] += cur_feed_balance['lactating']
        
        
        if cur_feed_balance['booster'] is not None:
            if total['booster'] is None:
                total['booster'] = cur_feed_balance['booster']
            else:
                total['booster'] += cur_feed_balance['booster']
        
        
        if cur_feed_balance['prestarter'] is not None:
            if total['prestarter'] is None:
                total['prestarter'] = cur_feed_balance['prestarter']
            else:
                total['prestarter'] += cur_feed_balance['prestarter']
        
        
        if cur_feed_balance['starter'] is not None:
            if total['starter'] is None:
                total['starter'] = cur_feed_balance['starter']
            else:
                total['starter'] += cur_feed_balance['starter']
        
        
        if cur_feed_balance['grower'] is not None:
            if total['grower'] is None:
                total['grower'] = cur_feed_balance['grower']
            else:
                total['grower'] += cur_feed_balance['grower']
        
        
        if cur_feed_balance['finisher'] is not None:
            if total['finisher'] is None:
                total['finisher'] = cur_feed_balance['finisher']
            else:
                total['finisher'] += cur_feed_balance['finisher']
        
        
        
        prod_feed_cost = 0.0
        
        
        if cur_feed_cost['lactating'] is not None:
            prod_feed_cost += cur_feed_cost['lactating']
        
        
        if cur_feed_cost['booster'] is not None:
            prod_feed_cost += cur_feed_cost['booster']
        
        
        if cur_feed_cost['prestarter'] is not None:
            prod_feed_cost += cur_feed_cost['prestarter']
        
        
        if cur_feed_cost['starter'] is not None:
            prod_feed_cost += cur_feed_cost['starter']
        
        
        if cur_feed_cost['grower'] is not None:
            prod_feed_cost += cur_feed_cost['grower']
        
        
        if cur_feed_cost['finisher'] is not None:
            prod_feed_cost += cur_feed_cost['finisher']
        
        return prod_feed_cost
        
        
        
    def get_data(self, pig_farm_id, inc_historical=0, inc_cost=0, 
            inc_target_harvest = 0):
        """
        Fetch all data needed for the report.
        """
        
        
        # Get pig farm info
        pig_farm_info       = model['pig_farm'].get_pig_farm_info(pig_farm_id)
        get_location_address_names_and_replace_ids(pig_farm_info)
        
        print('pig_farm_info')
        print(pig_farm_info)
        
        # Get account info
        account_id          = pig_farm_info['account']['id']  
        account_info        = model['account'].get_info(account_id)
        settings_operations = account_info['settings_operations'] 
        
        
        
        # Get all active production list (type 5 = all active)
        pig_prod_list = model['pig_prod'].get_list(pig_farm_id, pig_prod_type=5)
        
        # Filter and enhance gestating sows with their operations
        list_gestating  = []
        
        list_lactating  = []
        
        list_fattening  = []
        
        
        # Total Feed balance for production
        # The production feed balance is assumed that each production feed balance
        # has the same date. Otherwise this is wrong.
        prod_feed_balance = {
            'lactating':    None,
            'booster':      None,
            'prestarter':   None,
            'starter':      None,
            'grower':       None,
            'finisher':     None
        }
        
        prod_feed_cost = 0.0
        

        for cur_entry in pig_prod_list:
            prod_status_id = cur_entry['pig_production']['prod_status_id']
            
            self._calculate_feed_consumed(cur_entry)
            
            if prod_status_id == PROD_STATUS_ID_GESTATING:
                
                # Calculate days since insemination
                insem_date = cur_entry['insemination']['insem_date']
                if insem_date:
                    dt_insem = datetime.strptime(insem_date, '%Y-%m-%d')
                    days_since = (datetime.now() - dt_insem).days
                    cur_entry['insemination']['days_since_insem'] = days_since
                
                
                # Get gestating operations for this production
                operation_type = PIG_OPERATION_TYPE_GESTATING
                pig_prod_id = cur_entry['pig_production']['id']
                
                res = model['pig_prod_pig_ops'].get_list(
                    operation_type, 
                    pig_prod_id=pig_prod_id, 
                    inc_user_audit=0, 
                    order_by=0
                )
                
                cur_entry['gestating_ops'] = res
                list_gestating.append(cur_entry)
            
            
            if prod_status_id == PROD_STATUS_ID_LACTATING:
                # Get lactating operations for this production
                
                operation_type = PIG_OPERATION_TYPE_LACTATING_COMBINED
                pig_prod_id = cur_entry['pig_production']['id']
                
                res = model['pig_prod_pig_ops'].get_list(
                    operation_type, 
                    pig_prod_id=pig_prod_id, 
                    inc_user_audit=0, 
                    order_by=0
                )
                
                cur_entry['lactating_ops'] = res
                list_lactating.append(cur_entry)
                
                
                # Add to feed Balance
                prod_feed_cost += self._add_feed_balance(prod_feed_balance, cur_entry)
                
            
            if  prod_status_id == PROD_STATUS_ID_WEANING  or prod_status_id == PROD_STATUS_ID_GROWING:
                
                
                list_fattening.append(cur_entry)

                # Add to feed Balance
                prod_feed_cost += self._add_feed_balance(prod_feed_balance, cur_entry)
            


        farm_settings = self._get_farm_settings(pig_farm_id)

        
        pprint.pprint(list_fattening[0])
        
        
        # Prepare data for template
        data = {
            'pig_farm_info':        pig_farm_info,
            'acc_settings_ops':     settings_operations,
            'farm_settings':        farm_settings,
            'list_gestating':       list_gestating,
            'list_lactating':       list_lactating,
            'list_fattening':       list_fattening,
            
            'prod_feed_balance':    prod_feed_balance,
            'prod_feed_cost':       prod_feed_cost,
            
            'inc_historical':       False,
            'inc_cost':             inc_cost,
            'inc_target_harvest':   inc_target_harvest
        }
        
        return data
    
    
    def _get_farm_settings(self, pig_farm_id):
        """
        Get farm-specific settings for reports.
        You can store these in a farm_settings table, or use defaults.
        """

        return {
            'report_title':     'Pig Farm Summary Report',
            'report_subtitle':  None
        }
    
    
    def _get_boar_display(self, sow):
        """
        Get display string for boar/semen information.
        """
        insem_type = sow['insemination']['insem_type']
        
        if insem_type == 'B':
            # Natural mating with boar
            boar = sow['insemination']['boar']
            if boar and boar.get('name'):
                return boar['name']
            elif boar and boar.get('number'):
                return boar['number']
            return "Unknown Boar"
        
        elif insem_type == 'AI_X':
            # External AI - semen from supplier
            ai = sow['insemination']['ai']
            if ai and ai.get('semen_supplier') and ai['semen_supplier'].get('semen'):
                return ai['semen_supplier']['semen']['name']
            return "External AI"
        
        elif insem_type == 'AI_N':
            # Internal AI - semen from farm boar
            ai = sow['insemination']['ai']
            if ai and ai.get('internal_boar'):
                internal_boar = ai['internal_boar']
                if internal_boar.get('name'):
                    return internal_boar['name']
                elif internal_boar.get('number'):
                    return internal_boar['number']
            return "Internal AI"
        
        return "Unknown"
        

    def _calculate_days(self, entry):
        """Calculate days since various events"""
        # Days since insemination
        insem_date = entry['insemination']['insem_date']
        if insem_date:
            dt_insem = datetime.strptime(insem_date, '%Y-%m-%d')
            days_since = (datetime.now() - dt_insem).days
            entry['insemination']['days_since_insem'] = days_since
            
            # Create formatted display string
            # Format: 20 NOV 2025 (Day 121)
            formatted_date = datetime.strftime(dt_insem, '%d %b %Y').upper()
            entry['insemination']['mating_display'] = f"{formatted_date} (Day {days_since})"
