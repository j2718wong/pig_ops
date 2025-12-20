# January 3, 2024
# Jack Wong

from common_constants       import *


class AccountSelection:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'Account Selection'


    def add(self, data):
        """
        PROCEDURE account_selection_add(
            in_user_id              INT,
            
            in_feed_brand_id        INT,
            in_feed_supplier_id     INT,
            in_semen_supplier_id    INT
        )  
        """
        
        sql =  'CALL account_selection_add('
        sql += '%s,'    % data.user_id
        
        if data.feed_brand_id > 0:
            sql += '%s,'    % data.feed_brand_id
        else:
            sql += 'NULL,'
        
        if data.feed_supplier_id > 0:
            sql += '%s,'    % data.feed_supplier_id
        else:
            sql += 'NULL,'
        
        if data.semen_supplier_id > 0:
            sql += '%s);'    % data.semen_supplier_id
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
                
                'account': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def delete(self, data):
        """
        PROCEDURE account_selection_delete(
            in_user_id              INT,
            
            in_feed_brand_id        INT,
            in_feed_supplier_id     INT,
            in_semen_supplier_id    INT
        )  
        """
        
        sql =  'CALL account_selection_delete('
        sql += '%s,'    % data.user_id
        
        if data.feed_brand_id is not None and data.feed_brand_id > 0:
            sql += '%s,'    % data.feed_brand_id
        else:
            sql += 'NULL,'
        
        if data.feed_supplier_id is not None and data.feed_supplier_id > 0:
            sql += '%s,'    % data.feed_supplier_id
        else:
            sql += 'NULL,'
        
        if data.semen_supplier_id and data.semen_supplier_id > 0:
            sql += '%s);'    % data.semen_supplier_id
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
                
                'account': {
                    'id':               row[3]
                }
            }

        return None
    
        
    
    def get_business_obj_selection(self, account_id, business_obj_id):
        
        if business_obj_id == BUSINESS_OBJ_ID_SEMEN_SUPPLIER:
            sql =   """
                    SELECT semen_supplier_id
                    FROM account_selection
                    WHERE account_id = %s AND semen_supplier_id > 0
                    """ % account_id
                    
        if business_obj_id == BUSINESS_OBJ_ID_FEED_SUPPLIER:
            sql =   """
                    SELECT feed_supplier_id
                    FROM account_selection
                    WHERE account_id = %s AND feed_supplier_id > 0
                    """ % account_id
            
        if business_obj_id == BUSINESS_OBJ_ID_FEED_BRAND:
            sql =   """
                    SELECT feed_brand_id
                    FROM account_selection
                    WHERE account_id = %s AND feed_brand_id > 0
                    """ % account_id
            
        
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
            msg = 'get_business_obj_selection(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        result = []
        if rows is not None:
            
            for row in rows:
                result.append(row[0])
        
        return result
    
    