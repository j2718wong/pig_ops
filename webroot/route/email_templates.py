# March 17, 2026
# Jack Wong (zhaoshan99@gmail.com)

import os
import sys

from datetime                   import  datetime


class EmailTemplate:
    def __init__(self):
        self.company_name       = "JSysDev Limited"
        self.application_name   = "SuperPig"
        self.company_website    = "https://superpig.jsysdev.com"
        self.support_email      = "jsysdev.contact@gmail.com"
        self.company_address    = None  # Optional
        
        self.primary_color      = "#1e3a8a"  # Corporate Blue
        
        self.text_dark          = "#333333"  # Dark gray for better readability
        self.text_light         = "#666666"  # Medium gray for secondary text
        self.border_color       = "#e0e0e0"  # Light gray for borders
        self.white              = "#ffffff"  # White background

        self.accent_color       = "#ff9800"  # Orange for warnings
        
        self.current_year       = datetime.now().year
        
        
    def get_footer(self) -> str:
        """Common footer for all emails"""
        
        
        
        return f"""
        <hr style="border: none; border-top: 1px solid {self.border_color}; margin: 20px 0;">
        <p style="font-size: 12px; color: {self.text_light}; text-align: center; margin: 0;">
            &copy; {self.current_year} {self.company_name}. All rights reserved.<br>
            <a href="{self.company_website}" style="color: {self.text_light}; text-decoration: underline;">{self.company_website}</a>
        </p>
        """

    
    def get_header(self, title: str) -> str:
        """Common header for all emails"""
        return f"""
        <div style="background: {self.primary_color}; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
            <h2 style="color: white; margin: 0;">{title}</h2>
        </div>
        """


class EmailVerificationCode(EmailTemplate):
    
    
    def get_email_body(self, verification_code: str, expiry_minutes: int) -> str:
        """
        Generate email verification body with white background for better visibility
        """
        formatted_code = verification_code
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify your email for {self.application_name}</title>
        </head>
        <body style="font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; line-height: 1.6; margin: 0; padding: 10px; background: #f5f5f5;">
            <!-- Main container with white background -->
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #f5f5f5; padding: 10px;">
                <tr>
                    <td align="center">
                        <table width="100%" max-width="500px" cellpadding="0" cellspacing="0" border="0" style="background: {self.white}; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); max-width: 500px; width: 100%; border: 1px solid {self.border_color};">
                            
                            <!-- Header with accent color only at top -->
                            <tr>
                                <td style="background: {self.primary_color}; padding: 20px; text-align: center; border-radius: 12px 12px 0 0;">
                                    <h1 style="color: {self.white}; margin: 0; font-size: 24px; font-weight: 600;">{self.application_name}</h1>
                                </td>
                            </tr>
                            
                            <!-- White content area -->
                            <tr>
                                <td style="padding: 10px 10px; background: {self.white};">
                                    
                                    <h2 style="color: {self.text_dark}; margin: 0 0 10px 0; font-size: 22px; font-weight: 600;">Verify Your Email</h2>
                                    
                                    <p style="color: {self.text_dark}; margin: 0 0 15px 0; font-size: 16px;">
                                        Thank you for signing up! Please use the verification code below:
                                    </p>
                                    
                                    <!-- Code box with light background -->
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 25px 0;">
                                        <tr>
                                            <td align="center" style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid {self.border_color};">
                                                <span style="font-size: 36px; font-weight: 700; letter-spacing: 8px; color: {self.primary_color}; font-family: 'Courier New', monospace;">
                                                    {formatted_code}
                                                </span>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Expiry notice -->
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 20px 0; background: #fff9e6; border-left: 4px solid #ffc107; padding: 12px 15px;">
                                        <tr>
                                            <td>
                                                <p style="color: {self.text_dark}; margin: 0; font-size: 14px;">
                                                    <strong>⏱️ Expires in:</strong> {expiry_minutes} minutes
                                                </p>
                                                <p style="color: {self.text_light}; margin: 5px 0 0 0; font-size: 13px;">
                                                    For security, never share this code with anyone.
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Footer note -->
                                    <p style="color: {self.text_light}; margin: 25px 0 0 0; font-size: 13px; text-align: center; border-top: 1px solid {self.border_color}; padding-top: 20px;">
                                        If you didn't request this code, please ignore this email.<br>
                                        Need help? <a href="mailto:{self.support_email}" style="color: {self.primary_color}; text-decoration: underline;">Contact Support</a>
                                    </p>
                                    
                                </td>
                            </tr>
                            
                            <!-- Simple footer -->
                            <tr>
                                <td style="background: #f8f9fa; padding: 15px 20px; text-align: center; border-radius: 0 0 12px 12px; border-top: 1px solid {self.border_color};">
                                    <p style="color: {self.text_light}; margin: 0; font-size: 12px;">
                                        &copy; {self.current_year} {self.company_name}. All rights reserved.<br>
                                        <a href="{self.company_website}" style="color: {self.text_light}; text-decoration: underline;">{self.company_website}</a>
                                    </p>
                                </td>
                            </tr>
                            
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    
    
    def get_plain_text_body(self, verification_code: str, expiry_minutes: int) -> str:
        """Plain text version for email clients that don't support HTML"""
        return f"""
============================================
{self.company_name} - Email Verification
============================================

Thank you for signing up!

Your verification code: {verification_code}

This code expires in {expiry_minutes} minutes.

For security, never share this code with anyone.

If you didn't request this code, please ignore this email.

--------------------------------------------
{self.company_website} | {self.support_email}
============================================
        """
    
    
    def get_email_subject(self) -> str:
        return f"Verify your email for {self.application_name}"


# Example: Creating a different company by extending EmailTemplate
class AnotherCompanyEmailTemplate(EmailTemplate):
    def __init__(self):
        super().__init__()
        self.company_name = "AnotherApp"
        self.company_website = "https://anotherapp.com"
        self.support_email = "help@anotherapp.com"
        self.primary_color = "#667eea"  # Purple
        self.accent_color = "#764ba2"   # Dark purple


# Now EmailVerificationCode will use the new company settings
class AnotherAppVerificationCode(AnotherCompanyEmailTemplate, EmailVerificationCode):
    def __init__(self):
        # Multiple inheritance - initialize both parents properly
        AnotherCompanyEmailTemplate.__init__(self)
        # No need to call EmailVerificationCode.__init__ as it just calls super()
    
    def get_email_subject(self) -> str:
        return f"Verify Your {self.company_name} Account"
