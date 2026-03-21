#!/usr/bin/env python3
# testing/test_pdf.py
# Test the PDF formatter with sample data

import os
import sys
from datetime import datetime

# Add paths
webroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, webroot)
sys.path.insert(0, os.path.join(webroot, 'report'))
sys.path.insert(0, os.path.join(webroot, 'report', 'formatters'))

from weasyprint import HTML
from formatters.f_pdf import F_PDF

def test_minimal_template():
    """Test with minimal template"""
    print("\n" + "=" * 60)
    print("Testing Minimal Template")
    print("=" * 60)
    
    # Use double braces {{ }} to escape CSS curly braces
    # Or use string concatenation to avoid formatting issues
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    minimal_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ 
            font-family: Arial; 
            margin: 40px; 
        }}
        h1 {{ 
            color: blue; 
        }}
    </style>
</head>
<body>
    <h1>Minimal Test</h1>
    <p>If you can see this, the PDF is working.</p>
    <p>Generated: {date_str}</p>
</body>
</html>
    """
    
    output_path = os.path.join(webroot, 'test_minimal.pdf')
    HTML(string=minimal_html).write_pdf(output_path)
    print(f"✓ Minimal PDF generated: {output_path}")
    if os.path.exists(output_path):
        print(f"  Size: {os.path.getsize(output_path)} bytes")
    else:
        print("  ✗ File not created!")

def test_simple_html():
    """Test simple HTML to PDF without template"""
    print("\n" + "=" * 60)
    print("Testing Simple HTML to PDF")
    print("=" * 60)
    
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Using f-string with double braces to escape CSS curly braces
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 40px; 
        }}
        h1 {{ 
            color: #1e3a8a; 
            border-bottom: 2px solid #1e3a8a; 
        }}
        table {{ 
            border-collapse: collapse; 
            width: 100%; 
            margin-top: 20px; 
        }}
        th, td {{ 
            border: 1px solid #ccc; 
            padding: 8px; 
            text-align: left; 
        }}
        th {{ 
            background-color: #1e3a8a; 
            color: white; 
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: gray;
        }}
    </style>
</head>
<body>
    <h1>Test PDF - Simple HTML</h1>
    <p>This is a test to verify WeasyPrint is working correctly.</p>
    <p>Generated on: {date_str}</p>
    <table>
        <thead>
            <tr><th>Test</th><th>Result</th></tr>
        </thead>
        <tbody>
            <tr><td>WeasyPrint</td><td>Working!</td></tr>
        </tbody>
    </table>
    <div class="footer">
        Pig Operations Management System
    </div>
</body>
</html>
    """
    
    output_path = os.path.join(webroot, 'test_simple.pdf')
    HTML(string=html).write_pdf(output_path)
    print(f"✓ Simple PDF generated: {output_path}")
    if os.path.exists(output_path):
        print(f"  Size: {os.path.getsize(output_path)} bytes")
    else:
        print("  ✗ File not created!")

