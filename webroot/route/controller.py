# November 27, 2025
# Jack Wong (zhaoshan99@gmail.com)

import os
import sys
import json
import pprint

from datetime               import datetime, timedelta


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)
webroot_directory           = os.path.dirname(module_directory)


# Add route directory to Python path
locale_dir = os.path.join(webroot_directory, 'locale')
if locale_dir not in sys.path:
    sys.path.insert(0, locale_dir)


from common_constants       import *

TRANSLATED_LANGUAGES = [
    {'key': 'en',       'lang_input': ['default', 'en', 'english']},

    {'key': 'ph-bis',   'lang_input': ['ph-bis', 'bis', 'bisaya', 'ceb']},
    {'key': 'ph-tag',   'lang_input': ['ph-tag', 'tag', 'tagalog']}

]



class Controller:
    
    def __init__(self, logger = None, model = None):
        self.TAG                = 'Controller'

        self.APP_VERSION        = ''
        
        self.is_prod_envi       = False
        
        self.use_minified_js    = 1
        
        self.logger             = logger
        
        self.model              = model
        
        
        self.view               = None
        

        self.translations       = {}
        
        self.load_translations()

        
    def load_translations(self):
        
        # Load Bisaya
        abspath_ph_bis = os.path.join(locale_dir, 'locale_bisaya.json')

        f = open(abspath_ph_bis, 'r', encoding='utf-8')
        s = f.read();
        f.close();
        
        translation = None
        try:
            translation = json.loads(s)
        except Exception as e:
            print('Error Loading translation: ' + str(e))

        
        if translation is not None:
            self.translations['ph-bis'] = translation

    
    def get_language_key(self, input_lang):
        """
        Convert user input language (e.g., 'bis', 'bisaya', 'en') to internal language key
        Returns the language key or None if not found
        """
        if input_lang is None:
            return None
            
        input_lang_lower = input_lang.lower().strip()
        
        # Loop through TRANSLATED_LANGUAGES to find matching input
        for lang_entry in TRANSLATED_LANGUAGES:
            for lang_input in lang_entry['lang_input']:
                if lang_input == input_lang_lower:
                    return lang_entry['key']
        
        return None


    
    def get_translation(self, language_key):
        """
        Returns the translation dictionary for the given language key
        Returns None if no translation exists (use default English from frontend)
        """
        if language_key is None:
            return None
            
        
        # Check if translation exists for this language key
        if language_key in self.translations:
            return self.translations[language_key]
        
        # No translation found - frontend will use default English
        return None
    


    def set_view(self, view):
        self.view = view
        

    def get_directory_where_to_save_report_file(self, pig_farm_id, 
        report_type_id, report_date):
        """
        1.) The reports directory should be saved in ~/projects/jsys/pig_ops/webroot/data/user/reports

        2.) The reports directory should be organized by pig_farm_id; example 
        ..webroot/data/user/reports/0001

        where 1 is the pig_farm_id

        3.) The subdirectory structure is further organized into year month folder

        ..webroot/data/user/reports/0001/202603

        where 202603 is the year month taken from report_date

        Returns:
            str: Full path to the directory where report should be saved
            None: If directory creation fails
        """
        try:
            # Base reports directory
            reports_base_dir = os.path.join(webroot_directory, 'data', 'user', 'reports')
            
            # Create base directory if it doesn't exist
            if not os.path.exists(reports_base_dir):
                os.makedirs(reports_base_dir, exist_ok=True)
            
            # Farm ID directory (padded to 4 digits)
            farm_dir = f"{pig_farm_id:04d}"
            farm_path = os.path.join(reports_base_dir, farm_dir)
            
            if not os.path.exists(farm_path):
                os.makedirs(farm_path, exist_ok=True)
            
            # Year-month directory from report_date
            if isinstance(report_date, str):
                dt_report = datetime.strptime(report_date, '%Y-%m-%d')
            elif isinstance(report_date, datetime):
                dt_report = report_date
            else:
                # If report_date is not a date object, use current date
                dt_report = datetime.now()
            
            year_month = dt_report.strftime('%Y%m')
            year_month_path = os.path.join(farm_path, year_month)
            
            if not os.path.exists(year_month_path):
                os.makedirs(year_month_path, exist_ok=True)
            
            return year_month_path
            
        except Exception as e:
            if self.logger:
                self.logger.append(
                    log_level= LOG_ERROR,
                    tag=self.TAG,
                    msg=f'Error creating report directory: {e}'
                )
            return None

    
    def save_report_file(self, pdf_bytes, pig_farm_id, report_type_id, 
        report_date, report_name):
        """
        Will save a pdf_bytes to a file.

        Parameters:
        ==========
        pdf_bytes : bytes
            The PDF content to save
        pig_farm_id : int
            The farm ID
        report_type_id : int
            Type of report (1=summary, 2=gestating, etc.)
        report_date : str or datetime
            The date of the report (used for folder structure)
        report_name : str
            The name of the report file (without extension)

        Returns: str
            relative path of the file starting from data/...
            returns None if not saved
        """
        try:
            # Get the directory to save the report
            save_dir = self.get_directory_where_to_save_report_file(
                pig_farm_id, report_type_id, report_date
            )
            
            if save_dir is None:
                return None
            
            # Use CURRENT TIME for timestamp, not report_date
            # This ensures unique filenames and shows actual generation time
            current_time = datetime.now()
            timestamp = current_time.strftime('%Y%m%d_%H%M%S')
                
            # Format: report_name_20260330_143022.pdf
            filename = f"{report_name}_{timestamp}.pdf"
            
            


            # Full file path
            file_path = os.path.join(save_dir, filename)
            
            print('tosave = ' + str(file_path))

            # Save the PDF bytes
            with open(file_path, 'wb') as f:
                f.write(pdf_bytes)
            
            # Get relative path from webroot/data
            # Convert to relative path starting from data/...
            relative_path = os.path.relpath(file_path, os.path.join(webroot_directory, 'data'))
            
            return relative_path
            
        except Exception as e:
            if self.logger:
                self.logger.append(
                    log_level=LOG_ERROR,
                    tag=self.TAG,
                    msg=f'Error saving report: {e}'
                )
            return None

    
    def save_report_with_auto_name(self, pdf_bytes, pig_farm_id, report_type_id, 
        report_date):
        """
        Saves report with auto-generated name based on report type.

        Parameters:
        ==========
        pdf_bytes : bytes
            The PDF content to save
        pig_farm_id : int
            The farm ID
        report_type_id : int
            Type of report (1=summary, 2=gestating, etc.)
        report_date : str or datetime
            The date of the report

        Returns: str
            relative path of the file starting from data/...
            returns None if not saved
        """
        # Get report type name
        report_type_name = REPORT_TYPES.get(report_type_id, 'report')
        
        # Generate farm name (you may want to fetch this from database)
        farm_name = f"farm_{pig_farm_id:04d}"
        
        # Generate report name
        report_name = f"{farm_name}_{report_type_name}"
        
        return self.save_report_file(
            pdf_bytes, 
            pig_farm_id, 
            report_type_id, 
            report_date, 
            report_name
        )
        
        
        
