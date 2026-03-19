# January 3, 2024
# Jack Wong

from common_constants       import *


"""
sow_boar.flag bits
0 = is_disposed
1 = is_external 
2 = is_production_ready

"""

FLAG_BIT_SOW_BOAR_IS_DISPOSED           = 1
FLAG_BIT_SOW_BOAR_IS_EXTERNAL           = 2
FLAG_BIT_SOW_BOAR_IS_PRODUCTION_READY   = 4
        

class SowBoar:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SowBoar'

    
    def get_sow_status_list(self, is_dispose = 0):
        """
        Will get sow_status list.
        
        
        Returns
        -------
        list of dictionary

        """
        
        where_clause = ''
        if is_dispose > 0:
            where_clause = 'WHERE flag = 1'
        
        sql =   """
                SELECT 
                    id,
                    name
                FROM sow_status
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
            msg = 'get_sow_status_list(); error in executing query[] = ' + sql
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
        PROCEDURE sow_boar_add(
            in_user_id              INT,
            
            in_pig_farm_id          INT,
            in_line_id              INT,
            in_sow_status_id        INT,
            
            in_sex                  CHAR(1),
            in_num_nipples          INT,
            in_is_external          INT,
            in_is_production_ready  INT,
            
            in_parent_sow_id        INT,
            in_parent_boar_id       INT,
    
                    
            in_number               VARCHAR(10),
            in_name                 VARCHAR(20),
            in_date_of_birth        VARCHAR(10),
            in_notes                VARCHAR(160)
        )    
        """
        
        sql =  'CALL sow_boar_add('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.pig_farm_id
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        
        sql += '"%s",'  % data.sex
        
        if data.num_nipples is not None and data.num_nipples > 0:
            sql += '%s,'  % data.num_nipples
        else:
            sql += 'NULL,'
        
        
        sql += '%s,'    % data.is_external
        sql += '%s,'    % data.is_production_ready
        
        if data.parent_sow_id > 0:
            sql += '%s,'    % data.parent_sow_id
        else:
            sql += 'NULL,'
            
        if data.parent_boar_id > 0:
            sql += '%s,'    % data.parent_boar_id
        else:
            sql += 'NULL,'
        
        
        if data.number is not None and len(data.number) > 0:
            sql += '"%s",'  % data.number
        else:
            sql += 'NULL,'
        
        if data.name is not None and len(data.name) > 0:
            sql += '"%s",'    % data.name
        else:
            sql += 'NULL,'
            
        if data.date_of_birth is not None and len(data.date_of_birth) > 0:
            sql += '"%s",'    % data.date_of_birth
        else:
            sql += 'NULL,'            
            
        
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
                
                'sow_boar': {
                    'id':               row[3],
                    'farm_sow_id':      row[4],
                    'farm_boar_id':     row[5],
                    'is_external':      data.is_external,
                    'is_production_ready': data.is_production_ready
                }
            }

        return None

    
    def update(self, data = None):
        """
        PROCEDURE sow_boar_update(
            in_user_id              INT,
            
            in_sow_boar_id          INT,
            in_line_id              INT,
            in_sow_status_id        INT,
            in_is_external          INT,
            in_is_production_ready  INT,
            
            in_parent_sow_id        INT,
            in_parent_boar_id       INT,
    
            in_number               VARCHAR(10),
            in_name                 VARCHAR(20),
            in_date_of_birth        VARCHAR(10),
            in_date_eartag          VARCHAR(10),
            in_notes                VARCHAR(160)
        )    
        """
        
        sql =  'CALL sow_boar_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.sow_boar_id
        sql += '%s,'    % data.line_id
        sql += '%s,'    % data.sow_status_id
        sql += '%s,'    % data.is_external
        sql += '%s,'    % data.is_production_ready
        
        
        if data.parent_sow_id > 0:
            sql += '%s,'    % data.parent_sow_id
        else:
            sql += 'NULL,'
            
        if data.parent_boar_id > 0:
            sql += '%s,'    % data.parent_boar_id
        else:
            sql += 'NULL,'
        
        
        if data.number is not None and len(data.number) > 0:
            sql += '"%s",'  % data.number
        else:
            sql += 'NULL,'
        
        if data.name is not None and len(data.name) > 0:
            sql += '"%s",'    % data.name
        else:
            sql += 'NULL,'
            
        if data.date_of_birth is not None:
            sql += '"%s",'    % data.date_of_birth
        else:
            sql += 'NULL,'            
            
        if data.date_eartag is not None and len(data.date_eartag) > 0:
            sql += '"%s",'    % data.date_eartag
        else:
            sql += 'NULL,'
            
        if data.notes is not None:
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
            
            sow_boar_id = row[3]
            
            res_update = {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2]
                }
            }
            
            sow_boar_list = self.get_list(sow_boar_id = sow_boar_id)
            
            # return whole sow_boar
            if sow_boar_list is not None:
                res_update['sow_boar'] = sow_boar_list[0]['sow_boar']
            
            
            return res_update;

        return None

    
    def dispose(self, data = None):
        """
        PROCEDURE sow_boar_dispose(
            in_user_id              INT,
            
            in_sow_boar_id          INT,
            in_dispose_status_id    INT,
            
            in_date_dispose         VARCHAR(10),
            in_dispose_notes        VARCHAR(160)
        )
        """
        
        sql =  'CALL sow_boar_dispose('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.sow_boar_id
        sql += '%s,'    % data.dispose_status_id
        
        
        sql += '"%s",'  % data.date_dispose
            
        if data.dispose_notes is not None:
            sql += '"%s");'   % data.dispose_notes
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
            msg = 'dispose(); error in executing query[] = ' + sql
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
                
                'sow_boar': {
                    'id':               row[3]
                }
            }

        return None

    
    def get_entry(self, sow_boar_id):
        sql =   """
                SELECT 
                    id,
                    farm_sow_id,
                    farm_boar_id,
                    number,
                    name,
                    sex,
                    sow_status_id
                    
                FROM sow_boar 
                WHERE id = %s
                """ % sow_boar_id
        
        
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
            msg = 'get_entry(); error in executing query[] = ' + sql
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
                    'farm_sow_id':          row[1],
                    'farm_boar_id':         row[2],
                    'number':               row[3], 
                    'name':                 row[4],
                    'sex':                  row[5],
                    'sow_status_id':        row[6]
                }
                
                return cur_entry

        
        return None
    
    
    def get_data_ver_num(self, sow_boar_id):
        sql =   """
                SELECT 
                    data_ver_num_sow_boar,
                    data_ver_num_medvac,
                    data_ver_num_health_notes,
                    data_ver_num_output,
                    data_ver_num_mates
                    
                FROM sow_boar 
                WHERE id = %s
                """ % sow_boar_id
        
        
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
            msg = 'get_data_ver_num(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:


            for row in rows:
                cur_data_ver_num_sow_boar   = row[0]
                cur_data_ver_num_medvac     = row[1]
                cur_data_ver_num_health_notes= row[2]
                cur_data_ver_num_output     = row[3]
                cur_data_ver_num_mates      = row[4]

                                
                cur_entry = {
                    'data_ver_num': {
                        'sow_boar':         cur_data_ver_num_sow_boar,   
                        'medvac':           cur_data_ver_num_medvac,     
                        'health_notes':     cur_data_ver_num_health_notes,
                        'output':           cur_data_ver_num_output,     
                        'mates':            cur_data_ver_num_mates
                    }
                }
                
                return cur_entry

        
        return None

    
    
    def get_list(self, pig_farm_id = None, sex = None, sow_boar_id = None, 
            is_disposed = 0, inc_user_audit = 0, order_by = 0):
        """
        Will get sow_boar list.
        
        Parameters
        ----------
        
        pig_farm_id : integer
            farm_id
        
        sex : char
            M = returns boar
            F = returns gilts/sows
            
        is_disposed: int 
            if > 0, will get disposed sow_boar only; user_audit will always be returned
            
        inc_user_audit : int 
            0 = will not include user audit

        order_by : int
            0 = ORDER BY date_of_birth DESC
            1 = ORDER BY name ASC, number ASC

            
        
        Returns
        -------
        list of dictionary
        
        
        """
       
        if is_disposed == 0:
       
            if sow_boar_id is None:
                where_clause = 'WHERE a.pig_farm_id = %s ' % pig_farm_id
                where_clause += ' AND a.is_disposed = 0 '
                
                if sex is not None:
                    where_clause += ' AND a.sex = "%s" ' % sex
                
                
                if order_by == 0:
                    order_clause = ' ORDER BY a.date_of_birth DESC '
                else:
                    order_clause = ' ORDER BY a.name ASC, a.number ASC'
            
            else:
                where_clause = 'WHERE a.id = %s ' % sow_boar_id
                order_clause = ''
                   
        else:
            where_clause = 'WHERE a.pig_farm_id = %s ' % pig_farm_id
            where_clause += ' AND a.is_disposed = 1 '
            
            order_clause = ' ORDER BY a.date_dispose DESC'
            
            inc_user_audit = 1
            
            
               
        if inc_user_audit == 0:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.farm_sow_id,
                        a.farm_boar_id,
                        a.number,
                        a.name,
                       
                        a.sow_status_id,
                        a.birth_pig_prod_id,
                        
                        a.dispose_status_id,
                        a.date_dispose,
                        
                        a.parent_sow_id,
                        b.number,
                        b.name,
                       
                        a.parent_boar_id,
                        c.number,
                        c.name,
                        
                        a.date_of_birth,
                        a.date_eartag,
                        
                        a.is_external,
                        a.is_production_ready,
                        
                        a.num_nipples,
                        
                        a.num_births,
                        a.num_pigs_wean,
                        
                        
                        a.last_pig_production_id,
                        d.farm_prod_id,
                        d.prod_status_id,
                        
                        d.insemination_type,
                        
                        d.date_insemination,
                        d.date_expected_birth,
                        d.date_actual_birth,
                        d.date_weaning,
                        
                        d.boar_id,
                        d.semen_supplier_id,
                        d.semen_sup_semen_id,
                        d.semen_ai_boar_id,
                        
                        d.num_pigs_live_m,
                        d.num_pigs_live_f,
                        d.num_pigs_dead_at_birth,
                        d.num_dead_after_birth,
                        
                        d.num_pigs_current,
                        
                        d.num_pigs_weaning_m,
                        d.num_pigs_weaning_f,
                        d.num_pigs_weaning,
                        d.wean_pigs_weight_total,
                        d.wean_pigs_weight_pp,
                        
                        
                        e.name      AS boar_name,
                        e.number    AS boar_number,
                        e.is_external,
                        
                        f.name      AS semen_supplier_name,
                        g.name      AS semen_name,
                        
                        h.name      AS ai_boar_name,
                        h.number    AS ai_boar_number,
                        
                        
                        a.last_mate_sow_boar_id,
                        a.mate_count,
                        a.date_last_mate,
                        
                        
                        a.data_ver_num_sow_boar,
                        a.data_ver_num_medvac,
                        a.data_ver_num_health_notes,
                        a.data_ver_num_output,
                        a.data_ver_num_mates
                        
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_boar b          ON a.parent_sow_id          = b.id
                    LEFT OUTER JOIN sow_boar c          ON a.parent_boar_id         = c.id
                    LEFT OUTER JOIN pig_production d    ON a.last_pig_production_id  = d.id
                    
                    LEFT OUTER JOIN sow_boar e          ON d.boar_id                = e.id
                    LEFT OUTER JOIN common_supplier f   ON d.semen_supplier_id      = f.id
                    LEFT OUTER JOIN semen_supplier_semen g  ON d.semen_sup_semen_id = g.id
                    
                    LEFT OUTER JOIN sow_boar h          ON d.semen_ai_boar_id       = h.id
                    
                    %s
                    %s 
                    """ % (where_clause, order_clause)
            
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.farm_sow_id,
                        a.farm_boar_id,
                        a.number,
                        a.name,
                       
                        a.sow_status_id,
                        a.birth_pig_prod_id,
                        
                        a.dispose_status_id,
                        a.date_dispose,
                        
                        a.parent_sow_id,
                        b.number,
                        b.name,
                       
                        a.parent_boar_id,
                        c.number,
                        c.name,
                        
                        a.date_of_birth,
                        a.date_eartag,
                        
                        a.is_external,
                        a.is_production_ready,
                        
                        a.num_nipples,
                        
                        a.num_births,
                        a.num_pigs_wean,
                        
                        
                        a.last_pig_production_id,
                        d.farm_prod_id,
                        d.prod_status_id,
                        
                        d.insemination_type,
                        
                        d.date_insemination,
                        d.date_expected_birth,
                        d.date_actual_birth,
                        d.date_weaning,
                        
                        d.boar_id,
                        d.semen_supplier_id,
                        d.semen_sup_semen_id,
                        d.semen_ai_boar_id,
                        
                        d.num_pigs_live_m,
                        d.num_pigs_live_f,
                        d.num_pigs_dead_at_birth,
                        d.num_dead_after_birth,
                        
                        d.num_pigs_current,
                        
                        d.num_pigs_weaning_m,
                        d.num_pigs_weaning_f,
                        d.num_pigs_weaning,
                        d.wean_pigs_weight_total,
                        d.wean_pigs_weight_pp,
                        
                        
                        e.name      AS boar_name,
                        e.number    AS boar_number,
                        e.is_external,
                        
                        f.name      AS semen_supplier_name,
                        g.name      AS semen_name,
                        
                        h.name      AS ai_boar_name,
                        h.number    AS ai_boar_number,
                        
                        
                        a.last_mate_sow_boar_id,
                        a.mate_count,
                        a.date_last_mate,
                        
                        
                        a.data_ver_num_sow_boar,
                        a.data_ver_num_medvac,
                        a.data_ver_num_health_notes,
                        a.data_ver_num_output,
                        a.data_ver_num_mates,
                        
                        
                        j.name_last,
                        j.name_first,
                        a.dt_entry,
                        
                        k.name_last,
                        k.name_first,
                        a.dt_last_update
                        
                        
                        
                    FROM sow_boar a
                    LEFT OUTER JOIN sow_boar b          ON a.parent_sow_id          = b.id
                    LEFT OUTER JOIN sow_boar c          ON a.parent_boar_id         = c.id
                    LEFT OUTER JOIN pig_production d    ON a.last_pig_production_id  = d.id
                    
                    LEFT OUTER JOIN sow_boar e          ON d.boar_id                = e.id
                    LEFT OUTER JOIN common_supplier f   ON d.semen_supplier_id      = f.id
                    LEFT OUTER JOIN semen_supplier_semen g  ON d.semen_sup_semen_id = g.id
                    
                    LEFT OUTER JOIN sow_boar h          ON d.semen_ai_boar_id       = h.id

                    
                    LEFT OUTER JOIN user j              ON a.added_by_user_id       = j.id
                    LEFT OUTER JOIN user k              ON a.last_update_user_id    = k.id
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
                cur_id                      = row[0]
                cur_farm_sow_id             = row[1]
                cur_farm_boar_id            = row[2]
                cur_number                  = row[3]
                cur_name                    = row[4]
                    
                cur_sow_status_id           = row[5]
                cur_birth_pig_prod_id       = row[6]
                    
                cur_dispose_status_id       = row[7]
                cur_date_dispose            = str(row[8]) if row[8] else None
                    
                cur_parent_sow_id           = row[9]
                cur_parent_sow_number       = row[10]
                cur_parent_sow_name         = row[11]
                    
                cur_parent_boar_id          = row[12]
                cur_parent_boar_number      = row[13]
                cur_parent_boar_name        = row[14]
                    
                cur_date_of_birth           = str(row[15]) if row[15] else None
                cur_date_eartag             = str(row[16]) if row[16] else None
                    
                cur_is_external             = row[17]
                cur_is_production_ready     = row[18]
                    
                cur_num_nipples             = row[19]
                
                cur_num_births              = row[20]
                cur_num_pigs_wean           = row[21]
                        
                    
                cur_pig_prod_id             = row[22]
                cur_farm_prod_id            = row[23]
                cur_prod_status_id          = row[24]    
                
                cur_prod_insemination_type  = row[25]
                
                cur_date_insemination       = str(row[26]) if row[26] else None 
                cur_date_expected_birth     = str(row[27]) if row[27] else None
                cur_date_actual_birth       = str(row[28]) if row[28] else None
                cur_date_weaning            = str(row[29]) if row[29] else None
                    
                cur_boar_id                 = row[30]
                cur_semen_supplier_id       = row[31]
                cur_semen_sup_semen_id      = row[32]
                cur_semen_ai_boar_id        = row[33]
                    
                cur_num_pigs_live_m         = row[34]
                cur_num_pigs_live_f         = row[35]
                cur_num_pigs_dead_birth     = row[36]
                cur_num_dead_after_birth    = row[37]
                    
                cur_num_pigs_current        = row[38]
                    
                cur_num_pigs_weaning_m      = row[39]
                cur_num_pigs_weaning_f      = row[40]
                cur_num_pigs_weaning        = row[41]
                cur_weight_weaning          = row[42]
                cur_weight_weaning_pp       = row[43]
                    
                    
                cur_boar_name               = row[44]
                cur_boar_number             = row[45]
                cur_boar_is_external        = row[46]
                    
                    
                cur_semen_supplier_name     = row[47]
                cur_semen_sup_semen_name    = row[48]
                
                cur_semen_ai_boar_name      = row[49]
                cur_semen_ai_boar_number    = row[50]
                
                cur_last_mate_sow_boar_id   = row[51]
                cur_mate_count              = row[52]
                cur_date_last_mate          = str(row[53]) if  row[53] else None
                
                
                cur_data_ver_num_sow_boar   = row[54]
                cur_data_ver_num_medvac     = row[55]
                cur_data_ver_num_health_notes= row[56]
                cur_data_ver_num_output     = row[57]
                cur_data_ver_num_mates      = row[58]

               
                sow_boar = {
                    'id':                   cur_id,
                    'farm_sow_id':          cur_farm_sow_id,
                    'farm_boar_id':         cur_farm_boar_id,
                    'number':               cur_number, 
                    'name':                 cur_name,
                    
                    'status_id':            cur_sow_status_id,
                    'birth_pig_prod_id':    cur_birth_pig_prod_id,
                    
                    
                    'dispose_status_id':    cur_dispose_status_id,
                    'date_dispose':         cur_date_dispose,
                        
                    
                    'parent_sow_id':        cur_parent_sow_id,
                    'parent_sow_number':    cur_parent_sow_number,
                    'parent_sow_name':      cur_parent_sow_name,
                    
                    'parent_boar_id':       cur_parent_boar_id,
                    'parent_boar_number':   cur_parent_boar_number,
                    'parent_boar_name':     cur_parent_boar_name,
                    
                    'date_of_birth':        cur_date_of_birth,
                    'date_eartag':          cur_date_eartag,
                    
                    'is_external':          cur_is_external,
                    'is_production_ready':  cur_is_production_ready,
                    
                    'num_nipples':          cur_num_nipples,
                    
                    'num_births':           cur_num_births,
                    'num_pigs_wean':        cur_num_pigs_wean,
                    
                    
                    'cur_pig_production': {
                        'pig_production': {
                            'id':                   cur_pig_prod_id,
                            'farm_prod_id':         cur_farm_prod_id,
                            'prod_status_id':       cur_prod_status_id,
                            'cur_pig_count':        cur_num_pigs_current,
                            'dead_after_birth':     cur_num_dead_after_birth
                        },
                        
                        'insemination':{
                            'insem_type':       cur_prod_insemination_type,
                            'insem_date':       cur_date_insemination,
                        
                            'boar': {
                                'id':           cur_boar_id,
                                'number':       cur_boar_number,
                                'name':         cur_boar_name,
                                'is_external':  cur_boar_is_external
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
                                }
                            }
                        },
                     
                        'birth': {
                            'date_expected':    cur_date_expected_birth,
                            'date_actual':      cur_date_actual_birth,
                            
                            'num_dead_at_birth':cur_num_pigs_dead_birth,
                            
                            'pigs_live_m':      cur_num_pigs_live_m,
                            'pigs_live_f':      cur_num_pigs_live_f
                        },
                        
                        'weaning': {
                            'date_weaning':     cur_date_weaning,
                            'num_pigs_m':       cur_num_pigs_weaning_m,
                            'num_pigs_f':       cur_num_pigs_weaning_f,
                            'num_pigs':         cur_num_pigs_weaning,
                            'weight':           cur_weight_weaning,
                            'weight_pp':        cur_weight_weaning_pp
                        }
                        
                    },
                    
                    
                    'last_mate_sow_boar_id': cur_last_mate_sow_boar_id,
                    'mate_count':           cur_mate_count,
                    'date_last_mate':       cur_date_last_mate,
                    
                    
                    'data_ver_num':{
                        'sow_boar':         cur_data_ver_num_sow_boar,   
                        'medvac':           cur_data_ver_num_medvac,     
                        'health_notes':     cur_data_ver_num_health_notes,
                        'output':           cur_data_ver_num_output,     
                        'mates':            cur_data_ver_num_mates      
                    }
                    
                }
                
                
                # Remove null entries if possible
                sow_only = 0
                boar_only = 0
                
                
                if is_disposed == 0:
                    del sow_boar['dispose_status_id']
                    del sow_boar['date_dispose']
                
                
                if sex is not None:
                    if sex == 'F':
                        sow_only = 1
                    else:
                        boar_only = 1
                else:
                    if sow_boar['farm_sow_id'] is not None:
                        sow_only = 1
                    else:
                        boar_only = 1
                    
                        
                if sow_only > 0:
                    del sow_boar['farm_boar_id']
                    del sow_boar['is_external']
                    
                    if sow_boar['num_nipples'] is None:
                        del sow_boar['num_nipples']
                    
                    
                    # sow_boar['cur_pig_production'] is for sow only
                    
                    if sow_boar['cur_pig_production']['pig_production']['id'] is None:
                        del sow_boar['cur_pig_production']
                    else:  
                        if cur_prod_insemination_type == 'B':
                            del sow_boar['cur_pig_production']['insemination']['ai']
                            
                            if cur_boar_is_external == 0:
                                del sow_boar['cur_pig_production']['insemination']['boar']['is_external']
                            
                        else:
                            del sow_boar['cur_pig_production']['insemination']['boar']
                            
                            if cur_prod_insemination_type == 'AI_X':
                                del sow_boar['cur_pig_production']['insemination']['ai']['internal_boar']
                                
                            else:
                                del sow_boar['cur_pig_production']['insemination']['ai']['semen_supplier']
                        
                        
                        if cur_date_actual_birth is None:
                            del sow_boar['cur_pig_production']['birth']['pigs_live_m']
                            del sow_boar['cur_pig_production']['birth']['pigs_live_f']
                            
                            del sow_boar['cur_pig_production']['weaning']
                            
                        else:
                            if cur_date_weaning is None:
                                del sow_boar['cur_pig_production']['weaning']
                        
                        
                if boar_only > 0:
                    # These are for sow only
                    del sow_boar['farm_sow_id'] 
                    del sow_boar['status_id']
                    del sow_boar['num_nipples'] 
                    del sow_boar['num_births']
                    del sow_boar['num_pigs_wean']
                    
                    del sow_boar['cur_pig_production'] 
                        
                
                
                if sow_boar['parent_sow_id'] is None:
                    del sow_boar['parent_sow_id']
                    del sow_boar['parent_sow_name']
                    del sow_boar['parent_sow_number']
                    
                    
                if sow_boar['parent_boar_id'] is None:
                    del sow_boar['parent_boar_id']
                    del sow_boar['parent_boar_name']
                    del sow_boar['parent_boar_number']
                    
                    
                if sow_boar['date_eartag'] is None:
                    del sow_boar['date_eartag']
                
                
                if sow_boar['last_mate_sow_boar_id'] is None:
                    del sow_boar['last_mate_sow_boar_id']
                
                if sow_boar['date_last_mate'] is None:
                    del sow_boar['date_last_mate']
                

                
                if inc_user_audit > 0:
                    
                    added_by = {
                        'name_last':        row[58],
                        'name_first':       row[59],
                        'dt_entry':         str(row[60])
                    }
                    
                    last_update = {
                        'name_last':        row[61],
                        'name_first':       row[62],
                        'dt_update':        str(row[63]) if row[63] else None
                    }
                
                    sow_boar['added_by']    = added_by
                    sow_boar['last_update'] = last_update
                            
                
                cur_entry = {'sow_boar': sow_boar}
                    
                result.append(cur_entry)

        
        return result


    def get_list_disposed(self, farm_id):
        """
        Dedicated query for disposed pigs. This will return maximum information
        bacuse the user edit is also returned. This will return both sows and 
        boars.
        
        Parameters
        ----------
        
        
        Returns
        -------
        list of dictionary
        
        
        """
        
       
            
        sql =   """
                SELECT 
                    a.id,
                    a.farm_sow_id,
                    a.farm_boar_id,
                    a.number,
                    a.name,
                    a.sex,
                    
                    a.is_external,
                    a.is_production_ready,
                    
                    b.farm_prod_id,
                    
                    a.num_nipples,
                    
                    a.last_mate_sow_boar_id,
                    a.mate_count, 
                   
                    a.sow_status_id,
                    a.dispose_status_id,
                    
                    a.date_of_birth,
                    a.date_eartag,
                    a.date_dispose,
                    a.date_last_mate,
                    
                    c.notes AS add_notes,
                    d.notes AS dispose_notes,
                    
                    e.name_last,
                    e.name_first,
                    a.dt_entry,
                    
                    f.name_last,
                    f.name_first,
                    a.dt_last_update
                    
                FROM sow_boar a
                LEFT OUTER JOIN pig_production b    ON a.last_pig_production_id = b.id
                LEFT OUTER JOIN pig_prod_notes c    ON a.add_notes_id      = c.id
                LEFT OUTER JOIN pig_prod_notes d    ON a.dispose_notes_id  = d.id
                LEFT OUTER JOIN user e              ON a.added_by_user_id   = e.id
                LEFT OUTER JOIN user f              ON a.last_update_user_id = f.id
                WHERE a.pig_farm_id = %s AND is_disposed = 1
                ORDER BY a.date_dispose DESC;
                """ % farm_id
        
        
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
                cur_sex     = row[5]
                
                cur_entry = {
                    'sow_boar': {
                        'id':                   row[0],
                        'farm_sow_id':          row[1],
                        'farm_boar_id':         row[2],
                        'number':               row[3], 
                        'name':                 row[4],
                        'sex':                  row[5],
                        
                        'is_external':          row[6],
                        'is_production_ready':  row[7],
                        
                        
                        'last_prod_id':         row[8],
                        
                        'num_nipples':          row[9],
                        
                        'last_mate_sow_boar_id':row[10],
                        'mate_count':           row[11],
                                                
                        'status_id':            row[12],
                        'dispose_status_id':    row[13],
                        
                        'date_of_birth':        str(row[14])  if row[14] else None,
                        'date_eartag':          str(row[15])  if row[15] else None,
                        'date_dispose':         str(row[16])  if row[16] else None,
                        'date_last_mate':       str(row[17])  if row[17] else None,
                        
                        'add_notes':            row[18],
                        'dispose_notes':        row[19]
                    },
                    
                    'added_by': {
                        'name_last':        row[20],
                        'name_first':       row[21],
                        'dt_entry':         str(row[22])
                    },
                    
                    'last_update':{
                        'name_last':        row[23],
                        'name_first':       row[24],
                        'dt_update':        str(row[25]) if row[25] else None
                    }                    
                }
                
                if cur_sex == 'F':
                    del cur_entry['sow_boar']['farm_boar_id']
                    del cur_entry['sow_boar']['is_external']
                else:
                    # These are for sow only
                    del cur_entry['sow_boar']['farm_sow_id'] 
                    del cur_entry['sow_boar']['num_nipples'] 
                    
                
                result.append(cur_entry)

        
        return result

    
    def get_parent_trace(self, sow_id, boar_id, pig_farm_id):
        """
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        """
        
        """
        Notes:
        
        1.) The sow_boar.parent_sow_id and sow_boar.parent_boar_id
            are set by user when sow_boar.birth_pig_prod_id was not set.
            
        2.) The sow_boar.birth_pig_prod_id is set by the system;
            This is when a production piglet is ear tagged or a production
            pig is harvested as sow or boar;
            
            When a piglet is eartagged at production or a production pig is 
            harvested as sow or boar, this pig parents will be computed by the system.
            This should not be editable by user.
            
            
        3.) When sow_boar.birth_pig_prod_id is set, it will read the 
            insemination information of this pig_production entry.
        
        4.) There are 3 insemination types
            - sow + boar
            - sow + artifical insemination, external semen (semen brought from outside the farm`)
            - sow + artifical insemination, internal semen (taken from one of the farm boars)
        
        """
        
        
        if pig_farm_id > 0:
            where_clause = 'WHERE a.pig_farm_id = %s AND a.is_disposed = 0' % pig_farm_id
        
        else:
            list_id = []
            
            if sow_id > 0:
                list_id.append(str(sow_id))
                
            if boar_id > 0:
                list_id.append(str(boar_id))
            
            where_clause = ','.join(list_id)
            
            
        sql =   """
                SELECT 
                    a.id,
                    a.birth_pig_prod_id,
                    
                    a.parent_sow_id,
                    b.name,
                    b.number,
                    b.is_disposed,
                    
                    a.parent_boar_id,
                    c.name,
                    c.number,
                    c.is_disposed,
                    
                    d.insemination_type,
                    d.sow_id,
                    d.boar_id,
                    d.semen_ai_boar_id,
                    
                    d.semen_supplier_id,
                    e.name AS semen_supplier_name,
                    
                    d.semen_sup_semen_id,
                    f.name AS semen_name,
                    
                    a.sex
                    
                FROM sow_boar a
                LEFT OUTER JOIN sow_boar b              ON a.parent_sow_id = b.id
                LEFT OUTER JOIN sow_boar c              ON a.parent_boar_id = c.id
                
                LEFT OUTER JOIN pig_production d        ON a.birth_pig_prod_id = d.id
                LEFT OUTER JOIN common_supplier e       ON d.semen_supplier_id = e.id
                LEFT OUTER JOIN semen_supplier_semen f  ON d.semen_sup_semen_id = f.id
                
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
            msg = 'get_parent_trace(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            for row in rows:
                cur_id                      = row[0]
                cur_birth_pig_prod_id       = row[1]
                    
                cur_parent_sow_id           = row[2]
                cur_parent_sow_name         = row[3]
                cur_parent_sow_number       = row[4]
                cur_parent_sow_is_disposed  = row[5]
                    
                cur_parent_boar_id          = row[6]
                cur_parent_boar_name        = row[7]
                cur_parent_boar_number      = row[8]
                cur_parent_boar_is_disposed = row[9]
                    
                    
                cur_insem_type              = row[10]
                cur_insem_sow_id            = row[11]
                cur_insem_boar_id           = row[12]
                cur_insem_semen_ai_boar_id  = row[13]
                    
                cur_semen_supplier_id       = row[14]
                cur_semen_supplier_name     = row[15]
                    
                cur_semen_sup_semen_id      = row[16]
                cur_semen_sup_semen_name    = row[17]

                cur_sex                     = row[18]
                
                cur_entry = {
                    'sow_boar':{
                        'id':               cur_id,
                        'sex':              cur_sex
                    },
                    
                    'parent_sow':{
                        'id':               cur_parent_sow_id,
                        'name':             cur_parent_sow_name,
                        'number':           cur_parent_sow_number,
                        'is_disposed':      cur_parent_sow_is_disposed
                    },
                    
                    
                    'parent_boar':{
                        'id':               cur_parent_boar_id,
                        'name':             cur_parent_boar_name,
                        'number':           cur_parent_boar_number,
                        'is_disposed':      cur_parent_boar_is_disposed
                    },
                    
                    
                    'insemination':{
                        'type':             cur_insem_type,
                        'sow_id':           cur_insem_sow_id,
                        'boar_id':          cur_insem_boar_id,
                        'ai_boar_id':       cur_insem_semen_ai_boar_id,
                        
                        'semen_supplier':{
                            'id':           cur_semen_supplier_id,
                            'name':         cur_semen_supplier_name,
                                
                            'semen':     {
                                'id':       cur_semen_sup_semen_id,
                                'name':     cur_semen_sup_semen_name
                            }
                        }
                    }
                }
                
                if cur_entry['insemination']['ai_boar_id'] is None:
                    del cur_entry['insemination']['ai_boar_id']
                
                if cur_entry['insemination']['semen_supplier']['id'] is None:
                    del cur_entry['insemination']['semen_supplier']
                
                result.append(cur_entry)

        return result

    
    