def create_sample_data():
    """Create sample data that mimics your actual data structure"""
    
    # Sample gestating sows
    list_gestating = [
        {
            'pig_production': {'farm_prod_id': 28},
            'sow': {'name': 'Sheryl', 'number': None},
            'insemination': {
                'insem_type': 'B',
                'insem_date': '2025-11-20',
                'days_since_insem': 121,
                'boar': {'name': 'Bob', 'number': None},
                'ai': {}
            },
            'birth': {'date_expected': '2026-03-15'},
            'gestating_ops': [
                {
                    'account_pig_ops': {'id': 1, 'name': 'Check Reheat'},
                    'pig_prod_pig_ops': {
                        'date_target': '2025-12-11',
                        'date_actual': '2025-12-13'
                    }
                },
                {
                    'account_pig_ops': {'id': 2, 'name': 'Inject Iron'},
                    'pig_prod_pig_ops': {
                        'date_target': '2026-02-08',
                        'date_actual': '2026-02-10'
                    }
                },
                {
                    'account_pig_ops': {'id': 3, 'name': 'Deworm'},
                    'pig_prod_pig_ops': {
                        'date_target': '2026-02-28',
                        'date_actual': '2026-03-02'
                    }
                }
            ]
        },
        {
            'pig_production': {'farm_prod_id': 29},
            'sow': {'name': 'Jennifer', 'number': None},
            'insemination': {
                'insem_type': 'AI_X',
                'insem_date': '2026-01-14',
                'days_since_insem': 66,
                'boar': None,
                'ai': {
                    'semen_supplier': {
                        'name': 'Growbest Agrivet',
                        'semen': {'name': 'PIC 337'}
                    }
                }
            },
            'birth': {'date_expected': '2026-05-08'},
            'gestating_ops': [
                {
                    'account_pig_ops': {'id': 1, 'name': 'Check Reheat'},
                    'pig_prod_pig_ops': {
                        'date_target': '2026-02-04',
                        'date_actual': '2026-02-04'
                    }
                },
                {
                    'account_pig_ops': {'id': 2, 'name': 'Inject Iron'},
                    'pig_prod_pig_ops': {
                        'date_target': '2026-04-04',
                        'date_actual': None
                    }
                },
                {
                    'account_pig_ops': {'id': 3, 'name': 'Deworm'},
                    'pig_prod_pig_ops': {
                        'date_target': '2026-04-24',
                        'date_actual': None
                    }
                }
            ]
        },
        {
            'pig_production': {'farm_prod_id': 19},
            'sow': {'name': 'Tifanny', 'number': '1234'},
            'insemination': {
                'insem_type': 'B',
                'insem_date': '2026-01-18',
                'days_since_insem': 62,
                'boar': {'name': 'Charlie', 'number': None},
                'ai': {}
            },
            'birth': {'date_expected': '2026-05-12'},
            'gestating_ops': [
                {
                    'account_pig_ops': {'id': 1, 'name': 'Check Reheat'},
                    'pig_prod_pig_ops': {
                        'date_target': '2026-02-08',
                        'date_actual': '2026-02-08'
                    }
                },
                {
                    'account_pig_ops': {'id': 2, 'name': 'Inject Iron'},
                    'pig_prod_pig_ops': {
                        'date_target': '2026-04-08',
                        'date_actual': None
                    }
                },
                {
                    'account_pig_ops': {'id': 3, 'name': 'Deworm'},
                    'pig_prod_pig_ops': {
                        'date_target': '2026-04-28',
                        'date_actual': None
                    }
                }
            ]
        }
    ]
    
    # Create the full context
    context = {
        'pig_farm_info': {
            'pig_farm': {
                'id': 1,
                'name': 'Jackson Farm (Punod)',
                'address_level_1_id': 49,
                'address_level_2_id': 1013,
                'address_level_3_id': 27033
            },
            'account': {'id': 1, 'name': 'Jackson Farm'},
            'country': {'id': 1, 'name': 'Philippines'}
        },
        'farm_settings': {
            'report_title': 'Pig Farm Summary Report',
            'report_subtitle': 'Gestating Sows Section'
        },
        'list_gestating': list_gestating,
        'inc_historical': False,
        'inc_cost': False,
        'inc_target_harvest': False
    }
    
    return context

def test_pdf_formatter():
    """Test PDF generation with formatter"""
    print("\n" + "=" * 60)
    print("Testing PDF Formatter")
    print("=" * 60)
    
    # Create sample data
    print("\n1. Creating sample data...")
    context = create_sample_data()
    print(f"   - {len(context['list_gestating'])} gestating sows")
    
    # Initialize PDF formatter
    print("\n2. Initializing PDF formatter...")
    template_dir = os.path.join(webroot, 'templates_report')
    print(f"   - Template directory: {template_dir}")
    print(f"   - Directory exists: {os.path.exists(template_dir)}")
    
    # Check if template exists
    template_path = os.path.join(template_dir, 'pig_farm_summary_report.html')
    print(f"   - Template exists: {os.path.exists(template_path)}")
    
    if not os.path.exists(template_path):
        print("\n✗ ERROR: Template file not found!")
        print(f"   Create: {template_path}")
        return
    
    pdf_formatter = F_PDF(template_dir=template_dir)
    
    # Generate PDF
    print("\n3. Generating PDF...")
    try:
        pdf_bytes = pdf_formatter.generate_pig_farm_summary_report(context)
        
        # Save PDF
        output_path = os.path.join(webroot, 'test_report_output.pdf')
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"\n✓ PDF generated successfully!")
        print(f"  File: {output_path}")
        print(f"  Size: {len(pdf_bytes)} bytes")
        
    except Exception as e:
        print(f"\n✗ ERROR generating PDF: {e}")
        import traceback
        traceback.print_exc()

def test_simple_weasyprint():
    """Test the absolute simplest PDF"""
    print("\n" + "=" * 60)
    print("Testing Simplest WeasyPrint")
    print("=" * 60)
    
    # Simple HTML with no CSS formatting to avoid any issues
    simple_html = "<html><body><h1>Hello PDF</h1><p>This is a test.</p></body></html>"
    
    output_path = os.path.join(webroot, 'test_simplest.pdf')
    HTML(string=simple_html).write_pdf(output_path)
    print(f"✓ Simplest PDF generated: {output_path}")
    if os.path.exists(output_path):
        print(f"  Size: {os.path.getsize(output_path)} bytes")
    else:
        print("  ✗ File not created!")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PDF Formatter Test Suite")
    print("=" * 60)
    print(f"Webroot: {webroot}")
    
    # Test 0: Simplest possible (no CSS)
    test_simple_weasyprint()
    
    # Test 1: Minimal template
    test_minimal_template()
    
    # Test 2: Simple HTML with CSS
    test_simple_html()
    
    # Test 3: Full formatter with sample data
    test_pdf_formatter()
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print("\nGenerated PDFs:")
    print("  - test_simplest.pdf")
    print("  - test_minimal.pdf")
    print("  - test_simple.pdf")
    print("  - test_report_output.pdf")
