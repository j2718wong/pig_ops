# August 23, 2025
# Jack Wong

from common_constants       import *


class PigProdPigDead:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigProdPigDead'
    
    
    def get_pig_dead_type_list(self):
        
      
        sql =   """
                SELECT 
                    id,
                    name
                    
                FROM pig_dead_type 
                ORDER BY id
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

            
        except Exception as e:
            msg = 'get_pig_dead_type_list(); error in executing query[] = ' + sql
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
                    'id':                   row[0],
                    'name':                 row[1]
                }

                result.append(cur_entry)
        
        return result
    
    

    def add(self, data = None):
        """
        PROCEDURE pig_prod_pig_dead_add(
            in_user_id              INT,
           
            in_pig_prod_id          INT,
            in_pig_prod_group_id    INT,
            
            in_date_dead            VARCHAR(10),
            in_pig_dead_type_id     INT,
            in_num_pigs_dead        INT,
            in_notes                VARCHAR(160)
        )  
        """
        
        sql =  'CALL pig_prod_pig_dead_add('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        sql += '%s,'    % data.pig_prod_group_id
        
        sql += '"%s",'  % data.date_dead
        sql += '%s,'    % data.pig_dead_type_id
        sql += '%s,'    % data.num_pigs_dead
        
        if data.notes is not None and len(data.notes) > 0:
            sql += '"%s");'   % data.notes
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
                
                'prod_pig_dead': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE pig_prod_pig_dead_update(
            in_user_id                  INT,
    
            in_pig_prod_pig_dead_id     INT,
            
            in_date_dead                VARCHAR(10),
            in_pig_dead_type_id         INT,
            in_num_pigs_dead            INT,
            in_notes                    VARCHAR(160)
        )
        """
       
        sql =  'CALL pig_prod_pig_dead_update('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_pig_dead_id
        sql += '"%s",'  % data.date_dead
        sql += '%s,'    % data.pig_dead_type_id
        sql += '%s,'    % data.num_pigs_dead
                
        if data.notes is not None and len(data.notes) > 0:
            sql += '"%s");'   % data.notes
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
                
                'prod_pig_dead': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        pig_race_line_id    = data['pig_race_line_id']
        
        """
        PROCEDURE pig_race_line_delete(
            in_user_id                  INT,
            
            in_pig_race_line_id         INT
        )
        """
       
        sql =  'CALL pig_race_line_delete('
        sql += '%s,'    % user_id
        sql += '%s);'   % pig_race_line_id
        
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
                
                'pig_race_line': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_list(self, pig_farm_id = 0, pig_prod_id = 0, inc_user_audit = 0):
        
        
        sql =   """
                SELECT 
                    a.id,
                    a.date_dead,
                    a.num_pigs_dead,
                    
                    a.dead_type_id,
                    b.name as dead_type,
                    
                    a.pig_prod_id,
                    c.farm_prod_id,
                    
                    c.insemination_type,
                    c.date_actual_birth,
                    c.date_weaning,
                    
                    c.sow_id,
                    d.number,
                    d.name,
                    
                    c.boar_id,
                    e.number,
                    e.name,
                    
                    c.semen_supplier_id,
                    f.name AS semen_supplier_name,
                    
                    c.semen_sup_semen_id,
                    g.name as semen_supplier_semen_name,
                    
                    c.semen_ai_boar_id,
                    h.number,
                    h.name,
                    
                    
                    i.notes
                    
                    
                FROM pig_prod_pig_dead a 
                LEFT OUTER JOIN pig_dead_type b     ON a.dead_type_id   = b.id
                
                LEFT OUTER JOIN pig_production c    ON a.pig_prod_id    = c.id
                LEFT OUTER JOIN sow_boar d          ON c.sow_id         = d.id
                LEFT OUTER JOIN sow_boar e          ON c.boar_id        = e.id
                
                LEFT OUTER JOIN common_supplier f   ON c.semen_supplier_id = f.id
                LEFT OUTER JOIN semen_supplier_semen g ON c.semen_sup_semen_id = g.id
                LEFT OUTER JOIN sow_boar h          ON c.semen_ai_boar_id = h.id
                
                LEFT OUTER JOIN pig_prod_notes i    ON a.notes_id = i.id
                
                WHERE a.pig_farm_id = %s
                ORDER BY a.date_dead DESC
                """ % pig_farm_id
        
        
        
        
        
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
                cur_id                  = row[0]
                cur_date_dead           = str(row[1])
                cur_num_pigs_dead       = row[2]
                
                cur_dead_type_id        = row[3]
                cur_dead_type           = row[4]
                
                cur_pig_prod_id         = row[5]
                cur_farm_prod_id        = row[6]
                
                cur_insemination_type   = row[7]
                cur_date_actual_birth   = row[8]
                cur_date_weaning        = row[9]
                
                cur_sow_id              = row[10]
                cur_sow_number          = row[11]
                cur_sow_name            = row[12]
                
                cur_boar_id             = row[13]
                cur_boar_number         = row[14]
                cur_boar_name           = row[15]
                
                cur_semen_supplier_id   = row[16]
                cur_semen_supplier_name = row[17]
                
                cur_semen_sup_semen_id  = row[18]
                cur_semen_sup_semen_name= row[19]
                
                cur_semen_ai_boar_id    = row[20]
                cur_semen_ai_boar_number= row[21]
                cur_semen_ai_boar_name  = row[22]
                
                
                cur_notes               = row[23]
                
                cur_entry = {
                    'pig_dead':{
                        'id':               cur_id,
                        'date_dead':        cur_date_dead,
                        'dead_type_id':     cur_dead_type_id,
                        'dead_type':        cur_dead_type,
                        'num_pigs_dead':    cur_num_pigs_dead,
                        'notes':            cur_notes,
                    },
                   
                    'production':{
                        'pig_production' :{
                            'id':               cur_pig_prod_id, 
                            'farm_prod_id':     cur_farm_prod_id
                        },
                        
                        'sow': {
                            'id':               cur_sow_id,
                            'number':           cur_sow_number,
                            'name':             cur_sow_name,
                        },
                        
                        'insemination': {
                            'insem_type':       cur_insemination_type,
                            
                            'boar': {
                                'id':           cur_boar_id,
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
                                    'number':       cur_semen_ai_boar_number,
                                    'name':         cur_semen_ai_boar_name
                                },
                                
                            }
                        },
                        
                        'birth': {
                            'date_actual':      cur_date_actual_birth,
                        },
                        
                        'weaning': {
                            'date_weaning':     cur_date_weaning,
                        }
                    }
                }
            
                
                result.append(cur_entry)
        
        return result
    
    
