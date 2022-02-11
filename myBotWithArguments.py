import cloudscraper
import sys
from bs4 import BeautifulSoup
from ctypes import windll
from gc import collect
from loguru import logger
from names import get_first_name
from os import system
from random import choice, randint
from random_username.generate import generate_username
from requests import get
from sys import stderr
from threading import Thread
from time import sleep
from urllib3 import disable_warnings
from uuid import uuid4


disable_warnings()
system("cls")
def clear(): return system('cls')
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('LegionNetwork Auto Reger | by overgoodman&NAZAVOD')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")

refferalCode = sys.argv[1]
threads = int(sys.argv[2])
use_proxy = sys.argv[3]
if use_proxy in ('y', 'Y'):
   proxy_type = str(input('Укажите тип прокси (http/https/socks4/socks5): '))
   proxy_folder = str(input('Перетяните TXT файл с прокси, формат: (ip:port or user:pass@ip:port): '))

def take_proxy():
   with open(proxy_folder) as file:
      lines = file.readlines()
      proxy_str = choice(lines)
   return proxy_str

def mainth():
   while True:
      try:
         udid = str(uuid4())
         scraper = cloudscraper.create_scraper()
         if use_proxy in ('y', 'Y'):
            proxy_str = take_proxy()
            scraper.proxies.update({'http': f'{proxy_type}://{proxy_str}', 'https': f'{proxy_type}://{proxy_str}'})
         scraper.headers.update({'Content-Type': 'application/json', 'cf-visitor': 'https', 'User-Agent': 'Legion/5.2 CFNetwork/1209 Darwin/20.2.0', 'Connection': 'keep-alive', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru', 'x-forwarded-proto': 'https', 'Accept-Encoding': 'gzip, deflate, br'})

         username = generate_username()[0]+''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' if i != 5 else 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(5)])
         nameOfAcc = get_first_name()
         password = str(randint(0,9))+''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' if i != 25 else 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(25)])
         body = {"password":str(password)+"!","email":str(username)+"@xojxe.com","name":str(nameOfAcc),"udid":udid,"referralCode":str(refferalCode)}
         r = scraper.post('https://api.legionnetwork.io/api1/user/create', json = body)

         if r.status_code == 200:
            logger.info(f"Начало регистрации для {username}")

            logger.info(f'Ожидаю письмо для {username}')
            for i in range(100):
               r = get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain=xojxe.com")
               r_json = r.json()
               if len(r_json) > 0:
                  latest_mail = r_json[0].get('id')
                  req = get(f"https://www.1secmail.com/mailbox/?action=mailBody&id={latest_mail}&login={username}&domain=xojxe.com")
                  urlVerify = BeautifulSoup(req.text,'html').find_all("a", href=True)[1].get("href")
                  logger.success(f'Письмо для {username} успешно получено')
                  break
               else:
                  if i == 12:
                     logger.error(f'Письмо для {username} не получено')
                     raise Exception('email_timeout')
                  else:
                     sleep(30)
            for i in range(30):
               logger.info(f'Ожидание подтверждения для {username}')
               r = scraper.get(urlVerify).url
               if 'token=' in r:
                  token = r.split('=')[-1]
                  break
               elif i == 29:
                  raise Exception('token_timeout')

            for i in range(30):
               r = scraper.get('https://api.legionnetwork.io/api1/user/verify/link?token='+str(token)).text
               if r == '{"msg":"Verified"}':
                  logger.success(f'Аккаунт {username} подтвержден')
                  break
               elif i == 29:
                  raise Exception('token_timeout')
         else:
            raise Exception('wrong_code')
      except Exception as error:
         if str(error) == 'email_timeout':
            logger.error(f'Error: email timeout')
         elif str(error) == 'wrong_code':
            if 'used Cloudflare to restrict access' in str(r.text) or r.status_code == 504:
               logger.error('CloudFlare')
            else:
               logger.error(f'Error: wrong code - {str(r.status_code)}')
         elif str(error) == 'token_timeout':
            logger.error(f'Token timeout for {str(username)}')
         else:
            logger.error(f'Unexpected error: {str(error)}')
      else:
         with open('LegionAccounts.txt', 'a', encoding='utf-8') as file:
            file.write(f'{str(password)}!:{str(username)}@xojxe.com:{str(nameOfAcc)}:{udid}\n')
         logger.success(f'Аккаунт {username} успшено зарегистрирован')

def cleaner():
   while True:
      sleep(60)
      #clear()
      collect()

clear()
for _ in range(threads):
   Thread(target=mainth).start()

Thread(target=cleaner, daemon=True).start()
