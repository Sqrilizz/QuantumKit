#!/usr/bin/env python3
"""
QuantumKit v6.0 - Telegram Report
Advanced Telegram reporting and monitoring tool
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.utils.ui import (
        print_banner, print_header, print_separator, print_success, 
        print_error, print_warning, print_info, Spinner, ProgressBar, 
        Notification, confirm_action, create_table, animate_loading
    )
    from src.utils.logo import QuantumKitLogo
    NEW_UI_AVAILABLE = True
except ImportError:
    NEW_UI_AVAILABLE = False

# Always import colorama for fallback
from colorama import Fore, Back, Style, init
init(autoreset=True)

class TelegramReport:
    def __init__(self):
        self.sent_emails = 0
        self.failed_emails = 0
        self.start_time = None
        self.max_workers = 5
        self.delay_between_emails = 3
        self.is_running = False
        
        # Email configuration for Telegram support
        self.senders = {
            'janetsewell2018@hepatolimail.com': 'ystkfngdS!5198',
            'elaineparker1949@unconsmail.com': 'vprehbrpS!3083',
            'thomasjudge1923@soliedmail.com': 'ebftsbqoX!2211',
            'ernestcadet1968@inappreciatmail.com': 'xembpywyS!4446',
            'glmcfsfjvk@rambler.ru': '04804372Q5lml',
            'korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
            'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
            'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
            'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
            'aria.therese.svensson@mail.com': 'Zorro1ab',
            'taterbug@verizon.net': 'Holly1!',
            'ejbrickner@comcast.net': 'Pass1178',
            'teressapeart@cox.net': 'Quinton2329!',
            'liznees@verizon.net': 'Dancer008',
            'olajakubovich@mail.com': 'OlaKub2106OlaKub2106',
            'kcdg@charter.net': 'Jennifer3*',
            'bean_118@hotmail.com': 'Liverpool118!',
            'dsdhjas@mail.com': 'LONGHACH123',
            'robitwins@comcast.net': 'May241996',
            'wasina@live.com': 'Marlas21',
            'aruzhan.01@mail.com': '1234567!',
            'rob.tackett@live.com': 'metallic',
            'lindahallenbeck@verizon.net': 'Anakin@2014',
            'hlaw82@mail.com': 'Snoopy37$$',
            'paintmadman@comcast.net': 'mycat2200*',
            'prideandjoy@verizon.net': 'Ihatejen12',
            'sdgdfg56@mail.com': 'kenwood4201',
            'garrett.danelz@comcast.net': 'N11golfer!',
            'gillian_1211@hotmail.com': 'Gilloveu1211',
            'sunpit16@hotmail.com': 'Putter34!',
            'fdshelor@verizon.net': 'Masco123*',
            'yeags1@cox.net': 'Zoomom1965!',
            'amine002@usa.com': 'iScrRoXAei123',
            'bbarcelo16@cox.net': 'Bsb161089$$',
            'laliebert@hotmail.com': 'pirates2',
            'vallen285@comcast.net': 'Delft285!1!',
            'sierra12@email.com': 'tegen1111',
            'luanne.zapevalova@mail.com': 'FqWtJdZ5iN@',
            'kmay@windstream.net': 'Nascar98',
            'redbrick1@mail.com': 'Redbrick11',
            'ivv9ah7f@mail.com': 'K226nw8duwg',
            'erkobir@live.com': 'floydLAWTON019',
            'Misscarter@mail.com': 'ashtray19',
            'carlieruby10@cox.net': 'Lollypop789$',
            'blackops2013@mail.com': 'amason123566',
            'caroline_cullum@comcast.net': 'carter14',
            'dpb13@live.com': 'Ic&ynum13',
            'heirhunter@usa.com': 'Noguys@714',
            'sherri.edwards@verizon.net': 'Dreaming123#',
            'rami.rami1980@hotmail.com': 'ramirami1980',
            'jmsingleton2@comcast.net': '151728Jn$$',
            'aberancho@aol.com': '10diegguuss10',
            'dgidel@iowatelecom.net': 'Buster48',
            'gpopandopul@mail.com': 'GEORG62A',
            'bolgodonsk@mail.com': '012345678!',
            'colbycolb@cox.net': 'Signals@1',
            'nicrey4@comcast.net': 'Dabears54',
            'mordechai@mail.com': 'Mordechai',
            'inemrzoya@mail.com': 'rLS1elaUrLS1elaU',
            'tarabedford@comcast.net': 'Money4me',
            'mycockneedsit@mail.com': 'benjamin3',
            'saralaine@mail.com': 'sarlaine12!1',
            'jonb2006@verizon.net': '1969Camaro',
            'rjhssa1@verizon.net': 'Donna613*',
            'cameron.doug@charter.net': 'Jake2122$',
            'bridget.shappell@comcast.net': 'Brennan1',
            'rugs8@comcast.net': 'baseball46',
            'averyjacobs3@mail.com': '1960682644!',
            'lstefanick@hotmail.com': 'Luv2dance2',
            'bchavez123@mail.com': 'aadrianachavez',
            'lukejamesjones@mail.com': 'tinkerbell1',
            'emahoney123@comcast.net': 'Shieknmme3#',
            'mandy10.mcevoy@btinternet.com': 'Tr1plets3',
            'jet747@cox.net': 'Sadie@1234',
            'landsgascareservices@mail.com': 'Alisha25@',
            'samantha224@mail.com': 'Madden098!@',
            'kbhamil@wowway.com': 'Carol1940',
            'email@bjasper.com': 'Lhsnh4us123!',
            'biggsbrian@cox.net': 'Trains@2247Trains@2247',
            'dzzeblnd@aol.com': 'Geosgal@1',
            'jtrego@indy.rr.com': 'Jackwill14!',
            'chrisphonte.rj@comcast.net': 'Junior@3311',
            'tvwifiguy@comcast.net': 'Bill#0101',
            'defenestrador@mail.com': 'm0rb1d8ss',
            'glangley@gmx.com': 'ironhide',
            'charlotte2850@hotmail.com': 'kelalu2850'
        }
        
        # Telegram support addresses
        self.receivers = [
            'sms@telegram.org', 
            'dmca@telegram.org', 
            'abuse@telegram.org',
            'sticker@telegram.org', 
            'support@telegram.org'
        ]
        
        # Complaint templates for Telegram
        self.complaint_templates = {
            'account': {
                'spam': "Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя который отправляет много ненужных сообщений - СПАМ. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю.",
                'personal_data': "Здравствуйте, уважаемая поддержка, на вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                'trolling': "Здравствуйте, уважаемая поддержка телеграм. Я нашел пользователя который открыто выражается нецензурной лексикой и спамит в чатах. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                'session_reset': "Здравствуйте, уважаемая поддержка. Я случайно перешел по фишинговой ссылке и утерял доступ к своему аккаунту. Его юзернейм - {username}, его айди - {id}. Пожалуйста удалите аккаунт или обнулите сессии",
                'premium': "Добрый день поддержка Telegram! Аккаунт {username} {id} приобрёл премиум в вашем мессенджере чтобы рассылать спам-сообщения и обходить ограничения Telegram.Прошу проверить данную жалобу и принять меры!",
                'virtual_number': "Добрый день поддержка Telegram!Аккаунт {username} , {id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться.Прошу разберитесь с этим. Заранее спасибо!"
            },
            'channel': {
                'personal_data': "Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел канал, который распространяет личные данные невинных людей. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                'animal_abuse': "Здравствуйте, уважаемая поддержка телеграма. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                'child_content': "Здравствуйте, уважаемая поддержка телеграма. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                'doxxing_services': "Здравствуйте,уважаемый модератор телеграмм,хочу пожаловаться вам на канал,который продает услуги доксинга, сваттинга. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал."
            },
            'bot': {
                'god_eye': "Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота."
            }
        }

    def print_banner(self):
        """Print modern banner"""
        if NEW_UI_AVAILABLE:
            print_banner()
            print_header("Telegram Report v6.2")
            print_info("📱 Advanced Telegram Reporting Tool")
            print_separator()
        else:
            print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║                           TELEGRAM REPORT v6.2                              ║")
            print(f"{Fore.CYAN}║                      📱 ADVANCED TELEGRAM REPORTING TOOL 📱               ║")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def show_menu(self):
        """Show main menu with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("REPORTING OPTIONS")
            headers = ["Option", "Description", "Details"]
            menu_data = [
                ["1", "Account Reports", "Report user accounts for violations"],
                ["2", "Channel Reports", "Report channels for policy violations"],
                ["3", "Bot Reports", "Report bots for violations"],
                ["4", "Settings", "Configure reporting parameters"],
                ["5", "Statistics", "View reporting statistics"],
                ["0", "Exit", "Exit the application"]
            ]
            create_table(headers, menu_data, title="Main Menu")
        else:
            print(f"{Fore.CYAN}Main Menu:")
            print(f"{Fore.WHITE}1. Account Reports")
            print(f"{Fore.WHITE}2. Channel Reports") 
            print(f"{Fore.WHITE}3. Bot Reports")
            print(f"{Fore.WHITE}4. Settings")
            print(f"{Fore.WHITE}5. Statistics")
            print(f"{Fore.WHITE}0. Exit")

    def get_user_input(self, prompt, required=True):
        """Get user input with validation"""
        while True:
            if NEW_UI_AVAILABLE:
                user_input = input(f"{Fore.CYAN}[?] {prompt}: {Fore.WHITE}").strip()
            else:
                user_input = input(f"{Fore.CYAN}[?] {prompt}: {Fore.WHITE}").strip()
            
            if user_input or not required:
                return user_input
            else:
                if NEW_UI_AVAILABLE:
                    print_error("This field is required!")
                else:
                    print(f"{Fore.RED}[!] This field is required!")

    def send_email(self, receiver, sender_email, sender_password, subject, body):
        """Send email with error handling"""
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Determine SMTP server based on email domain
            if 'mail.ru' in sender_email:
                smtp_server = 'smtp.mail.ru'
                smtp_port = 587
            elif 'gmail.com' in sender_email:
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587
            elif 'hotmail.com' in sender_email or 'outlook.com' in sender_email:
                smtp_server = 'smtp-mail.outlook.com'
                smtp_port = 587
            elif 'yahoo.com' in sender_email:
                smtp_server = 'smtp.mail.yahoo.com'
                smtp_port = 587
            else:
                smtp_server = 'smtp.mail.ru'
                smtp_port = 587
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver, msg.as_string())
            server.quit()
            
            return True
        except Exception as e:
            if NEW_UI_AVAILABLE:
                print_error(f"Failed to send email from {sender_email}: {str(e)}")
            else:
                print(f"{Fore.RED}[!] Failed to send email from {sender_email}: {str(e)}")
            return False

    def send_complaint_batch(self, complaint_data):
        """Send a batch of complaints"""
        receiver, sender_email, sender_password, subject, body = complaint_data
        
        if self.send_email(receiver, sender_email, sender_password, subject, body):
            self.sent_emails += 1
            if NEW_UI_AVAILABLE:
                print_success(f"✓ Sent to {receiver} from {sender_email}")
            else:
                print(f"{Fore.GREEN}[+] Sent to {receiver} from {sender_email}")
        else:
            self.failed_emails += 1
        
        time.sleep(self.delay_between_emails)

    def report_account(self):
        """Handle account reporting"""
        if NEW_UI_AVAILABLE:
            print_header("ACCOUNT REPORTING")
            print_info("Select the type of violation to report:")
        else:
            print(f"\n{Fore.CYAN}=== ACCOUNT REPORTING ===")
        
        violation_types = {
            '1': ('spam', 'Spam'),
            '2': ('personal_data', 'Personal Data Violation'),
            '3': ('trolling', 'Trolling/Harassment'),
            '4': ('session_reset', 'Session Reset Request'),
            '5': ('premium', 'Premium Abuse'),
            '6': ('virtual_number', 'Virtual Number Usage')
        }
        
        if NEW_UI_AVAILABLE:
            headers = ["Option", "Violation Type"]
            violation_menu = [[k, v[1]] for k, v in violation_types.items()]
            create_table(headers, violation_menu, title="Violation Types")
        else:
            for key, (_, name) in violation_types.items():
                print(f"{Fore.WHITE}{key}. {name}")
        
        choice = self.get_user_input("Select violation type (1-6)")
        if choice not in violation_types:
            if NEW_UI_AVAILABLE:
                print_error("Invalid choice!")
            else:
                print(f"{Fore.RED}[!] Invalid choice!")
            return
        
        violation_type, violation_name = violation_types[choice]
        
        # Get account details
        username = self.get_user_input("@username")
        user_id = self.get_user_input("Telegram ID")
        
        if violation_type in ['spam', 'personal_data', 'trolling']:
            chat_link = self.get_user_input("Chat link")
            violation_link = self.get_user_input("Violation link")
            body = self.complaint_templates['account'][violation_type].format(
                username=username, id=user_id, chat_link=chat_link, violation_link=violation_link
            )
        else:
            body = self.complaint_templates['account'][violation_type].format(
                username=username, id=user_id
            )
        
        if NEW_UI_AVAILABLE:
            if not confirm_action(f"Start reporting {username} for {violation_name}?"):
                print_warning("Operation cancelled")
                return
        else:
            confirm = input(f"\n{Fore.YELLOW}[?] Start reporting {username} for {violation_name}? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print(f"{Fore.YELLOW}[!] Operation cancelled")
                return
        
        self.start_reporting('Account Report', body)

    def report_channel(self):
        """Handle channel reporting"""
        if NEW_UI_AVAILABLE:
            print_header("CHANNEL REPORTING")
            print_info("Select the type of violation to report:")
        else:
            print(f"\n{Fore.CYAN}=== CHANNEL REPORTING ===")
        
        violation_types = {
            '1': ('personal_data', 'Personal Data Violation'),
            '2': ('animal_abuse', 'Animal Abuse Content'),
            '3': ('child_content', 'Child Exploitation Content'),
            '4': ('doxxing_services', 'Doxxing/Swatting Services')
        }
        
        if NEW_UI_AVAILABLE:
            headers = ["Option", "Violation Type"]
            violation_menu = [[k, v[1]] for k, v in violation_types.items()]
            create_table(headers, violation_menu, title="Violation Types")
        else:
            for key, (_, name) in violation_types.items():
                print(f"{Fore.WHITE}{key}. {name}")
        
        choice = self.get_user_input("Select violation type (1-4)")
        if choice not in violation_types:
            if NEW_UI_AVAILABLE:
                print_error("Invalid choice!")
            else:
                print(f"{Fore.RED}[!] Invalid choice!")
            return
        
        violation_type, violation_name = violation_types[choice]
        
        channel_link = self.get_user_input("Channel link")
        violation_link = self.get_user_input("Violation link")
        
        body = self.complaint_templates['channel'][violation_type].format(
            channel_link=channel_link, channel_violation=violation_link
        )
        
        if NEW_UI_AVAILABLE:
            if not confirm_action(f"Start reporting channel for {violation_name}?"):
                print_warning("Operation cancelled")
                return
        else:
            confirm = input(f"\n{Fore.YELLOW}[?] Start reporting channel for {violation_name}? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print(f"{Fore.YELLOW}[!] Operation cancelled")
                return
        
        self.start_reporting('Channel Report', body)

    def report_bot(self):
        """Handle bot reporting"""
        if NEW_UI_AVAILABLE:
            print_header("BOT REPORTING")
            print_info("Select the type of violation to report:")
        else:
            print(f"\n{Fore.CYAN}=== BOT REPORTING ===")
        
        violation_types = {
            '1': ('god_eye', 'God Eye Bot (Personal Data Search)')
        }
        
        if NEW_UI_AVAILABLE:
            headers = ["Option", "Violation Type"]
            violation_menu = [[k, v[1]] for k, v in violation_types.items()]
            create_table(headers, violation_menu, title="Violation Types")
        else:
            for key, (_, name) in violation_types.items():
                print(f"{Fore.WHITE}{key}. {name}")
        
        choice = self.get_user_input("Select violation type (1)")
        if choice not in violation_types:
            if NEW_UI_AVAILABLE:
                print_error("Invalid choice!")
            else:
                print(f"{Fore.RED}[!] Invalid choice!")
            return
        
        violation_type, violation_name = violation_types[choice]
        bot_username = self.get_user_input("Bot @username")
        
        body = self.complaint_templates['bot'][violation_type].format(bot_user=bot_username)
        
        if NEW_UI_AVAILABLE:
            if not confirm_action(f"Start reporting bot {bot_username} for {violation_name}?"):
                print_warning("Operation cancelled")
                return
        else:
            confirm = input(f"\n{Fore.YELLOW}[?] Start reporting bot {bot_username} for {violation_name}? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print(f"{Fore.YELLOW}[!] Operation cancelled")
                return
        
        self.start_reporting('Bot Report', body)

    def start_reporting(self, report_type, body):
        """Start the reporting process with progress tracking"""
        self.sent_emails = 0
        self.failed_emails = 0
        self.start_time = time.time()
        self.is_running = True
        
        total_emails = len(self.senders) * len(self.receivers)
        
        if NEW_UI_AVAILABLE:
            print_header(f"STARTING {report_type.upper()}")
            print_info(f"Total emails to send: {total_emails}")
            print_info(f"Using {len(self.senders)} sender accounts")
            print_info(f"Targeting {len(self.receivers)} Telegram support addresses")
            print_separator()
            
            with Spinner("Preparing email batches..."):
                time.sleep(2)
            
            with ProgressBar(total_emails, "Sending reports") as progress:
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = []
                    
                    for sender_email, sender_password in self.senders.items():
                        for receiver in self.receivers:
                            complaint_data = (receiver, sender_email, sender_password, report_type, body)
                            future = executor.submit(self.send_complaint_batch, complaint_data)
                            futures.append(future)
                    
                    for future in futures:
                        future.result()
                        progress.update(1)
                        
                        if not self.is_running:
                            break
        else:
            print(f"\n{Fore.CYAN}=== STARTING {report_type.upper()} ===")
            print(f"{Fore.WHITE}Total emails to send: {total_emails}")
            print(f"{Fore.WHITE}Using {len(self.senders)} sender accounts")
            print(f"{Fore.WHITE}Targeting {len(self.receivers)} Telegram support addresses")
            print(f"{Fore.CYAN}{'='*60}\n")
            
            print(f"{Fore.YELLOW}[*] Preparing email batches...")
            time.sleep(2)
            
            current = 0
            for sender_email, sender_password in self.senders.items():
                for receiver in self.receivers:
                    if not self.is_running:
                        break
                    
                    complaint_data = (receiver, sender_email, sender_password, report_type, body)
                    self.send_complaint_batch(complaint_data)
                    current += 1
                    
                    # Progress indicator
                    progress = (current / total_emails) * 100
                    print(f"{Fore.CYAN}[*] Progress: {current}/{total_emails} ({progress:.1f}%)")
        
        self.is_running = False
        self.show_final_stats()

    def show_final_stats(self):
        """Show final reporting statistics"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            
            if NEW_UI_AVAILABLE:
                print_header("REPORTING COMPLETED")
                
                headers = ["Metric", "Value", "Status"]
                stats_data = [
                    ["Successful Reports", str(self.sent_emails), "green"],
                    ["Failed Reports", str(self.failed_emails), "red"],
                    ["Total Attempts", str(self.sent_emails + self.failed_emails), "white"],
                    ["Elapsed Time", f"{elapsed:.2f}s", "cyan"],
                    ["Success Rate", f"{(self.sent_emails/(self.sent_emails+self.failed_emails)*100):.1f}%", "yellow"]
                ]
                
                create_table(headers, stats_data, title="Final Statistics")
                
                if self.sent_emails > 0:
                    print_success("Reports sent successfully!")
                if self.failed_emails > 0:
                    print_warning(f"{self.failed_emails} reports failed to send")
            else:
                print(f"\n{Fore.CYAN}=== REPORTING COMPLETED ===")
                print(f"{Fore.GREEN}[+] Successful Reports: {self.sent_emails}")
                print(f"{Fore.RED}[!] Failed Reports: {self.failed_emails}")
                print(f"{Fore.WHITE}[*] Total Attempts: {self.sent_emails + self.failed_emails}")
                print(f"{Fore.CYAN}[*] Elapsed Time: {elapsed:.2f}s")
                print(f"{Fore.YELLOW}[*] Success Rate: {(self.sent_emails/(self.sent_emails+self.failed_emails)*100):.1f}%")

    def show_settings(self):
        """Show and modify settings"""
        if NEW_UI_AVAILABLE:
            print_header("SETTINGS")
            print_info("Current configuration:")
            
            headers = ["Setting", "Value", "Type"]
            settings_data = [
                ["Max Workers", str(self.max_workers), "cyan"],
                ["Delay Between Emails", f"{self.delay_between_emails}s", "cyan"],
                ["Sender Accounts", str(len(self.senders)), "white"],
                ["Target Addresses", str(len(self.receivers)), "white"]
            ]
            
            create_table(headers, settings_data, title="Current Settings")
            
            print_info("Modify settings:")
            print("1. Change max workers")
            print("2. Change delay between emails")
            print("3. Back to main menu")
        else:
            print(f"\n{Fore.CYAN}=== SETTINGS ===")
            print(f"{Fore.WHITE}Max Workers: {self.max_workers}")
            print(f"{Fore.WHITE}Delay Between Emails: {self.delay_between_emails}s")
            print(f"{Fore.WHITE}Sender Accounts: {len(self.senders)}")
            print(f"{Fore.WHITE}Target Addresses: {len(self.receivers)}")
            print(f"\n{Fore.CYAN}Modify settings:")
            print(f"{Fore.WHITE}1. Change max workers")
            print(f"{Fore.WHITE}2. Change delay between emails")
            print(f"{Fore.WHITE}3. Back to main menu")
        
        choice = self.get_user_input("Select option (1-3)")
        
        if choice == '1':
            new_workers = self.get_user_input("Enter new max workers (1-10)")
            try:
                workers = int(new_workers)
                if 1 <= workers <= 10:
                    self.max_workers = workers
                    if NEW_UI_AVAILABLE:
                        print_success(f"Max workers updated to {workers}")
                    else:
                        print(f"{Fore.GREEN}[+] Max workers updated to {workers}")
                else:
                    if NEW_UI_AVAILABLE:
                        print_error("Workers must be between 1 and 10")
                    else:
                        print(f"{Fore.RED}[!] Workers must be between 1 and 10")
            except ValueError:
                if NEW_UI_AVAILABLE:
                    print_error("Invalid number")
                else:
                    print(f"{Fore.RED}[!] Invalid number")
        
        elif choice == '2':
            new_delay = self.get_user_input("Enter new delay in seconds (1-10)")
            try:
                delay = int(new_delay)
                if 1 <= delay <= 10:
                    self.delay_between_emails = delay
                    if NEW_UI_AVAILABLE:
                        print_success(f"Delay updated to {delay}s")
                    else:
                        print(f"{Fore.GREEN}[+] Delay updated to {delay}s")
                else:
                    if NEW_UI_AVAILABLE:
                        print_error("Delay must be between 1 and 10 seconds")
                    else:
                        print(f"{Fore.RED}[!] Delay must be between 1 and 10 seconds")
            except ValueError:
                if NEW_UI_AVAILABLE:
                    print_error("Invalid number")
                else:
                    print(f"{Fore.RED}[!] Invalid number")

    def show_statistics(self):
        """Show current statistics"""
        if NEW_UI_AVAILABLE:
            print_header("STATISTICS")
            
            headers = ["Metric", "Value", "Status"]
            stats_data = [
                ["Total Sender Accounts", str(len(self.senders)), "white"],
                ["Target Support Addresses", str(len(self.receivers)), "white"],
                ["Max Possible Reports", str(len(self.senders) * len(self.receivers)), "cyan"],
                ["Last Session Sent", str(self.sent_emails), "green"],
                ["Last Session Failed", str(self.failed_emails), "red"]
            ]
            
            create_table(headers, stats_data, title="Current Statistics")
            
            if self.start_time:
                elapsed = time.time() - self.start_time
                print_info(f"Last session duration: {elapsed:.2f}s")
        else:
            print(f"\n{Fore.CYAN}=== STATISTICS ===")
            print(f"{Fore.WHITE}Total Sender Accounts: {len(self.senders)}")
            print(f"{Fore.WHITE}Target Support Addresses: {len(self.receivers)}")
            print(f"{Fore.WHITE}Max Possible Reports: {len(self.senders) * len(self.receivers)}")
            print(f"{Fore.GREEN}Last Session Sent: {self.sent_emails}")
            print(f"{Fore.RED}Last Session Failed: {self.failed_emails}")
            
            if self.start_time:
                elapsed = time.time() - self.start_time
                print(f"{Fore.CYAN}Last session duration: {elapsed:.2f}s")

    def run(self):
        """Main run method"""
        self.print_banner()
        
        while True:
            try:
                self.show_menu()
                choice = self.get_user_input("Select option")
                
                if choice == '1':
                    self.report_account()
                elif choice == '2':
                    self.report_channel()
                elif choice == '3':
                    self.report_bot()
                elif choice == '4':
                    self.show_settings()
                elif choice == '5':
                    self.show_statistics()
                elif choice == '0':
                    if NEW_UI_AVAILABLE:
                        print_success("Thank you for using Telegram Report!")
                    else:
                        print(f"{Fore.GREEN}[+] Thank you for using Telegram Report!")
                    break
                else:
                    if NEW_UI_AVAILABLE:
                        print_error("Invalid choice!")
                    else:
                        print(f"{Fore.RED}[!] Invalid choice!")
                
                if choice in ['1', '2', '3']:
                    input(f"\n{Fore.CYAN}Press Enter to continue...")
                
            except KeyboardInterrupt:
                if NEW_UI_AVAILABLE:
                    print_warning("\nOperation interrupted by user")
                else:
                    print(f"\n{Fore.YELLOW}[!] Operation interrupted by user")
                break
            except Exception as e:
                if NEW_UI_AVAILABLE:
                    print_error(f"An error occurred: {str(e)}")
                else:
                    print(f"{Fore.RED}[!] An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        reporter = TelegramReport()
        reporter.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Application interrupted by user")
    except Exception as e:
        print(f"{Fore.RED}[!] Application error: {str(e)}")
