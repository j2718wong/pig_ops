# March 17, 2026
# Jack Wong (zhaoshan99@gmail.com)

import os
import sys

from datetime                   import  datetime


BG_PROCESS_NOTIFY_ACCOUNT_NOT_STARTED_TRIAL         = 1
BG_PROCESS_NOTIFY_USER_INCOMPLETE_ACCOUNT           = 2



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
                                        Please use the verification code below:
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


class EmailAccountNotStartedTrial(EmailTemplate):
    """
    Notify user that they have not started their free trial yet.
    Send reminder to add breeding pigs and start using the app.
    """
    
    def get_email_body(self, user_first_name: str, farm_name: str, notify_type_id: int = 1) -> str:
        """
        Generate email body for account not started trial notification
        """
        # Image URLs with version for cache busting
        dashboard_img = f"{self.company_website}/static_m/images/mar/mar_home.png"
        sow_list_img  = f"{self.company_website}/static_m/images/mar/mar_sow_list.png"
        gestating_img = f"{self.company_website}/static_m/images/mar/mar_gesta.png"
        farrowing_img = f"{self.company_website}/static_m/images/mar/mar_farrowing.png"
        
        html_acc_not_started = f"""
        <p style="color: {self.text_dark}; margin: 0 0 15px 0; font-size: 16px;">
            We noticed that your account for <strong>{farm_name}</strong> has not started using {self.application_name} yet.
            Feel free to explore by adding your breeding pigs and production entries.
        </p>
        """
        
        
        html_user_user_no_acc = f"""
        <p style="color: {self.text_dark}; margin: 0 0 15px 0; font-size: 16px;">
            We noticed that you have not completed creating your Pig Farm account for <b>{self.application_name}</b> yet.
            You can continue creating your account and start using {self.application_name}
            to check how it can help managing you pig farm.
        </p>
        
        <p style="font-size: 16px;">
            <a href="https://superpig.jsysdev.com/signup">Continue Create your Account </a>
        </p>
        """
        
        
        # Login Button HTML (added before images)
        login_button = f"""
        <div style="text-align: center; margin: 20px 0 30px 0;">
            <a href="{self.company_website}/login" style="
                background: {self.primary_color}; 
                color: white; 
                padding: 14px 32px; 
                text-decoration: none; 
                border-radius: 50px; 
                display: inline-block; 
                font-weight: bold; 
                font-size: 18px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                🔐 Login to SuperPig
            </a>
        </div>
        """
        
        html_message = ''
        
        
        html_message = ''
        
        if notify_type_id == BG_PROCESS_NOTIFY_ACCOUNT_NOT_STARTED_TRIAL:
            html_message = html_acc_not_started
        
        
        if notify_type_id == BG_PROCESS_NOTIFY_USER_INCOMPLETE_ACCOUNT:
            html_message = html_user_user_no_acc
        
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Start your free trial using {self.application_name}</title>
        </head>
        <body style="font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; line-height: 1.6; margin: 0; padding: 0; background: #f5f5f5;">
            <!-- Main container with white background -->
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #f5f5f5; padding: 10px;">
                <tr>
                    <td align="center">
                        <table width="100%" max-width="500px" cellpadding="0" cellspacing="0" border="0" style="background: {self.white}; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); max-width: 500px; width: 100%; border: 1px solid {self.border_color};">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background: {self.primary_color}; padding: 20px; text-align: center; border-radius: 12px 12px 0 0;">
                                    <h1 style="color: {self.white}; margin: 0; font-size: 24px; font-weight: 600;">{self.application_name}</h1>
                                </td>
                            </tr>
                            
                            <!-- White content area -->
                            <tr>
                                <td style="padding: 24px 20px; background: {self.white};">
                                    
                                    <h2 style="color: {self.text_dark}; margin: 0 0 10px 0; font-size: 22px; font-weight: 600;">
                                        Hello {user_first_name},
                                    </h2>
                                    
                                    {html_message}
                                    
                                    <p style="color: {self.text_dark}; margin: 0 0 20px 0; font-size: 16px;">
                                        Take a look at how {self.application_name} is used in managing and automating your pig production data.
                                    </p>
                                    
                                    
                                    <!-- LOGIN BUTTON - Added before images -->
                                    {login_button}
                                    
                                    
                                    <!-- Dashboard Preview -->
                                    <div style="margin: 25px 0;">
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; text-align: center;">
                                            <h3 style="color: {self.primary_color}; margin: 0 0 12px 0; font-size: 18px;">📱 Your Dashboard on Mobile</h3>
                                            <img src="{dashboard_img}" alt="SuperPig Dashboard" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid {self.border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                            <p style="color: {self.text_light}; margin: 12px 0 0 0; font-size: 13px;">Track your farm at a glance</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Sow List Preview -->
                                    <div style="margin: 25px 0;">
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; text-align: center;">
                                            <h3 style="color: {self.primary_color}; margin: 0 0 12px 0; font-size: 18px;">🐷 Sow List on Your Phone</h3>
                                            <img src="{sow_list_img}" alt="SuperPig Sow List" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid {self.border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                            <p style="color: {self.text_light}; margin: 12px 0 0 0; font-size: 13px;">View all your sows at a glance</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Gestating Info Preview -->
                                    <div style="margin: 25px 0;">
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; text-align: center;">
                                            <h3 style="color: {self.primary_color}; margin: 0 0 12px 0; font-size: 18px;">🤰 Gestating Info at a Glance</h3>
                                            <img src="{gestating_img}" alt="SuperPig Gestating Info" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid {self.border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                            <p style="color: {self.text_light}; margin: 12px 0 0 0; font-size: 13px;">Track pregnancy progress easily</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Farrowing Schedule Preview -->
                                    <div style="margin: 25px 0;">
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; text-align: center;">
                                            <h3 style="color: {self.primary_color}; margin: 0 0 12px 0; font-size: 18px;">🏠 Farrowing Schedule</h3>
                                            <img src="{farrowing_img}" alt="SuperPig Farrowing Schedule" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid {self.border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                            <p style="color: {self.text_light}; margin: 12px 0 0 0; font-size: 13px;">Automatically check if your crates are enough</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Feature List -->
                                    <div style="margin: 25px 0; background: #f0f7ff; padding: 15px; border-radius: 8px;">
                                        <p style="color: {self.text_dark}; margin: 0 0 10px 0; font-size: 15px; font-weight: bold;">
                                            ✨ And many more features:
                                        </p>
                                        <ul style="color: {self.text_dark}; margin: 0; padding-left: 20px; font-size: 14px;">
                                            <li style="margin: 8px 0;">📊 Track feed inventory and costs</li>
                                            <li style="margin: 8px 0;">💊 Manage medications and vaccinations</li>
                                            <li style="margin: 8px 0;">📈 Monitor harvest and sales data</li>
                                            <li style="margin: 8px 0;">👥 Share with farm staff</li>
                                        </ul>
                                    </div>
                                    
                                    <p style="color: {self.text_dark}; margin: 20px 0 10px 0; font-size: 16px;">
                                        All of these can be entered and viewed on your phone and shared with people connected to your farm.
                                        We also provided local translations so that it is easily for all people in your farm to follow.
                                    </p>
                                    
                                    <p style="color: {self.text_dark}; margin: 20px 0 10px 0; font-size: 16px;">
                                        <a href="{self.company_website}/signup" style="background: {self.primary_color}; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold;">
                                            Start Your Free Trial Now
                                        </a>
                                    </p>
                                    
                                    <p style="color: {self.text_light}; margin: 25px 0 0 0; font-size: 13px; text-align: center; border-top: 1px solid {self.border_color}; padding-top: 20px;">
                                        Need help? <a href="mailto:{self.support_email}" style="color: {self.primary_color}; text-decoration: underline;">Contact Support</a>
                                    </p>
                                    
                                </td>
                            </tr>
                            
                            <!-- Simple footer -->
                            <tr>
                                <td style="background: #f8f9fa; padding: 15px 20px; text-align: center; border-radius: 0 0 12px 12px; border-top: 1px solid {self.border_color};">
                                    <p style="color: {self.text_light}; margin: 0; font-size: 12px;">
                                        Happy Farming,<br>
                                        <strong>{self.application_name} Team</strong>
                                    </p>
                                    <p style="color: {self.text_light}; margin: 10px 0 0 0; font-size: 11px;">
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
    
    
    def get_plain_text_body(self, user_first_name: str, farm_name: str) -> str:
        """Plain text version for email clients that don't support HTML"""
        return f"""
============================================
{self.company_name} - {self.application_name}
============================================

Hello {user_first_name},

We noticed that your account for {farm_name} has not started using {self.application_name} yet.
Feel free to explore by adding your breeding pigs and production entries.

Take a look at how {self.application_name} is used in managing pig production data.

Visit our website to see screenshots:
{self.company_website}

Features include:
- Dashboard view of your farm
- Sow and boar management
- Gestating and farrowing tracking
- Feed inventory and costs
- Medication and vaccination records
- Harvest and sales data
- Share with farm staff

All of these can be entered and viewed on your phone and shared with people connected to your farm.

Start your free trial: {self.company_website}/signup

Need help? Contact us: {self.support_email}

Happy Farming,
{self.application_name} Team

--------------------------------------------
{self.company_website} | {self.support_email}
============================================
        """
    
    def get_email_subject(self, notify_type_id: int = 1) -> str:
        if notify_type_id == BG_PROCESS_NOTIFY_ACCOUNT_NOT_STARTED_TRIAL:
            return f"Start using {self.application_name} - Add your breeding pigs today"
        
        
        if notify_type_id == BG_PROCESS_NOTIFY_USER_INCOMPLETE_ACCOUNT:
            return f"Start using {self.application_name} - Create your Pig Farm Account"
        
        
        
        return ''


class EmailUserInstallApp(EmailTemplate):
    """
    Email to users who haven't installed the PWA app yet.
    Send instructions on how to install SuperPig as an app on their phone.
    """
    
    def get_email_body(self, user_first_name: str) -> str:
        """
        Generate email body for PWA installation notification
        """
        # Facebook Reel URL for installation instructions
        facebook_reel_url = "https://www.facebook.com/share/r/1FS2J15SBo/"
        
        # Image URLs with version for cache busting
        dashboard_img = f"{self.company_website}/static_m/images/mar/mar_home.png"
        sow_list_img  = f"{self.company_website}/static_m/images/mar/mar_sow_list.png"
        gestating_img = f"{self.company_website}/static_m/images/mar/mar_gesta.png"
        farrowing_img = f"{self.company_website}/static_m/images/mar/mar_farrowing.png"
        
        html_install_instructions = f"""
        <div style="margin: 20px 0; background: #f0f7ff; padding: 20px; border-radius: 12px;">
            <h3 style="color: {self.primary_color}; margin: 0 0 15px 0; font-size: 18px;">📱 How to Install SuperPig App</h3>
            
            <p style="color: {self.text_dark}; margin: 0 0 15px 0; font-size: 16px;">
                <strong>Option 1 - Quick Installation:</strong>
            </p>
            <ol style="color: {self.text_dark}; margin: 0 0 20px 0; padding-left: 20px; font-size: 15px;">
                <li style="margin: 8px 0;">Open <strong>jsysdev.com</strong> on your phone's browser (Chrome for Android or Safari for iPhone)</li>
                <li style="margin: 8px 0;">If you've logged in before, it should automatically open the dashboard</li>
                <li style="margin: 8px 0;">Look for the <strong>"Install SuperPig App"</strong> button at the bottom of the screen</li>
                <li style="margin: 8px 0;">Tap the button and follow the prompts to install</li>
            </ol>
            
            <p style="color: {self.text_dark}; margin: 0 0 15px 0; font-size: 16px;">
                <strong>Option 2 - Watch Video Tutorial:</strong>
            </p>
            <p style="color: {self.text_dark}; margin: 0 0 15px 0; font-size: 15px;">
                Watch this short video tutorial on how to install SuperPig on your phone:
            </p>
            
            <div style="text-align: center; margin: 20px 0;">
                <a href="{facebook_reel_url}" style="background: #1877f2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold;">
                    📺 Watch Installation Tutorial on Facebook
                </a>
            </div>
            
            <p style="color: {self.text_light}; margin: 15px 0 0 0; font-size: 13px; text-align: center;">
                Once installed, SuperPig will work like a native app on your phone!
            </p>
        </div>
        """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Install {self.application_name} App on Your Phone</title>
        </head>
        <body style="font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; line-height: 1.6; margin: 0; padding: 0; background: #f5f5f5;">
            <!-- Main container with white background -->
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #f5f5f5; padding: 10px;">
                <tr>
                    <td align="center">
                        <table width="100%" max-width="500px" cellpadding="0" cellspacing="0" border="0" style="background: {self.white}; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); max-width: 500px; width: 100%; border: 1px solid {self.border_color};">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background: {self.primary_color}; padding: 20px; text-align: center; border-radius: 12px 12px 0 0;">
                                    <h1 style="color: {self.white}; margin: 0; font-size: 24px; font-weight: 600;">{self.application_name}</h1>
                                 </td>
                            </tr>
                            
                            <!-- White content area -->
                            <tr>
                                <td style="padding: 24px 20px; background: {self.white};">
                                    
                                    <h2 style="color: {self.text_dark}; margin: 0 0 10px 0; font-size: 22px; font-weight: 600;">
                                        Hello {user_first_name},
                                    </h2>
                                    
                                    <p style="color: {self.text_dark}; margin: 0 0 20px 0; font-size: 16px;">
                                        You can install <strong>{self.application_name}</strong> as a standalone app on your phone for easier access and a better experience!
                                    </p>
                                    
                                    {html_install_instructions}
                                    
                                    <p style="color: {self.text_dark}; margin: 20px 0 20px 0; font-size: 16px;">
                                        Take a look at how {self.application_name} is used in managing and automating your pig production data.
                                    </p>
                                    
                                    <!-- Dashboard Preview -->
                                    <div style="margin: 25px 0;">
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; text-align: center;">
                                            <h3 style="color: {self.primary_color}; margin: 0 0 12px 0; font-size: 18px;">📱 Your Dashboard on Mobile</h3>
                                            <img src="{dashboard_img}" alt="SuperPig Dashboard" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid {self.border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                            <p style="color: {self.text_light}; margin: 12px 0 0 0; font-size: 13px;">Track your farm at a glance</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Sow List Preview -->
                                    <div style="margin: 25px 0;">
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; text-align: center;">
                                            <h3 style="color: {self.primary_color}; margin: 0 0 12px 0; font-size: 18px;">🐷 Sow List on Your Phone</h3>
                                            <img src="{sow_list_img}" alt="SuperPig Sow List" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid {self.border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                            <p style="color: {self.text_light}; margin: 12px 0 0 0; font-size: 13px;">View all your sows at a glance</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Gestating Info Preview -->
                                    <div style="margin: 25px 0;">
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; text-align: center;">
                                            <h3 style="color: {self.primary_color}; margin: 0 0 12px 0; font-size: 18px;">🤰 Gestating Info at a Glance</h3>
                                            <img src="{gestating_img}" alt="SuperPig Gestating Info" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid {self.border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                            <p style="color: {self.text_light}; margin: 12px 0 0 0; font-size: 13px;">Track pregnancy progress easily</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Farrowing Schedule Preview -->
                                    <div style="margin: 25px 0;">
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; text-align: center;">
                                            <h3 style="color: {self.primary_color}; margin: 0 0 12px 0; font-size: 18px;">🏠 Farrowing Schedule</h3>
                                            <img src="{farrowing_img}" alt="SuperPig Farrowing Schedule" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid {self.border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                            <p style="color: {self.text_light}; margin: 12px 0 0 0; font-size: 13px;">Automatically check if your crates are enough</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Feature List -->
                                    <div style="margin: 25px 0; background: #f0f7ff; padding: 15px; border-radius: 8px;">
                                        <p style="color: {self.text_dark}; margin: 0 0 10px 0; font-size: 15px; font-weight: bold;">
                                            ✨ And many more features:
                                        </p>
                                        <ul style="color: {self.text_dark}; margin: 0; padding-left: 20px; font-size: 14px;">
                                            <li style="margin: 8px 0;">📊 Track feed inventory and costs</li>
                                            <li style="margin: 8px 0;">💊 Manage medications and vaccinations</li>
                                            <li style="margin: 8px 0;">📈 Monitor harvest and sales data</li>
                                            <li style="margin: 8px 0;">👥 Share with farm staff</li>
                                        </ul>
                                    </div>
                                    
                                    <p style="color: {self.text_dark}; margin: 20px 0 10px 0; font-size: 16px;">
                                        All of these can be entered and viewed on your phone and shared with people connected to your farm.
                                        We also provided local translations so that it is easy for all people in your farm to follow.
                                    </p>
                                    
                                    <p style="color: {self.text_dark}; margin: 20px 0 10px 0; font-size: 16px;">
                                        <a href="{self.company_website}/signup" style="background: {self.primary_color}; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold;">
                                            Start Your Free Trial Now
                                        </a>
                                    </p>
                                    
                                    <p style="color: {self.text_light}; margin: 25px 0 0 0; font-size: 13px; text-align: center; border-top: 1px solid {self.border_color}; padding-top: 20px;">
                                        Need help? <a href="mailto:{self.support_email}" style="color: {self.primary_color}; text-decoration: underline;">Contact Support</a>
                                    </p>
                                    
                                 </td>
                            </tr>
                            
                            <!-- Simple footer -->
                            <tr>
                                <td style="background: #f8f9fa; padding: 15px 20px; text-align: center; border-radius: 0 0 12px 12px; border-top: 1px solid {self.border_color};">
                                    <p style="color: {self.text_light}; margin: 0; font-size: 12px;">
                                        Happy Farming,<br>
                                        <strong>{self.application_name} Team</strong>
                                    </p>
                                    <p style="color: {self.text_light}; margin: 10px 0 0 0; font-size: 11px;">
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
    
    def get_plain_text_body(self, user_first_name: str) -> str:
        """Plain text version for email clients that don't support HTML"""
        facebook_reel_url = "https://www.facebook.com/share/r/1FS2J15SBo/"
        
        return f"""
============================================
{self.company_name} - {self.application_name}
============================================

Hello {user_first_name},

You can install {self.application_name} as a standalone app on your phone for easier access!

How to install:

Option 1 - Quick Installation:
1. Open jsysdev.com on your phone's browser
2. If you've logged in before, it should automatically open the dashboard
3. Look for the "Install SuperPig App" button at the bottom of the screen
4. Tap the button and follow the prompts to install

Option 2 - Watch Video Tutorial:
Watch this short video on how to install SuperPig:
{facebook_reel_url}

Once installed, SuperPig will work like a native app on your phone!

Features include:
- Dashboard view of your farm
- Sow and boar management
- Gestating and farrowing tracking
- Feed inventory and costs
- Medication and vaccination records
- Harvest and sales data
- Share with farm staff

All of these can be entered and viewed on your phone and shared with people connected to your farm.

Start your free trial: {self.company_website}/signup

Need help? Contact us: {self.support_email}

Happy Farming,
{self.application_name} Team

--------------------------------------------
{self.company_website} | {self.support_email}
============================================
        """
    
    def get_email_subject(self) -> str:
        return f"📱 Install {self.application_name} App on Your Phone"


