import spammers as s
from spammers import color

s.banner(text="")

print("""



1: Friend Request Sender
2: Guild Leaver
3: Message Sender (Single Channel)
4: Mass Message Spammer (All Channels) ⭐ NEW
5: Simple Spammer (No Channel Check) 🚀 NEW
6: No Proxy Spammer (Direct Connection) ⚡ NEW
7: Token Manager 🔧 NEW
8: Shows the help message.
9: Exit

""")

while True:
	_input = str(input(f"{color.YELLOW}[?] > {color.RESET_ALL}").lower())

	if _input == "1":
		userid = input(f"{color.YELLOW}[?] Enter the ID of the user you want to send a friend request to > {color.RESET_ALL}").lower()
		for tokens in s.tokens():
			s.friend_request(token = tokens , userid = userid , userAgent = s.userAgent() , proxies = s.proxies())
		print(f"{color.GREEN}The transaction is finished. {color.RESET_ALL}")

	elif _input == "10000":
		print("Not working unless you have hCaptcha bypass")



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
		print(f"{color.CYAN}[*] Simple Spammer - No channel checking, direct spam{color.RESET_ALL}")
		print("""
1: Simple Single Channel Spam
2: Mass Simple Spam (Popular Channels)
3: Back to Main Menu
		""")
		
		while True:
			simple_input = str(input(f"{color.YELLOW}[Simple Spammer] > {color.RESET_ALL}").lower())
			
			if simple_input == "1":
				channelid = input(f"{color.YELLOW}[?] Enter channel ID to spam > {color.RESET_ALL}")
				message = input(f"{color.YELLOW}[?] Enter message to send > {color.RESET_ALL}")
				
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
				
				print(f"{color.GREEN}[+] Starting simple spam to channel {channelid}{color.RESET_ALL}")
				print(f"{color.GREEN}[+] Message: {message}{color.RESET_ALL}")
				
				# Запускаем простой спам
				result = s.multi_token_simple_spam(tokens, channelid, message, userAgents, proxies_list)
				
				print(f"\n{color.GREEN}=== SIMPLE SPAM COMPLETED ==={color.RESET_ALL}")
				print(f"{color.GREEN}[+] Successfully sent: {result['success']}{color.RESET_ALL}")
				print(f"{color.RED}[-] Failed: {result['failed']}{color.RESET_ALL}")
				print(f"{color.CYAN}[*] Total tokens used: {result['total']}{color.RESET_ALL}")
			
			elif simple_input == "2":
				message = input(f"{color.YELLOW}[?] Enter message to send to popular channels > {color.RESET_ALL}")
				
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
				
				print(f"{color.GREEN}[+] Starting mass simple spam{color.RESET_ALL}")
				print(f"{color.GREEN}[+] Message: {message}{color.RESET_ALL}")
				
				# Запускаем массовый простой спам
				result = s.mass_simple_spam(tokens, message, userAgents, proxies_list)
				
				print(f"\n{color.GREEN}=== MASS SIMPLE SPAM COMPLETED ==={color.RESET_ALL}")
				print(f"{color.GREEN}[+] Successfully sent: {result['success']}{color.RESET_ALL}")
				print(f"{color.RED}[-] Failed: {result['failed']}{color.RESET_ALL}")
				print(f"{color.CYAN}[*] Total attempts: {result['total_channels']}{color.RESET_ALL}")
			
			elif simple_input == "3":
				break
			
			else:
				print(f"{color.RED}[-] Invalid option{color.RESET_ALL}")

	elif _input == "6":
		print(f"{color.CYAN}[*] No Proxy Spammer - Direct connection without proxies{color.RESET_ALL}")
		print("""
1: No Proxy Single Channel Spam
2: No Proxy Mass Spam (Popular Channels)
3: Back to Main Menu
		""")
		
		while True:
			noproxy_input = str(input(f"{color.YELLOW}[No Proxy Spammer] > {color.RESET_ALL}").lower())
			
			if noproxy_input == "1":
				channelid = input(f"{color.YELLOW}[?] Enter channel ID to spam > {color.RESET_ALL}")
				message = input(f"{color.YELLOW}[?] Enter message to send > {color.RESET_ALL}")
				
				# Получаем все токены
				tokens = s.tokens()
				if not tokens:
					print(f"{color.RED}[-] No tokens found in ./assets/tokens.txt{color.RESET_ALL}")
					continue
				
				# Получаем userAgents
				userAgents = []
				
				try:
					with open("./assets/userAgents.txt", "r", encoding="utf-8") as f:
						userAgents = [line.strip() for line in f.readlines() if line.strip()]
				except:
					print(f"{color.YELLOW}[!] Could not load userAgents.txt{color.RESET_ALL}")
				
				print(f"{color.GREEN}[+] Starting no-proxy spam to channel {channelid}{color.RESET_ALL}")
				print(f"{color.GREEN}[+] Message: {message}{color.RESET_ALL}")
				
				# Запускаем спам без прокси
				result = s.multi_token_no_proxy_spam(tokens, channelid, message, userAgents)
				
				print(f"\n{color.GREEN}=== NO PROXY SPAM COMPLETED ==={color.RESET_ALL}")
				print(f"{color.GREEN}[+] Successfully sent: {result['success']}{color.RESET_ALL}")
				print(f"{color.RED}[-] Failed: {result['failed']}{color.RESET_ALL}")
				print(f"{color.CYAN}[*] Total tokens used: {result['total']}{color.RESET_ALL}")
			
			elif noproxy_input == "2":
				message = input(f"{color.YELLOW}[?] Enter message to send to popular channels > {color.RESET_ALL}")
				
				# Получаем все токены
				tokens = s.tokens()
				if not tokens:
					print(f"{color.RED}[-] No tokens found in ./assets/tokens.txt{color.RESET_ALL}")
					continue
				
				# Получаем userAgents
				userAgents = []
				
				try:
					with open("./assets/userAgents.txt", "r", encoding="utf-8") as f:
						userAgents = [line.strip() for line in f.readlines() if line.strip()]
				except:
					print(f"{color.YELLOW}[!] Could not load userAgents.txt{color.RESET_ALL}")
				
				print(f"{color.GREEN}[+] Starting mass no-proxy spam{color.RESET_ALL}")
				print(f"{color.GREEN}[+] Message: {message}{color.RESET_ALL}")
				
				# Запускаем массовый спам без прокси
				result = s.mass_no_proxy_spam(tokens, message, userAgents)
				
				print(f"\n{color.GREEN}=== MASS NO PROXY SPAM COMPLETED ==={color.RESET_ALL}")
				print(f"{color.GREEN}[+] Successfully sent: {result['success']}{color.RESET_ALL}")
				print(f"{color.RED}[-] Failed: {result['failed']}{color.RESET_ALL}")
				print(f"{color.CYAN}[*] Total attempts: {result['total_channels']}{color.RESET_ALL}")
			
			elif noproxy_input == "3":
				break
			
			else:
				print(f"{color.RED}[-] Invalid option{color.RESET_ALL}")

	elif _input == "7":
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
		print("Use Token Manager (option 7) to add/remove tokens easily.")
		print("Use Simple Spammer (option 5) if you have proxy issues.")
		print("Use No Proxy Spammer (option 6) for direct connection without proxies.")

	elif _input == "9":
		quit()

	else:
		print(f"{color.RED}[-]Invalid options. {color.RESET_ALL}")
