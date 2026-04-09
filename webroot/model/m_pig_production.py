# August 17, 2025
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


class PigProduction(BaseModel):
    def __init__(self, model):
        super().__init__(model)

    
    def add(self, data = None):
        """
        PROCEDURE pig_prod_add(
            in_user_id              INT,
           
            in_sow_id               INT,    /* Cannot be updated*/
            in_boar_id              INT,
            in_semen_supplier_id    INT,
            in_semen_sup_semen_id   INT,    /* semen supplier semen_id*/
            in_semen_ai_boar_id     INT,    /* semen coming from one of farm's boar*/
    
            in_semen_cost           DECIMAL(6,2),
            in_insemination_cost    DECIMAL(6,2),
            in_comments             VARCHAR(160),
            
            in_insem_staff_id       INT,
            in_done_by_user         INT, 
            
            in_date_insemination    VARCHAR(10)  /* in YYYY-MM-DD format*/
        )  
        """
        
        is_ai = not (data.boar_id and data.boar_id > 0)
        
        params = [
            data.user_id,
            
            data.sow_id,
            data.boar_id                if not is_ai else None,
            
            data.semen_supplier_id      if is_ai else None,
            data.semen_sup_semen_id     if is_ai else None,
            data.semen_ai_boar_id       if is_ai else None,
            
            data.semen_cost             if is_ai else None,
            data.insemination_cost,
            
            
            data.comments               if data.comments and data.comments.strip() else None,
                                        
            data.insem_staff_id         if data.insem_staff_id and data.insem_staff_id > 0 else None,
            data.done_by_user,
            
            data.insem_date
        ]
        
        res = self._call_procedure('pig_prod_add', params)
        
        if res is None:
            return None
        
        
        row = res[0]
        
        
        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod': {
                    'id':               row[3]
                }
            }

        return None

    
    def add_fattening(self, data = None):
        """
        PROCEDURE pig_prod_fattening_add(
            in_user_id              INT,
            in_pig_farm_id          INT,
            
            in_num_pigs             INT,
            
            in_date_weaning         VARCHAR(10),
            in_date_added           VARCHAR(10)
        )  
        """
        
        params = [
            data.user_id,
            data.pig_farm_id,
            
            data.num_pigs,
            
            data.date_weaning,
            data.date_added
        ]
        
        res = self._call_procedure('pig_prod_fattening_add', params)
        
        if res is None:
            return None
        
        row = res[0]
    

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod': {
                    'id':               row[3]
                }
            }

        return None

    
    def update_insemination(self, data = None):
        """
        PROCEDURE pig_prod_update_insem(
            in_user_id              INT,
            
            in_pig_prod_id          INT,
            in_boar_id              INT,
            
            in_semen_supplier_id    INT,
            in_semen_sup_semen_id  	INT,    /* semen supplier semen_id*/
            in_semen_ai_boar_id     INT,    /* semen coming from one of farm's boar*/
            
            
            in_semen_cost           DECIMAL(6,2),
            in_insemination_cost    DECIMAL(6,2),
            in_comments             VARCHAR(160),
            
            in_insem_staff_id       INT,
            in_date_insemination    VARCHAR(10)  /* in YYYY-MM-DD format*/
        )  
        """
        
        is_ai = not (data.boar_id and data.boar_id > 0)
        
        params = [
            data.user_id,
            data.pig_prod_id,

            data.boar_id                if not is_ai else None,
            
            data.semen_supplier_id      if is_ai else None,
            data.semen_sup_semen_id     if is_ai else None,
            data.semen_ai_boar_id       if is_ai else None,
            
            data.semen_cost             if is_ai else None,
            data.insemination_cost      if data.insemination_cost is not None else None,
            
            data.comments               if data.comments and data.comments.strip() else None,
            
            data.insem_staff_id         if data.insem_staff_id and data.insem_staff_id > 0 else None,
            data.insem_date
        ]
        
        res = self._call_procedure('pig_prod_update_insem', params)
        
        if res is None:
            return None
        
        row = res[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod': {
                    'id':               row[3]
                }
            }

        return None

    
    def update_status(self, data = None):
        """
        PROCEDURE pig_prod_update_status(
            in_user_id              INT,
            
            in_pig_production_id    INT,
            in_pig_prod_status_id   INT,
            
            in_date_status          VARCHAR(10),
            in_notes                VARCHAR(160)
        )  
        """
        
        params = [
            data.user_id,
            
            data.pig_prod_id,
            data.prod_status_id,
            
            data.date_status,
            
            data.notes                  if data.notes and data.notes.strip() else None
        ]
        
        res = self._call_procedure('pig_prod_update_status', params)
        
        if res is None:
            return None
        
        row = res[0]
    

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod': {
                    'id':               row[3]
                }
            }

        return None

    
    def update_birth(self, data = None):
        """
        PROCEDURE pig_prod_update_birth(
            in_user_id                  INT,
            
            in_pig_production_id        INT,
            
            in_date_actual_birth        VARCHAR(10),  /* in YYYY-MM-DD format*/
            in_num_pigs_dead_at_birth   INT,
            in_num_pigs_live_male       INT,
            in_num_pigs_live_female     INT,
            
            in_birth_staff_id           INT,
            in_done_by_user             INT
        )  
        """
        
        params = [
            data.user_id,
            
            data.pig_prod_id,
            
            data.date_actual_birth,
            data.num_pigs_dead,
            data.num_pigs_male,
            data.num_pigs_female,
            
            data.birth_staff_id         if data.birth_staff_id and data.birth_staff_id > 0 else None,
            data.done_by_user
        ]
        
        res = self._call_procedure('pig_prod_update_birth', params)
        
        if res is None:
            return None

        
        row = res[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod': {
                    'id':               row[3]
                },
                
                'added_new_staff':      row[4]
            }

        return None

    
    def update_weaning(self, data = None):
        """
        PROCEDURE pig_prod_update_weaning(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            in_date_weaning         VARCHAR(10),
            
            in_num_pigs_female      INT,
            in_num_pigs_male        INT,
            
            /* There is an option to count the pigs 
            regardless of sex. This is because it maybe time 
            consuming to count per sex at wean. */
            in_num_pigs             INT,    
            
            in_total_weight         DECIMAL(6,2),
            in_per_pig_weight       VARCHAR(200)
        )  
        """
        
        # Determine if we're using per-sex counts or total count
        use_combined = True if data.num_pigs else False
        
        params = [
            data.user_id,
            
            data.pig_prod_id,
            data.date_weaning,
            
            data.num_pigs_female            if not use_combined else None,
            data.num_pigs_male              if not use_combined else None,
            
            data.num_pigs                   if use_combined else None,
            data.num_pigs_xsmall            if (data.num_pigs_xsmall and data.num_pigs_xsmall > 0) else None, 
            
            data.total_weight               if data.total_weight is not None else None,
            data.weight_pp                  if data.weight_pp and data.weight_pp.strip() else None
        ]
        
        res = self._call_procedure('pig_prod_update_weaning', params)
        
        
        if res is None:
            return None
        
        
        row = res[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update_pig_count(self, data = None):
        """
        PROCEDURE pig_prod_update_pig_count(
            in_user_id              INT,           
            in_pig_prod_id          INT,
            
            in_num_pigs             INT,
            in_date_notes           VARCHAR(10),
            in_notes                VARCHAR(160)

        )  
        """
        
        params = [
            data.user_id,
            data.pig_prod_id,
            
            data.num_pigs,
            data.date_notes,
            data.notes                  if data.notes and data.notes.strip() else None
        ]
        
        res = self._call_procedure('pig_prod_update_pig_count', params)
        
        if res is None:
            return None
        
        
        row = res[0]
        
    
        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod': {
                    'id':               row[3]
                }
            }

        return None

    
    def update_feed_start_date(self, data = None):
        """
        PROCEDURE pig_prod_update_feed_start_date(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            in_feed_type_id         INT,
            in_feed_start_date      VARCHAR(10)
        )
        """
        
        params = [
            data.user_id,
            
            data.pig_prod_id,
            
            data.feed_type_id,
            data.date_start
        ]
        
        res = self._call_procedure('pig_prod_update_feed_start_date', params)
        
        if res is None:
            return None

        
        row = res[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                }
            }

        return None
    
    
    def create_group(self, data = None):
        """
        PROCEDURE production_group_create(
            in_user_id              INT,

            in_pig_prod_id          INT, /*initial pig_production in the production_group*/
            
            in_date_added           VARCHAR(10)
        ) 
        """
        
        params = [
            data['user_id'],
            
            data['pig_prod_id'],
            
            data['date_added']
        ]
        
        res = self._call_procedure('production_group_create', params)
        
        if res is None:
            return None

        
        row = res[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod':{
                    'id':               row[3]
                }
            }

        return None
    
   
    def add_to_group(self, data = None):
        """
        PROCEDURE production_group_pig_prod_add(
            in_user_id              INT,

            in_production_group_id  INT,
            in_pig_prod_id          INT,
            
            in_date_added           VARCHAR(10)
        )  
        """
        
        params = [
            data['user_id'],
            
            data['prod_group_id'],
            data['pig_prod_id'],
            
            data['date_added']
        ]
        
        res = self._call_procedure('production_group_pig_prod_add', params)
        
        if res is None:
            return None

        
        row = res[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_prod':{
                    'id':               row[3]
                }
            }

        return None
    


