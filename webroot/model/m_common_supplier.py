# August 24, 2025
# Jack Wong

from common_constants       import *

FLAG_BIT_COMMON_SUPPLIER_IS_VERIFIED    = 2;

class CommonSupplier:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'CommonSupplier'


    def add(self, data = None):
        """
        PROCEDURE common_supplier_add(
            in_user_id              INT,

            in_country_id           INT,
            in_address_level_1_id   INT,
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            
            in_is_feed_supplier     INT,
            in_is_gilt_supplier     INT,
            in_is_semen_supplier    INT,
            
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5),
    
            in_name                 VARCHAR(50)
            in_contact_number       VARCHAR(20),
            in_whatsapp             VARCHAR(20),
            in_messenger            VARCHAR(50)
        )  
        """
        
        sql =  'CALL common_supplier_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.country_id
        sql += '%s,'    % data.level_1_id
        sql += '%s,'    % data.level_2_id
        
        if data.level_3_id is not None and data.level_3_id > 0:
            sql += '%s,'    % data.level_3_id
        else:
            sql += 'NULL,'
        
        
        sql += '%s,'    % data.is_feed_supplier
        sql += '%s,'    % data.is_gilt_supplier
        sql += '%s,'    % data.is_semen_supplier

        
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
            cur_flag = row[4]
                    
            is_verified = 0
            if cur_flag & FLAG_BIT_COMMON_SUPPLIER_IS_VERIFIED > 0:
                is_verified = 1
                
                
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'supplier': {
                    'id':               row[3],
                    'name':             row[5],
                    
                    'is_verified':      is_verified,
                    
                    'is_fs':            data.is_feed_supplier,
                    'is_gs':            data.is_gilt_supplier,
                    'is_ss':            data.is_semen_supplier
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
                        },
                        
                        'geoloc':{
                            'latitude':     data.latitude,
                            'longitude':    data.longitude
                        }
                        
                    }
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE common_supplier_update(
            in_user_id              INT,
            
            in_common_supplier_id   INT,
            
            in_address_level_3_id   INT,
            
            in_is_feed_supplier     INT,
            in_is_gilt_supplier     INT,
            in_is_semen_supplier    INT,
            
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5),
            
            in_name                 VARCHAR(50),
            in_contact_number       VARCHAR(20),
            in_whatsapp             VARCHAR(20),
            in_messenger            VARCHAR(50)
        )  
        """
        
        sql =  'CALL common_supplier_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.supplier_id
        
        
        if data.level_3_id is not None and data.level_3_id > 0:
            sql += '%s,'    % data.level_3_id
        else:
            sql += 'NULL,'
        
        
        sql += '%s,'    % data.is_feed_supplier
        sql += '%s,'    % data.is_gilt_supplier
        sql += '%s,'    % data.is_semen_supplier
        
        
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
            
            cur_is_feed_supplier    = row[9]
            cur_is_gilt_supplier    = row[10]
            cur_is_semen_supplier   = row[11]
    
            
            cur_country_id          = row[12]
            cur_address_level_1_id  = row[13]
            cur_address_level_2_id  = row[14]
            cur_address_level_3_id  = row[15]
            
            cur_address_latitude    = float(row[16]) if row[16] is not None else None
            cur_address_longitude   = float(row[17]) if row[17] is not None else None
            
            
                    
            is_verified = 0
            if cur_flag & FLAG_BIT_COMMON_SUPPLIER_IS_VERIFIED > 0:
                is_verified = 1
          
            
            return {
                'result':{
                    'num':              cur_res_num,
                    'code':             cur_res_code,
                    'desc':             cur_res_desc,
                },
                
                'supplier': {
                    'id':               cur_id,
                    'name':             cur_name,
                    'contact_number':   cur_contact_number,
                    'whatsapp':         cur_whatsapp,
                    'messenger':        cur_messenger,
                    
                    'is_verified':      is_verified,
                    
                    'is_fs':            cur_is_feed_supplier,
                    'is_gs':            cur_is_gilt_supplier,
                    'is_ss':            cur_is_semen_supplier
                    
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
    
    
    def get_list(self, account_id = 0, 
            address_level_1_id  = 0, 
            address_level_2_id  = 0, 
            
            is_feed_supplier    = 0, 
            is_gilt_supplier    = 0, 
            is_semen_supplier   = 0):
        
       
        if address_level_1_id > 0:
            
            # Only include not deleted 
            
            where_clause = 'WHERE address_level_1_id = %s ' % address_level_1_id
            where_clause += ' AND (flag & 1) = 0'
            
            if is_feed_supplier > 0:
                where_clause += ' AND is_feed_supplier > 0 '
            
            elif is_gilt_supplier > 0:
                where_clause += ' AND is_gilt_supplier > 0 '
                
            elif is_semen_supplier > 0:
                where_clause += ' AND is_semen_supplier > 0 '
                
            sql =   """
                    SELECT 
                        id,
                        flag,
                        name,
                        contact_number,
                        whatsapp,
                        messenger,
                        
                        country_id,
                        address_level_1_id,
                        address_level_2_id,
                        address_level_3_id,
                        
                        latitude,
                        longitude,
                        
                        is_feed_supplier,
                        is_gilt_supplier,
                        is_semen_supplier
                        
                    FROM common_supplier
                    %s
                    ORDER BY name
                    """ % where_clause
        
        
        if address_level_2_id > 0:
            
            # Only include not deleted 
            
            where_clause = 'WHERE address_level_2_id = %s ' % address_level_2_id
            where_clause += ' AND (flag & 1) = 0'
            
            if is_feed_supplier > 0:
                where_clause += ' AND is_feed_supplier > 0 '
            
            elif is_gilt_supplier > 0:
                where_clause += ' AND is_gilt_supplier > 0 '
                
            elif is_semen_supplier > 0:
                where_clause += ' AND is_semen_supplier > 0 '
            
            sql =   """
                    SELECT 
                        id,
                        flag,
                        name,
                        contact_number,
                        whatsapp,
                        messenger,
                        
                        country_id,
                        address_level_1_id,
                        address_level_2_id,
                        address_level_3_id,
                        
                        latitude,
                        longitude,
                        
                        is_feed_supplier,
                        is_gilt_supplier,
                        is_semen_supplier
                                                
                    FROM common_supplier 
                    %s 
                    ORDER BY name
                    """ % where_clause
        
        
        if account_id > 0:
            
            if is_feed_supplier > 0:
                sql =   """
                        SELECT 
                            a.feed_supplier_id,
                            
                            b.flag,
                            b.name,
                            b.contact_number,
                            b.whatsapp,
                            b.messenger,
                            
                            b.country_id,
                            b.address_level_1_id,
                            b.address_level_2_id,
                            b.address_level_3_id,
                            
                            b.latitude,
                            b.longitude,
                        
                            b.is_feed_supplier,
                            b.is_gilt_supplier,
                            b.is_semen_supplier
                            
                        FROM account_selection a
                        LEFT OUTER JOIN common_supplier b   ON a.feed_supplier_id = b.id
                        WHERE   a.account_id = %s AND 
                                a.feed_supplier_id IS NOT NULL  AND 
                                (a.flag & 1) = 0 AND
                                b.is_feed_supplier > 0
                        ORDER BY b.name; 
                """% account_id
                    
            
            elif is_gilt_supplier > 0:
                sql =   """
                        SELECT 
                            a.gilt_supplier_id,
                            
                            b.flag,
                            b.name,
                            b.contact_number,
                            b.whatsapp,
                            b.messenger,
                            
                            b.country_id,
                            b.address_level_1_id,
                            b.address_level_2_id,
                            b.address_level_3_id,
                            
                            b.latitude,
                            b.longitude,
                        
                            b.is_feed_supplier,
                            b.is_gilt_supplier,
                            b.is_semen_supplier
                            
                        FROM account_selection a
                        LEFT OUTER JOIN common_supplier b   ON a.gilt_supplier_id = b.id
                        WHERE   a.account_id = %s AND 
                                a.gilt_supplier_id IS NOT NULL AND 
                                (a.flag & 1) = 0 AND
                                b.is_gilt_supplier > 0
                        ORDER BY b.name; 
                """% account_id
                    
                
            elif is_semen_supplier > 0:
                sql =   """
                        SELECT 
                            a.semen_supplier_id,
                            
                            b.flag,
                            b.name,
                            b.contact_number,
                            b.whatsapp,
                            b.messenger,
                            
                            b.country_id,
                            b.address_level_1_id,
                            b.address_level_2_id,
                            b.address_level_3_id,
                            
                            b.latitude,
                            b.longitude,
                        
                            b.is_feed_supplier,
                            b.is_gilt_supplier,
                            b.is_semen_supplier
                            
                        FROM account_selection a
                        LEFT OUTER JOIN common_supplier b   ON a.semen_supplier_id = b.id
                        WHERE   a.account_id = %s AND 
                                a.semen_supplier_id IS NOT NULL AND 
                                (a.flag & 1) = 0 AND
                                b.is_semen_supplier > 0
                        ORDER BY b.name; 
                """% account_id
            
       
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
                    
                cur_supplier_id         = row[0]
                cur_flag                = row[1]
                cur_name                = row[2]
                cur_contact_number      = row[3]
                cur_whatsapp            = row[4]
                cur_messenger           = row[5]
                    
                cur_country_id          = row[6]
                cur_address_level_1_id  = row[7]
                cur_address_level_2_id  = row[8]
                cur_address_level_3_id  = row[9]
                
                cur_address_latitude    = float(row[10]) if row[10] is not None else None
                cur_address_longitude   = float(row[11]) if row[11] is not None else None
            
                cur_is_feed_supplier    = row[12]
                cur_is_gilt_supplier    = row[13]
                cur_is_semen_supplier   = row[14]
                
                is_verified = 0
                if cur_flag & FLAG_BIT_COMMON_SUPPLIER_IS_VERIFIED > 0:
                    is_verified = 1
                
                cur_entry = {
                    'supplier': {
                        'id':               cur_supplier_id,
                        'name':             cur_name,
                        'contact_number':   cur_contact_number,
                        'whatsapp':         cur_whatsapp,
                        'messenger':        cur_messenger,
                        
                        'is_verified':      is_verified,
                        
                        'is_fs':            cur_is_feed_supplier,
                        'is_gs':            cur_is_gilt_supplier,
                        'is_ss':            cur_is_semen_supplier
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
                            },
                            
                            'geoloc':{
                                'latitude':     cur_address_latitude,
                                'longitude':    cur_address_longitude
                            }
                            
                        }
                    }
                }
                
                
                if cur_entry['supplier']['contact_number'] is None:
                    del cur_entry['supplier']['contact_number']
                else:
                    if len(cur_entry['supplier']['contact_number']) == 0:
                        del cur_entry['supplier']['contact_number']
                   
                   
                if cur_entry['supplier']['whatsapp'] is None:
                    del cur_entry['supplier']['whatsapp']
                else:
                    if len(cur_entry['supplier']['whatsapp']) == 0:
                        del cur_entry['supplier']['whatsapp']
                
                
                if cur_entry['supplier']['messenger'] is None:
                    del cur_entry['supplier']['messenger']
                else:
                    if len(cur_entry['supplier']['messenger']) == 0:
                        del cur_entry['supplier']['messenger']
                
                
                if cur_entry['location']['address']['geoloc']['latitude'] is None:
                    del cur_entry['location']['address']['geoloc']
                    
                result.append(cur_entry)
        
        return result
    
    
    def get_supplier_count(self, country_id = 1, 
            address_level_1_id = None,
            is_feed_supplier = 0,
            is_gilt_supplier = 0,
            is_semen_supplier = 0):
        
        if address_level_1_id is None:
            where_clause = 'WHERE country_id = %s AND  flag & 1 = 0 ' % country_id
            
            if is_feed_supplier > 0:
                where_clause += ' AND is_feed_supplier > 0 '
            
            elif is_gilt_supplier > 0:
                where_clause += ' AND is_gilt_supplier > 0 '
                
            elif is_semen_supplier > 0:
                where_clause += ' AND is_semen_supplier > 0 '
            
            
            sql =   """
                    SELECT 
                        address_level_1_id,
                        COUNT(*) AS cnt
                    FROM common_supplier 
                    %s
                    GROUP BY address_level_1_id;
                    """ % where_clause
        
        else:
            where_clause = 'WHERE   address_level_1_id = %s AND flag & 1 = 0 ' % address_level_1_id
            
            if is_feed_supplier > 0:
                where_clause += ' AND is_feed_supplier > 0 '
            
            elif is_gilt_supplier > 0:
                where_clause += ' AND is_gilt_supplier > 0 '
                
            elif is_semen_supplier > 0:
                where_clause += ' AND is_semen_supplier > 0 '
            
            sql =   """
                    SELECT 
                        address_level_2_id,
                        COUNT(*) AS cnt
                    FROM common_supplier 
                    %s  
                    GROUP BY address_level_2_id;
                    """ % where_clause
        
        print(sql)
                
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
            msg = 'get_supplier_count(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        result = []
        if rows is not None:
            
            for row in rows:
                cur_entry = {
                    'id':               row[0],
                    'count':            row[1]
                }
                
                result.append(cur_entry)
        
        return result
    
