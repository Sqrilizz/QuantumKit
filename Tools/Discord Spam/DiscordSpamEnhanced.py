import spammers as s
from spammers import color
import time

s.banner(text="")

print("""



1: Friend Request Sender
2: Guild Leaver
3: Message Sender (Single Channel)
4: Mass Message Spammer (All Channels) ⭐ NEW
5: Token Manager 🔧 NEW
6: Shows the help message.
7: Exit

""")

while True:
	_input = str(input(f"{color.YELLOW}[?] > {color.RESET_ALL}").lower())

	if _input == "1":
		userid = input(f"{color.YELLOW}[?] Enter the ID of the user you want to send a friend request to > {color.RESET_ALL}").lower()
		for tokens in s.tokens():
			s.friend_request(token = tokens , userid = userid , userAgent = s.userAgent() , proxies = s.proxies())
		print(f"{color.GREEN}The transaction is finished. {color.RESET_ALL}")

	elif _input == "2":
		guildid = input(f"{color.YELLOW}[?] Enter the ID of the server you want to leave > {color.RESET_ALL}").lower()
		for tokens in s.tokens():
			s.leave_guild(token = tokens , guildid=guildid , userAgent=s.userAgent() , proxies=s.proxies())
		print(f"{color.GREEN}The transaction is finished. {color.RESET_ALL}")

	elif _input == "3":
		channelid = input(f"{color.YELLOW}[?] Enter the ID of the channel you will message > {color.RESET_ALL}").lower()
		message = input(f"{color.YELLOW}[?] enter message > {color.RESET_ALL}").lower()
		
		# Получаем все токены
		tokens = s.tokens()
		if not tokens:
			print(f"{color.RED}[-] No tokens found in ./assets/tokens.txt{color.RESET_ALL}")
			continue
		
		# Получаем userAgents и proxies
		userAgents = []
		proxies_list = []
		
		try:
			with open("./assets/userAgents.txt", "r", encoding="utf-8") as f:
				userAgents = [line.strip() for line in f.readlines() if line.strip()]
		except:
			print(f"{color.YELLOW}[!] Could not load userAgents.txt{color.RESET_ALL}")
		
		try:
			with open("./assets/proxies.txt", "r", encoding="utf-8") as f:
				proxies_list = [line.strip() for line in f.readlines() if line.strip()]
		except:
			print(f"{color.YELLOW}[!] Could not load proxies.txt{color.RESET_ALL}")
		
		print(f"{color.GREEN}[+] Starting message spam with {len(tokens)} tokens{color.RESET_ALL}")
		print(f"{color.GREEN}[+] Message: {message}{color.RESET_ALL}")
		
		# Запускаем спам с возможностью добавления токенов
		result = s.multi_token_message_spam(tokens, channelid, message, userAgents, proxies_list)
		
		print(f"\n{color.GREEN}=== MESSAGE SPAM COMPLETED ==={color.RESET_ALL}")
		print(f"{color.GREEN}[+] Successfully sent: {result['success']}{color.RESET_ALL}")
		print(f"{color.RED}[-] Failed: {result['failed']}{color.RESET_ALL}")
		print(f"{color.CYAN}[*] Total tokens used: {result['total']}{color.RESET_ALL}")

	elif _input == "4":
		print(f"{color.CYAN}[*] Mass Message Spammer - Sends to ALL available channels{color.RESET_ALL}")
		message = input(f"{color.YELLOW}[?] Enter message to send to all channels > {color.RESET_ALL}")
		
		# Получаем все токены
		tokens = s.tokens()
		if not tokens:
			print(f"{color.RED}[-] No tokens found in ./assets/tokens.txt{color.RESET_ALL}")
			continue
		
		# Получаем userAgents и proxies
		userAgents = []
		proxies_list = []
		
		try:
			with open("./assets/userAgents.txt", "r", encoding="utf-8") as f:
				userAgents = [line.strip() for line in f.readlines() if line.strip()]
		except:
			print(f"{color.YELLOW}[!] Could not load userAgents.txt{color.RESET_ALL}")
		
		try:
			with open("./assets/proxies.txt", "r", encoding="utf-8") as f:
				proxies_list = [line.strip() for line in f.readlines() if line.strip()]
		except:
			print(f"{color.YELLOW}[!] Could not load proxies.txt{color.RESET_ALL}")
		
		print(f"{color.GREEN}[+] Starting mass spam with {len(tokens)} tokens{color.RESET_ALL}")
		print(f"{color.GREEN}[+] Message: {message}{color.RESET_ALL}")
		
		# Запускаем массовый спам
		result = s.multi_token_mass_spam(tokens, message, userAgents, proxies_list)
		
		print(f"\n{color.GREEN}=== MASS SPAM COMPLETED ==={color.RESET_ALL}")
		print(f"{color.GREEN}[+] Successfully sent: {result['success']}{color.RESET_ALL}")
		print(f"{color.RED}[-] Failed: {result['failed']}{color.RESET_ALL}")
		print(f"{color.CYAN}[*] Total channels found: {result['total_channels']}{color.RESET_ALL}")

	elif _input == "5":
		print(f"{color.CYAN}[*] Token Manager{color.RESET_ALL}")
		print("""
1: Add Token
2: Remove Token
3: Show All Tokens
4: Clear All Tokens
5: Back to Main Menu
		""")
		
		while True:
			token_input = str(input(f"{color.YELLOW}[Token Manager] > {color.RESET_ALL}").lower())
			
			if token_input == "1":
				token = input(f"{color.YELLOW}[?] Enter Discord bot token > {color.RESET_ALL}")
				if s.validate_token(token):
					s.add_token(token)
				else:
					print(f"{color.RED}[-] Invalid token format{color.RESET_ALL}")
			
			elif token_input == "2":
				s.show_tokens()
				token = input(f"{color.YELLOW}[?] Enter token to remove > {color.RESET_ALL}")
				s.remove_token(token)
			
			elif token_input == "3":
				s.show_tokens()
			
			elif token_input == "4":
				confirm = input(f"{color.RED}[!] Are you sure? (y/n) > {color.RESET_ALL}").lower()
				if confirm == "y":
					s.clear_all_tokens()
			
			elif token_input == "5":
				break
			
			else:
				print(f"{color.RED}[-] Invalid option{color.RESET_ALL}")

	elif _input == "6":
		print("Simply put the tokens in the ./assets/tokens.txt file.")
		print("For mass spam: Make sure your tokens have access to servers with channels.")
		print("Use Token Manager (option 5) to add/remove tokens easily.")

	elif _input == "7":
		quit()

	else:
		print(f"{color.RED}[-]Invalid options. {color.RESET_ALL}") 