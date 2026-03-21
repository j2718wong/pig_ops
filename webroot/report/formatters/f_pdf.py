# report/formatters/f_pdf.py
import os
from datetime import datetime
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader


from common_fast_api import get_application_data  # Import the function


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
    
    def _format_date(self, date_string):
        """Format date from YYYY-MM-DD to DD MMM YYYY"""
        if not date_string:
            return ''
        try:
            dt = datetime.strptime(date_string, '%Y-%m-%d')
            return dt.strftime('%d %b %Y').upper()
        except:
            return date_string
    


    def generate_pig_farm_summary_report(self, context):
        """
        Generate gestating sows report PDF.
        """
        # IMPORTANT: Add generated_date to context FIRST
        context['generated_date'] = datetime.now()
        context['today_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Add application data for footer
        context['app_data'] = get_application_data()
        
        # Process gestating operations to get unique column headers
        gestating_ops = {}
        for sow in context.get('list_gestating', []):
            for op in sow.get('gestating_ops', []):
                op_id = op['account_pig_ops']['id']
                if op_id not in gestating_ops:
                    gestating_ops[op_id] = {
                        'id': op_id,
                        'name': op['account_pig_ops']['name']
                    }
        
        # Sort operations by ID to maintain consistent order
        context['gestating_operations'] = sorted(gestating_ops.values(), key=lambda x: x['id'])
        
        # Add boar display for each sow
        for sow in context.get('list_gestating', []):
            sow['boar_display'] = self._get_boar_display(sow)
        
        # Now render the template
        template = self.jinja_env.get_template('pig_farm_summary_report.html')
        html = template.render(**context)
        
        # Debug: Save HTML to file
        debug_path = os.path.join(self.template_dir, 'debug_output.html')
        with open(debug_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"DEBUG: HTML saved to {debug_path}")
        
        # Load CSS if exists
        css_path = os.path.join(self.template_dir, 'css', 'report.css')
        
        if os.path.exists(css_path):
            css = CSS(filename=css_path)
            return HTML(string=html).write_pdf(stylesheets=[css])
        else:
            return HTML(string=html).write_pdf()            
                    
        
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
