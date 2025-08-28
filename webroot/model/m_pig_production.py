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
            #conn.close()
            
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

    
    def get_by_id(self, prod_id):
        sql =   """
                SELECT 
                    id,
                    account_id,
                    pig_farm_id,
                    farm_prod_id,
                    sow_id,
                    insemination_type,
                    
                    semen_boar_id,
                    semen_source_id,
                    semen_cost,
                    insemination_cost,
                    insem_cost_comments,
                    insem_staff_id,
                    date_insemination,
                    date_expected_birth,
                    date_actual_birth,
                    num_days_actual,
                    status_id,
                    num_pigs_dead_at_birth,
                    num_pigs_live_m',
                    num_pigs_live_f,
                    birth_staff_id,
                    
                    num_pigs_weaning_m',
                    num_pigs_weaning_f',
                    total_pigs_weight_weaning
                    num_pigs_current_m,
                    num_pigs_current_f,
                    
                    date_iron_1,
                    date_iron_2,
                    date_vitamins_1,
                    date_vitamins_2,
                    date_kapon,
                    date_deworm,
                    
                    date_booster,
                    date_prestarter,
                    date_weaning,
                    date_starter,
                    date_grower,
                    date_finisher,
                    date_harvest,
                    
                    num_b_lactating,
                    num_b_booster,
                    num_b_prestarter,
                    num_b_starter,
                    num_b_grower,
                    num_b_finisher,
                    
                    num_l_lactating,
                    num_l_booster,
                    num_l_prestarter,
                    num_l_starter,
                    num_l_grower,
                    num_l_finisher,
                    
                    cost_lactating,
                    cost_booster,
                    cost_prestarter,
                    cost_starter,
                    cost_grower,
                    cost_finisher

                FROM pig_production
                WHERE id = %s
                """ % prod_id
        
        
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
            """
            
            for row in rows:
                       
               
                cur_entry = {
                    'id':,
                    'account_id':,
                    'pig_farm_id':,
                    'farm_prod_id':,
                    'sow_id':,
                    'insemination_type':,
                    
                    'semen_boar_id':,
                    'semen_source_id':,
                    'semen_cost':,
                    'insemination_cost':,
                    'insem_cost_comments':,
                    'insem_staff_id':,
                    'date_insemination':,
                    'date_expected_birth':,
                    'date_actual_birth':,
                    'num_days_actual':,
                    'status_id':,
                    'num_pigs_dead_at_birth':,
                    'num_pigs_live_m':,
                    'num_pigs_live_f':,
                    'birth_staff_id':,
                    
                    'num_pigs_weaning_m':,
                    'num_pigs_weaning_f':,
                    'total_pigs_weight_weaning':
                    'num_pigs_current_m':,
                    'num_pigs_current_f':,
                    
                    'date_iron_1':,
                    'date_iron_2':,
                    'date_vitamins_1':,
                    'date_vitamins_2':,
                    'date_kapon':,
                    'date_deworm':,
                    
                    'date_booster':,
                    'date_prestarter':,
                    'date_weaning':,
                    'date_starter':,
                    'date_grower':,
                    'date_finisher':,
                    'date_harvest':,
                    
                    'feed_buy':
                    'num_b_lactating':,
                    'num_b_booster':,
                    'num_b_prestarter':,
                    'num_b_starter':,
                    'num_b_grower':,
                    'num_b_finisher':,
                    
                    'num_l_lactating':,
                    'num_l_booster':,
                    'num_l_prestarter':,
                    'num_l_starter':,
                    'num_l_grower':,
                    'num_l_finisher':,
                    
                    'cost_lactating':,
                    'cost_booster':,
                    'cost_prestarter':,
                    'cost_starter':,
                    'cost_grower':,
                    'cost_finisher':
                    
                }
                
                return cur_entry
            """
        
        return result
    
    
        
        
    
    def add(self, data = None):
        """
        PROCEDURE pig_prod_add(
            in_user_id              INT,
           
            in_sow_id               INT,
            in_boar_id              INT,
            in_semen_source_id      INT,
            
            in_semen_cost           DECIMAL(6,2),
            in_insemination_cost    DECIMAL(6,2),
            in_insem_cost_comments  VARCHAR(200),
            
            in_insem_staff_id       INT,
            in_date_insemination    VARCHAR(10)  /* in YYYY-MM-DD format*/
        )  
        """
        
        sql =  'CALL pig_prod_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.sow_id
        
        if data.boar_id is not None:
            sql += '%s,'    % data.boar_id
            sql += 'NULL,'
            sql += '0.0,'
        else:
            sql += 'NULL,'
            sql += '%s,'    % data.semen_source_id
            sql += '%s,'    % data.semen_cost
            
            
        sql += '%s,'    % data.insemination_cost
            
        if data.insem_cost_comments is not None:
            sql += '"%s",'    % data.insem_cost_comments
        else:
            sql += 'NULL,'
            
        sql += '%s,'    % data.insem_staff_id
        sql += '"%s");' % data.date_insemination
        
        
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
                
                'pig_prod': {
                    'id':               row[3]
                },
                
                'pig_prod_ai' :{
                    'id':               row[4]
                }
            }

        return None

    
    def update_insemination(self, data = None):
        """
        PROCEDURE pig_prod_update_insem(
            in_user_id              INT,
            
            in_pig_prod_id          INT,
            
            in_semen_cost           DECIMAL(6,2),
            in_insemination_cost    DECIMAL(6,2),
            in_insem_cost_comments  VARCHAR(200),
            
            in_insem_staff_id       INT,
            in_date_insemination    VARCHAR(10)  /* in YYYY-MM-DD format*/
        )  
        """
        
        sql =  'CALL pig_prod_update_insem('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        
        sql += '%s,'    % data.insemination_cost
        
        if data.insem_cost_comments is not None:
            sql += '"%s",'    % data.insem_cost_comments
        else:
            sql += 'NULL,'
            
        sql += '%s,'    % data.insem_staff_id
        sql += '"%s");' % data.date_insemination
       
        
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
            msg = 'update_birth(); error in executing query[] = ' + sql
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
            
            in_birth_staff_id           INT
        )  
        """
        
        sql =  'CALL pig_production_update_birth('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        
        sql += '"%s",'  % data.date_actual_birth
        sql += '%s,'    % data.num_pigs_dead
            
        sql += '%s,'    % data.num_pigs_male
        sql += '%s,'    % data.num_pigs_female
        sql += '%s);'   % data.birth_staff_id
       
        
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
            msg = 'update_birth(); error in executing query[] = ' + sql
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
                
                'pig_prod': {
                    'id':               row[3]
                }
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
            
            in_total_weight         INT
        )  
        """
        
        sql =  'CALL pig_prod_update_weaning('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        
        sql += '"%s",'  % data.date_weaning
            
        sql += '%s,'    % data.num_pigs_male
        sql += '%s,'    % data.num_pigs_female
        
        if data.total_weight is not None:
            sql += '%s);'    % data.total_weight
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
            msg = 'update_weaning(); error in executing query[] = ' + sql
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
                
                'pig_prod': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update_current_count(self, data = None):
        """
        PROCEDURE pig_prod_update_current_count(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            
            in_num_pigs_female      INT,
            in_num_pigs_male        INT
        )  
        """
        
        sql =  'CALL pig_prod_update_current_count('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        
        sql += '%s,'    % data.num_pigs_female
        sql += '%s);'   % data.num_pigs_male
       
        
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
            msg = 'update_current_count(); error in executing query[] = ' + sql
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
                
                'pig_prod': {
                    'id':               row[3]
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
                    'hid':             cur_farm_hashid, 
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
    
    