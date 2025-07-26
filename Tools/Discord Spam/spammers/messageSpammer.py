import requests
from .assetsManager import *
from .color import color
from .tokenManager import add_token

def send_message(token : str , channelid : str , message : str , userAgent: str , proxies : str) -> None:
	"""It sends the message you want to the channel whose ID you entered."""
	headers = {"content-type": "application/json",	"authorization": token , "User-Agent" : userAgent}
	data = {"content": message, "tts": False}
	proxy_dict = {"http": proxies, "https": proxies}
	try:
		x = requests.post(f"https://discordapp.com/api/v7/channels/{channelid}/messages" , headers=headers , json=data, proxies=proxy_dict)
	except Exception as err:
		print(f"{color.RED}[-] ERROR: {color.RESET_ALL} {err}")
		return
	if x.status_code == 200:
		print(f"{color.GREEN}[+] Message sent successfully. {color.RESET_ALL}")
	else:
		print(f"{color.RED}[-] Message could not be sent. {color.RESET_ALL} {x.json()}")

def multi_token_message_spam(tokens: list, channelid: str, message: str, userAgents: list, proxies_list: list) -> dict:
	"""Отправляет сообщения от всех токенов в один канал с возможностью добавления токенов"""
	success_count = 0
	failed_count = 0
	
	print(f"{color.CYAN}[*] Starting multi-token message spam with {len(tokens)} tokens{color.RESET_ALL}")
	print(f"{color.YELLOW}[*] Type 'add' to add new token during spam{color.RESET_ALL}")
	print(f"{color.YELLOW}[*] Type 'skip' to skip current token{color.RESET_ALL}")
	print(f"{color.YELLOW}[*] Type 'quit' to stop spam{color.RESET_ALL}")
	
	for i, token in enumerate(tokens, 1):
		print(f"\n{color.BLUE}[Token {i}/{len(tokens)}]{color.RESET_ALL}")
		
		# Выбираем случайные userAgent и proxy для каждого токена
		userAgent = userAgents[i % len(userAgents)] if userAgents else ""
		proxy = proxies_list[i % len(proxies_list)] if proxies_list else ""
		
		# Проверяем команды пользователя
		user_input = input(f"{color.CYAN}[?] Press Enter to continue, 'add' to add token, 'skip' to skip, 'quit' to stop > {color.RESET_ALL}").lower().strip()
		
		if user_input == "quit":
			print(f"{color.YELLOW}[*] Spam stopped by user{color.RESET_ALL}")
			break
		elif user_input == "skip":
			print(f"{color.YELLOW}[*] Skipping token {i}{color.RESET_ALL}")
			continue
		elif user_input == "add":
			new_token = input(f"{color.YELLOW}[?] Enter new Discord token > {color.RESET_ALL}")
			if new_token.strip():
				if add_token(new_token.strip()):
					# Добавляем новый токен в текущий список
					tokens.append(new_token.strip())
					print(f"{color.GREEN}[+] Token added and will be used{color.RESET_ALL}")
				else:
					print(f"{color.RED}[-] Failed to add token{color.RESET_ALL}")
			else:
				print(f"{color.RED}[-] Token cannot be empty{color.RESET_ALL}")
		
		# Отправляем сообщение с текущим токеном
		headers = {"content-type": "application/json", "authorization": token, "User-Agent": userAgent}
		data = {"content": message, "tts": False}
		proxy_dict = {"http": proxy, "https": proxy}
		
		try:
			response = requests.post(
				f"https://discordapp.com/api/v7/channels/{channelid}/messages",
				headers=headers,
				json=data,
				proxies=proxy_dict
			)
			
			if response.status_code == 200:
				print(f"{color.GREEN}[+] Message sent successfully with token {i}{color.RESET_ALL}")
				success_count += 1
			else:
				print(f"{color.RED}[-] Failed to send message with token {i}: {response.status_code}{color.RESET_ALL}")
				failed_count += 1
				
		except Exception as err:
			print(f"{color.RED}[-] ERROR with token {i}: {err}{color.RESET_ALL}")
			failed_count += 1
	
	return {
		"success": success_count,
		"failed": failed_count,
		"total": len(tokens)
	}
