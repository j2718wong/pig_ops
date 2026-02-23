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
        
        sql =  'CALL pig_prod_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.sow_id
        
        if data.boar_id is not None and data.boar_id > 0:
            sql += '%s,'    % data.boar_id
            sql += 'NULL,'
            sql += 'NULL,'
            sql += 'NULL,'
            sql += 'NULL,'
        else:
            sql += 'NULL,'
            
            if data.semen_supplier_id is not None:
                sql += '%s,'    % data.semen_supplier_id
            else:
                sql += 'NULL,'
                
            if data.semen_sup_semen_id is not None:
                sql += '%s,'    % data.semen_sup_semen_id
            else:
                sql += 'NULL,'
            
            if data.semen_ai_boar_id is not None:
                sql += '%s,'    % data.semen_ai_boar_id
            else:
                sql += 'NULL,'
            
            if data.semen_cost is not None:
                sql += '%s,'    % data.semen_cost
            else:
                sql += 'NULL,'
            
            
        sql += '%s,'    % data.insem_cost
            
        if data.insem_notes is not None and len(data.insem_notes) > 0:
            sql += '"%s",'    % data.insem_notes
        else:
            sql += 'NULL,'
        
        if data.insem_staff_id is not None and data.insem_staff_id > 0: 
            sql += '%s,'    % data.insem_staff_id
        else:
            sql += 'NULL,'
            
        sql += '%s,'    % data.done_by_user
        
        
        sql += '"%s");' % data.insem_date
        
        
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
        
        sql =  'CALL pig_prod_fattening_add('
        sql += '%s,'    % data.user_id        
        sql += '%s,'    % data.pig_farm_id
        sql += '%s,'    % data.num_pigs
        
        sql += '"%s",'  % data.date_weaning
        sql += '"%s");'  % data.date_added
        
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
            msg = 'add_fattening(); error in executing query[] = ' + sql
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
        
        sql =  'CALL pig_prod_update_insem('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        
        if data.boar_id is not None and data.boar_id > 0:
            sql += '%s,'    % data.boar_id
            sql += 'NULL,'
            sql += 'NULL,'
            sql += 'NULL,'
            sql += 'NULL,'
        else:
            sql += 'NULL,'
            
            if data.semen_supplier_id is not None:
                sql += '%s,'    % data.semen_supplier_id
            else:
                sql += 'NULL,'
                
            if data.semen_sup_semen_id is not None:
                sql += '%s,'    % data.semen_sup_semen_id
            else:
                sql += 'NULL,'
            
            if data.semen_ai_boar_id is not None:
                sql += '%s,'    % data.semen_ai_boar_id
            else:
                sql += 'NULL,'
                
            if data.semen_cost is not None:
                sql += '%s,'    % data.semen_cost
            else:
                sql += 'NULL,'
        
        sql += '%s,'    % data.insem_cost
        
        if data.insem_notes is not None:
            sql += '"%s",'    % data.insem_notes
        else:
            sql += 'NULL,'
            
        sql += '%s,'    % data.insem_staff_id
        sql += '"%s");' % data.insem_date
        
        
        
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
        
        sql =  'CALL pig_prod_update_status('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_prod_id
        sql += '%s,'    % data.prod_status_id
        
        sql += '"%s",'  % data.date_status
        
        
        if data.notes is not None:
            sql += '"%s");'    % data.notes
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
            
            in_birth_staff_id           INT,
            in_done_by_user             INT
        )  
        """
        
        sql =  'CALL pig_prod_update_birth('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        
        sql += '"%s",'  % data.date_actual_birth
        sql += '%s,'    % data.num_pigs_dead
            
        sql += '%s,'    % data.num_pigs_male
        sql += '%s,'    % data.num_pigs_female
        if data.birth_staff_id is not None:
            sql += '%s,'    % data.birth_staff_id
        else:
            sql += 'NULL,'
        
        sql += '%s);'   % data.done_by_user
        
        
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
            
            in_total_weight         INT
        )  
        """
        
        sql =  'CALL pig_prod_update_weaning('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        sql += '"%s",'  % data.date_weaning
        
        if data.num_pigs is None:
            sql += '%s,'    % data.num_pigs_male
            sql += '%s,'    % data.num_pigs_female
            sql += 'NULL,'
        else:
            sql += 'NULL,'
            sql += 'NULL,'
            sql += '%s,'    % data.num_pigs
        
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
        
        sql =  'CALL pig_prod_update_pig_count('
        sql += '%s,'    % data.user_id        
        sql += '%s,'    % data.pig_prod_id
        
        sql += '%s,'    % data.num_pigs
        sql += '"%s",'   % data.date_notes
        sql += '"%s");'  % data.notes
       
        
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
            msg = 'update_pig_count(); error in executing query[] = ' + sql
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

    
    def update_feed_start_date(self, data = None):
        """
        PROCEDURE pig_prod_update_feed_start_date(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            in_feed_type_id         INT,
            in_feed_start_date      VARCHAR(10)
        )
        """
        
        sql =  'CALL pig_prod_update_feed_start_date('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        
        sql += '%s,'    % data.feed_type_id
        sql += '"%s");' % data.date_start
        
      
        
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
                }
            }

        return None
    
    
    def get_list(self, pig_farm_id = 0 , pig_prod_type = 0, pig_prod_id = None):
        """
        Will get pig_production list.
        
       
        
        Returns
        -------
        list of dictionary

        """
        
        if pig_farm_id > 0:
            order_clause = 'ORDER BY a.date_insemination'
            
            if pig_prod_type == 1:
                where_clause = 'WHERE a.pig_farm_id = %s AND  a.prod_status_id = 1 ' % pig_farm_id
            
            if pig_prod_type == 2:
                where_clause = 'WHERE a.pig_farm_id = %s AND  a.prod_status_id = 4 ' % pig_farm_id
            
            if pig_prod_type == 3:
                where_clause = 'WHERE a.pig_farm_id = %s AND  a.prod_status_id IN (1, 4) ' % pig_farm_id
            
            if pig_prod_type == 4:
                where_clause = 'WHERE a.pig_farm_id = %s AND  a.prod_status_id IN (5, 6) ' % pig_farm_id
                
            if pig_prod_type == 5:
                where_clause = 'WHERE a.pig_farm_id = %s AND  a.prod_status_id IN (1, 4, 5, 6) ' % pig_farm_id
                
            if pig_prod_type == 6:
                where_clause = 'WHERE a.pig_farm_id = %s AND  a.prod_status_id IN (8, 9) ' % pig_farm_id
                
                order_clause = 'ORDER BY a.date_weaning DESC'
            
        else:
            where_clause = 'WHERE a.id = %s ' % pig_prod_id
                
    
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
                    
                    a.semen_supplier_id,
                    d.name AS semen_supplier_name,
                    
                    a.semen_sup_semen_id,
                    e.name as semen_supplier_semen_name,
                    
                    a.semen_ai_boar_id,
                    f.farm_boar_id,
                    f.number,
                    f.name,
                    
                    a.semen_cost,
                    a.insemination_cost,
                    a.date_insemination,
                    
                    
                    g.notes AS insem_notes,
                    
                    
                    a.insem_staff_id,
                    h.name AS insem_staff_name,
                    
                    a.prod_status_id,
                    i.name AS prod_status_name,
                    
                    a.date_expected_birth,
                    a.date_actual_birth,
                    a.num_days_actual,
                    a.num_pigs_dead_at_birth,
                    a.num_pigs_live_m,
                    a.num_pigs_live_f,
                    a.birth_staff_id,
                    j.name AS birth_staff_name,
                    
                    a.date_weaning,
                    a.num_pigs_weaning_m,
                    a.num_pigs_weaning_f,
                    a.num_pigs_weaning,
                    a.total_pigs_weight_weaning,
                    
                    a.num_pigs_current,
                    
                    a.num_b_gestating,
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    k.date_balance,
                    k.num_gestating,
                    k.num_lactating,
                    k.num_booster,
                    k.num_prestarter,
                    k.num_starter,
                    k.num_grower,
                    k.num_finisher,
                    
                    a.cost_gestating,
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher,
                    
                    a.date_gestating,
                    a.date_lactating,
                    a.date_booster,
                    a.date_prestarter,
                    a.date_starter,
                    a.date_grower,
                    a.date_finisher,
                    
                    
                    a.data_ver_num_pig_prod,
                    a.data_ver_num_medvac, 
                    a.data_ver_num_health_notes,
                    a.data_ver_num_prod_feed,
                    a.data_ver_num_feed_balance,
                    a.data_ver_num_harvest     
                    
                   
                FROM pig_production a
                LEFT OUTER JOIN sow_boar b          ON a.sow_id = b.id
                LEFT OUTER JOIN sow_boar c          ON a.boar_id = c.id
                
                LEFT OUTER JOIN common_supplier d   ON a.semen_supplier_id = d.id
                LEFT OUTER JOIN semen_supplier_semen e ON a.semen_sup_semen_id = e.id
                LEFT OUTER JOIN sow_boar f          ON a.semen_ai_boar_id = f.id
                
                LEFT OUTER JOIN pig_prod_notes g    ON a.insem_notes_id = g.id
                LEFT OUTER JOIN pig_farm_staff h    ON a.insem_staff_id = h.id
                LEFT OUTER JOIN pig_prod_status i   ON a.prod_status_id = i.id
                LEFT OUTER JOIN pig_farm_staff j    ON a.birth_staff_id = j.id
                LEFT OUTER JOIN feed_balance k      ON a.last_feed_balance_id = k.id
                %s
                %s
                """ % (where_clause, order_clause)


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
                
                cur_semen_supplier_id       = row[11]
                cur_semen_supplier_name     = row[12]
                
                cur_semen_sup_semen_id      = row[13]
                cur_semen_sup_semen_name    = row[14]
                
                cur_semen_ai_boar_id        = row[15]
                cur_semen_ai_farm_boar_id   = row[16]
                cur_semen_ai_boar_number    = row[17]
                cur_semen_ai_boar_name      = row[18]
                
                cur_insem_semen_cost        = float(row[19]) if row[19] else 0.0
                cur_insem_insemination_cost = float(row[20]) if row[20] else 0.0
                cur_insem_date_insemination = str(row[21]) if row[21] else None
                
                
                cur_insem_notes             = row[22]
                
                
                cur_insem_staff_id          = row[23]
                cur_insem_staff_name        = row[24]
                
                cur_prod_status_id          = row[25]
                cur_prod_status_name        = row[26]
                
                cur_prod_date_expected_birth    = str(row[27]) if row[27] else None
                cur_prod_date_actual_birth      = str(row[28]) if row[28] else None
                cur_prod_num_days_actual        = row[29] 
                cur_prod_num_pigs_dead_at_birth = row[30]
                cur_prod_num_pigs_live_m    = row[31]
                cur_prod_num_pigs_live_f    = row[32]
                cur_prod_birth_staff_id     = row[33]
                cur_prod_birth_staff_name   = row[34]
                
                cur_weaning_date            = row[35]
                cur_weaning_num_pigs_m      = row[36]
                cur_weaning_num_pigs_f      = row[37]
                cur_weaning_num_pigs        = row[38]
                cur_weaning_weight          = row[39]
                
                
                cur_pig_count               = row[40]
                
                
                cur_prod_num_b_gestating    = row[41]
                cur_prod_num_b_lactating    = row[42]
                cur_prod_num_b_booster      = row[43]
                cur_prod_num_b_prestarter   = row[44]
                cur_prod_num_b_starter      = row[45]
                cur_prod_num_b_grower       = row[46]
                cur_prod_num_b_finisher     = row[47]
                
                cur_feed_bal_date_balance   = row[48]
               
                cur_feed_bal_gestating      = row[49]
                cur_feed_bal_lactating      = row[50]
                cur_feed_bal_booster        = row[51]
                cur_feed_bal_prestarter     = row[52]
                cur_feed_bal_starter        = row[53]
                cur_feed_bal_grower         = row[54]
                cur_feed_bal_finisher       = row[55]
                
                cur_prod_cost_gestating     = row[56]
                cur_prod_cost_lactating     = row[57]
                cur_prod_cost_booster       = row[58]
                cur_prod_cost_prestarter    = row[59]
                cur_prod_cost_starter       = row[60]
                cur_prod_cost_grower        = row[61]
                cur_prod_cost_finisher      = row[62]
                
                cur_prod_date_gestating     = row[63]
                cur_prod_date_lactating     = row[64]
                cur_prod_date_booster       = row[65]
                cur_prod_date_prestarter    = row[66]
                cur_prod_date_starter       = row[67]
                cur_prod_date_grower        = row[68]
                cur_prod_date_finisher      = row[69]
            
                
                cur_data_ver_num_pig_prod       = row[70]
                cur_data_ver_num_medvac         = row[71] 
                cur_data_ver_num_health_notes   = row[72]
                cur_data_ver_num_prod_feed      = row[73]
                cur_data_ver_num_feed_balance   = row[74]
                cur_data_ver_num_harvest        = row[75] 
                
                
                cur_entry = {
                    'pig_production' :{
                        'id':               cur_prod_id, 
                        'farm_prod_id':     cur_prod_farm_prod_id,
                        'prod_status_id':   cur_prod_status_id,
                        'prod_status_name': cur_prod_status_name,
                        'cur_pig_count':    cur_pig_count
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
                        
                        'ai': {
                            'semen_supplier':{
                                'id':       cur_semen_supplier_id,
                                'name':     cur_semen_supplier_name,
                                
                                'semen': {
                                    'id':   cur_semen_sup_semen_id,
                                    'name': cur_semen_sup_semen_name
                                }
                            },
                            
                            'internal_boar':{
                                'id':           cur_semen_ai_boar_id,
                                'farm_sow_id':  cur_semen_ai_farm_boar_id,
                                'number':       cur_semen_ai_boar_number,
                                'name':         cur_semen_ai_boar_name
                            },
                            
                            'semen_cost':   cur_insem_semen_cost
                        },
                        
                        'insem_cost':       cur_insem_insemination_cost,
                        'insem_notes':      cur_insem_notes,
                        'insem_date':       cur_insem_date_insemination,
                        'insem_staff_id':   cur_insem_staff_id,
                        'insem_staff_name': cur_insem_staff_name
                    },
                    
                    'birth': {
                        'date_expected':    cur_prod_date_expected_birth,
                        'date_actual':      cur_prod_date_actual_birth,
                        'num_days_actual':  cur_prod_num_days_actual,
                        'num_dead_at_birth':cur_prod_num_pigs_dead_at_birth,
                        
                        'pigs_live_m':      cur_prod_num_pigs_live_m,
                        'pigs_live_f':      cur_prod_num_pigs_live_f,
                        'birth_staff_id':   cur_prod_birth_staff_id,
                        'birth_staff_name': cur_prod_birth_staff_name
                    },
                    
                    'weaning': {
                        'date_weaning':     cur_weaning_date,
                        'num_pigs_m':       cur_weaning_num_pigs_m,
                        'num_pigs_f':       cur_weaning_num_pigs_f,
                        'num_pigs':         cur_weaning_num_pigs,
                        'weight':           cur_weaning_weight    
                    },
                    
                    
                    'feeds':{
                        'bought':{
                            'gestating':    cur_prod_num_b_gestating,
                            'lactating':    cur_prod_num_b_lactating,
                            'booster':      cur_prod_num_b_booster,
                            'prestarter':   cur_prod_num_b_prestarter,
                            'starter':      cur_prod_num_b_starter,
                            'grower':       cur_prod_num_b_grower,
                            'finisher':     cur_prod_num_b_finisher
                        },
                        
                        'balance':{
                            'date_balance': str(cur_feed_bal_date_balance)      if cur_feed_bal_date_balance    is not None else None,
                            
                            'gestating':    float(cur_feed_bal_gestating)       if cur_feed_bal_gestating       is not None else None,
                            'lactating':    float(cur_feed_bal_lactating)       if cur_feed_bal_lactating       is not None else None,
                            'booster':      float(cur_feed_bal_booster)         if cur_feed_bal_booster         is not None else None,
                            'prestarter':   float(cur_feed_bal_prestarter)      if cur_feed_bal_prestarter      is not None else None,
                            'starter':      float(cur_feed_bal_starter)         if cur_feed_bal_starter         is not None else None,
                            'grower':       float(cur_feed_bal_grower)          if cur_feed_bal_grower          is not None else None,
                            'finisher':     float(cur_feed_bal_finisher)        if cur_feed_bal_finisher        is not None else None
                        },
                        
                        'cost':{
                            'gestating':    float(cur_prod_cost_gestating)      if cur_prod_cost_gestating      is not None else None,
                            'lactating':    float(cur_prod_cost_lactating)      if cur_prod_cost_lactating      is not None else None,
                            'booster':      float(cur_prod_cost_booster)        if cur_prod_cost_booster        is not None else None,
                            'prestarter':   float(cur_prod_cost_prestarter)     if cur_prod_cost_prestarter     is not None else None,
                            'starter':      float(cur_prod_cost_starter)        if cur_prod_cost_starter        is not None else None,
                            'grower':       float(cur_prod_cost_grower)         if cur_prod_cost_grower         is not None else None,
                            'finisher':     float(cur_prod_cost_finisher)       if cur_prod_cost_finisher       is not None else None
                        },
                        
                        'date_change_feed':{
                            'gestating':    str(cur_prod_date_gestating)        if cur_prod_date_gestating      is not None else None,
                            'lactating':    str(cur_prod_date_lactating)        if cur_prod_date_lactating      is not None else None,
                            'booster':      str(cur_prod_date_booster)          if cur_prod_date_booster        is not None else None,
                            'prestarter':   str(cur_prod_date_prestarter)       if cur_prod_date_prestarter     is not None else None,
                            'starter':      str(cur_prod_date_starter)          if cur_prod_date_starter        is not None else None,
                            'grower':       str(cur_prod_date_grower)           if cur_prod_date_grower         is not None else None,
                            'finisher':     str(cur_prod_date_finisher)         if cur_prod_date_finisher       is not None else None
                        }
                    
                    },
                    
                    
                    'data_ver_num': {
                        'pig_prod':         cur_data_ver_num_pig_prod,
                        'medvac':           cur_data_ver_num_medvac,
                        'health_notes':     cur_data_ver_num_health_notes,
                        'prod_feed':        cur_data_ver_num_prod_feed,
                        'feed_balance':     cur_data_ver_num_feed_balance,
                        'harvest':          cur_data_ver_num_harvest
                    
                    }
                    
                }
                
                 
                result.append(cur_entry)

        
        return result
    
    
    def get_feed_summary_by_id(self, pig_prod_id):
        sql =   """
                SELECT 
                    
                    a.num_b_gestating,
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    i.date_balance,
                    i.num_gestating,
                    i.num_lactating,
                    i.num_booster,
                    i.num_prestarter,
                    i.num_starter,
                    i.num_grower,
                    i.num_finisher,
                    
                    a.cost_gestating,
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher,
                    
                    a.date_gestating,
                    a.date_lactating,
                    a.date_booster,
                    a.date_prestarter,
                    a.date_starter,
                    a.date_grower,
                    a.date_finisher
                    
                   
                FROM pig_production a
                LEFT OUTER JOIN feed_balance i      ON a.last_feed_balance_id = i.id
                WHERE a.id = %s
                """ % pig_prod_id


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
            msg = 'get_feed_summary_by_id(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
    
     
            
            for row in rows:
                
                cur_prod_num_b_gestating    = row[0]
                cur_prod_num_b_lactating    = row[1]
                cur_prod_num_b_booster      = row[2]
                cur_prod_num_b_prestarter   = row[3]
                cur_prod_num_b_starter      = row[4]
                cur_prod_num_b_grower       = row[5]
                cur_prod_num_b_finisher     = row[6]
                
                cur_feed_bal_date_balance   = row[7]
                
                cur_feed_bal_gestating      = row[8]
                cur_feed_bal_lactating      = row[9]
                cur_feed_bal_booster        = row[10]
                cur_feed_bal_prestarter     = row[11]
                cur_feed_bal_starter        = row[12]
                cur_feed_bal_grower         = row[13]
                cur_feed_bal_finisher       = row[14]
                
                cur_prod_cost_gestating     = row[15]
                cur_prod_cost_lactating     = row[16]
                cur_prod_cost_booster       = row[17]
                cur_prod_cost_prestarter    = row[18]
                cur_prod_cost_starter       = row[19]
                cur_prod_cost_grower        = row[20]
                cur_prod_cost_finisher      = row[21]
                
                cur_prod_date_gestating     = row[22]
                cur_prod_date_lactating     = row[23]
                cur_prod_date_booster       = row[24]
                cur_prod_date_prestarter    = row[25]
                cur_prod_date_starter       = row[26]
                cur_prod_date_grower        = row[27]
                cur_prod_date_finisher      = row[28]
            
                
                cur_entry = {
                    
                    'feeds':{
                        'bought':{
                            'gestating':    cur_prod_num_b_gestating,
                            'lactating':    cur_prod_num_b_lactating,
                            'booster':      cur_prod_num_b_booster,
                            'prestarter':   cur_prod_num_b_prestarter,
                            'starter':      cur_prod_num_b_starter,
                            'grower':       cur_prod_num_b_grower,
                            'finisher':     cur_prod_num_b_finisher
                        },
                        
                        'balance':{
                            'date_balance': str(cur_feed_bal_date_balance)      if cur_feed_bal_date_balance    is not None else None,
                            
                            'gestating':    float(cur_feed_bal_gestating)       if cur_feed_bal_gestating       is not None else None,
                            'lactating':    float(cur_feed_bal_lactating)       if cur_feed_bal_lactating       is not None else None,
                            'booster':      float(cur_feed_bal_booster)         if cur_feed_bal_booster         is not None else None,
                            'prestarter':   float(cur_feed_bal_prestarter)      if cur_feed_bal_prestarter      is not None else None,
                            'starter':      float(cur_feed_bal_starter)         if cur_feed_bal_starter         is not None else None,
                            'grower':       float(cur_feed_bal_grower)          if cur_feed_bal_grower          is not None else None,
                            'finisher':     float(cur_feed_bal_finisher)        if cur_feed_bal_finisher        is not None else None
                        },
                        
                        'cost':{
                            'gestating':    float(cur_prod_cost_gestating)      if cur_prod_cost_gestating      is not None else None,
                            'lactating':    float(cur_prod_cost_lactating)      if cur_prod_cost_lactating      is not None else None,
                            'booster':      float(cur_prod_cost_booster)        if cur_prod_cost_booster        is not None else None,
                            'prestarter':   float(cur_prod_cost_prestarter)     if cur_prod_cost_prestarter     is not None else None,
                            'starter':      float(cur_prod_cost_starter)        if cur_prod_cost_starter        is not None else None,
                            'grower':       float(cur_prod_cost_grower)         if cur_prod_cost_grower         is not None else None,
                            'finisher':     float(cur_prod_cost_finisher)       if cur_prod_cost_finisher       is not None else None
                        },
                        
                        'date_change_feed':{
                            'gestating':    str(cur_prod_date_gestating)        if cur_prod_date_gestating      is not None else None,
                            'lactating':    str(cur_prod_date_lactating)        if cur_prod_date_lactating      is not None else None,
                            'booster':      str(cur_prod_date_booster)          if cur_prod_date_booster        is not None else None,
                            'prestarter':   str(cur_prod_date_prestarter)       if cur_prod_date_prestarter     is not None else None,
                            'starter':      str(cur_prod_date_starter)          if cur_prod_date_starter        is not None else None,
                            'grower':       str(cur_prod_date_grower)           if cur_prod_date_grower         is not None else None,
                            'finisher':     str(cur_prod_date_finisher)         if cur_prod_date_finisher       is not None else None
                        }
                    
                    }
                    
                }
                
                return cur_entry

        
        return None
    
    
    def get_cur_pig_count_by_id(self, pig_prod_id):
        sql =   """
                SELECT 
                    
                    num_pigs_current
                    
                FROM pig_production 
                WHERE id = %s
                """ % pig_prod_id


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
            msg = 'get_pig_count_current_by_id(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        


        if rows is not None:

            for row in rows:
                
                cur_prod_cur_pig_count    = row[0]
                

                cur_entry = {
                    
                    'pig_production':{
                        'cur_pig_count': cur_prod_cur_pig_count
                    }
                    
                }
                
                return cur_entry

        return None
    
    
    def get_data_ver_num(self, pig_prod_id):
        sql =   """
                SELECT 
                    
                    data_ver_num_pig_prod,
                    data_ver_num_medvac, 
                    data_ver_num_health_notes,
                    data_ver_num_prod_feed,
                    data_ver_num_feed_balance,
                    data_ver_num_harvest     
                    
                FROM pig_production 
                WHERE id = %s
                """ % pig_prod_id


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
            msg = 'get_data_ver_num(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        


        if rows is not None:

            for row in rows:
                
                cur_data_ver_num_pig_prod       = row[0]
                cur_data_ver_num_medvac         = row[1] 
                cur_data_ver_num_health_notes   = row[2]
                cur_data_ver_num_prod_feed      = row[3]
                cur_data_ver_num_feed_balance   = row[4]
                cur_data_ver_num_harvest        = row[5] 
                

                cur_entry = {
                    'data_ver_num': {
                        'pig_prod':     cur_data_ver_num_pig_prod,    
                        'medvac':       cur_data_ver_num_medvac,      
                        'health_notes': cur_data_ver_num_health_notes,
                        'prod_feed':    cur_data_ver_num_prod_feed,   
                        'feed_balance': cur_data_ver_num_feed_balance,
                        'harvest':      cur_data_ver_num_harvest
                    }
                }
                
                return cur_entry

        return None
    
    
    
    
    def get_pig_prod_ops_list(self, pig_farm_id,  inc_historical = 0):
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        
        # Include PROD_STATUS_ID_GESTATING that has already bought up lactating feeds 
        
        where_clause = 'WHERE (a.pig_farm_id = %s AND  a.prod_status_id IN (4, 5, 6)) ' % pig_farm_id
        where_clause += ' OR (a.pig_farm_id = %s AND a.prod_status_id = 1 AND a.num_b_lactating IS NOT NULL) ' % pig_farm_id
        
        if inc_historical > 0:
            where_clause = 'WHERE (a.pig_farm_id = %s AND a.prod_status_id IN (4,5,6,8,9)) ' % pig_farm_id
            where_clause += ' OR (a.pig_farm_id = %s AND a.prod_status_id = 1 AND a.num_b_lactating IS NOT NULL) ' % pig_farm_id
       
        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    b.number,
                    b.name AS sow_name,
                    
                    a.prod_status_id,
                    c.name AS prod_status,
                    
                    a.num_pigs_current,
                    
                    a.date_actual_birth,
                    
                    a.date_iron_1,
                    a.date_iron_2,
                    a.date_vitamins_1,
                    a.date_kapon,
                    a.date_vitamins_2,
                    a.date_deworm_1,
                    
                    a.date_booster,
                    a.date_prestarter,
                    a.date_weaning,
                    a.date_starter,
                    a.date_grower,
                    a.date_finisher,
                    
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    d.date_balance,
                    d.num_lactating,
                    d.num_booster,
                    d.num_prestarter,
                    d.num_starter,
                    d.num_grower,
                    d.num_finisher,
                    
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher,
                    
                    a.date_harvest
                    
                FROM pig_production a
                LEFT OUTER JOIN sow_boar b          ON a.sow_id = b.id
                LEFT OUTER JOIN pig_prod_status c   ON a.prod_status_id = c.id
                LEFT OUTER JOIN feed_balance d      ON a.last_feed_balance_id = d.id
                %s
                ORDER BY a.date_actual_birth DESC
                """ % where_clause 
    
        rows = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()

        except Exception as e:
            msg = 'get_pig_prod_ops_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            for row in rows:
                cur_id                  = row[0]
                cur_farm_prod_id        = row[1]
                cur_sow_number          = row[2]
                cur_sow_name            = row[3]
                
                cur_status_id           = row[4]
                cur_status_name         = row[5]
                
                cur_num_pigs_current    = row[6]
               
                cur_date_actual         = str(row[7])   if row[7]  else None
                
                cur_date_iron_1         = str(row[8])   if row[8]  else None
                cur_date_iron_2         = str(row[9])   if row[9]  else None
                cur_date_vitamins_1     = str(row[10])  if row[10]  else None
                cur_date_kapon          = str(row[11])  if row[11] else None
                cur_date_vitamins_2     = str(row[12])  if row[12] else None
                cur_date_deworm_1       = str(row[13])  if row[13] else None
                
                
                cur_date_booster        = str(row[14])  if row[14] else None
                cur_date_prestarter     = str(row[15])  if row[15] else None
                cur_date_weaning        = str(row[16])  if row[16] else None
                cur_date_starter        = str(row[17])  if row[17] else None
                cur_date_grower         = str(row[18])  if row[18] else None
                cur_date_finisher       = str(row[19])  if row[19] else None
                
                cur_num_b_lactating     = row[20]
                cur_num_b_booster       = row[21]
                cur_num_b_prestarter    = row[22]
                cur_num_b_starter       = row[23]
                cur_num_b_grower        = row[24]
                cur_num_b_finisher      = row[25]
                
                cur_feed_date_balance   = str(row[26])   if row[26] is not None else None
                cur_num_l_lactating     = float(row[27]) if row[27] is not None else None
                cur_num_l_booster       = float(row[28]) if row[28] is not None else None
                cur_num_l_prestarter    = float(row[29]) if row[29] is not None else None
                cur_num_l_starter       = float(row[30]) if row[30] is not None else None
                cur_num_l_grower        = float(row[31]) if row[31] is not None else None
                cur_num_l_finisher      = float(row[32]) if row[32] is not None else None
                
                cur_cost_lactating      = float(row[33]) if row[33] is not None else None
                cur_cost_booster        = float(row[34]) if row[34] is not None else None
                cur_cost_prestarter     = float(row[35]) if row[35] is not None else None
                cur_cost_starter        = float(row[36]) if row[36] is not None else None
                cur_cost_grower         = float(row[37]) if row[37] is not None else None
                cur_cost_finisher       = float(row[38]) if row[38] is not None else None
                
                cur_date_harvest        = str(row[39]) if row[39] else None
                
                
                cur_num_c_lactating     = None
                cur_num_c_booster       = None
                cur_num_c_prestarter    = None
                cur_num_c_starter       = None
                cur_num_c_grower        = None
                cur_num_c_finisher      = None
            
            
                if cur_num_b_lactating is not None and cur_num_l_lactating is not None:
                    cur_num_c_lactating = float(cur_num_b_lactating) - cur_num_l_lactating
                
                if cur_num_b_booster is not None and cur_num_l_booster is not None:
                    cur_num_c_booster = float(cur_num_b_booster) - cur_num_l_booster
                
                if cur_num_b_prestarter is not None and cur_num_l_prestarter is not None:
                    cur_num_c_prestarter = float(cur_num_b_prestarter) - cur_num_l_prestarter
                
                if cur_num_b_starter is not None and cur_num_l_starter is not None:
                    cur_num_c_starter = float(cur_num_b_starter) - cur_num_l_starter
                
                if cur_num_b_grower is not None and cur_num_l_grower is not None:
                    cur_num_c_grower = float(cur_num_b_grower) - cur_num_l_grower
                
                if cur_num_b_finisher is not None and cur_num_l_finisher is not None:
                    cur_num_c_finisher = float(cur_num_b_finisher) - cur_num_l_finisher
                
                
                cur_entry = {
                    'pig_prod':{
                        'id':           cur_id,
                        'farm_prod_id': cur_farm_prod_id,
                        
                        'status_id':    cur_status_id, 
                        'status':       cur_status_name,
                    
                        'num_pigs_current': cur_num_pigs_current
                    },
                    
                    'sow': {
                        'number':       cur_sow_number,
                        'name':         cur_sow_name
                    },
                    
                    'dates':{
                        'birth':        cur_date_actual,
                        
                        'iron_1':       cur_date_iron_1,
                        'iron_2':       cur_date_iron_2,
                        'vitamins_1':   cur_date_vitamins_1,
                        'kapon':        cur_date_kapon,
                        'vitamins_2':   cur_date_vitamins_2,
                        'deworm_1':     cur_date_deworm_1,
                        
                        'booster':      cur_date_booster,
                        'prestarter':   cur_date_prestarter,
                        'weaning':      cur_date_weaning,
                        'starter':      cur_date_starter,
                        'grower':       cur_date_grower,
                        'finisher':     cur_date_finisher,
                        
                        'harvest':      cur_date_harvest
                    },
                    
                    'num_feeds': {
                        'date_balance': cur_feed_date_balance,
                    
                        'lactating': {
                            'bought':   cur_num_b_lactating,
                            'consumed': cur_num_c_lactating,
                            'left':     cur_num_l_lactating
                        },
                        
                        'booster': {
                            'bought':   cur_num_b_booster,
                            'consumed': cur_num_c_booster,
                            'left':     cur_num_l_booster
                        },
                            
                        'prestarter': {
                            'bought':   cur_num_b_prestarter,
                            'consumed': cur_num_c_prestarter,
                            'left':     cur_num_l_prestarter
                        },
                            
                        'starter': {     
                            'bought':   cur_num_b_starter,
                            'consumed': cur_num_c_starter,
                            'left':     cur_num_l_starter
                        },
                        
                        'grower': {
                            'bought':   cur_num_b_grower,
                            'consumed': cur_num_c_grower,
                            'left':     cur_num_l_grower
                        },
                        
                        'finisher': {    
                            'bought':   cur_num_b_finisher,
                            'consumed': cur_num_c_finisher,
                            'left':     cur_num_l_finisher
                        }
                    },
                    
                    'cost_feeds': {
                        'lactating':    cur_cost_lactating,
                        'booster':      cur_cost_booster,
                        'prestarter':   cur_cost_prestarter,
                        'starter':      cur_cost_starter,
                        'grower':       cur_cost_grower,
                        'finisher':     cur_cost_finisher
                    }
                   
                }
                result.append(cur_entry)

        
        return result
        
    
    def get_production_output(self, pig_farm_id = 0, sow_id = 0):
        """
        
        
        Notes:
        1.) The number of piglets output at weaning are entered in two ways
            - separate counts: num_pigs_weaning_m, num_pigs_weaning_f  
            - total count no separation: num_pigs_weaning
        
        2.) If entered via separate count, num_pigs_weaning is NULL; 
        
        """
        
        where_clause = ''
        order_clause = ''
        
        if pig_farm_id > 0:
            where_clause = 'WHERE a.pig_farm_id = %s AND a.date_actual_birth IS NOT NULL' % pig_farm_id
            order_clause = 'ORDER BY a.sow_id ASC, a.date_actual_birth DESC'
            
        if sow_id > 0:
            where_clause = 'WHERE a.sow_id = %s AND a.date_actual_birth IS NOT NULL' % sow_id
            order_clause = 'ORDER BY a.date_actual_birth DESC'
            
            
        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    
                    a.sow_id,
                    b.name AS sow_name,
                    b.number AS sow_number,
                    b.date_dispose AS sow_date_dispose, 
                    
                    a.insemination_type,
                    
                    a.boar_id,
                    c.name AS boar_name,
                    c.number AS boar_number,
                    c.date_dispose AS boar_date_dispose,
                    
                    
                    a.semen_supplier_id,
                    d.name AS semen_supplier_name,
                    
                    a.semen_sup_semen_id,
                    e.name AS semen_name,
                    
                    a.semen_ai_boar_id,
                    f.name AS boar_name,
                    f.number AS boar_number,
                    f.date_dispose AS boar_date_dispose,
                    
                    
                    a.date_actual_birth,
                    a.num_pigs_live_m,
                    a.num_pigs_live_f,
                    a.num_pigs_dead_at_birth,
                    
                    a.date_weaning,
                    a.num_pigs_weaning_m,
                    a.num_pigs_weaning_f,
                    a.num_pigs_weaning,
                    a.total_pigs_weight_weaning
                    
                FROM pig_production a 
                LEFT OUTER JOIN sow_boar b              ON a.sow_id = b.id
                LEFT OUTER JOIN sow_boar c              ON a.boar_id = c.id
                LEFT OUTER JOIN common_supplier d       ON a.semen_supplier_id = d.id
                LEFT OUTER JOIN semen_supplier_semen e  ON a.semen_sup_semen_id = e.id
                LEFT OUTER JOIN sow_boar f              ON a.semen_ai_boar_id = f.id
                
                %s
                %s
                """ % (where_clause, order_clause)
    
            
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
            msg = 'get_production_output(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            cur_sow = None
            last_sow_id = None
          
            for row in rows:
                

                cur_pig_prod_id             = row[0]
                cur_farm_prod_id            = row[1]
                
                cur_sow_id                  = row[2]
                cur_sow_name                = row[3]
                cur_sow_number              = row[4]
                cur_sow_date_dispose        = str(row[5]) if row[5] else None
                
                cur_insemination_type       = row[6]
                
                cur_boar_id                 = row[7]
                cur_boar_name               = row[8]
                cur_boar_number             = row[9]
                cur_boar_date_dispose       = str(row[10]) if row[10] else None
                
                
                cur_semen_supplier_id       = row[11]
                cur_semen_supplier_name     = row[12]
                
                cur_semen_sup_semen_id      = row[13]
                cur_semen_sup_semen_name    = row[14]
                
                cur_semen_ai_boar_id        = row[15]
                cur_semen_ai_boar_name      = row[16]
                cur_semen_ai_boar_number    = row[17]
                cur_semen_ai_boar_date_dispose = str(row[18]) if row[18] else None
                
                
                cur_date_actual_birth       = str(row[19])
                cur_pigs_live_m             = row[20]
                cur_pigs_live_f             = row[21]
                cur_dead_at_birth           = row[22]
                
                
                cur_weaning_date            = row[23]
                cur_weaning_pigs_m          = int(row[24])   if row[24] is not None else None
                cur_weaning_pigs_f          = int(row[25])   if row[25] is not None else None
                cur_weaning_pigs            = int(row[26])   if row[26] is not None else None
                cur_weaning_pigs_weight     = float(row[27]) if row[27] is not None else None
               
               
               
                if last_sow_id is None or last_sow_id !=  cur_sow_id:
                    last_sow_id = cur_sow_id
                    
                    cur_entry = {
                        'sow':{
                            'id':           cur_sow_id,
                            'name':         cur_sow_name,
                            'number':       cur_sow_number,
                            'date_dispose': cur_sow_date_dispose
                        },
                        
                        'production':[]
                    }
                    
                    result.append(cur_entry)
                    
                
                cur_prod = {
                    'pig_production':{
                        'id':               cur_pig_prod_id,
                        'farm_prod_id':     cur_farm_prod_id
                    },
                    
                    'insemination': {
                        'insem_type':       cur_insemination_type,
                        
                        'boar': {
                            'id':           cur_boar_id,
                            'number':       cur_boar_number,
                            'name':         cur_boar_name,
                            'date_dispose': cur_boar_date_dispose
                        },
                        
                        'ai': {
                            'semen_supplier':{
                                'id':       cur_semen_supplier_id,
                                'name':     cur_semen_supplier_name,
                                
                                'semen': {
                                    'id':   cur_semen_sup_semen_id,
                                    'name': cur_semen_sup_semen_name
                                }
                            },
                            
                            'internal_boar':{
                                'id':           cur_semen_ai_boar_id,
                                'number':       cur_semen_ai_boar_number,
                                'name':         cur_semen_ai_boar_name,
                                'date_dispose': cur_semen_ai_boar_date_dispose
                            },
                           
                        }
                    },
                    
                    
                    'birth':{
                        'date_actual':      cur_date_actual_birth,
                        'pigs_live_m':      cur_pigs_live_m,
                        'pigs_live_f':      cur_pigs_live_f,
                        'dead':             cur_dead_at_birth
                    },
                    
                    
                    'weaning': {
                        'date_weaning':     cur_weaning_date,
                        'num_pigs_m':       cur_weaning_pigs_m,
                        'num_pigs_f':       cur_weaning_pigs_f,
                        'num_pigs':         cur_weaning_pigs,
                        'weight':           cur_weaning_pigs_weight    
                    }
                }
                
                
                if cur_boar_id and cur_boar_id > 0:
                     del cur_prod['insemination']['ai']
                
                else:
                    del cur_prod['insemination']['boar']
                    
                    if cur_semen_supplier_id and cur_semen_supplier_id > 0:
                        del cur_prod['insemination']['ai']['internal_boar']
                        
                    else:
                        del cur_prod['insemination']['ai']['semen_supplier']
                    
            
                cur_entry['production'].append(cur_prod)
        
        
        return result
    
    
    
    def get_production_output_group_per_sow(self, pig_farm_id = 0):
        """
        
        Notes:
        1.) The number of piglets output at weaning are entered in two ways
            - separate counts: num_pigs_weaning_m, num_pigs_weaning_f  
            - total count no separation: num_pigs_weaning
        
        2.) If entered via separate count, num_pigs_weaning is NULL; 
        
        """
        
        
        
            
        # This sql return number of piglets at weaning + currently lactating.
        # This includes both active sows and disposed sows.
        # The basic info of the sow is also returned.
        # The num_dead column is the number of dead piglets at birth.
        # The number of dead piglets after birth and before weaning should 
        # computed.
        
        sql = """
        SELECT 
            a.sow_id,
            SUM(a.cnt) AS num_birth,
            
            SUM(a.num_pigs_live_m) AS num_live_m,
            SUM(a.num_pigs_live_f) AS num_live_f,
            SUM(a.num_dead_birth) AS num_dead_birth,
            
            SUM(a.num_pigs_wean_m) as num_wean_m,
            SUM(a.num_pigs_wean_f) as num_wean_f,
            SUM(a.num_pigs_wean) as num_wean,
            
            b.name,
            b.number,
            b.date_dispose
            
        FROM (
            SELECT
                'weaning' as record_type,
                sow_id,
                COUNT(*) AS cnt,
                
                SUM(num_pigs_live_m) AS num_pigs_live_m,
                SUM(num_pigs_live_f) AS num_pigs_live_f,
                SUM(num_pigs_dead_at_birth) AS num_dead_birth,
                
                SUM(num_pigs_weaning_m) as num_pigs_wean_m,
                SUM(num_pigs_weaning_f) as num_pigs_wean_f,
                SUM(num_pigs_weaning)   as num_pigs_wean
            FROM pig_production 
            WHERE pig_farm_id = %s AND date_weaning IS NOT NULL
            GROUP BY sow_id

            UNION ALL

            SELECT
                'birth' as record_type,
                sow_id,
                COUNT(*) AS cnt,
                
                SUM(num_pigs_live_m) as num_pigs_live_m,
                SUM(num_pigs_live_f) as num_pigs_live_f,
                SUM(num_pigs_dead_at_birth) AS num_dead_birth,
                
                SUM(num_pigs_live_m) as num_pigs_wean_m,
                SUM(num_pigs_live_f) as num_pigs_wean_f,
                0 as num_pigs_wean
            FROM pig_production 
            WHERE pig_farm_id = %s AND date_actual_birth IS NOT NULL AND date_weaning IS NULL
            GROUP BY sow_id

            ORDER BY sow_id, record_type ASC
        ) a
        LEFT OUTER JOIN sow_boar b ON a.sow_id = b.id
        GROUP BY a.sow_id; 
        """ %(pig_farm_id, pig_farm_id)
            
            
            
            
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
            msg = 'get_production_output(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
          
            for row in rows:
                
                cur_sow_id                  = row[0]
                cur_birth_count             = int(row[1]) if row[1] is not None else None
                cur_pigs_live_m             = int(row[2]) if row[2] is not None else None
                cur_pigs_live_f             = int(row[3]) if row[3] is not None else None
                cur_dead_at_birth           = int(row[4]) if row[4] is not None else None
                
                cur_pigs_wean_m             = int(row[5]) if row[6] is not None else None
                cur_pigs_wean_f             = int(row[6]) if row[6] is not None else None
                cur_pigs_wean               = int(row[7]) if row[7] is not None else None
                
                
                cur_sow_name                = row[8]
                cur_sow_number              = row[9]
                cur_date_disposed           = str(row[10]) if row[10] is not None else None
                
                
                # compute total live births
                cur_pigs_live_birth         =  cur_pigs_live_m + cur_pigs_live_f
                
                # compute total live pigs at wean
                cur_total_wean = 0
                if cur_pigs_wean_m is not None:
                    cur_total_wean += cur_pigs_wean_m
                    
                if cur_pigs_wean_f is not None:
                    cur_total_wean += cur_pigs_wean_f
                    
                if cur_pigs_wean is not None:
                    cur_total_wean += cur_pigs_wean
                    
                    
                # compute dead before wean
                cur_dead_before_wean = cur_pigs_live_birth - cur_total_wean
                
                cur_entry ={
                    'sow_id':               cur_sow_id,
                    'sow_name':             cur_sow_name,     
                    'sow_number':           cur_sow_number,   
                    'date_disposed':        cur_date_disposed,
                    
                    'num_births':           cur_birth_count,
                    
                    'num_pigs_live_m':      cur_pigs_live_m,
                    'num_pigs_live_f':      cur_pigs_live_f,
                    'dead_at_birth':        cur_dead_at_birth,
                    
                    'num_pigs_wean':        cur_total_wean,
                    'dead_before_wean':     cur_dead_before_wean
                }
                    
            
                result.append(cur_entry)
        
        return result
    
    
    
        
