# report/formatters/f_pdf.py
import os
from datetime           import datetime, timedelta
from weasyprint         import HTML, CSS
from jinja2             import Environment, FileSystemLoader


from common_fast_api    import get_application_data  


class F_PDF:
    """PDF formatter for reports"""
    
    def __init__(self, template_dir=None):
        if template_dir is None:
            webroot = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            self.template_dir = os.path.join(webroot, 'templates_report')
        else:
            self.template_dir = template_dir
        
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_dir)
        )
        
        # Add custom filters
        self.jinja_env.filters['format_date'] = self._format_date
        self.jinja_env.filters['string_to_date'] = self._string_to_date
    
    
    def _format_date(self, date_string):
        """Format date from YYYY-MM-DD to DD MMM YYYY"""
        if not date_string:
            return ''
        try:
            dt = datetime.strptime(date_string, '%Y-%m-%d')
            return dt.strftime('%d %b %Y').upper()
        except:
            return date_string
    
    
    def _string_to_date(self, date_string):
        """Convert string to date object for calculations"""
        if not date_string:
            return None
        try:
            return datetime.strptime(date_string, '%Y-%m-%d')
        except:
            return None
    
    
    def _calculate_days_since_birth(self, birth_date, acc_settings_ops):
        """Calculate days since birth based on account settings"""
        if not birth_date:
            return 0
        try:
            dt_birth = datetime.strptime(birth_date, '%Y-%m-%d')
            dt_now = datetime.now()
            diff_days = (dt_now - dt_birth).days
            
            if acc_settings_ops and acc_settings_ops.get('day_1_on_date_of_birth', 0) == 1:
                diff_days += 1
            
            return diff_days
        except:
            return 0
    
    
    def _calculate_expected_wean_date(self, birth_date, acc_settings_ops):
        """Calculate expected weaning date based on birth date and account settings"""
        if not birth_date:
            return None
        
        try:
            dt_birth = datetime.strptime(birth_date, '%Y-%m-%d')
            num_days_wean = acc_settings_ops.get('num_days_wean', 42) if acc_settings_ops else 42
            
            if acc_settings_ops and acc_settings_ops.get('day_1_on_date_of_birth', 0) == 1:
                num_days_wean -= 1
            
            dt_wean = dt_birth + timedelta(days=num_days_wean)
            return dt_wean.strftime('%Y-%m-%d')
        except:
            return None
    
    
    def _get_boar_display(self, sow):
        """Get formatted boar/semen display string."""
        insem_type = sow['insemination']['insem_type']
        
        if insem_type == 'B':
            boar = sow['insemination']['boar']
            if boar and boar.get('name'):
                return boar['name']
            elif boar and boar.get('number'):
                return boar['number']
            return "Unknown Boar"
        
        elif insem_type == 'AI_X':
            ai = sow['insemination']['ai']
            if ai and ai.get('semen_supplier') and ai['semen_supplier'].get('semen'):
                semen_name = ai['semen_supplier']['semen']['name']
                supplier_name = ai['semen_supplier'].get('name', '')
                if supplier_name:
                    return f"{semen_name} (from {supplier_name})"
                return semen_name
            return "External AI"
        
        elif insem_type == 'AI_N':
            ai = sow['insemination']['ai']
            if ai and ai.get('internal_boar'):
                internal_boar = ai['internal_boar']
                if internal_boar.get('name'):
                    return f"{internal_boar['name']} (Internal AI)"
                elif internal_boar.get('number'):
                    return f"{internal_boar['number']} (Internal AI)"
            return "Internal AI"
        
        return "Unknown"
    
    
    def generate_pig_farm_summary_report(self, context):
        """Generate complete pig farm summary report PDF."""
        
        # Add generated date and today's date
        context['generated_date'] = datetime.now()
        today = datetime.now()
        context['today_date'] = today.strftime('%Y-%m-%d')
        context['today_date_obj'] = today
        
        # Add application data for footer
        context['app_data'] = get_application_data()
        
        # Get account settings
        acc_settings_ops = context.get('acc_settings_ops', {})
        
        # Process gestating operations - preserve order from database
        gestating_ops_template = []
        if context.get('list_gestating'):
            first_sow = context['list_gestating'][0]
            for op in first_sow.get('gestating_ops', []):
                gestating_ops_template.append({
                    'id': op['account_pig_ops']['id'],
                    'name': op['account_pig_ops']['name']
                })
        context['gestating_operations'] = gestating_ops_template
        
        # Add boar display for each gestating sow
        for sow in context.get('list_gestating', []):
            sow['boar_display'] = self._get_boar_display(sow)
        
        # Process lactating operations - preserve order from database
        lactating_ops_template = []
        if context.get('list_lactating'):
            first_sow = context['list_lactating'][0]
            for op in first_sow.get('lactating_ops', []):
                op_type = op.get('pig_prod_pig_ops', {}).get('operation_type', 0)
                lactating_ops_template.append({
                    'id': op['account_pig_ops']['id'],
                    'name': op['account_pig_ops']['name'],
                    'operation_type': op_type
                })
        context['lactating_operations'] = lactating_ops_template
        
        # Calculate for lactating sows
        for sow in context.get('list_lactating', []):
            birth_date = sow.get('birth', {}).get('date_actual')
            
            # Calculate days since birth
            sow['days_since_birth'] = self._calculate_days_since_birth(birth_date, acc_settings_ops)
            
            # Get birth date formatted
            if birth_date:
                dt_birth = datetime.strptime(birth_date, '%Y-%m-%d')
                sow['birth_display'] = f"{dt_birth.strftime('%d %b %Y').upper()} (Day {sow['days_since_birth']})"
            else:
                sow['birth_display'] = ''
            
            # Calculate expected wean date
            sow['expected_wean_date'] = self._calculate_expected_wean_date(birth_date, acc_settings_ops)
            if sow['expected_wean_date']:
                dt_wean = datetime.strptime(sow['expected_wean_date'], '%Y-%m-%d')
                sow['expected_wean_display'] = dt_wean.strftime('%d %b %Y').upper()
            else:
                sow['expected_wean_display'] = ''
        
        # Render HTML
        template = self.jinja_env.get_template('pig_farm_summary_report.html')
        html = template.render(**context)
        
        # Save debug HTML
        debug_path = os.path.join(self.template_dir, 'debug_output.html')
        with open(debug_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Generate PDF
        css_path = os.path.join(self.template_dir, 'css', 'report.css')
        if os.path.exists(css_path):
            css = CSS(filename=css_path)
            return HTML(string=html).write_pdf(stylesheets=[css])
        else:
            return HTML(string=html).write_pdf()
