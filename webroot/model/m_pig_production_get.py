# April 9, 2026
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


FLAG_BIT_IS_A_GROUP         = 2


class PigProductionGet(BaseModel):
    def __init__(self, model):
        super().__init__(model)

    
    def get_pig_prod_status_list(self):
        """
        Will get pig_prod_status list.
        
        
        Returns
        -------
        list of dictionary

        """
            
        sql =   """
                SELECT 
                    id,
                    name
                FROM pig_prod_status
                """ 
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        

        result = []
        if rows is not None:
            
            for row in rows:
                cur_status_id           = row[0]
                cur_status_name         = row[1]
                
                cur_entry = {
                    'id':               cur_status_id, 
                    'name':             cur_status_name
                }
                
                result.append(cur_entry)

        return result

    
    def get_list(self, pig_farm_id = 0 , pig_prod_type = 0, pig_prod_id = None):
        """
        Will get pig_production list.
        
        Parameters
        ==========
        pig_farm_id : int
            Farm ID to filter by
            
        pig_prod_type : int
            Type of production records to return:
            1 = Gestating only (status_id = 1) - Pregnant sows
            2 = Lactating only (status_id = 4) - Sows with piglets
            3 = Active sows (status_id = 1, 4) - Gestating + Lactating
            4 = Post-lactation (status_id = 5, 6) - Weaning + Growing
            5 = All active (status_id = 1, 4, 5, 6) - All non-harvested/closed
            6 = Completed (status_id = 7, 8, 9) - Combined + Harvested + Closed
        pig_prod_id : int
            Specific production ID (overrides farm filter)
        
        Returns
        -------
        list of dictionary
        """
        order_clause = 'ORDER BY a.date_insemination'
            
        if pig_farm_id > 0:
            
            # pig_prod_type = 1: Gestating only
            # Status: 1 = Gestating (pregnant sows, not yet farrowed)
            if pig_prod_type == 1:
                where_clause = 'WHERE a.pig_farm_id = %s AND a.prod_status_id = 1 ' % pig_farm_id
            
            # pig_prod_type = 2: Lactating only
            # Status: 4 = Lactating (sows with piglets, before weaning)
            if pig_prod_type == 2:
                where_clause = 'WHERE a.pig_farm_id = %s AND a.prod_status_id = 4 ' % pig_farm_id
            
            # pig_prod_type = 3: Active sows (Gestating + Lactating)
            # Statuses: 1 = Gestating, 4 = Lactating
            # These are sows currently in production cycle
            if pig_prod_type == 3:
                where_clause = 'WHERE a.pig_farm_id = %s AND a.prod_status_id IN (1, 4) ' % pig_farm_id
            
            # pig_prod_type = 4: Post-lactation (Weaning + Growing)
            # Statuses: 5 = Weaning (piglets separated from sow), 6 = Growing (piglets growing)
            # These are piglets after weaning, before harvest
            if pig_prod_type == 4:
                where_clause = 'WHERE a.pig_farm_id = %s AND a.prod_status_id IN (5, 6) ' % pig_farm_id
                
            # pig_prod_type = 5: All active production
            # Statuses: 1=Gestating, 4=Lactating, 5=Weaning, 6=Growing
            # Everything except terminated, not pregnant, harvested, closed
            if pig_prod_type == 5:
                where_clause = 'WHERE a.pig_farm_id = %s AND a.prod_status_id IN (1, 4, 5, 6) ' % pig_farm_id
                
            # pig_prod_type = 6: Completed/Harvested
            # Statuses: 7 = Combined to Group; 8 = Harvested, 9 = Closed 
            if pig_prod_type == 6:
                where_clause = 'WHERE a.pig_farm_id = %s AND a.prod_status_id IN (7, 8, 9) ' % pig_farm_id
                order_clause = 'ORDER BY a.id DESC'
            
        else:
            # Get specific production record by ID (overrides all other filters)
            where_clause = 'WHERE a.id = %s ' % pig_prod_id
        
                
    
        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    a.flag,
                    
                    a.insemination_type,
                    
                    a.sow_id,
                    b.farm_sow_id,
                    b.number,
                    b.name,
                    
                    a.boar_id,
                    c.farm_boar_id,
                    c.number,
                    c.name,
                    
                    a.semen_supplier_id,
                    d.name AS semen_supplier_name,
                    
                    a.semen_sup_semen_id,
                    e.name as semen_supplier_semen_name,
                    
                    a.semen_ai_boar_id,
                    f.farm_boar_id,
                    f.number,
                    f.name,
                    
                    a.semen_cost,
                    a.insemination_cost,
                    a.date_insemination,
                    
                    
                    g.notes AS insem_notes,
                    
                    
                    a.insem_staff_id,
                    h.name AS insem_staff_name,
                    
                    a.prod_status_id,
                    i.name AS prod_status_name,
                    
                    a.date_expected_birth,
                    a.date_actual_birth,
                    a.num_days_actual,
                    a.num_pigs_dead_at_birth,
                    a.num_pigs_live_m,
                    a.num_pigs_live_f,
                    a.birth_staff_id,
                    j.name AS birth_staff_name,
                    
                    a.num_dead_after_birth,
                    
                    a.date_weaning,
                    a.num_pigs_weaning_m,
                    a.num_pigs_weaning_f,
                    a.num_pigs_weaning,
                    a.num_pigs_wean_xsmall,
                    a.wean_pigs_weight_total,
                    a.wean_pigs_weight_pp,
                        
                    
                    a.num_pigs_current,
                    
                    a.num_b_gestating,
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    k.date_balance,
                    k.num_gestating,
                    k.num_lactating,
                    k.num_booster,
                    k.num_prestarter,
                    k.num_starter,
                    k.num_grower,
                    k.num_finisher,
                    
                    a.cost_gestating,
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher,
                    
                    a.date_gestating,
                    a.date_lactating,
                    a.date_booster,
                    a.date_prestarter,
                    a.date_starter,
                    a.date_grower,
                    a.date_finisher,
                    
                    
                    a.data_ver_num_pig_prod,
                    a.data_ver_num_medvac, 
                    a.data_ver_num_health_notes,
                    a.data_ver_num_prod_feed,
                    a.data_ver_num_feed_balance,
                    a.data_ver_num_harvest     
                    
                   
                FROM pig_production a
                LEFT OUTER JOIN sow_boar b          ON a.sow_id = b.id
                LEFT OUTER JOIN sow_boar c          ON a.boar_id = c.id
                
                LEFT OUTER JOIN common_supplier d   ON a.semen_supplier_id = d.id
                LEFT OUTER JOIN semen_supplier_semen e ON a.semen_sup_semen_id = e.id
                LEFT OUTER JOIN sow_boar f          ON a.semen_ai_boar_id = f.id
                
                LEFT OUTER JOIN pig_prod_notes g    ON a.insem_notes_id = g.id
                LEFT OUTER JOIN pig_farm_staff h    ON a.insem_staff_id = h.id
                LEFT OUTER JOIN pig_prod_status i   ON a.prod_status_id = i.id
                LEFT OUTER JOIN pig_farm_staff j    ON a.birth_staff_id = j.id
                LEFT OUTER JOIN feed_balance k      ON a.last_feed_balance_id = k.id
                %s
                %s
                """ % (where_clause, order_clause)


        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        

        result = []
            
        for row in rows:
            cur_prod_id                     = row[0]
            cur_prod_farm_prod_id           = row[1]
            cur_prod_flag                   = row[2]
            cur_prod_insemination_type      = row[3]  

            cur_sow_id                      = row[4]  
            cur_sow_farm_sow_id             = row[5]  
            cur_sow_number                  = row[6]  
            cur_sow_name                    = row[7]  

            cur_boar_id                     = row[8]  
            cur_boar_farm_boar_id           = row[9]  
            cur_boar_number                 = row[10] 
            cur_boar_name                   = row[11] 

            cur_semen_supplier_id           = row[12] 
            cur_semen_supplier_name         = row[13] 

            cur_semen_sup_semen_id          = row[14] 
            cur_semen_sup_semen_name        = row[15] 

            cur_semen_ai_boar_id            = row[16] 
            cur_semen_ai_farm_boar_id       = row[17] 
            cur_semen_ai_boar_number        = row[18] 
            cur_semen_ai_boar_name          = row[19] 

            cur_insem_semen_cost            = float(row[20]) if row[20] else 0.0  
            cur_insem_insemination_cost     = float(row[21]) if row[21] else 0.0  
            cur_insem_date_insemination     = str(row[22]) if row[22] else None   

            cur_insem_notes                 = row[23] 

            cur_insem_staff_id              = row[24] 
            cur_insem_staff_name            = row[25] 

            cur_prod_status_id              = row[26] 
            cur_prod_status_name            = row[27] 

            cur_prod_date_expected_birth    = str(row[28]) if row[28] else None    
            cur_prod_date_actual_birth      = str(row[29]) if row[29] else None    
            cur_prod_num_days_actual        = row[30] 
            cur_prod_num_pigs_dead_at_birth = row[31] 
            cur_prod_num_pigs_live_m        = row[32] 
            cur_prod_num_pigs_live_f        = row[33] 
            cur_prod_birth_staff_id         = row[34] 
            cur_prod_birth_staff_name       = row[35] 

            cur_prod_num_dead_after_birth   = row[36] 

            cur_weaning_date                = row[37] 
            cur_weaning_num_pigs_m          = row[38] 
            cur_weaning_num_pigs_f          = row[39] 
            cur_weaning_num_pigs            = row[40] 
            cur_weaning_num_pigs_xsmall     = row[41]
            cur_weaning_weight              = row[42]  
            cur_weaning_weight_pp           = row[43]  

            cur_pig_count                   = row[44]  

            cur_prod_num_b_gestating        = row[45]  
            cur_prod_num_b_lactating        = row[46]  
            cur_prod_num_b_booster          = row[47]  
            cur_prod_num_b_prestarter       = row[48]  
            cur_prod_num_b_starter          = row[49]  
            cur_prod_num_b_grower           = row[50]  
            cur_prod_num_b_finisher         = row[51]  

            cur_feed_bal_date_balance       = row[52]  

            cur_feed_bal_gestating          = row[53]  
            cur_feed_bal_lactating          = row[54]  
            cur_feed_bal_booster            = row[55]  
            cur_feed_bal_prestarter         = row[56]  
            cur_feed_bal_starter            = row[57]  
            cur_feed_bal_grower             = row[58]  
            cur_feed_bal_finisher           = row[59]  

            cur_prod_cost_gestating         = row[60]  
            cur_prod_cost_lactating         = row[61]  
            cur_prod_cost_booster           = row[62]  
            cur_prod_cost_prestarter        = row[63]  
            cur_prod_cost_starter           = row[64]  
            cur_prod_cost_grower            = row[65]  
            cur_prod_cost_finisher          = row[66]  

            cur_prod_date_gestating         = row[67]  
            cur_prod_date_lactating         = row[68]  
            cur_prod_date_booster           = row[69]  
            cur_prod_date_prestarter        = row[70]  
            cur_prod_date_starter           = row[71]  
            cur_prod_date_grower            = row[72]  
            cur_prod_date_finisher          = row[73]  

            cur_data_ver_num_pig_prod       = row[74]  
            cur_data_ver_num_medvac         = row[75]  
            cur_data_ver_num_health_notes   = row[76]  
            cur_data_ver_num_prod_feed      = row[77]  
            cur_data_ver_num_feed_balance   = row[78]  
            cur_data_ver_num_harvest        = row[79]    
                        
            
            cur_entry = {
                'pig_production' :{
                    'id':               cur_prod_id, 
                    'farm_prod_id':     cur_prod_farm_prod_id,
                    'flag':             cur_prod_flag,
                    'prod_status_id':   cur_prod_status_id,
                    'prod_status_name': cur_prod_status_name,
                    'cur_pig_count':    cur_pig_count,
                    'dead_after_birth': cur_prod_num_dead_after_birth
                },
                
                'sow': {
                    'id':               cur_sow_id,
                    'farm_sow_id':      cur_sow_farm_sow_id,
                    'number':           cur_sow_number,
                    'name':             cur_sow_name,
                },
                
                'insemination': {
                    'insem_type':       cur_prod_insemination_type,
                    
                    'boar': {
                        'id':           cur_boar_id,
                        'farm_sow_id':  cur_boar_farm_boar_id,
                        'number':       cur_boar_number,
                        'name':         cur_boar_name
                    },
                    
                    'ai': {
                        'semen_supplier':{
                            'id':       cur_semen_supplier_id,
                            'name':     cur_semen_supplier_name,
                            
                            'semen': {
                                'id':   cur_semen_sup_semen_id,
                                'name': cur_semen_sup_semen_name
                            }
                        },
                        
                        'internal_boar':{
                            'id':           cur_semen_ai_boar_id,
                            'farm_sow_id':  cur_semen_ai_farm_boar_id,
                            'number':       cur_semen_ai_boar_number,
                            'name':         cur_semen_ai_boar_name
                        },
                        
                        'semen_cost':   cur_insem_semen_cost
                    },
                    
                    'insem_cost':       cur_insem_insemination_cost,
                    'insem_notes':      cur_insem_notes,
                    'insem_date':       cur_insem_date_insemination,
                    'insem_staff_id':   cur_insem_staff_id,
                    'insem_staff_name': cur_insem_staff_name
                },
                
                'birth': {
                    'date_expected':    cur_prod_date_expected_birth,
                    'date_actual':      cur_prod_date_actual_birth,
                    'num_days_actual':  cur_prod_num_days_actual,
                    'num_dead_at_birth':cur_prod_num_pigs_dead_at_birth,
                    
                    'pigs_live_m':      cur_prod_num_pigs_live_m,
                    'pigs_live_f':      cur_prod_num_pigs_live_f,
                    'birth_staff_id':   cur_prod_birth_staff_id,
                    'birth_staff_name': cur_prod_birth_staff_name
                },
                
                'weaning': {
                    'date_weaning':     cur_weaning_date,
                    'num_pigs_m':       cur_weaning_num_pigs_m,
                    'num_pigs_f':       cur_weaning_num_pigs_f,
                    'num_pigs':         cur_weaning_num_pigs,
                    'num_pigs_xsmall':  cur_weaning_num_pigs_xsmall,
                    'weight':           cur_weaning_weight,
                    'weight_pp':        cur_weaning_weight_pp      
                },
                
                
                'feeds':{
                    'bought':{
                        'gestating':    cur_prod_num_b_gestating,
                        'lactating':    cur_prod_num_b_lactating,
                        'booster':      cur_prod_num_b_booster,
                        'prestarter':   cur_prod_num_b_prestarter,
                        'starter':      cur_prod_num_b_starter,
                        'grower':       cur_prod_num_b_grower,
                        'finisher':     cur_prod_num_b_finisher
                    },
                    
                    'balance':{
                        'date_balance': str(cur_feed_bal_date_balance)  if cur_feed_bal_date_balance    is not None else None,
                        
                        'gestating':    float(cur_feed_bal_gestating)   if cur_feed_bal_gestating       is not None else None,
                        'lactating':    float(cur_feed_bal_lactating)   if cur_feed_bal_lactating       is not None else None,
                        'booster':      float(cur_feed_bal_booster)     if cur_feed_bal_booster         is not None else None,
                        'prestarter':   float(cur_feed_bal_prestarter)  if cur_feed_bal_prestarter      is not None else None,
                        'starter':      float(cur_feed_bal_starter)     if cur_feed_bal_starter         is not None else None,
                        'grower':       float(cur_feed_bal_grower)      if cur_feed_bal_grower          is not None else None,
                        'finisher':     float(cur_feed_bal_finisher)    if cur_feed_bal_finisher        is not None else None
                    },
                    
                    'cost':{
                        'gestating':    float(cur_prod_cost_gestating)  if cur_prod_cost_gestating      is not None else None,
                        'lactating':    float(cur_prod_cost_lactating)  if cur_prod_cost_lactating      is not None else None,
                        'booster':      float(cur_prod_cost_booster)    if cur_prod_cost_booster        is not None else None,
                        'prestarter':   float(cur_prod_cost_prestarter) if cur_prod_cost_prestarter     is not None else None,
                        'starter':      float(cur_prod_cost_starter)    if cur_prod_cost_starter        is not None else None,
                        'grower':       float(cur_prod_cost_grower)     if cur_prod_cost_grower         is not None else None,
                        'finisher':     float(cur_prod_cost_finisher)   if cur_prod_cost_finisher       is not None else None
                    },
                    
                    'date_change_feed':{
                        'gestating':    str(cur_prod_date_gestating)    if cur_prod_date_gestating      is not None else None,
                        'lactating':    str(cur_prod_date_lactating)    if cur_prod_date_lactating      is not None else None,
                        'booster':      str(cur_prod_date_booster)      if cur_prod_date_booster        is not None else None,
                        'prestarter':   str(cur_prod_date_prestarter)   if cur_prod_date_prestarter     is not None else None,
                        'starter':      str(cur_prod_date_starter)      if cur_prod_date_starter        is not None else None,
                        'grower':       str(cur_prod_date_grower)       if cur_prod_date_grower         is not None else None,
                        'finisher':     str(cur_prod_date_finisher)     if cur_prod_date_finisher       is not None else None
                    }
                
                },
                
                
                'data_ver_num': {
                    'pig_prod':         cur_data_ver_num_pig_prod,
                    'medvac':           cur_data_ver_num_medvac,
                    'health_notes':     cur_data_ver_num_health_notes,
                    'prod_feed':        cur_data_ver_num_prod_feed,
                    'feed_balance':     cur_data_ver_num_feed_balance,
                    'harvest':          cur_data_ver_num_harvest
                
                }
            }
            
            
            # Remove null entries
            if cur_prod_date_actual_birth is None:
                del cur_entry['birth']['num_days_actual'] 
                del cur_entry['birth']['num_dead_at_birth']
                
                del cur_entry['birth']['pigs_live_m']
                del cur_entry['birth']['pigs_live_f']   
                del cur_entry['birth']['birth_staff_id'] 
                del cur_entry['birth']['birth_staff_name']
                
                
            if cur_weaning_date is None:
                del cur_entry['weaning']['num_pigs_m']
                del cur_entry['weaning']['num_pigs_f']
                del cur_entry['weaning']['num_pigs']
                del cur_entry['weaning']['num_pigs_xsmall']
                del cur_entry['weaning']['weight']
                del cur_entry['weaning']['weight_pp']
            
            else:
                if cur_weaning_num_pigs_xsmall is None:
                    del cur_entry['weaning']['num_pigs_xsmall']
                  
                if cur_weaning_weight is None:
                    del cur_entry['weaning']['weight']
                        
                if cur_weaning_weight_pp is None:
                    del cur_entry['weaning']['weight_pp']
                
            # Remove feeds that are only needed after birth
            if cur_prod_status_id == PROD_STATUS_ID_GESTATING:
                del cur_entry['feeds']['bought']['prestarter']
                del cur_entry['feeds']['bought']['starter']
                del cur_entry['feeds']['bought']['grower']
                del cur_entry['feeds']['bought']['finisher']
            
                del cur_entry['feeds']['balance']['prestarter']
                del cur_entry['feeds']['balance']['starter']
                del cur_entry['feeds']['balance']['grower']
                del cur_entry['feeds']['balance']['finisher']
            
                del cur_entry['feeds']['cost']['prestarter']
                del cur_entry['feeds']['cost']['starter']
                del cur_entry['feeds']['cost']['grower']
                del cur_entry['feeds']['cost']['finisher']
            
                del cur_entry['feeds']['date_change_feed']['prestarter']
                del cur_entry['feeds']['date_change_feed']['starter']
                del cur_entry['feeds']['date_change_feed']['grower']
                del cur_entry['feeds']['date_change_feed']['finisher']


            # Get Group members if production is a Group
            if (cur_prod_flag & FLAG_BIT_IS_A_GROUP) > 0:
                group_members = self.get_production_group_members(
                    pig_farm_id, cur_prod_id)
                    
                if group_members and len(group_members) > 0:
                    cur_entry['group_members'] = group_members
                    
            

            result.append(cur_entry)

        
        return result
    
    
    def get_feed_summary_by_id(self, pig_prod_id):
        sql =   """
                SELECT 
                    
                    a.num_b_gestating,
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    i.date_balance,
                    i.num_gestating,
                    i.num_lactating,
                    i.num_booster,
                    i.num_prestarter,
                    i.num_starter,
                    i.num_grower,
                    i.num_finisher,
                    
                    a.cost_gestating,
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher,
                    
                    a.date_gestating,
                    a.date_lactating,
                    a.date_booster,
                    a.date_prestarter,
                    a.date_starter,
                    a.date_grower,
                    a.date_finisher
                    
                   
                FROM pig_production a
                LEFT OUTER JOIN feed_balance i      ON a.last_feed_balance_id = i.id
                WHERE a.id = %s
                """ % pig_prod_id


        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        

        result = []
            
        for row in rows:
            
            cur_prod_num_b_gestating    = row[0]
            cur_prod_num_b_lactating    = row[1]
            cur_prod_num_b_booster      = row[2]
            cur_prod_num_b_prestarter   = row[3]
            cur_prod_num_b_starter      = row[4]
            cur_prod_num_b_grower       = row[5]
            cur_prod_num_b_finisher     = row[6]
            
            cur_feed_bal_date_balance   = row[7]
            
            cur_feed_bal_gestating      = row[8]
            cur_feed_bal_lactating      = row[9]
            cur_feed_bal_booster        = row[10]
            cur_feed_bal_prestarter     = row[11]
            cur_feed_bal_starter        = row[12]
            cur_feed_bal_grower         = row[13]
            cur_feed_bal_finisher       = row[14]
            
            cur_prod_cost_gestating     = row[15]
            cur_prod_cost_lactating     = row[16]
            cur_prod_cost_booster       = row[17]
            cur_prod_cost_prestarter    = row[18]
            cur_prod_cost_starter       = row[19]
            cur_prod_cost_grower        = row[20]
            cur_prod_cost_finisher      = row[21]
            
            cur_prod_date_gestating     = row[22]
            cur_prod_date_lactating     = row[23]
            cur_prod_date_booster       = row[24]
            cur_prod_date_prestarter    = row[25]
            cur_prod_date_starter       = row[26]
            cur_prod_date_grower        = row[27]
            cur_prod_date_finisher      = row[28]
        
            
            cur_entry = {
                
                'feeds':{
                    'bought':{
                        'gestating':    cur_prod_num_b_gestating,
                        'lactating':    cur_prod_num_b_lactating,
                        'booster':      cur_prod_num_b_booster,
                        'prestarter':   cur_prod_num_b_prestarter,
                        'starter':      cur_prod_num_b_starter,
                        'grower':       cur_prod_num_b_grower,
                        'finisher':     cur_prod_num_b_finisher
                    },
                    
                    'balance':{
                        'date_balance': str(cur_feed_bal_date_balance)      if cur_feed_bal_date_balance    is not None else None,
                        
                        'gestating':    float(cur_feed_bal_gestating)       if cur_feed_bal_gestating       is not None else None,
                        'lactating':    float(cur_feed_bal_lactating)       if cur_feed_bal_lactating       is not None else None,
                        'booster':      float(cur_feed_bal_booster)         if cur_feed_bal_booster         is not None else None,
                        'prestarter':   float(cur_feed_bal_prestarter)      if cur_feed_bal_prestarter      is not None else None,
                        'starter':      float(cur_feed_bal_starter)         if cur_feed_bal_starter         is not None else None,
                        'grower':       float(cur_feed_bal_grower)          if cur_feed_bal_grower          is not None else None,
                        'finisher':     float(cur_feed_bal_finisher)        if cur_feed_bal_finisher        is not None else None
                    },
                    
                    'cost':{
                        'gestating':    float(cur_prod_cost_gestating)      if cur_prod_cost_gestating      is not None else None,
                        'lactating':    float(cur_prod_cost_lactating)      if cur_prod_cost_lactating      is not None else None,
                        'booster':      float(cur_prod_cost_booster)        if cur_prod_cost_booster        is not None else None,
                        'prestarter':   float(cur_prod_cost_prestarter)     if cur_prod_cost_prestarter     is not None else None,
                        'starter':      float(cur_prod_cost_starter)        if cur_prod_cost_starter        is not None else None,
                        'grower':       float(cur_prod_cost_grower)         if cur_prod_cost_grower         is not None else None,
                        'finisher':     float(cur_prod_cost_finisher)       if cur_prod_cost_finisher       is not None else None
                    },
                    
                    'date_change_feed':{
                        'gestating':    str(cur_prod_date_gestating)        if cur_prod_date_gestating      is not None else None,
                        'lactating':    str(cur_prod_date_lactating)        if cur_prod_date_lactating      is not None else None,
                        'booster':      str(cur_prod_date_booster)          if cur_prod_date_booster        is not None else None,
                        'prestarter':   str(cur_prod_date_prestarter)       if cur_prod_date_prestarter     is not None else None,
                        'starter':      str(cur_prod_date_starter)          if cur_prod_date_starter        is not None else None,
                        'grower':       str(cur_prod_date_grower)           if cur_prod_date_grower         is not None else None,
                        'finisher':     str(cur_prod_date_finisher)         if cur_prod_date_finisher       is not None else None
                    }
                }
            }
            
            return cur_entry

        return None
    
    
    def get_cur_pig_count_by_id(self, pig_prod_id):
        sql =   """
                SELECT 
                    
                    num_pigs_current
                    
                FROM pig_production 
                WHERE id = %s
                """ % pig_prod_id


        rows = self._execute_query(sql)
        
        if rows is None:
            return None

            
        for row in rows:
            
            cur_prod_cur_pig_count    = row[0]
            

            cur_entry = {
                
                'pig_production':{
                    'cur_pig_count': cur_prod_cur_pig_count
                }
                
            }
            
            return cur_entry

        return None
    
    
    def get_data_ver_num(self, pig_prod_id):
        sql =   """
                SELECT 
                    
                    data_ver_num_pig_prod,
                    data_ver_num_medvac, 
                    data_ver_num_health_notes,
                    data_ver_num_prod_feed,
                    data_ver_num_feed_balance,
                    data_ver_num_harvest     
                    
                FROM pig_production 
                WHERE id = %s
                """ % pig_prod_id


        rows = self._execute_query(sql)
        
        if rows is None:
            return None


        for row in rows:
            
            cur_data_ver_num_pig_prod       = row[0]
            cur_data_ver_num_medvac         = row[1] 
            cur_data_ver_num_health_notes   = row[2]
            cur_data_ver_num_prod_feed      = row[3]
            cur_data_ver_num_feed_balance   = row[4]
            cur_data_ver_num_harvest        = row[5] 
            

            cur_entry = {
                'data_ver_num': {
                    'pig_prod':     cur_data_ver_num_pig_prod,    
                    'medvac':       cur_data_ver_num_medvac,      
                    'health_notes': cur_data_ver_num_health_notes,
                    'prod_feed':    cur_data_ver_num_prod_feed,   
                    'feed_balance': cur_data_ver_num_feed_balance,
                    'harvest':      cur_data_ver_num_harvest
                }
            }
            
            return cur_entry

        return None
    
    
    def get_pig_prod_ops_list(self, pig_farm_id,  inc_historical = 0):
        
        # Include PROD_STATUS_ID_GESTATING that has already bought up lactating feeds 
        
        where_clause = 'WHERE (a.pig_farm_id = %s AND  a.prod_status_id IN (4, 5, 6)) ' % pig_farm_id
        where_clause += ' OR (a.pig_farm_id = %s AND a.prod_status_id = 1 AND a.num_b_lactating IS NOT NULL) ' % pig_farm_id
        
        if inc_historical > 0:
            where_clause = 'WHERE (a.pig_farm_id = %s AND a.prod_status_id IN (4,5,6,8,9)) ' % pig_farm_id
            where_clause += ' OR (a.pig_farm_id = %s AND a.prod_status_id = 1 AND a.num_b_lactating IS NOT NULL) ' % pig_farm_id
       
        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    b.number,
                    b.name AS sow_name,
                    
                    a.prod_status_id,
                    c.name AS prod_status,
                    
                    a.num_pigs_current,
                    
                    a.date_actual_birth,
                    
                    a.date_iron_1,
                    a.date_iron_2,
                    a.date_vitamins_1,
                    a.date_kapon,
                    a.date_vitamins_2,
                    a.date_deworm_1,
                    
                    a.date_booster,
                    a.date_prestarter,
                    a.date_weaning,
                    a.date_starter,
                    a.date_grower,
                    a.date_finisher,
                    
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    d.date_balance,
                    d.num_lactating,
                    d.num_booster,
                    d.num_prestarter,
                    d.num_starter,
                    d.num_grower,
                    d.num_finisher,
                    
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher,
                    
                    a.date_harvest
                    
                FROM pig_production a
                LEFT OUTER JOIN sow_boar b          ON a.sow_id = b.id
                LEFT OUTER JOIN pig_prod_status c   ON a.prod_status_id = c.id
                LEFT OUTER JOIN feed_balance d      ON a.last_feed_balance_id = d.id
                %s
                ORDER BY a.date_actual_birth DESC
                """ % where_clause 
    
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
            

        result = []
            
        for row in rows:
            cur_id                  = row[0]
            cur_farm_prod_id        = row[1]
            cur_sow_number          = row[2]
            cur_sow_name            = row[3]
            
            cur_status_id           = row[4]
            cur_status_name         = row[5]
            
            cur_num_pigs_current    = row[6]
           
            cur_date_actual         = str(row[7])   if row[7]  else None
            
            cur_date_iron_1         = str(row[8])   if row[8]  else None
            cur_date_iron_2         = str(row[9])   if row[9]  else None
            cur_date_vitamins_1     = str(row[10])  if row[10]  else None
            cur_date_kapon          = str(row[11])  if row[11] else None
            cur_date_vitamins_2     = str(row[12])  if row[12] else None
            cur_date_deworm_1       = str(row[13])  if row[13] else None
            
            
            cur_date_booster        = str(row[14])  if row[14] else None
            cur_date_prestarter     = str(row[15])  if row[15] else None
            cur_date_weaning        = str(row[16])  if row[16] else None
            cur_date_starter        = str(row[17])  if row[17] else None
            cur_date_grower         = str(row[18])  if row[18] else None
            cur_date_finisher       = str(row[19])  if row[19] else None
            
            cur_num_b_lactating     = row[20]
            cur_num_b_booster       = row[21]
            cur_num_b_prestarter    = row[22]
            cur_num_b_starter       = row[23]
            cur_num_b_grower        = row[24]
            cur_num_b_finisher      = row[25]
            
            cur_feed_date_balance   = str(row[26])   if row[26] is not None else None
            cur_num_l_lactating     = float(row[27]) if row[27] is not None else None
            cur_num_l_booster       = float(row[28]) if row[28] is not None else None
            cur_num_l_prestarter    = float(row[29]) if row[29] is not None else None
            cur_num_l_starter       = float(row[30]) if row[30] is not None else None
            cur_num_l_grower        = float(row[31]) if row[31] is not None else None
            cur_num_l_finisher      = float(row[32]) if row[32] is not None else None
            
            cur_cost_lactating      = float(row[33]) if row[33] is not None else None
            cur_cost_booster        = float(row[34]) if row[34] is not None else None
            cur_cost_prestarter     = float(row[35]) if row[35] is not None else None
            cur_cost_starter        = float(row[36]) if row[36] is not None else None
            cur_cost_grower         = float(row[37]) if row[37] is not None else None
            cur_cost_finisher       = float(row[38]) if row[38] is not None else None
            
            cur_date_harvest        = str(row[39]) if row[39] else None
            
            
            cur_num_c_lactating     = None
            cur_num_c_booster       = None
            cur_num_c_prestarter    = None
            cur_num_c_starter       = None
            cur_num_c_grower        = None
            cur_num_c_finisher      = None
        
        
            if cur_num_b_lactating is not None and cur_num_l_lactating is not None:
                cur_num_c_lactating = float(cur_num_b_lactating) - cur_num_l_lactating
            
            if cur_num_b_booster is not None and cur_num_l_booster is not None:
                cur_num_c_booster = float(cur_num_b_booster) - cur_num_l_booster
            
            if cur_num_b_prestarter is not None and cur_num_l_prestarter is not None:
                cur_num_c_prestarter = float(cur_num_b_prestarter) - cur_num_l_prestarter
            
            if cur_num_b_starter is not None and cur_num_l_starter is not None:
                cur_num_c_starter = float(cur_num_b_starter) - cur_num_l_starter
            
            if cur_num_b_grower is not None and cur_num_l_grower is not None:
                cur_num_c_grower = float(cur_num_b_grower) - cur_num_l_grower
            
            if cur_num_b_finisher is not None and cur_num_l_finisher is not None:
                cur_num_c_finisher = float(cur_num_b_finisher) - cur_num_l_finisher
            
            
            cur_entry = {
                'pig_prod':{
                    'id':           cur_id,
                    'farm_prod_id': cur_farm_prod_id,
                    
                    'status_id':    cur_status_id, 
                    'status':       cur_status_name,
                
                    'num_pigs_current': cur_num_pigs_current
                },
                
                'sow': {
                    'number':       cur_sow_number,
                    'name':         cur_sow_name
                },
                
                'dates':{
                    'birth':        cur_date_actual,
                    
                    'iron_1':       cur_date_iron_1,
                    'iron_2':       cur_date_iron_2,
                    'vitamins_1':   cur_date_vitamins_1,
                    'kapon':        cur_date_kapon,
                    'vitamins_2':   cur_date_vitamins_2,
                    'deworm_1':     cur_date_deworm_1,
                    
                    'booster':      cur_date_booster,
                    'prestarter':   cur_date_prestarter,
                    'weaning':      cur_date_weaning,
                    'starter':      cur_date_starter,
                    'grower':       cur_date_grower,
                    'finisher':     cur_date_finisher,
                    
                    'harvest':      cur_date_harvest
                },
                
                'num_feeds': {
                    'date_balance': cur_feed_date_balance,
                
                    'lactating': {
                        'bought':   cur_num_b_lactating,
                        'consumed': cur_num_c_lactating,
                        'left':     cur_num_l_lactating
                    },
                    
                    'booster': {
                        'bought':   cur_num_b_booster,
                        'consumed': cur_num_c_booster,
                        'left':     cur_num_l_booster
                    },
                        
                    'prestarter': {
                        'bought':   cur_num_b_prestarter,
                        'consumed': cur_num_c_prestarter,
                        'left':     cur_num_l_prestarter
                    },
                        
                    'starter': {     
                        'bought':   cur_num_b_starter,
                        'consumed': cur_num_c_starter,
                        'left':     cur_num_l_starter
                    },
                    
                    'grower': {
                        'bought':   cur_num_b_grower,
                        'consumed': cur_num_c_grower,
                        'left':     cur_num_l_grower
                    },
                    
                    'finisher': {    
                        'bought':   cur_num_b_finisher,
                        'consumed': cur_num_c_finisher,
                        'left':     cur_num_l_finisher
                    }
                },
                
                'cost_feeds': {
                    'lactating':    cur_cost_lactating,
                    'booster':      cur_cost_booster,
                    'prestarter':   cur_cost_prestarter,
                    'starter':      cur_cost_starter,
                    'grower':       cur_cost_grower,
                    'finisher':     cur_cost_finisher
                }
               
            }
            result.append(cur_entry)

        
        return result
        
    
    def get_production_output(self, pig_farm_id = 0, sow_id = 0):
        """
        
        
        Notes:
        1.) The number of piglets output at weaning are entered in two ways
            - separate counts: num_pigs_weaning_m, num_pigs_weaning_f  
            - total count no separation: num_pigs_weaning
        
        2.) If entered via separate count, num_pigs_weaning is NULL; 
        
        """
        
        where_clause = ''
        order_clause = ''
        
        if pig_farm_id > 0:
            where_clause = 'WHERE a.pig_farm_id = %s AND a.date_actual_birth IS NOT NULL' % pig_farm_id
            order_clause = 'ORDER BY a.sow_id ASC, a.date_actual_birth DESC'
            
        if sow_id > 0:
            where_clause = 'WHERE a.sow_id = %s AND a.date_actual_birth IS NOT NULL' % sow_id
            order_clause = 'ORDER BY a.date_actual_birth DESC'
            
            
        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    a.flag, 
                    
                    a.sow_id,
                    b.name AS sow_name,
                    b.number AS sow_number,
                    b.date_dispose AS sow_date_dispose, 
                    
                    a.insemination_type,
                    
                    a.boar_id,
                    c.name AS boar_name,
                    c.number AS boar_number,
                    c.date_dispose AS boar_date_dispose,
                    
                    
                    a.semen_supplier_id,
                    d.name AS semen_supplier_name,
                    
                    a.semen_sup_semen_id,
                    e.name AS semen_name,
                    
                    a.semen_ai_boar_id,
                    f.name AS boar_name,
                    f.number AS boar_number,
                    f.date_dispose AS boar_date_dispose,
                    
                    
                    a.date_actual_birth,
                    a.num_pigs_live_m,
                    a.num_pigs_live_f,
                    a.num_pigs_dead_at_birth,
                    a.num_dead_after_birth,
                    
                    a.date_weaning,
                    a.num_pigs_weaning_m,
                    a.num_pigs_weaning_f,
                    a.num_pigs_weaning,
                    a.wean_pigs_weight_total,
                    a.wean_pigs_weight_pp
                    
                    
                FROM pig_production a 
                LEFT OUTER JOIN sow_boar b              ON a.sow_id = b.id
                LEFT OUTER JOIN sow_boar c              ON a.boar_id = c.id
                LEFT OUTER JOIN common_supplier d       ON a.semen_supplier_id = d.id
                LEFT OUTER JOIN semen_supplier_semen e  ON a.semen_sup_semen_id = e.id
                LEFT OUTER JOIN sow_boar f              ON a.semen_ai_boar_id = f.id
                
                %s
                %s
                """ % (where_clause, order_clause)
    
            
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
            

        result = []
            
        cur_sow     = None
        last_sow_id = None
      
        for row in rows:
            
            cur_pig_prod_id             = row[0]
            cur_farm_prod_id            = row[1]
            cur_pig_prod_flag           = row[2]

            cur_sow_id                  = row[3]  
            cur_sow_name                = row[4]  
            cur_sow_number              = row[5]  
            cur_sow_date_dispose        = str(row[6]) if row[6] else None  

            cur_insemination_type       = row[7]  

            cur_boar_id                 = row[8]  
            cur_boar_name               = row[9]  
            cur_boar_number             = row[10] 
            cur_boar_date_dispose       = str(row[11]) if row[11] else None

            cur_semen_supplier_id       = row[12] 
            cur_semen_supplier_name     = row[13] 

            cur_semen_sup_semen_id      = row[14] 
            cur_semen_sup_semen_name    = row[15] 

            cur_semen_ai_boar_id        = row[16] 
            cur_semen_ai_boar_name      = row[17] 
            cur_semen_ai_boar_number    = row[18] 
            cur_semen_ai_boar_date_dispose = str(row[19]) if row[19] else None  

            cur_date_actual_birth       = str(row[20]) 
            cur_pigs_live_m             = row[21] 
            cur_pigs_live_f             = row[22] 
            cur_dead_at_birth           = row[23] 
            cur_dead_after_birth        = row[24] 

            cur_weaning_date            = row[25] 
            cur_weaning_pigs_m          = int(row[26])   if row[26] is not None else None  
            cur_weaning_pigs_f          = int(row[27])   if row[27] is not None else None  
            cur_weaning_pigs            = int(row[28])   if row[28] is not None else None  
            cur_weaning_pigs_weight     = float(row[29]) if row[29] is not None else None  
           
           
            if last_sow_id is None or last_sow_id !=  cur_sow_id:
                last_sow_id = cur_sow_id
                
                cur_entry = {
                    'sow':{
                        'id':           cur_sow_id,
                        'name':         cur_sow_name,
                        'number':       cur_sow_number,
                        'date_dispose': cur_sow_date_dispose
                    },
                    
                    'production':[]
                }
                
                result.append(cur_entry)
                
            
            cur_prod = {
                'pig_production':{
                    'id':               cur_pig_prod_id,
                    'farm_prod_id':     cur_farm_prod_id,
                    'flag':             cur_pig_prod_flag,
                    'dead_after_birth': cur_dead_after_birth
                },
                
                'insemination': {
                    'insem_type':       cur_insemination_type,
                    
                    'boar': {
                        'id':           cur_boar_id,
                        'number':       cur_boar_number,
                        'name':         cur_boar_name,
                        'date_dispose': cur_boar_date_dispose
                    },
                    
                    'ai': {
                        'semen_supplier':{
                            'id':       cur_semen_supplier_id,
                            'name':     cur_semen_supplier_name,
                            
                            'semen': {
                                'id':   cur_semen_sup_semen_id,
                                'name': cur_semen_sup_semen_name
                            }
                        },
                        
                        'internal_boar':{
                            'id':           cur_semen_ai_boar_id,
                            'number':       cur_semen_ai_boar_number,
                            'name':         cur_semen_ai_boar_name,
                            'date_dispose': cur_semen_ai_boar_date_dispose
                        },
                       
                    }
                },
                
                
                'birth':{
                    'date_actual':      cur_date_actual_birth,
                    'pigs_live_m':      cur_pigs_live_m,
                    'pigs_live_f':      cur_pigs_live_f,
                    'dead':             cur_dead_at_birth
                },
                
                
                'weaning': {
                    'date_weaning':     cur_weaning_date,
                    'num_pigs_m':       cur_weaning_pigs_m,
                    'num_pigs_f':       cur_weaning_pigs_f,
                    'num_pigs':         cur_weaning_pigs,
                    'weight':           cur_weaning_pigs_weight    
                }
            }
            
            
            
            if cur_boar_id and cur_boar_id > 0:
                 del cur_prod['insemination']['ai']
            
            else:
                del cur_prod['insemination']['boar']
                
                if cur_semen_supplier_id and cur_semen_supplier_id > 0:
                    del cur_prod['insemination']['ai']['internal_boar']
                    
                else:
                    del cur_prod['insemination']['ai']['semen_supplier']
            
            
            cur_entry['production'].append(cur_prod)
    
        
        return result
    
    
    def get_production_not_pregnant(self, pig_farm_id):


        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    a.flag,
                    
                    a.sow_id,
                    b.name AS sow_name,
                    b.number AS sow_number,
                    b.date_dispose AS sow_date_dispose, 
                    
                    a.insemination_type,
                    a.date_insemination,
                    
                    a.boar_id,
                    c.name AS boar_name,
                    c.number AS boar_number,
                    c.date_dispose AS boar_date_dispose,
                    
                    
                    a.semen_supplier_id,
                    d.name AS semen_supplier_name,
                    
                    a.semen_sup_semen_id,
                    e.name AS semen_name,
                    
                    a.semen_ai_boar_id,
                    f.name AS boar_name,
                    f.number AS boar_number,
                    f.date_dispose AS boar_date_dispose
                    
                    
                FROM pig_production a 
                LEFT OUTER JOIN sow_boar b              ON a.sow_id = b.id
                LEFT OUTER JOIN sow_boar c              ON a.boar_id = c.id
                LEFT OUTER JOIN common_supplier d       ON a.semen_supplier_id = d.id
                LEFT OUTER JOIN semen_supplier_semen e  ON a.semen_sup_semen_id = e.id
                LEFT OUTER JOIN sow_boar f              ON a.semen_ai_boar_id = f.id
                
                WHERE a.pig_farm_id = %s AND a.prod_status_id = 3
                ORDER BY a.date_insemination DESC; 
                """ % pig_farm_id
    
            
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        

        result = []
          
        for row in rows:
            
            cur_pig_prod_id             = row[0]
            cur_farm_prod_id            = row[1]
            cur_pig_prod_flag           = row[2]

            cur_sow_id                  = row[3]  
            cur_sow_name                = row[4]  
            cur_sow_number              = row[5]  
            cur_sow_date_dispose        = str(row[6]) if row[6] else None  

            cur_insemination_type       = row[7] 
            cur_date_insemination       = str(row[8]) if row[8] else None  

            cur_boar_id                 = row[9]  
            cur_boar_name               = row[10] 
            cur_boar_number             = row[11] 
            cur_boar_date_dispose       = str(row[12]) if row[12] else None  

            cur_semen_supplier_id       = row[13] 
            cur_semen_supplier_name     = row[14] 

            cur_semen_sup_semen_id      = row[15] 
            cur_semen_sup_semen_name    = row[16] 

            cur_semen_ai_boar_id        = row[17] 
            cur_semen_ai_boar_name      = row[18] 
            cur_semen_ai_boar_number    = row[19] 
            cur_semen_ai_boar_date_dispose = str(row[20]) if row[20] else None 
            
            
            cur_entry = {
                'pig_production':{
                    'id':               cur_pig_prod_id,
                    'farm_prod_id':     cur_farm_prod_id,
                    'flag':             cur_pig_prod_flag
                },
                
                'sow':{
                    'id':               cur_sow_id,
                    'name':             cur_sow_name,
                    'number':           cur_sow_number,
                    'date_dispose':     cur_sow_date_dispose
                },
                    
                    
                'insemination': {
                    'insem_type':       cur_insemination_type,
                    'insem_date':       cur_date_insemination,
                    
                    'boar': {
                        'id':           cur_boar_id,
                        'number':       cur_boar_number,
                        'name':         cur_boar_name,
                        'date_dispose': cur_boar_date_dispose
                    },
                    
                    'ai': {
                        'semen_supplier':{
                            'id':       cur_semen_supplier_id,
                            'name':     cur_semen_supplier_name,
                            
                            'semen': {
                                'id':   cur_semen_sup_semen_id,
                                'name': cur_semen_sup_semen_name
                            }
                        },
                        
                        'internal_boar':{
                            'id':           cur_semen_ai_boar_id,
                            'number':       cur_semen_ai_boar_number,
                            'name':         cur_semen_ai_boar_name,
                            'date_dispose': cur_semen_ai_boar_date_dispose
                        }
                    }
                }
            
            }

            
            """
            if cur_boar_id and cur_boar_id > 0:
                 del cur_entry['insemination']['ai']
            
            else:
                del cur_entry['insemination']['boar']
                
                if cur_semen_supplier_id and cur_semen_supplier_id > 0:
                    del cur_entry['insemination']['ai']['internal_boar']
                    
                else:
                    del cur_entry['insemination']['ai']['semen_supplier']
            """
    
            result.append(cur_entry)

        
        return result
    
    
    def get_production_output_group_per_sow(self, pig_farm_id = 0):
        """
        
        Notes:
        1.) The number of piglets output at weaning are entered in two ways
            - separate counts: num_pigs_weaning_m, num_pigs_weaning_f  
            - total count no separation: num_pigs_weaning
        
        2.) If entered via separate count, num_pigs_weaning is NULL; 
        
        """
        
            
        # This sql return number of piglets at weaning + currently lactating.
        # This includes both active sows and disposed sows.
        # The basic info of the sow is also returned.
        # The num_dead column is the number of dead piglets at birth.
        # The number of dead piglets after birth and before weaning should 
        # computed.
        
        sql = """
        SELECT 
            a.sow_id,
            SUM(a.cnt) AS num_birth,
            
            SUM(a.num_pigs_live_m) AS num_live_m,
            SUM(a.num_pigs_live_f) AS num_live_f,
            SUM(a.num_dead_birth) AS num_dead_birth,
            
            SUM(a.num_pigs_wean_m) as num_wean_m,
            SUM(a.num_pigs_wean_f) as num_wean_f,
            SUM(a.num_pigs_wean) as num_wean,
            
            b.name,
            b.number,
            b.date_dispose
            
        FROM (
            SELECT
                'weaning' as record_type,
                sow_id,
                COUNT(*) AS cnt,
                
                SUM(num_pigs_live_m) AS num_pigs_live_m,
                SUM(num_pigs_live_f) AS num_pigs_live_f,
                SUM(num_pigs_dead_at_birth) AS num_dead_birth,
                
                SUM(num_pigs_weaning_m) as num_pigs_wean_m,
                SUM(num_pigs_weaning_f) as num_pigs_wean_f,
                SUM(num_pigs_weaning)   as num_pigs_wean
            FROM pig_production 
            WHERE pig_farm_id = %s AND date_weaning IS NOT NULL
            GROUP BY sow_id

            UNION ALL

            SELECT
                'birth' as record_type,
                sow_id,
                COUNT(*) AS cnt,
                
                SUM(num_pigs_live_m) as num_pigs_live_m,
                SUM(num_pigs_live_f) as num_pigs_live_f,
                SUM(num_pigs_dead_at_birth) AS num_dead_birth,
                
                SUM(num_pigs_live_m) as num_pigs_wean_m,
                SUM(num_pigs_live_f) as num_pigs_wean_f,
                0 as num_pigs_wean
            FROM pig_production 
            WHERE pig_farm_id = %s AND date_actual_birth IS NOT NULL AND date_weaning IS NULL
            GROUP BY sow_id

            ORDER BY sow_id, record_type ASC
        ) a
        LEFT OUTER JOIN sow_boar b ON a.sow_id = b.id
        GROUP BY a.sow_id; 
        """ %(pig_farm_id, pig_farm_id)
            
            
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
            

        result = []
          
        for row in rows:
            
            cur_sow_id                  = row[0]
            cur_birth_count             = int(row[1]) if row[1] is not None else None
            cur_pigs_live_m             = int(row[2]) if row[2] is not None else None
            cur_pigs_live_f             = int(row[3]) if row[3] is not None else None
            cur_dead_at_birth           = int(row[4]) if row[4] is not None else None
            
            cur_pigs_wean_m             = int(row[5]) if row[6] is not None else None
            cur_pigs_wean_f             = int(row[6]) if row[6] is not None else None
            cur_pigs_wean               = int(row[7]) if row[7] is not None else None
            
            
            cur_sow_name                = row[8]
            cur_sow_number              = row[9]
            cur_date_disposed           = str(row[10]) if row[10] is not None else None
            
            
            # compute total live births
            cur_pigs_live_birth         =  cur_pigs_live_m + cur_pigs_live_f
            
            # compute total live pigs at wean
            cur_total_wean = 0
            if cur_pigs_wean_m is not None:
                cur_total_wean += cur_pigs_wean_m
                
            if cur_pigs_wean_f is not None:
                cur_total_wean += cur_pigs_wean_f
                
            if cur_pigs_wean is not None:
                cur_total_wean += cur_pigs_wean
                
                
            # compute dead before wean
            cur_dead_before_wean = cur_pigs_live_birth - cur_total_wean
            
            cur_entry ={
                'sow_id':               cur_sow_id,
                'sow_name':             cur_sow_name,     
                'sow_number':           cur_sow_number,   
                'date_disposed':        cur_date_disposed,
                
                'num_births':           cur_birth_count,
                
                'num_pigs_live_m':      cur_pigs_live_m,
                'num_pigs_live_f':      cur_pigs_live_f,
                'dead_at_birth':        cur_dead_at_birth,
                
                'num_pigs_wean':        cur_total_wean,
                'dead_before_wean':     cur_dead_before_wean
            }
                
        
            result.append(cur_entry)
    
        return result
    
    
    def get_production_group_members(self, pig_farm_id, pig_prod_id):
        
        sql = """
        SELECT 
            id,
            farm_prod_id,
            num_pigs_current
        FROM pig_production 
        WHERE pig_farm_id = %s AND production_group_id = %s  
        """ %(pig_farm_id, pig_prod_id)
            
            
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
            

        result = []
          
        for row in rows:
            
            cur_id                      = row[0]
            cur_farm_prod_id            = row[1]
            cur_num_pigs_current        = row[2]
          
            cur_entry ={
                'id':               cur_id,
                'farm_prod_id':     cur_farm_prod_id,     
                'pigs_join_group':  cur_num_pigs_current
                
            }
                
            result.append(cur_entry)
    
        return result
    
    
    
        

    
        
