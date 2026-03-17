# March 17, 2026
# Jack Wong (zhaoshan99@gmail.com)

import os
import sys


class EmailTemplate:
    def __init__(self):
        self.company_name       = "JSysDev Limited"
        self.application_name   = "SuperPig"
        self.company_website    = "https://superpig.jsysdev.com"
        self.support_email      = "jsysdev.contact@gmail.com"
        self.company_address    = None  # Optional
        self.primary_color      = "#1e3a8a"  # Corporate Blue
        self.secondary_color    = "#693FE9"
        self.accent_color       = "#ff9800"  # Orange for warnings
        
        
    def get_footer(self) -> str:
        """Common footer for all emails"""
        return f"""
        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
        <p style="font-size: 12px; color: #999; text-align: center;">
            &copy; 2024 {self.company_name}. All rights reserved.<br>
            <a href="{self.company_website}" style="color: #999; text-decoration: none;">{self.company_website}</a>
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
    
    def __init__(self):
        super().__init__()
        # Override any company-specific settings if needed
        # self.primary_color = "#667eea"  # Different color for verification emails
        
        
    def get_email_body(self, verification_code: str, expiry_minutes: int) -> str:
        """
        Generate email verification body
        """
        # Format code for better readability (e.g., 123456 -> 123-456)
        formatted_code = f"{verification_code[:3]} {verification_code[3:]}" if len(str(verification_code)) == 6 else verification_code
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 500px; margin: 0 auto; padding: 20px;">
            {self.get_header("Email Verification")}
            
            <div style="background: {self.secondary_color}; padding: 30px; border-radius: 0 0 8px 8px; border: 1px solid #ddd;">
                <p style="font-size: 16px;">Thank you for signing up to {self.application_name}. Please use the code below to verify your email:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <div style="background: #fff; padding: 20px; border-radius: 8px; border: 2px dashed {self.primary_color}; font-size: 32px; font-weight: bold; letter-spacing: 8px; color: {self.primary_color}; font-family: monospace;">
                        {formatted_code}
                    </div>
                </div>
                
                <div style="background: #fff3e0; padding: 12px; border-left: 4px solid {self.accent_color}; margin: 20px 0;">
                    <p style="margin: 0; color: #333;">
                        ⏱️ This code expires in <strong>{expiry_minutes} minutes</strong>
                    </p>
                </div>
                
                <p style="font-size: 14px; color: #666; margin-top: 25px; text-align: center;">
                    If you didn't request this, please ignore this email or 
                    <a href="mailto:{self.support_email}" style="color: {self.primary_color}; text-decoration: none;">contact support</a>.
                </p>
                
                {self.get_footer()}
            </div>
        </body>
        </html>
        """
        
    
    def get_plain_text_body(self, verification_code: str, expiry_minutes: int) -> str:
        """
        Plain text version for email clients that don't support HTML
        """
        return f"""
{self.company_name.upper()} - EMAIL VERIFICATION
================================================

Thank you for signing up to {self.application_name}.

Your verification code: {verification_code}

This code expires in {expiry_minutes} minutes.

For security reasons, do not share this code with anyone.

If you didn't request this, please ignore this email.
Contact: {self.support_email}
Website: {self.company_website}
        """
    
    
    def get_email_subject(self) -> str:
        return f"Verify Your Email for {self.application_name}"



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
