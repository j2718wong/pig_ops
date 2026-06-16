# February 13, 2026
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


class PigProdFeed(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE pig_prod_feed_add(
            in_user_id              INT,
            
            in_pig_prod_id          INT,
            in_pig_farm_feed_buy_id INT,
            
            in_date_add             VARCHAR(10),
            
            
            in_num_gesta            INT, /** must be > 0; can be NULL; */
            in_num_lacta            INT, /** must be > 0; can be NULL; */   
            in_num_booster          INT, /** must be > 0; can be NULL; */
            in_num_prestarter       INT, /** must be > 0; can be NULL; */
            in_num_starter          INT, /** must be > 0; can be NULL; */
            in_num_grower           INT, /** must be > 0; can be NULL; */
            in_num_finisher         INT  /** must be > 0; can be NULL; */
        )  
        """
        
        params = [
            data.user_id,
            data.pig_prod_id,
            data.pig_farm_feed_buy_id,
            data.date_add,
            
            data.num_gesta       if data.num_gesta and data.num_gesta > 0 else None,
            data.num_lacta       if data.num_lacta and data.num_lacta > 0 else None,
            data.num_booster     if data.num_booster and data.num_booster > 0 else None,
            data.num_prestarter  if data.num_prestarter and data.num_prestarter > 0 else None,
            data.num_starter     if data.num_starter and data.num_starter > 0 else None,
            data.num_grower      if data.num_grower and data.num_grower > 0 else None,
            data.num_finisher    if data.num_finisher and data.num_finisher > 0 else None
        ]
        
        res = self._call_procedure('pig_prod_feed_add', params)
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
                
                'pig_prod_feed': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_prod_feed_update(
            in_user_id              INT,
            
            in_pig_prod_feed_id     INT,
    
    
            in_date_add             VARCHAR(10),
            
            
            in_num_gesta            INT, /** can be >= 0; cannot be NULL*/
            in_num_lacta            INT, /** can be >= 0; cannot be NULL*/   
            in_num_booster          INT, /** can be >= 0; cannot be NULL*/
            in_num_prestarter       INT, /** can be >= 0; cannot be NULL*/
            in_num_starter          INT, /** can be >= 0; cannot be NULL*/
            in_num_grower           INT, /** can be >= 0; cannot be NULL*/
            in_num_finisher         INT  /** can be >= 0; cannot be NULL*/
        )  
        """
        
        params = [
            data.user_id,
            data.pig_prod_feed_id,
            data.date_add,
            
            data.num_gesta,
            data.num_lacta,
            data.num_booster,
            data.num_prestarter,
            data.num_starter,
            data.num_grower,
            data.num_finisher
        ]
        
        res = self._call_procedure('pig_prod_feed_update', params)
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
                
                'pig_prod_feed': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def change_feed_date(self, data = None):
        """
        PROCEDURE pig_prod_feed_change_date(
            in_user_id              INT,
            in_pig_prod_id          INT,
            
            in_feed_type_id         INT,
            
            in_date_change          VARCHAR(10)
        )  
        """
        
        params = [
            data.user_id,
            data.pig_prod_id,
            data.feed_type_id,
            data.date_change
        ]
    
        res = self._call_procedure('pig_prod_feed_change_date', params)
        if res is None:
            return None

        
        row = res[0]


        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2]
                },
                
                'feed_change_date': {
                    'booster':          str(row[3]) if row[3] else None, 
                    'prestarter':       str(row[4]) if row[4] else None,
                    'starter':          str(row[5]) if row[5] else None,
                    'grower':           str(row[6]) if row[6] else None,
                    'finisher':         str(row[7]) if row[7] else None
                }
            }

        return None
    
    
    def get_list(self, pig_prod_id):
        
        sql =   """
                SELECT 
                    a.id,
                    a.pig_farm_feed_buy_id,
                    b.feed_supplier_id,
                    c.name AS supplier_name,
                    a.date_add        
                    
                FROM pig_prod_feed a
                LEFT OUTER JOIN pig_farm_feed_buy b ON a.pig_farm_feed_buy_id = b.id
                LEFT OUTER JOIN common_supplier c   ON b.feed_supplier_id = c.id
                WHERE a.pig_prod_id = %s
                ORDER BY a.date_add DESC
                """ % (pig_prod_id)
        
            
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
            
        for row in rows:
            cur_id                      = row[0]
            cur_pig_farm_feed_buy_id    = row[1]
            cur_feed_supplier_id        = row[2]
            cur_feed_supplier_name      = row[3]
            cur_date_add                = str(row[4])
            
           
            cur_entry = {
                'pig_prod_feed': {
                    'id':               cur_id,
                    'pf_feed_buy_id':   cur_pig_farm_feed_buy_id,
                    'date_add':         cur_date_add
                },
                
                'feed_supplier': {
                    'id':           cur_feed_supplier_id,
                    'name':         cur_feed_supplier_name
                } 
            }
            
            feed_items = self.get_list_items(cur_id)
            cur_entry['feed_items'] = feed_items
            
            result.append(cur_entry)
                

        return result
    
    
    
    def get_list_items(self, pig_prod_feed_id):
        
        sql =   """
                SELECT 
                    
                    a.id,
                    a.feed_type_id,
                    a.feed_brand_id,
                    
                    a.quantity,
                    a.kg_per_unit,
                    a.kg_total,
                    
                    a.unit_cost,
                    a.total_cost,

                    b.name_short  AS feed_type_name,
                    c.name  AS feed_brand_name
                    
                FROM feed_buy a 
                LEFT OUTER JOIN feed_type b         ON a.feed_type_id = b.id
                LEFT OUTER JOIN feed_brand c        ON a.feed_brand_id = c.id
                WHERE a.pig_prod_feed_id = %s
                ORDER BY a.id ASC
        
                """ % (pig_prod_feed_id)
        
        rows = self._execute_query(sql)
        
        if rows is None:
            return []
        
        
        result = []
        
        for row in rows:
            cur_id                  = row[0]
            
            cur_feed_type_id        = row[1]
            cur_feed_brand_id       = row[2]

            cur_quantity            = row[3]
            cur_kg_per_unit         = row[4]
            cur_kg_total            = row[5]
        
            cur_unit_cost           = float(row[6]) if row[6] is not None else None
            cur_total_cost          = float(row[7]) if row[7] is not None else None
            
            cur_feed_type_name      = row[8]
            cur_feed_brand_name     = row[9]
            
            
            cur_entry = {
                
                'feed_item':{
                    'id':           cur_id,
                    'quantity':     cur_quantity,
                    'kg_per_unit':  cur_kg_per_unit,
                    'kg_total':     cur_kg_total,
                    
                    'unit_cost':    cur_unit_cost,
                    'total_cost':   cur_total_cost,
                },
                
                
                'feed_type':{
                    'id':           cur_feed_type_id,
                    'name':         cur_feed_type_name 
                },
                
                'feed_brand':{
                    'id':           cur_feed_brand_id,
                    'name':         cur_feed_brand_name
                }
                
            }
            
            result.append(cur_entry)
            
              
        return result
    
