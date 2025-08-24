# August 17, 2025
# Jack Wong

from common_constants       import *


class PigProduction:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProduction'

    
    def get_production_status_list(self):
        """
        Will get production_status list.
        
        
        Returns
        -------
        list of dictionary

        """
            
        sql =   """
                SELECT 
                    id,
                    name
                FROM production_status
                """ 
        
        
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
            conn.close()
            
        except Exception as e:
            msg = 'get_production_status_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

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

    
    def add(self, data = None):
        """
        PROCEDURE pig_farm_add(
            in_user_id              INT,

            in_name                 VARCHAR(50),
            
            in_country_id           INT, 
            in_adrs_level_1_id      INT,
            in_adrs_level_2_id      INT,
            in_adrs_level_3_id      INT,
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5)
        )  
        """
        
        sql =  'CALL pig_farm_add('
        sql += '%s,'    % data.user_id
        sql += '"%s",'  % data.name
        
        sql += '%s,'    % data.country_id
        sql += '%s,'    % data.adrs_level_1_id
        sql += '%s,'    % data.adrs_level_2_id
        sql += '%s,'    % data.adrs_level_3_id
        
        if data.latitude is not None:
            sql += '%s,'    % data.latitude
        else:
            sql += 'NULL,'
            
        if data.longitude is not None:
            sql += '%s);'   % data.longitude
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
                
                'pig_farm': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5]
                }
            }

        return None

    
    def update_hashid(self, data = None):
        pig_farm_id     = data['pig_farm_id']
        hashid          = data['hashid']
        
        values = (hashid, pig_farm_id)
        
        sql =   """
                UPDATE pig_farm SET
                    hashid    = "%s"
                WHERE id = %s;
                """ % values
        
        return self.model.execute_sql(sql)
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_farm_update(
            in_user_id              INT,
            in_pig_farm_id          INT,

            in_name                 VARCHAR(50),
            
            in_country_id           INT, 
            in_adrs_level_1_id      INT,
            in_adrs_level_2_id      INT,
            in_adrs_level_3_id      INT,
            in_latitude             DECIMAL(10,5),
            in_longitude            DECIMAL(10,5)
        )
        """
       
        sql =  'CALL pig_farm_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_farm_id
        sql += '"%s",'  % data.name
        
        sql += '%s,'    % data.country_id
        sql += '%s,'    % data.adrs_level_1_id
        sql += '%s,'    % data.adrs_level_2_id
        sql += '%s,'    % data.adrs_level_3_id
        
        if data.latitude is not None:
            sql += '%s,'    % data.latitude
        else:
            sql += 'NULL,'
            
        if data.longitude is not None:
            sql += '%s);'   % data.longitude
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
                
                'pig_farm': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5]
                }
            }

        return None
        
    
    def get_list(self, account_id = 0, id_list = None):
        """
        Will get pig farm list.
        
        
        Returns
        -------
        list of dictionary

        """
        
        if account_id > 0:
            where_clause = 'account_id = %s' % account_id
        else:
            
            for cur_entry in id_list:
                test = 1
            
        sql =   """
                SELECT 
                    a.hashid,
                    a.flag,
                    a.name,
                    a.country_id,
                    b.name AS country_name,
                    a.adrs_level_1_id,
                    a.adrs_level_2_id,
                    a.adrs_level_3_id,
                    a.latitude,
                    a.longitude
                FROM pig_farm a
                LEFT OUTER JOIN app_country b ON a.country_id = b.id
                WHERE account_id = %s
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
            conn.close()
            
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
                cur_farm_hashid         = row[0]
                cur_farm_flag           = row[1]
                cur_farm_name           = row[2]
                
                cur_country_id          = row[3]
                cur_country_name        = row[4]
                
                cur_farm_adrs_level_1_id= row[5]
                cur_farm_adrs_level_2_id= row[6]
                cur_farm_adrs_level_3_id= row[7]
                cur_farm_latitude       = float(row[8]) if row[8] else None
                cur_farm_longitude      = float(row[9]) if row[9] else None
                
               
                cur_entry = {
                    'h_id':             cur_farm_hashid, 
                    'flag':             cur_farm_flag,
                    'name':             cur_farm_name,
                    
                    'location':{
                        'country_id':   cur_country_id,
                        'country_name': cur_country_name,
                        
                        'address':{
                            'level_1_id': cur_farm_adrs_level_1_id,
                            'level_2_id': cur_farm_adrs_level_2_id,
                            'level_3_id': cur_farm_adrs_level_3_id
                        },
                        
                        'geoloc':{
                            'latitude':  cur_farm_latitude,
                            'longitude': cur_farm_longitude,
                        }
                    }
                    
                }
                
                result.append(cur_entry)

        
        return result
    
    