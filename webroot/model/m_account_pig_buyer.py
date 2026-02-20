# September 1, 2025
# Jack Wong

from common_constants       import *


"""

/* account_pig_buyer.flag bits*/
DECLARE FLAG_BIT_ACCOUNT_PIG_BUYER_IS_DELETED   INT             DEFAULT 1;
DECLARE FLAG_BIT_PIG_BUYER_IS_BOAR_CUSTOMER     INT             DEFAULT 2;
"""
FLAG_BIT_PIG_BUYER_IS_BOAR_CUSTOMER     = 2


class AccountPigBuyer:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'AccountPigBuyer'


    def add(self, data = None):
        """
        PROCEDURE account_pig_buyer_add(
            in_user_id              INT,
    
            in_country_id           INT,
            in_address_level_1_id   INT,
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5),
            
            in_is_boar_customer     INT,
            
            
            
            in_name                 VARCHAR(50),
            in_contact_number       VARCHAR(20),
            in_whatsapp             VARCHAR(20),
            in_messenger            VARCHAR(50),
            in_description          VARCHAR(160)
        )  
        """
        
        sql =  'CALL account_pig_buyer_add('
        sql += '%s,'    % data.user_id
        
        if data.country_id > 0:
            sql += '%s,'    % data.country_id
        else:
            sql += 'NULL,'
        
        
        if data.level_1_id > 0:
            sql += '%s,'    % data.level_1_id
        else:
            sql += 'NULL,'
        
        
        if data.level_2_id > 0:
            sql += '%s,'    % data.level_2_id
        else:
            sql += 'NULL,'
        
        if data.level_3_id > 0:
            sql += '%s,'    % data.level_3_id
        else:
            sql += 'NULL,'
            
        
        if data.latitude is not None:
            sql += '%s,'    % data.latitude
        else:
            sql += 'NULL,'
        
        
        if data.longitude is not None:
            sql += '%s,'    % data.longitude
        else:
            sql += 'NULL,'
        
        
        sql += '%s,'    % data.is_boar_customer
        
        
        sql += '"%s",'  % data.name
        
        if data.contact_number is not None:
            sql += '"%s",'   % data.contact_number
        else:
            sql += 'NULL,'
            
        if data.whatsapp is not None:
            sql += '"%s",'   % data.whatsapp
        else:
            sql += 'NULL,'
        
        if data.messenger is not None:
            sql += '"%s",'   % data.messenger
        else:
            sql += 'NULL,'
        
        
        if data.description is not None:
            sql += '"%s");'   % data.description
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
                
                'account_pig_buyer': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE account_pig_buyer_update(
            in_user_id              INT,
            
            in_account_pig_buyer_id INT,
    
            in_country_id           INT,
            in_address_level_1_id   INT,
            in_address_level_2_id   INT,
            in_address_level_3_id   INT,
            
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5),
            
            in_is_boar_customer     INT,
            
            
            in_name                 VARCHAR(50),
            in_contact_number       VARCHAR(20),
            in_whatsapp             VARCHAR(20),
            in_messenger            VARCHAR(50),
            in_description          VARCHAR(160)
        )  
        """
        
        sql =  'CALL account_pig_buyer_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.account_pig_buyer_id
        
        if data.country_id > 0:
            sql += '%s,'    % data.country_id
        else:
            sql += 'NULL,'
        
        
        if data.address_level_1_id:
            sql += '%s,'    % data.address_level_1_id
        else:
            sql += 'NULL,'
        
        
        if data.address_level_2_id > 0:
            sql += '%s,'    % data.address_level_2_id
        else:
            sql += 'NULL,'
        
        if data.address_level_3_id:
            sql += '%s,'    % data.address_level_3_id
        else:
            sql += 'NULL,'
            
        
        if data.latitude is not None:
            sql += '%s,'    % data.latitude
        else:
            sql += 'NULL,'
        
        
        if data.longitude is not None:
            sql += '%s,'    % data.longitude
        else:
            sql += 'NULL,'
        
        
        sql += '%s,'    % data.is_boar_customer
        
        
        
        sql += '"%s",'  % data.name
        
        if data.contact_number is not None:
            sql += '"%s",'   % data.contact_number
        else:
            sql += 'NULL,'
            
        if data.whatsapp is not None:
            sql += '"%s",'   % data.whatsapp
        else:
            sql += 'NULL,'
        
        if data.messenger is not None:
            sql += '"%s",'   % data.messenger
        else:
            sql += 'NULL,'
        
        
        if data.description is not None:
            sql += '"%s");'   % data.description
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
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'pig_buyer': {
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
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        account_pig_buyer_id  = data['account_pig_buyer_id']
        
        """
        PROCEDURE account_pig_buyer_delete(
            in_user_id              INT,
            
            in_account_pig_buyer_id INT
        )
        """
       
        sql =  'CALL account_pig_buyer_delete('
        sql += '%s,'    % user_id
        sql += '%s);'   % account_pig_buyer_id
        
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
            msg = 'delete(); error in executing query[] = ' + sql
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
                
                'account_pig_buyer': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_list(self, account_id, inc_deleted = 0, inc_user_audit = 0):
        
        where_clause = 'WHERE a.account_id = %s ' % account_id
        
        if inc_deleted == 0:
            where_clause += ' AND (a.flag & 1) = 0' 
        
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.country_id,
                        b.name AS country_name,
                        
                        a.address_level_1_id,
                        a.address_level_2_id,
                        a.address_level_3_id,
                        
                        a.latitude,
                        a.longitude,
                        
                        a.flag,
                        
                        a.name,
                        a.contact_number,
                        a.whatsapp,
                        a.messenger,
                        a.description
                        
                    FROM account_pig_buyer a
                    LEFT OUTER JOIN app_country b ON a.country_id = b.id
                    %s
                    ORDER BY a.name
                    """ % where_clause
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.country_id,
                        b.name AS country_name,
                        
                        a.address_level_1_id,
                        a.address_level_2_id,
                        a.address_level_3_id,
                        
                        a.latitude,
                        a.longitude,
                        
                        a.flag,
                        
                        a.name,
                        a.contact_number,
                        a.whatsapp,
                        a.messenger,
                        a.description,
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM account_pig_buyer a
                    LEFT OUTER JOIN app_country b   ON a.country_id = b.id
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    ORDER BY a.name
                    """ % where_clause

            
        
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
                cur_pig_buyer_id        = row[0]
                
                cur_country_id          = row[1]
                cur_country_name        = row[2]
                
                cur_address_level_1_id  = row[3]
                cur_address_level_2_id  = row[4]
                cur_address_level_3_id  = row[5]
                
                cur_address_latitude    = float(row[6]) if row[6] is not None else None
                cur_address_longitude   = float(row[7]) if row[7] is not None else None
                
                cur_flag                = row[8]
                
                cur_name                = row[9]
                cur_contact_number      = row[10]
                cur_whatsapp            = row[11]
                cur_messenger           = row[12]
                cur_description         = row[13]
                        
                
                is_boar_customer = 0
                if cur_flag & FLAG_BIT_PIG_BUYER_IS_BOAR_CUSTOMER > 0:
                    is_boar_customer = 1
                    
                
                cur_entry = {
                    'pig_buyer': {
                        'id':           cur_pig_buyer_id,
                        
                        'is_boar_customer': is_boar_customer,
                        
                        'name':         cur_name,
                        'contact_number': cur_contact_number,
                        'whatsapp':     cur_whatsapp,
                        'messenger':    cur_messenger,
                        'description':  cur_description
                        
                    },
                    
                    'location':{
                        'country': {
                            'id':       cur_country_id,
                            'name':     cur_country_name
                        },
                        
                        'address':{
                            'level_1':  {
                                'id':   cur_address_level_1_id
                            },
                            
                            'level_2':  {
                                'id':   cur_address_level_2_id
                            },
                            
                            'level_3_id': {
                                'id':   cur_address_level_3_id
                            }
                        }
                    }
                    
                }
                
                if cur_address_latitude is not None and cur_address_longitude is not None:
                    geoloc = {
                        'latitude':     cur_address_latitude,
                        'longitude':    cur_address_longitude
                    }
                    
                    cur_entry['location']['geoloc'] = geoloc
                    
                
                if inc_user_audit > 0:
                        
                    added_by = {
                        'name_last':        row[14],
                        'name_first':       row[15],
                        'dt_entry':         str(row[16])
                    }
                    
                    last_update = {
                        'name_last':        row[17],
                        'name_first':       row[18],
                        'dt_update':        str(row[19]) if row[19] else None
                    }
                    
                    cur_entry['added_by'] =  added_by
                    
                    if last_update['dt_update'] is not None:
                        cur_entry['last_update'] = last_update
                    
                    
                result.append(cur_entry)
        
        return result
    
    
