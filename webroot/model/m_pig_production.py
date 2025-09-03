# August 17, 2025
# Jack Wong

from common_constants       import *


class PigProduction:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProduction'

    
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
            msg = 'get_pig_prod_status_list(); error in executing query[] = ' + sql
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
            msg = 'update_insemination(); error in executing query[] = ' + sql
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
        
        sql =  'CALL pig_prod_update_birth('
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

    
    def update_feed_type(self, data = None):
        """
        PROCEDURE pig_prod_update_feed_type(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            in_feed_type_id         INT,
            in_date                 VARCHAR(10)
        )
        """
        
        sql =  'CALL pig_prod_update_feed_type('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        
        sql += '%s,'    % data.feed_type_id
        sql += '"%s");' % data.date
        
      
        
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
    
    
    def get_list(self, pig_farm_id = 0, list_ids = None):
        """
        Will get pig_production list.
        
        
        Returns
        -------
        list of dictionary

        """
        
        where_clause = ''
        
        if pig_farm_id > 0:
            where_clause = ' WHERE a.pig_farm_id = %s' % pig_farm_id
            
        else:
            count = 0
            s = ''
            for cur_entry in list_ids:
                if count > 0 : s += ','
                
                s += str(cur_entry)
            
            where_clause = ' WHERE a.id IN (%s)' % s
            
        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    
                    a.insemination_type,
                    
                    a.sow_id,
                    b.farm_sow_id,
                    b.number,
                    b.name,
                    
                    a.boar_id,
                    c.farm_boar_id,
                    c.number,
                    c.name,
                    
                    a.semen_source_id,
                    d.name AS semen_source_name,
                    d.description,
                    
                    a.semen_cost,
                    a.insemination_cost,
                    a.insem_cost_comments,
                    a.insem_staff_id,
                    a.date_insemination,
                    
                    e.name AS insem_staff_name,
                    
                    a.prod_status_id,
                    f.name AS prod_status_name,
                    
                    a.date_expected_birth,
                    a.date_actual_birth,
                    a.num_days_actual,
                    a.num_pigs_dead_at_birth,
                    a.num_pigs_live_m,
                    a.num_pigs_live_f,
                    
                    g.name AS birth_staff_name,
                    
                    a.date_weaning,
                    a.num_pigs_weaning_m,
                    a.num_pigs_weaning_f,
                    a.total_pigs_weight_weaning,
                    
                    a.num_pigs_current_m,
                    a.num_pigs_current_f,
                    
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    a.num_l_lactating,
                    a.num_l_booster,
                    a.num_l_prestarter,
                    a.num_l_starter,
                    a.num_l_grower,
                    a.num_l_finisher,
                    
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher
                    
                   
                FROM pig_production a
                LEFT OUTER JOIN sow_boar b          ON a.sow_id = b.id
                LEFT OUTER JOIN sow_boar c          ON a.boar_id = c.id
                LEFT OUTER JOIN semen_source d      ON a.semen_source_id = d.id
                LEFT OUTER JOIN pig_farm_staff e    ON a.insem_staff_id = e.id
                LEFT OUTER JOIN pig_prod_status f   ON a.prod_status_id = f.id
                LEFT OUTER JOIN pig_farm_staff g    ON a.insem_staff_id = g.id
                
                %s
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
                cur_prod_id                 = row[0]
                cur_prod_farm_prod_id       = row[1]
                cur_prod_insemination_type  = row[2]
                
                cur_sow_id                  = row[3]
                cur_sow_farm_sow_id         = row[4]
                cur_sow_number              = row[5]
                cur_sow_name                = row[6]
                
                cur_boar_id                 = row[7]
                cur_boar_farm_boar_id       = row[8]
                cur_boar_number             = row[9]
                cur_boar_name               = row[10]
                
                cur_semen_source_id         = row[11]
                cur_semen_source_name       = row[12]
                cur_semen_source_description = row[13]
                
                
                cur_insem_semen_cost        = row[14]
                cur_insem_insemination_cost = float(row[15])
                cur_insem_cost_comments     = row[16]
                    
                cur_insem_staff_id          = row[17]
                cur_insem_date_insemination = row[18]
                cur_insem_staff_name        = row[19]
                
                cur_prod_status_id          = row[20]
                cur_prod_status_name        = row[21]
                
                cur_prod_date_expected_birth    = row[22]
                cur_prod_date_actual_birth      = str(row[23]) if row[23] else None
                cur_prod_num_days_actual        = row[24] 
                cur_prod_num_pigs_dead_at_birth = row[25]
                cur_prod_num_pigs_live_m    = row[26]
                cur_prod_num_pigs_live_f    = row[27]
                cur_prod_birth_staff_name   = row[28]
                
                cur_weaning_date            = row[29]
                cur_weaning_num_pigs_m      = row[30]
                cur_weaning_num_pigs_f      = row[31]
                cur_weaning_weight          = row[32]
                
                
                cur_pig_count_m             = row[33]
                cur_pig_count_f             = row[34]
                
                
                cur_prod_num_b_lactating    = row[35]
                cur_prod_num_b_booster      = row[36]
                cur_prod_num_b_prestarter   = row[37]
                cur_prod_num_b_starter      = row[38]
                cur_prod_num_b_grower       = row[39]
                cur_prod_num_b_finisher     = row[40]
                
                cur_prod_num_l_lactating    = row[41]
                cur_prod_num_l_booster      = row[42]
                cur_prod_num_l_prestarter   = row[43]
                cur_prod_num_l_starter      = row[44]
                cur_prod_num_l_grower       = row[45]
                cur_prod_num_l_finisher     = row[46]
                
                cur_prod_cost_lactating     = row[47]
                cur_prod_cost_booster       = row[48]
                cur_prod_cost_prestarter    = row[49]
                cur_prod_cost_starter       = row[50]
                cur_prod_cost_grower        = row[51]
                cur_prod_cost_finisher      = row[52]
            
                
                cur_entry = {
                    'pig_production' :{
                        'id':               cur_prod_id, 
                        'farm_prod_id':     cur_prod_farm_prod_id,
                        'prod_status_id':   cur_prod_status_id,
                        'prod_status_name': cur_prod_status_name
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
                        
                        'semen_source': {
                            'id':           cur_semen_source_id,
                            'name':         cur_semen_source_name,
                            'description':  cur_semen_source_description,
                            'semen_cost':   cur_insem_semen_cost
                        },
                        
                        'insem_cost':       cur_insem_insemination_cost,
                        'cost_comments':    cur_insem_cost_comments,
                        'insem_date':       cur_insem_date_insemination,
                        'insem_staff_name': cur_insem_staff_name
                    },
                    
                    'birth': {
                        'date_expected':    cur_prod_date_expected_birth,
                        'date_actual':      cur_prod_date_actual_birth,
                        'num_days_actual':  cur_prod_num_days_actual,
                        'num_dead_at_birth':cur_prod_num_pigs_dead_at_birth,
                        
                        'pigs_live_m':      cur_prod_num_pigs_live_m,
                        'pigs_live_f':      cur_prod_num_pigs_live_f,
                        'birth_staff_name': cur_prod_birth_staff_name
                    },
                    
                    'weaning': {
                        'date_weaning':     cur_weaning_date,
                        'num_pigs_m':       cur_weaning_num_pigs_m,
                        'num_pigs_f':       cur_weaning_num_pigs_f,
                        'weight':           cur_weaning_weight    
                    },
                    
                    'current_pig_count': {
                        'm':                cur_pig_count_m,
                        'f':                cur_pig_count_f
                    },
                    
                    'feeds':{
                        'bought':{
                            'lactating':    cur_prod_num_b_lactating,
                            'booster':      cur_prod_num_b_booster,
                            'prestarter':   cur_prod_num_b_prestarter,
                            'starter':      cur_prod_num_b_starter,
                            'grower':       cur_prod_num_b_grower,
                            'finisher':     cur_prod_num_b_finisher
                        },
                        
                        'balance':{
                            'lactating':    float(cur_prod_num_l_lactating)     if cur_prod_num_l_lactating     is not None else None,
                            'booster':      float(cur_prod_num_l_booster)       if cur_prod_num_l_booster       is not None else None,
                            'prestarter':   float(cur_prod_num_l_prestarter)    if cur_prod_num_l_prestarter    is not None else None,
                            'starter':      float(cur_prod_num_l_starter)       if cur_prod_num_l_starter       is not None else None,
                            'grower':       float(cur_prod_num_l_grower)        if cur_prod_num_l_grower        is not None else None,
                            'finisher':     float(cur_prod_num_l_finisher)      if cur_prod_num_l_finisher      is not None else None
                        },
                        
                        'cost':{
                            'lactating':    float(cur_prod_cost_lactating)      if cur_prod_cost_lactating      is not None else None,
                            'booster':      float(cur_prod_cost_booster)        if cur_prod_cost_booster        is not None else None,
                            'prestarter':   float(cur_prod_cost_prestarter)     if cur_prod_cost_prestarter     is not None else None,
                            'starter':      float(cur_prod_cost_starter)        if cur_prod_cost_starter        is not None else None,
                            'grower':       float(cur_prod_cost_grower)         if cur_prod_cost_grower         is not None else None,
                            'finisher':     float(cur_prod_cost_finisher)       if cur_prod_cost_finisher       is not None else None
                        }
                    
                    }
                    
                }
                
                result.append(cur_entry)

        
        return result
    
    