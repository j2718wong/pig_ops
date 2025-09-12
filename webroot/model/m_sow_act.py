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
    
    
    def get_pig_prod_list(self, is_active = 0, is_growing = 0, is_harvested = 0, 
            year = None, sow = None):
        """
        Will get list of pig production list.
        
        Parameters
        ----------
        is_active : int
            if > 0, pig production with status gestating, lactating and weaning 
               will be returned
            
        is_growing : int
            if > 0, pig production with status growing, fattening, finishing will be returned
  
        is_harvested : int
            if > 0, pig production with status harvested will be returned
            
       
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
        
        where_clause    = ''
        order_by        = ' a.sow_id DESC, a.id DESC'
        
        if sow is not None:
            where_clause = "WHERE a.sow_number = '%s'" % sow
            
        else:
            if is_harvested > 0:
                where_clause = 'WHERE status_id = 10 '
                
                if year is not None:
                    where_clause += ' AND YEAR(a.date_weaning) =  %s ' % year
                
                order_by        = 'a.date_weaning DESC '
               
            else:
            
                if is_growing > 0:
                    where_clause = 'WHERE a.status_id IN (5,7,8,9)'
                    if year is not None:
                        where_clause += ' AND YEAR(a.date_weaning) =  %s ' % year
                else:
                    if is_active > 0:
                        where_clause = 'WHERE status_id IN(1,4,5) '
                        
                        if year is not None:
                            where_clause += ' AND YEAR(a.date_insemination) =  %s' % year
                            
                        order_by        = 'a.date_expected_birth '
        
        sql =   """
                SELECT 
                    a.id,
                    a.sow_number,
                    a.date_insemination,
                    a.date_expected_birth,
                    a.date_actual_birth,
                    a.num_days_actual,
                    a.status_id,
                    a.semen_desc,
                    b.name,
                    
                    a.num_pigs_dead_at_birth,
                    a.num_pigs_live_m,
                    a.num_pigs_live_f,
                    a.num_pigs_weaning_m,
                    a.num_pigs_weaning_f,
                    
                    a.date_weaning
         
                FROM pig_production a
                LEFT OUTER JOIN pig_prod_status b           ON a.prod_status_id = b.id
                %s
                ORDER BY %s
                """ % (where_clause, order_by)
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()

        except Exception as e:
            msg = 'get_pig_prod_list(); error in executing query[] = ' + sql
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
                cur_sow_number          = row[1]
                cur_date_insemination   = str(row[2])
                cur_date_expected       = str(row[3])
                
                cur_date_actual         = str(row[4]) if row[4] else None
                cur_num_days_actual     = row[5] if row[5] else None
                    
                cur_status_id           = row[6]
                cur_semen_desc          = row[7]
                cur_status              = row[8]
                    
                cur_num_b_dead          = row[9] if row[9] else None
                cur_num_b_male          = row[10] if row[10] else None
                cur_num_b_female        = row[11] if row[11] else None
                    
                cur_num_w_male          = row[12] if row[12] else None
                cur_num_w_female        = row[13] if row[13] else None
                
                cur_num_w_dead          = None
                if cur_num_w_male is not None and cur_num_w_female is not None:
                    cur_num_w_dead = cur_num_b_male + cur_num_b_female - \
                                        cur_num_w_male - cur_num_w_female
                                        
                                        
                cur_date_weaning        = str(row[14]) if row[14] else None
                
                
                cur_entry = {
                    'id':               cur_id,
                    'sow_number':       cur_sow_number, 
                    'date_ins':         cur_date_insemination,
                    'date_expected':    cur_date_expected,
                    'date_actual_birth': cur_date_actual,
                    'days_actual':      cur_num_days_actual,
                    'status_id':        cur_status_id,
                    'status':           cur_status,
                    'semen_desc':       cur_semen_desc,
                    'date_weaning':     cur_date_weaning,
                   
                    'num_piglets_birth':{
                        'dead':         cur_num_b_dead, 
                        'male':         cur_num_b_male,
                        'female':       cur_num_b_female
                    },
                    
                    'num_piglets_weaning':{
                        'dead':         cur_num_w_dead, 
                        'male':         cur_num_w_male,
                        'female':       cur_num_w_female
                    }
                   
                }
                
                result.append(cur_entry)

        
        return result
    
    
    def get_gestating_sow_list(self, pig_farm_id, inc_historical = 0):
        """
        Will get list of latest gestating sow list.
        
        
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
        
        filter = ' a.prod_status_id = 1'
        if inc_historical > 0:
            filter = ' a.prod_status_id IN (1, 4, 5, 6, 7, 8, 9)'
        
      
        sql =   """
                SELECT 
                    a.id,
                    a.farm_prod_id,
                    b.number,
                    b.name AS sow_name,
                    
                    a.date_insemination,
                    a.insemination_type,
                    a.date_expected_birth,
                    
                    a.boar_id,
                    a.semen_source_id,
                    
                    c.number,
                    c.name AS boar_name,
                    c.notes,
                    
                    d.name AS semen_source_name,
                    d.semen_supplier_id,
                    e.name AS semen_supplier_name,
                    
                    d.boar_id AS semen_source_boar_id,
                    f.number AS semen_source_boar_num
                    f.name AS semen_source_boar_name 
                    
                FROM pig_production a
                LEFT OUTER JOIN sow_boar       b    ON a.sow_id = b.id
                LEFT OUTER JOIN sow_boar       c    ON a.boar_id = c.id
                LEFT OUTER JOIN semen_source   d    ON a.semen_source_id = d.id
                LEFT OUTER JOIN semen_supplier e    ON d.semen_supplier_id = e.id
                LEFT OUTER JOIN sow_boar       f    ON d.boar_id = f.id
                WHERE a.pig_farm_id = %s AND %s
                ORDER BY a.date_insemination DESC
                """ % (pig_farm_id, filter)  
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            #conn.close()
            
        except Exception as e:
            msg = 'get_gestating_sow_list(); error in executing query[] = ' + sql
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
                cur_date_insemination   = str(row[4])
                cur_insem_type          = row[5]
                cur_date_expected       = str(row[6])
                
                cur_boar_id             = row[7]
                cur_semen_source_id     = row[8]
                
                cur_boar_number         = row[9]
                cur_boar_name           = row[10]
                cur_boar_notes          = row[11]
                
                cur_semen_source_name   = row[12]
                cur_semen_supplier_id   = row[13]
                cur_semen_supplier_name = row[14]
                
                cur_semen_source_boar_id    = row[15]
                cur_semen_source_boar_num   = row[16]
                cur_semen_source_boar_name  = row[17]
                
                cur_entry = {
                    'id':               cur_id,
                    'farm_prod_id':     cur_farm_prod_id, 
                   
                    'date_expected':    cur_date_expected,
                    
                    
                    'sow': {
                        'number':       cur_sow_number,
                        'name':         cur_sow_name,
                    },
                    
                    
                    'boar': {
                        'id':           cur_boar_id,
                        'number':       cur_boar_number,
                        'name':         cur_boar_name,
                        'notes':        cur_boar_notes
                    },
                    
                    'semen_source': {
                        'id':           cur_semen_source_id,
                        'name':         cur_semen_source_name,
                        
                        'is_external':  1,
                        
                        'supplier':{
                            'id':       cur_semen_supplier_id,
                            'name':     cur_semen_supplier_name
                        },
                        
                        'boar':{
                            'id':       cur_semen_source_boar_id,
                            'number':   cur_semen_source_boar_num,
                            'name':     cur_semen_source_boar_name,
                        }
                    },
                    
                    'insemination': {
                        'date':         cur_date_insemination,
                        'type':         cur_insem_type
                    }
                }
                
                if cur_semen_source_boar_id  and cur_semen_source_boar_id > 0:
                    cur_entry['semen_source']['is_external'] = 0
                
                result.append(cur_entry)

        return result
    
    
    
    