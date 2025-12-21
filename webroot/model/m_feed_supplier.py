# August 24, 2025
# Jack Wong

from common_constants       import *


class FeedSupplier:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'FeedSupplier'


    def add(self, data = None):
        """
        PROCEDURE feed_supplier_add(
            in_user_id              INT,

            in_country_id           INT,
            in_address_level_1_id   INT,
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5),
            
            in_name                 VARCHAR(50)
            in_contact_number       VARCHAR(20),
            in_whatsapp             VARCHAR(20),
            in_messenger            VARCHAR(50)
        )  
        """
        
        sql =  'CALL feed_supplier_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.country_id
        sql += '%s,'    % data.level_1_id
        sql += '%s,'    % data.level_2_id
        
        if data.level_3_id is not None and data.level_3_id > 0:
            sql += '%s,'    % data.level_3_id
        else:
            sql += 'NULL,'
        
        
        if data.latitude is not None and data.latitude > 0:
            sql += '%s,'    % data.latitude
        else:
            sql += 'NULL,'
        
        if data.longitude is not None and data.longitude > 0:
            sql += '%s,'    % data.longitude
        else:
            sql += 'NULL,'
        
        
        sql += '"%s",'  % data.name
        
        if data.contact_number is not None and len(data.contact_number) > 0:
            sql += '"%s",'  % data.contact_number
        else:
            sql += 'NULL,'
        
        if data.whatsapp is not None and len(data.whatsapp) > 0:
            sql += '"%s",'  % data.whatsapp
        else:
            sql += 'NULL,'
        
        
        if data.messenger is not None and len(data.messenger) > 0:
            sql += '"%s");' % data.messenger
        else:
            sql += 'NULL);'
        
        
        
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
                
                'feed_supplier': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                },
                
                'location':{
                            
                    'country': {
                        'id':           data.country_id
                    },
                    
                    'address': {
                        'level_1':{
                            'id':       data.level_1_id
                        },
                    
                        'level_2':{
                            'id':       data.level_2_id
                        },
                        
                        'level_3':{
                            'id':       data.level_3_id
                        }
                        
                    }
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE feed_supplier_update(
            in_user_id              INT,
            
            in_feed_supplier_id     INT,
            
            in_address_level_3_id   INT,
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5),
            
            in_name                 VARCHAR(50),
            in_contact_number       VARCHAR(20),
            in_whatsapp             VARCHAR(20),
            in_messenger            VARCHAR(50)
        )  
        """
        
        sql =  'CALL feed_supplier_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.feed_supplier_id
        
       
        if data.level_3_id is not None and data.level_3_id > 0:
            sql += '%s,'    % data.level_3_id
        else:
            sql += 'NULL,'
        
        if data.latitude is not None and data.latitude > 0:
            sql += '%s,'    % data.latitude
        else:
            sql += 'NULL,'
        
        if data.longitude is not None and data.longitude > 0:
            sql += '%s,'    % data.longitude
        else:
            sql += 'NULL,'
        
        sql += '"%s",'  % data.name
        
        if data.contact_number is not None and len(data.contact_number) > 0:
            sql += '"%s",'  % data.contact_number
        else:
            sql += 'NULL,'
        
        if data.whatsapp is not None and len(data.whatsapp) > 0:
            sql += '"%s",'  % data.whatsapp
        else:
            sql += 'NULL,'
        
        
        if data.messenger is not None and len(data.messenger) > 0:
            sql += '"%s");' % data.messenger
        else:
            sql += 'NULL);'
        
        
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
            cur_res_num             = row[0]
            cur_res_code            = row[1]
            cur_res_desc            = row[2]
            
            cur_id                  = row[3]
            cur_flag                = row[4]
            cur_name                = row[5]
            cur_contact_number      = row[6]
            cur_whatsapp            = row[7]
            cur_messenger           = row[8]
            
            cur_country_id          = row[9]
            cur_address_level_1_id  = row[10]
            cur_address_level_2_id  = row[11]
            cur_address_level_3_id  = row[12]
            
            cur_address_latitude    = float(row[13]) if row[13] is not None else None
            cur_address_longitude   = float(row[14]) if row[14] is not None else None
            
            
            
                    
            is_verified = 0
            if cur_flag & FLAG_BIT_SEMEN_SUPPLIER_IS_VERIFIED > 0:
                is_verified = 1
          
            return {
                'result':{
                    'num':              cur_res_num,
                    'code':             cur_res_code,
                    'desc':             cur_res_desc,
                },
                
                'feed_supplier': {
                    'id':               cur_id,
                    'name':             cur_name,
                    'contact_number':   cur_contact_number,
                    'whatsapp':         cur_whatsapp,
                    'messenger':        cur_messenger,
                    'is_verified':      is_verified
                },
                
                'location':{
                            
                    'country': {
                        'id':           cur_country_id
                    },
                    
                    'address': {
                        'level_1':{
                            'id':       cur_address_level_1_id
                        },
                    
                        'level_2':{
                            'id':       cur_address_level_2_id
                        },
                        
                        'level_3':{
                            'id':       cur_address_level_3_id
                        }
                        
                    },
                    
                    'geoloc':{
                        'latitude':     cur_address_latitude,
                        'longitude':    cur_address_longitude
                    }
                }
            }

        return None
    
    
    def get_list(self, account_id = 0, address_level_1_id = 0, 
            address_level_2_id = 0, list_ids = None, minimum_info = 1):
        
        if minimum_info == 0:
            if address_level_2_id > 0:
                sql =   """
                        SELECT 
                            a.id,
                            a.name,
                            a.contact_number,
                            a.whatsapp,
                            a.messenger,
                            
                            a.country_id,
                            b.name AS country_name,
                            a.address_level_1_id,
                            a.address_level_2_id,
                            a.address_level_3_id
                            
                        FROM feed_supplier a 
                        LEFT OUTER JOIN app_country b   ON a.country_id = b.id
                        WHERE  a.address_level_2_id = %s 
                        ORDER BY a.name
                        """ % address_level_2_id
            
            
            if address_level_1_id > 0:
                sql =   """
                        SELECT 
                            a.id,
                            a.name,
                            a.contact_number,
                            a.whatsapp,
                            a.messenger,
                            
                            a.country_id,
                            b.name AS country_name,
                            a.address_level_1_id,
                            a.address_level_2_id,
                            a.address_level_3_id
                            
                        FROM feed_supplier a 
                        LEFT OUTER JOIN app_country b   ON a.country_id = b.id
                        WHERE  a.address_level_1_id = %s 
                        ORDER BY a.name
                        """ % address_level_1_id
            
            
            if account_id > 0:
                sql =   """
                        SELECT 
                            a.feed_supplier_id,
                            
                            b.name,
                            b.contact_number,
                            b.whatsapp,
                            b.messenger,
                            
                            b.country_id,
                            c.name AS country_name,
                            b.address_level_1_id,
                            b.address_level_2_id,
                            b.address_level_3_id
                        FROM account_selection a
                        LEFT OUTER JOIN feed_supplier b   ON a.feed_supplier_id = b.id
                        LEFT OUTER JOIN app_country c   ON b.country_id = c.id
                        WHERE a.account_id = %s AND a.feed_supplier_id IS NOT NULL AND b.name IS NOT NULL
                        ORDER BY b.name; 
                """% account_id
        
            if list_ids is not None:
                
                list_str_ids = [str(cur_id) for cur_id in list_ids]
                ids = ','.join(list_str_ids)
                
                sql =   """
                        SELECT 
                            a.id,
                            
                            a.name,
                            a.contact_number,
                            a.whatsapp,
                            a.messenger,
                            
                            a.country_id,
                            b.name AS country_name,
                            a.address_level_1_id,
                            a.address_level_2_id,
                            a.address_level_3_id
                        FROM feed_supplier a
                        LEFT OUTER JOIN app_country b   ON a.country_id = b.id
                        WHERE a.id IN (%s)
                        ORDER BY a.id DESC; 
                """% ids
        
        else:
            if account_id > 0:
                sql =   """
                        SELECT 
                            a.feed_supplier_id,
                            b.name,
                            b.address_level_3_id
                        FROM account_selection a
                        LEFT OUTER JOIN feed_supplier b   ON a.feed_supplier_id = b.id
                        WHERE a.account_id = %s AND a.feed_supplier_id IS NOT NULL AND b.name IS NOT NULL
                        ORDER BY a.id DESC; 
                """% account_id
         
            
            if address_level_2_id > 0:
                sql =   """
                        SELECT 
                            a.id,
                            a.name,
                            a.address_level_3_id
                            
                        FROM feed_supplier a 
                        WHERE  a.address_level_2_id = %s 
                        ORDER BY a.name
                        """ % address_level_2_id
            
        
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
                if minimum_info == 0:
                    cur_entry = {
                        'feed_supplier': {
                            'id':               row[0],
                            'name':             row[1],
                            'contact_number':   row[2],
                            'whatsapp':         row[3],
                            'messenger':        row[4]
                        },
                        
                        'location':{
                            
                            'country': {
                                'id':           row[5],
                                'name':         row[6]
                            },
                            
                            'address': {
                                'level_1':{
                                    'id':       row[7]
                                },
                            
                                'level_2':{
                                    'id':       row[8]
                                },
                                
                                'level_3':{
                                    'id':       row[9]
                                }
                                
                            }
                        }
                    }
                    
                else: 
                    cur_entry = {
                        'id':               row[0],
                        'name':             row[1],
                        'level_3_id':       row[2]
                    }
                    
                result.append(cur_entry)
        
        return result
    
    