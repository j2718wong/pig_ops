# February 13, 2026
# Jack Wong

from common_constants       import *


class PigProdFeed:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProdFeed'


    def add(self, data = None):
        """
        PROCEDURE pig_prod_feed_add(
            in_user_id              INT,
            
            in_pig_prod_id          INT,
            in_pig_farm_feed_buy_id INT,
            
            in_date_add             VARCHAR(10),
            
            
            in_num_gesta            INT,
            in_num_lacta            INT,
            in_num_booster          INT,
            in_num_prestarter       INT,
            in_num_starter          INT,
            in_num_grower           INT,
            in_num_finisher         INT,
            
            
            in_feed_item_gesta_id        INT,
            in_feed_item_lacta_id        INT,
            in_feed_item_booster_id      INT,
            in_feed_item_prestarter_id   INT,
            in_feed_item_starter_id      INT,
            in_feed_item_grower_id       INT,
            in_feed_item_finisher_id     INT
        )  
        """
        
        sql =  'CALL pig_prod_feed_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        sql += '%s,'    % data.pig_farm_feed_buy_id
        
        sql += '"%s",'  % data.date_add
        
        
        if data.num_gesta is not None and data.num_gesta > 0:
            sql += '%s,'    % data.num_gesta
        
        if data.num_lacta is not None and data.num_lacta > 0:
            sql += '%s,'    % data.num_lacta
        
        if data.num_booster is not None and data.num_booster > 0:
            sql += '%s,'    % data.num_booster
        
        if data.num_prestarter is not None and data.num_prestarter > 0:
            sql += '%s,'    % data.num_prestarter
        
        if data.num_starter is not None and data.num_starter > 0:
            sql += '%s,'    % data.num_starter
        
        if data.num_grower is not None and data.num_grower > 0:
            sql += '%s,'    % data.num_grower
        
        if data.num_finisher is not None and data.num_finisher > 0:
            sql += '%s,'    % data.num_finisher
        
        
        if data.feed_item_gesta_id is not None and data.feed_item_gesta_id > 0:
            sql += '%s,'    % data.feed_item_gesta_id
        
        if data.feed_item_lacta_id is not None and data.feed_item_lacta_id > 0:
            sql += '%s,'    % data.feed_item_lacta_id
        
        if data.feed_item_booster_id is not None and data.feed_item_booster_id > 0:
            sql += '%s,'    % data.feed_item_booster_id
        
        if data.feed_item_prestarter_id is not None and data.feed_item_prestarter_id > 0:
            sql += '%s,'    % data.feed_item_prestarter_id
        
        if data.feed_item_starter_id is not None and data.feed_item_starter_id > 0:
            sql += '%s,'    % data.feed_item_starter_id
        
        if data.feed_item_grower_id is not None and data.feed_item_grower_id > 0:
            sql += '%s,'    % data.feed_item_grower_id
        
        if data.feed_item_finisher_id is not None and data.feed_item_finisher_id > 0:
            sql += '%s)'    % data.feed_item_finisher_id
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        row = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            row = cursor.fetchone()
            cursor.close()

        except Exception as e:
            msg = 'add(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

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
            
            
            in_num_gesta            INT,
            in_num_lacta            INT,
            in_num_booster          INT,
            in_num_prestarter       INT,
            in_num_starter          INT,
            in_num_grower           INT,
            in_num_finisher         INT,
            
            
            in_feed_item_gesta_id        INT,
            in_feed_item_lacta_id        INT,
            in_feed_item_booster_id      INT,
            in_feed_item_prestarter_id   INT,
            in_feed_item_starter_id      INT,
            in_feed_item_grower_id       INT,
            in_feed_item_finisher_id     INT
        )  
        """
        
        sql =  'CALL pig_prod_feed_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_prod_feed_id
        
        sql += '"%s",'  % data.date_add
        
        
        if data.num_gesta is not None and data.num_gesta > 0:
            sql += '%s,'    % data.num_gesta
        
        if data.num_lacta is not None and data.num_lacta > 0:
            sql += '%s,'    % data.num_lacta
        
        if data.num_booster is not None and data.num_booster > 0:
            sql += '%s,'    % data.num_booster
        
        if data.num_prestarter is not None and data.num_prestarter > 0:
            sql += '%s,'    % data.num_prestarter
        
        if data.num_starter is not None and data.num_starter > 0:
            sql += '%s,'    % data.num_starter
        
        if data.num_grower is not None and data.num_grower > 0:
            sql += '%s,'    % data.num_grower
        
        if data.num_finisher is not None and data.num_finisher > 0:
            sql += '%s,'    % data.num_finisher
        
        
        if data.feed_item_gesta_id is not None and data.feed_item_gesta_id > 0:
            sql += '%s,'    % data.feed_item_gesta_id
        
        if data.feed_item_lacta_id is not None and data.feed_item_lacta_id > 0:
            sql += '%s,'    % data.feed_item_lacta_id
        
        if data.feed_item_booster_id is not None and data.feed_item_booster_id > 0:
            sql += '%s,'    % data.feed_item_booster_id
        
        if data.feed_item_prestarter_id is not None and data.feed_item_prestarter_id > 0:
            sql += '%s,'    % data.feed_item_prestarter_id
        
        if data.feed_item_starter_id is not None and data.feed_item_starter_id > 0:
            sql += '%s,'    % data.feed_item_starter_id
        
        if data.feed_item_grower_id is not None and data.feed_item_grower_id > 0:
            sql += '%s,'    % data.feed_item_grower_id
        
        if data.feed_item_finisher_id is not None and data.feed_item_finisher_id > 0:
            sql += '%s)'    % data.feed_item_finisher_id
        
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        row = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            row = cursor.fetchone()
            cursor.close()

        except Exception as e:
            msg = 'update(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

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
    
    
    def get_list(self, pig_prod_id):
        
        
        sql =   """
                SELECT 
                    a.id,
                    
                    a.pig_farm_feed_buy_id,
                    
                    a.date_add,    
                    
                    a.num_gesta,                
                    a.num_lacta,                
                    a.num_booster,              
                    a.num_prestarter,             
                    a.num_starter,              
                    a.num_grower,               
                    a.num_finisher,             
                       
                    a.feed_brand_gesta_id,   
                    a.feed_brand_lacta_id,   
                    a.feed_brand_booster_id, 
                    a.feed_brand_prestarter_id, 
                    a.feed_brand_starter_id, 
                    a.feed_brand_grower_id,  
                    a.feed_brand_finisher_id,
                        
                    b.name AS feed_brand_gesta,   
                    c.name AS feed_brand_lacta,   
                    d.name AS feed_brand_booster, 
                    e.name AS feed_brand_prestarter, 
                    f.name AS feed_brand_starter, 
                    g.name AS feed_brand_grower,  
                    h.name AS feed_brand_finisher,
                    
                    a.unit_cost_gesta,                
                    a.unit_cost_lacta,                
                    a.unit_cost_booster,              
                    a.unit_cost_prestarter,             
                    a.unit_cost_starter,              
                    a.unit_cost_grower,               
                    a.unit_cost_finisher             
                    
                FROM pig_prod_feed a
                LEFT OUTER JOIN feed_brand b ON a.feed_brand_gesta_id = b.id
                LEFT OUTER JOIN feed_brand c ON a.feed_brand_lacta_id = c.id
                LEFT OUTER JOIN feed_brand d ON a.feed_brand_prestarter_id = d.id
                LEFT OUTER JOIN feed_brand e ON a.feed_brand_booster_id = e.id
                LEFT OUTER JOIN feed_brand f ON a.feed_brand_starter_id = f.id
                LEFT OUTER JOIN feed_brand g ON a.feed_brand_grower_id = g.id
                LEFT OUTER JOIN feed_brand h ON a.feed_brand_finisher_id = h.id
                
                WHERE a.pig_prod_id = %s
                ORDER BY a.date_add DESC
                """ % (pig_prod_id)
        
            
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            #conn.close()
            
        except Exception as e:
            msg = 'get_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_id                      = row[0]
                
                cur_pig_farm_feed_buy_id    = row[1]
                
                cur_date_add                = str(row[2])
                
                cur_num_gesta               = row[3]
                cur_num_lacta               = row[4]                
                cur_num_booster             = row[5]              
                cur_num_prestarter          = row[6]             
                cur_num_starter             = row[7]              
                cur_num_grower              = row[8]               
                cur_num_finisher            = row[9]             
                
                cur_feed_brand_gesta_id     = row[10]   
                cur_feed_brand_lacta_id     = row[11]   
                cur_feed_brand_booster_id   = row[12] 
                cur_feed_brand_prestarter_id= row[13] 
                cur_feed_brand_starter_id   = row[14] 
                cur_feed_brand_grower_id    = row[15]  
                cur_feed_brand_finisher_id  = row[16]
                
                cur_feed_brand_gesta        = row[17]   
                cur_feed_brand_lacta        = row[18]   
                cur_feed_brand_booster      = row[19] 
                cur_feed_brand_prestarter   = row[20]
                cur_feed_brand_starter      = row[21] 
                cur_feed_brand_grower       = row[22]  
                cur_feed_brand_finisher     = row[23]
                
                cur_unit_cost_gesta         = float(row[24]) if row[24] else None              
                cur_unit_cost_lacta         = float(row[25]) if row[25] else None              
                cur_unit_cost_booster       = float(row[26]) if row[26] else None            
                cur_unit_cost_prestarter    = float(row[27]) if row[27] else None         
                cur_unit_cost_starter       = float(row[28]) if row[28] else None            
                cur_unit_cost_grower        = float(row[29]) if row[29] else None             
                cur_unit_cost_finisher      = float(row[30]) if row[30] else None            
                
                
                cur_entry = {
                    'id':               cur_id,
                    'pf_feed_buy_id':   cur_pig_farm_feed_buy_id,
                    'date_add':         cur_date_add,
                    
                    'feed_items':[]
                }
                
                
                if cur_num_gesta and cur_num_gesta > 0:
                    cur_feed = {
                        'type':         'gesta',
                        'brand': {
                            'id':       cur_feed_brand_gesta_id,
                            'name':     cur_feed_brand_gesta
                        },
                        
                        'num':          cur_num_gesta,
                        'unit_cost':    cur_unit_cost_gesta
                    } 
                    
                    cur_entry['feed_items'].append(cur_feed)
                
                
                if cur_num_lacta and cur_num_lacta > 0:
                    cur_feed = {
                        'type':         'lacta',
                        'brand': {
                            'id':       cur_feed_brand_lacta_id,
                            'name':     cur_feed_brand_lacta
                        },
                        
                        'num':          cur_num_lacta,
                        'unit_cost':    cur_unit_cost_lacta
                    } 
                    
                    cur_entry['feed_items'].append(cur_feed)
                
                
                if cur_num_booster and cur_num_booster > 0:
                    cur_feed = {
                        'type':         'booster',
                        'brand': {
                            'id':       cur_feed_brand_booster_id,
                            'name':     cur_feed_brand_booster
                        },
                        
                        'num':          cur_num_booster,
                        'unit_cost':    cur_unit_cost_booster
                    } 
                    
                    cur_entry['feed_items'].append(cur_feed)
                
                
                if cur_num_prestarter and cur_num_prestarter > 0:
                    cur_feed = {
                        'type':         'prestarter',
                        'brand': {
                            'id':       cur_feed_brand_prestarter_id,
                            'name':     cur_feed_brand_prestarter
                        },
                        
                        'num':          cur_num_prestarter,
                        'unit_cost':    cur_unit_cost_prestarter
                    } 
                    
                    cur_entry['feed_items'].append(cur_feed)
                
                
                if cur_num_starter and cur_num_starter > 0:
                    cur_feed = {
                        'type':         'starter',
                        'brand': {
                            'id':       cur_feed_brand_starter_id,
                            'name':     cur_feed_brand_starter
                        },
                        
                        'num':          cur_num_starter,
                        'unit_cost':    cur_unit_cost_starter
                    } 
                    
                    cur_entry['feed_items'].append(cur_feed)
                
                
                if cur_num_grower and cur_num_grower > 0:
                    cur_feed = {
                        'type':         'grower',
                        'brand': {
                            'id':       cur_feed_brand_grower_id,
                            'name':     cur_feed_brand_grower
                        },
                        
                        'num':          cur_num_grower,
                        'unit_cost':    cur_unit_cost_grower
                    } 
                    
                    cur_entry['feed_items'].append(cur_feed)
                
                
                if cur_num_finisher and cur_num_finisher > 0:
                    cur_feed = {
                        'type':         'finisher',
                        'brand': {
                            'id':       cur_feed_brand_finisher_id,
                            'name':     cur_feed_brand_finisher
                        },
                        
                        'num':          cur_num_finisher,
                        'unit_cost':    cur_unit_cost_finisher
                    } 
                    
                    cur_entry['feed_items'].append(cur_feed)
                
                
                
                result.append(cur_entry)
                    

        return result
    
    
   
