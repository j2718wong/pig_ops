# March 21, 2026
# Jack Wong


from jinja2 import Environment, FileSystemLoader
import os

class ReportGenerator:
    def __init__(self):
        # Use reports subdirectory under templates
        template_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'templates', 'reports'
        )
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir)
        )
