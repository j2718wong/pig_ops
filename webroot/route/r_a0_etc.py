# August 24, 2025
# Jack Wong

import os
import sys
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse, PlainTextResponse, Response


from datetime               import datetime, timedelta, date

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


@app.get("/robots.txt", response_class=PlainTextResponse, include_in_schema=False)
async def robots_txt():
    """Serve robots.txt"""
    content = """User-agent: *
Disallow: 

Sitemap: https://superpig.jsysdev.com/sitemap.xml
"""
    return PlainTextResponse(content=content)



@app.get("/sitemap.xml", response_class=Response, include_in_schema=False)
async def sitemap():
    """Generate sitemap.xml dynamically"""
    
    pages = [
        {"loc": "https://superpig.jsysdev.com/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "https://superpig.jsysdev.com/login", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "https://superpig.jsysdev.com/signup", "priority": "0.8", "changefreq": "monthly"},
        
        {"loc": "https://superpig.jsysdev.com/terms", "priority": "0.5", "changefreq": "yearly"},
        {"loc": "https://superpig.jsysdev.com/privacy", "priority": "0.5", "changefreq": "yearly"}
    ]
    
    """
    ,
        {"loc": "https://superpig.jsysdev.com/docs", "priority": "0.7", "changefreq": "weekly"},
        {"loc": "https://superpig.jsysdev.com/about", "priority": "0.5", "changefreq": "monthly"},
    """
    
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += "  <url>\n"
        xml += f"    <loc>{page['loc']}</loc>\n"
        xml += f"    <lastmod>{date.today().isoformat()}</lastmod>\n"
        xml += f"    <changefreq>{page['changefreq']}</changefreq>\n"
        xml += f"    <priority>{page['priority']}</priority>\n"
        xml += "  </url>\n"
    
    xml += '</urlset>'
    
    return Response(content=xml, media_type="application/xml")
    
    
    
@app.get("/privacy", response_class = HTMLResponse, dependencies=[Depends(public_limit)])
async def privacy(response: Response):
    
    page = controller.view['privacy'].render()
    
    return page


@app.get("/terms", response_class = HTMLResponse, dependencies=[Depends(public_limit)])
async def term(response: Response):
    
    page = controller.view['terms'].render()
    
    return page


@app.get("/contact", response_class = HTMLResponse, dependencies=[Depends(public_limit)])
async def term(response: Response):
    
    page = controller.view['contact'].render()
    
    return page


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "port": int(os.getenv('PORT_WEB', '8080'))
    }

