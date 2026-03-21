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



class ReportProdOps(ReportBasic):
    def __init__(self):
        super().__init__()
        
        
    def get_data(self, pig_farm_id, inc_historical=0, inc_cost=0, inc_target_harvest=0):
        """
        Fetch all data needed for the report.
        """
        # Get pig farm info
        pig_farm_info = model['pig_farm'].get_pig_farm_info(pig_farm_id)
        get_location_address_names_and_replace_ids(pig_farm_info)
        
        print('pig_farm_info')
        pprint.pprint(pig_farm_info)
        
        

        
        # Get all active production list (type 5 = all active)
        pig_prod_list = model['pig_prod'].get_list(pig_farm_id, pig_prod_type=5)
        
        # Filter and enhance gestating sows with their operations
        list_gestating = []
        
        for cur_entry in pig_prod_list:
            if cur_entry['pig_production']['prod_status_id'] == PROD_STATUS_ID_GESTATING:
                
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
                    order_by=1
                )
                
                cur_entry['gestating_ops'] = res
                list_gestating.append(cur_entry)


        farm_settings = self._get_farm_settings(pig_farm_id)

        
        # Prepare data for template
        data = {
            'pig_farm_info':        pig_farm_info,
            'farm_settings':        farm_settings,
            'list_gestating':       list_gestating,
            'inc_historical':       False,
            'inc_cost':             False,
            'inc_target_harvest':   False
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
