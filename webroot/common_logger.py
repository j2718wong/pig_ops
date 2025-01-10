# October 10, 2018
# Jack Wong (zhaoshan99@gmail.com)


import os
import io
import random


from datetime               import datetime
from common_constants       import *


LOG_LEVELS  = ('DEBUG', 'WARN', 'ERROR', 'FATAL')


JOKES_SPIDER = [
    'A spider is enjoying the bug at',
    'Please love me, i bring you a bug at',
    'Meow.. Just kidding i\'m a spider',
    'I was a web developer before the internet'
]

JOKES_COCKROACH = [
    'Program is dead Jim! Cockroach inside'
]


LINE_TYPE_NORMAL_MSG    = 0
LINE_TYPE_PLAIN_MSG     = 1

class Logger:
    def __init__(self, path_logs = None, log_name = 'log'):
        """
        Common logger for all applications
        
        Parameters
        ----------
        
        path_logs : string
            absolute path where to write the logs; 
            if not provided, will create logs directory in current directory
            
        log_name : string 
            string to be appended to the date in the filename of the log.
            Typical log filenames will have this format ::
            
              dev01@lnx-dev-02:~/cyfi/data/logs/2022-11-22$ ls -lt
              total 12
              -rw-rw-r-- 1 dev01 dev01 1834 Nov 22 09:46 2022-11-22_web.log
              -rw-rw-r-- 1 dev01 dev01 2648 Nov 22 09:15 2022-11-22_bkops.log
              -rw-rw-r-- 1 dev01 dev01  300 Nov 22 02:00 2022-11-22_sched.log

            The web, bkops and sched are the log_name.
        """
        
        if path_logs is None:
            cur_dir         = os.getcwd()
            path_logs       = os.path.join(cur_dir, 'data', 'logs')
        
        self.path_logs      = path_logs
        self.log_name       = log_name
        
        
        self.logs           = []
        
        
    def _get_log_entry(self, fname):
        """
        Each entry in self.logs has this dictionary ::
        
            {
                'fname':            '2022-11-22_sched.log',
                'last_line_type':   0
            }
        """
        for cur_entry in self.logs:
            if cur_entry['fname'] == fname:
                return cur_entry
        return None
        
        
    def append_to_log_file(self, log_level = LOG_DEBUG, log_name = None, 
            tag = None, msg = None, write_plain_msg = 0):
        """
        Will append msg to log file.
        
        Parameters
        ----------
        
        log_level : integer, optional
            Must be one of these ::
            
              LOG_DEBUG               = 0
              LOG_WARNING             = 1
              LOG_ERROR               = 2
              LOG_FATAL               = 3
              
        log_name : string, optional
            This is useful if there are several thread running and a log per 
            thread is desired.
        
            If log_name is None, the log file name format 2019-06-20_loc.log
            If log_name is not None, the log file name format 2019-06-20_loc_125.log
            where 125 is the log_name.
            
        tag : string, optional
            The tag where the log comes from. This is usually the originating 
            class name.
            
        msg : string
            message to append to the log file.
            
        write_plain_msg : integer
            if > 0, will append directly message to log file.
        """
        
        if tag is None:
            tag = ' '
        
        # Add current date to path_logs
        now             = datetime.now()
        date_str        = now.strftime('%Y-%m-%d')
        path_log        = os.path.join(self.path_logs, date_str)

        if not os.path.isdir(path_log):
            os.makedirs(path_log)

        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        fname           = date_str 
        fname           += '_' + self.log_name
        
        if log_name is not None:
            fname       += '_' + str(log_name)
        
        fname           += '.log'
        abspath         = os.path.join(path_log, fname)
        
        
        log_entry       = self._get_log_entry(fname)
        if log_entry is None:
            log_entry   = {
                'fname':            fname,
                'last_line_type':   0
            }
            self.logs.append(log_entry)
        
        
        if write_plain_msg == 0:
            
            s = ''
            if log_level == LOG_ERROR:
                len_items       = len(JOKES_SPIDER)
                index           = random.randint(0,len_items-1)
                spider_msg      = JOKES_SPIDER[index]
                
                s += '\n\n'
                s += '  / _ \\         '    + now_ts + ' [' + LOG_LEVELS[log_level] + ']\n'
                s += '\\_\\(_)/_/       '   + spider_msg + '\n'
                s += ' _//o\\\\_        '   + tag + '\n'
                s += '  /   \\'             + '\n'
                s += msg + '\n' 
            
            elif log_level == LOG_FATAL:
                len_items       = len(JOKES_COCKROACH)
                index           = random.randint(0,len_items-1)
                cockroach_msg   = JOKES_COCKROACH[index]
                
                s += '\n\n'
                s += '       ,--.     .--.'         + '\n'
                s += '      /    \\. ./    \\'      + '\n'
                s += '     /  /\\/  "  \\/\\  \\'   + '\n'
                s += '    / _/ /~~~v~~~\\ \\_ \\'   + '\n'
                s += '   /    /####|####\\    \\'   + '\n'
                s += '  ;  /\\{#####|#####}/\\  \\' + '\n'
                s += '  |_/  {#####|#####}  \\_:'   + '\n'
                s += '  |    {#####|#####}    |   ' + now_ts + ' [' + LOG_LEVELS[log_level] + ']\n'
                s += '  |   /{#####|#####}\\   |   '+ cockroach_msg + '\n'
                s += '  |  / {#####|#####} \\  |'   + '\n'
                s += '  | /  {#####|#####}  \\ |   '+ tag  + '\n'
                s += '  |  \\ \\#####|#####/ /  |'  + '\n'
                s += '  |   \\ \\####|####/ /   |'  + '\n'
                s += '   \\   \\ \\###|###/ /   /'  + '\n'
                s += '    \\  /   ~~~~~   \\  /'    + '\n'
                s += msg + '\n'
            
            else:
                s = ''
                if log_entry['last_line_type'] == LINE_TYPE_PLAIN_MSG:
                    # This is added to separate the normal logs from plain logs 
                    s += '\n\n'
                
                s += now_ts + ' [' + LOG_LEVELS[log_level] + '] ' +  tag + ': ' + msg + '\n' 
            
            
            log_entry['last_line_type'] = LINE_TYPE_NORMAL_MSG
            
        else:
            s = msg
            
            log_entry['last_line_type'] = LINE_TYPE_PLAIN_MSG
            
        
        if os.path.isfile(abspath) == False:
            with io.open(abspath,'w',encoding='utf8') as f:
                f.write(s)
        else:
            with io.open(abspath,'a',encoding='utf8') as f:
                f.write(s)

