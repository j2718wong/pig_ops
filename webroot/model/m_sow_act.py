# December 13, 2024
# Jack Wong

from common_constants       import *



class SowActivity:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SowActivity'
    
    
    def get_latest_sow_activities(self, full_info = 0, list_ins_id = None):
        """
        Will get list of latest sow activities.
        
        
        Returns
        -------
        list of dictionary

        """
        
        s_list_ins_id = ''
        if list_ins_id is not None:
            s_list_ins_id = ','.join(list_ins_id)
            s_list_ins_id = ' AND insemination_id IN(' + s_list_ins_id + ')'
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        if full_info == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.insemination_id,
                        a.sow_number,
                        b.description AS activity,
                        a.date,
                        a.date_2,
                        a.days_since_ins,
                        a.description

                    FROM sow_coming_activity a
                    LEFT OUTER JOIN coming_activity b  ON a.coming_activity_id = b.id
                    LEFT OUTER JOIN pig_production c   ON a.insemination_id = c.id
                    WHERE c.status_id IN (1,4) AND (
                        (a.date >= CURRENT_DATE AND a.date_2 IS NULL) OR 
                        (a.date <= CURRENT_DATE AND CURRENT_DATE <= a.date_2)
                    ) %s
                    ORDER BY a.sow_number, a.id;
                    """ % s_list_ins_id
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.insemination_id,
                        a.sow_number,
                        b.description AS activity,
                        a.date,
                        a.date_2,
                        a.days_since_ins,
                        a.description

                    FROM sow_coming_activity a
                    LEFT OUTER JOIN coming_activity b           ON a.coming_activity_id = b.id
                    LEFT OUTER JOIN pig_production c   ON a.insemination_id = c.id
                    WHERE c.status_id IN (1,4) %s
                    ORDER BY a.sow_number, a.id;
                    """ % s_list_ins_id

        
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            
        except Exception as e:
            msg = 'get_latest_sow_activities(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            last_sow_number = None
            
            for row in rows:
                cur_id                  = row[0]
                cur_ins_id              = row[1]
                cur_sow_number          = row[2]
                cur_activity            = row[3]
                cur_date                = str(row[4])
                
                cur_date_2              = None
                if row[5] is not None:
                    cur_date_2          = str(row[5])
                
                cur_days_since_ins      = None
                if row[6] is not None:
                    cur_days_since_ins  = row[6]
                    
                cur_description         = ''
                if row[7] is not None:
                    cur_description     = row[7]
                
                
                if last_sow_number is None or last_sow_number != cur_sow_number:
                
                    cur_entry = {
                        'ins_id':           cur_ins_id,
                        'sow_number':       cur_sow_number,
                        
                        'activities':       []
                    }
                    
                    result.append(cur_entry) 
                    
                    last_sow_number = cur_sow_number
                
                
                cur_activity = {
                   'id':            cur_id,
                   'date':          cur_date,
                   'date_2':        cur_date_2,
                   'days_ins':      cur_days_since_ins,
                   'activity':      cur_activity,
                   'desc':          cur_description
                }
                
                cur_entry['activities'].append(cur_activity)

        
        return result
    
  
    def get_latest_calendar_activities(self, date_start, date_end):
        """
        Will get list of latest calendar activities.
        
        
        Returns
        -------
        list of dictionary

        """
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
      
        sql =   """
                SELECT 
                    a.id,
                    a.insemination_id,
                    a.sow_number,
                    b.description AS activity,
                    a.date,
                    a.date_2,
                    a.days_since_ins,
                    a.description

                FROM sow_coming_activity a
                LEFT OUTER JOIN coming_activity b  ON a.coming_activity_id = b.id
                LEFT OUTER JOIN pig_production c   ON a.insemination_id = c.id
                WHERE c.status_id IN (1,4) AND (
                    (a.date >= '%s' AND a.date <= '%s')
                )
                ORDER BY a.date, a.sow_number;
                """ % (date_start, date_end)
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            
        except Exception as e:
            msg = 'get_latest_calendar_activities(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            last_date = None
            
            for row in rows:
                cur_id                  = row[0]
                cur_ins_id              = row[1]
                cur_sow_number          = row[2]
                cur_activity            = row[3]
                cur_date                = str(row[4])
                
                cur_date_2              = None
                if row[5] is not None:
                    cur_date_2          = str(row[5])
                
                cur_days_since_ins       = None
                if row[6] is not None:
                    cur_days_since_ins   = row[6]
                    
                cur_description         = ''
                if row[7] is not None:
                    cur_description     = row[7]
                
                
                if last_date is None or last_date != cur_date:
                
                    cur_entry = {
                        'date':             cur_date,
                        
                        'activities':       []
                    }
                    
                    result.append(cur_entry) 
                    
                    last_date = cur_date
                
                
                cur_activity = {
                   'ins_id':        cur_ins_id,
                   'sow_number':    cur_sow_number, 
                   'id':            cur_id,
                   'days_ins':      cur_days_since_ins,
                   'activity':      cur_activity,
                   'desc':          cur_description
                }
                
                cur_entry['activities'].append(cur_activity)

        
        return result
    
     
    
    def get_production_sow_list(self, pig_farm_id, filter_type, inc_historical = 0):
        """
        Will get list of production sow list.
        
        
        filter_type:
            0 = gestating
            1 = weaning
        
        Returns
        -------
        list of dictionary

        """
        
        
        if filter_type == 0:
            filter_clause = ' a.prod_status_id = 1'
            if inc_historical > 0:
                filter_clause = ' a.prod_status_id IN (1, 4, 5, 6, 7, 8, 9)'
        
        else:
            filter_clause = ' a.prod_status_id IN (1, 4, 5, 6)'
            if inc_historical > 0:
                filter_clause = ' a.prod_status_id IN (1, 4, 5, 6, 7, 8, 9)'
        
      
        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    
                    a.sow_id,
                    b.number AS sow_number,
                    b.name AS sow_name,
                    
                    a.prod_status_id,
                    c.name AS status_name,
                    
                    a.date_insemination,
                    a.insemination_type,
                    
                    a.date_expected_birth,
                    a.date_actual_birth,
                    a.num_days_actual,
                    
                    a.num_pigs_dead_at_birth,
                    a.num_pigs_live_m,
                    a.num_pigs_live_f,
                    
                    a.date_weaning,
                    a.num_pigs_weaning_m,
                    a.num_pigs_weaning_f,
                    
                    
                    a.boar_id,
                    a.semen_source_id,
                    
                    d.number,
                    d.name AS boar_name,
                    d.notes,
                    
                    e.name AS semen_source_name,
                    e.semen_supplier_id,
                    f.name AS semen_supplier_name,
                    
                    e.boar_id AS semen_source_boar_id,
                    g.number AS semen_source_boar_num,
                    g.name AS semen_source_boar_name 
                    
                FROM pig_production a
                LEFT OUTER JOIN sow_boar       b    ON a.sow_id = b.id
                LEFT OUTER JOIN pig_prod_status c   ON a.prod_status_id = c.id
                LEFT OUTER JOIN sow_boar       d    ON a.boar_id = d.id
                LEFT OUTER JOIN semen_source   e    ON a.semen_source_id = e.id
                LEFT OUTER JOIN semen_supplier f    ON e.semen_supplier_id = f.id
                LEFT OUTER JOIN sow_boar       g    ON e.boar_id = g.id
                WHERE a.pig_farm_id = %s AND %s
                ORDER BY a.date_insemination DESC
                """ % (pig_farm_id, filter_clause)  
        
        
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
            msg = 'get_production_sow_list(); error in executing query[] = ' + sql
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
                
                cur_sow_id              = row[2]
                cur_sow_number          = row[3]
                cur_sow_name            = row[4]
                
                cur_prod_status_id      = row[5]
                cur_prod_status_name    = row[6]
                
                
                cur_date_insemination   = str(row[7])
                cur_insem_type          = row[8]
                
                cur_date_expected       = str(row[9])
                cur_date_actual         = str(row[10]) if row[10] else None
                cur_num_days_actual     = row[11]
                
                cur_num_pigs_dead_at_birth = row[12]
                cur_num_pigs_live_m     = row[13]
                cur_num_pigs_live_f     = row[14]
                    
                
                cur_date_weaning        = str(row[15]) if row[15] else None
                cur_num_pigs_weaning_m  = row[16]
                cur_num_pigs_weaning_f  = row[17]
                
                
                cur_boar_id             = row[18]
                cur_semen_source_id     = row[19]
                
                cur_boar_number         = row[20]
                cur_boar_name           = row[21]
                cur_boar_notes          = row[22]
                
                cur_semen_source_name   = row[23]
                cur_semen_supplier_id   = row[24]
                cur_semen_supplier_name = row[25]
                
                cur_semen_source_boar_id    = row[26]
                cur_semen_source_boar_num   = row[27]
                cur_semen_source_boar_name  = row[28]
                
                cur_entry = {
                    'pig_prod': {
                        'id':               cur_id,
                        'farm_prod_id':     cur_farm_prod_id, 
                        
                        'status_id':        cur_prod_status_id,
                        'status_name':      cur_prod_status_name,
                    },
                    
                    'insemination': {
                        'date':             cur_date_insemination,
                        'type':             cur_insem_type
                    },
                    
                    
                    'sow': {
                        'id':               cur_sow_id,
                        'number':           cur_sow_number,
                        'name':             cur_sow_name,
                    },
                    
                    
                    'boar': {
                        'id':               cur_boar_id,
                        'number':           cur_boar_number,
                        'name':             cur_boar_name,
                        'notes':            cur_boar_notes
                    },
                    
                    'semen_source': {
                        'id':               cur_semen_source_id,
                        'name':             cur_semen_source_name,
                        
                        'is_external':      1,
                        
                        'supplier':{
                            'id':           cur_semen_supplier_id,
                            'name':         cur_semen_supplier_name
                        },
                        
                        'boar':{
                            'id':           cur_semen_source_boar_id,
                            'number':       cur_semen_source_boar_num,
                            'name':         cur_semen_source_boar_name
                        }
                    },
                    
                    
                    'birth': {
                        'date_expected':    cur_date_expected,
                        'date_actual':      cur_date_actual,
                        'num_days_actual':  cur_num_days_actual,
                    
                        'num_pigs': {
                            'dead_at_birth':cur_num_pigs_dead_at_birth,
                            'live_m':       cur_num_pigs_live_m,
                            'live_f':       cur_num_pigs_live_f
                        }
                    },
                    
                    
                    'weaning': {
                        'date':             cur_date_weaning,
                        'num_pigs_m':       cur_num_pigs_weaning_m,
                        'num_pigs_f':       cur_num_pigs_weaning_f
                    }
                    
                    
                }
                
                if cur_semen_source_boar_id  and cur_semen_source_boar_id > 0:
                    cur_entry['semen_source']['is_external'] = 0
                
                result.append(cur_entry)

        return result
    
    
    
    