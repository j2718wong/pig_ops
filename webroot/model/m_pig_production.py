# August 17, 2025
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


class PigProduction(BaseModel):
    def __init__(self, model):
        super().__init__(model)

    
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
            
            in_total_weight         DECIMAL(6,2),
            in_per_pig_weight       VARCHAR(200)
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
            sql += '%s,'    % data.total_weight
        else:
            sql += 'NULL,'
        
        if data.weight_pp is not None:
            sql += '"%s");'    % data.weight_pp
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
    
   
