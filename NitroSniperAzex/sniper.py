import asyncio
import json
import time
import traceback
from os import system
from random import randint
from discord.ext import commands
import re, requests
from colorama import Fore, init
import platform

init()
data = {}

with open('token.json') as f:
    data = json.load(f)
token = data['token']

os = platform.system()

if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")

print(Fore.RED + """\
 _   _ _ _                _____       _                 
| \ | (_) |              / ____|     (_)                
|  \| |_| |_ _ __ ___   | (___  _ __  _ _ __   ___ _ __ 
| . ` | | __| '__/ _ \   \___ \| '_ \| | '_ \ / _ \ '__|
| |\  | | |_| | | (_) |  ____) | | | | | |_) |  __/ |   
|_| \_|_|\__|_|  \___/  |_____/|_| |_|_| .__/ \___|_|   
                                       | |              
                                       |_|              
 """ + Fore.RESET)

print(Fore.BLUE + """\
 _____   __    _    _________  __
| _ ) \ / /   /_\  |_  / __\ \/ /
| _ \\ V /   / _ \  / /| _| >  < 
|___/ |_|   /_/ \_\/___|___/_/\_\
                                 
 """ + Fore.RESET)

bot = commands.Bot(command_prefix=".", self_bot=True)
ready = False

codeRegex = re.compile("(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")

while 1:
    try:
        @bot.event
        async def on_message(ctx):
            global ready
            if not ready:
                print(Fore.LIGHTCYAN_EX + 'Sniping Discord Nitro on ' + str(
                    len(bot.guilds)) + ' Servers 🔫\n' + Fore.RESET)
                print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                print("[+] Nitro Sniper is ready")
                ready = True
            if codeRegex.search(ctx.content):
                print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                code = codeRegex.search(ctx.content).group(2)

                start_time = time.time()
                if len(code) < 16:
                    try:
                        print(
                            Fore.LIGHTRED_EX + "[=] Auto-detected a fake code: " + code + " From " + ctx.author.name + "#" + ctx.author.discriminator + Fore.LIGHTMAGENTA_EX + " [" + ctx.guild.name + " > " + ctx.channel.name + "]" + Fore.RESET)
                    except:
                        print(
                            Fore.LIGHTRED_EX + "[=] Auto-detected a fake code: " + code + " From " + ctx.author.name + "#" + ctx.author.discriminator + Fore.RESET)

                else:
                    r = requests
                    result = r.post('https://discordapp.com/api/v6/entitlements/gift-codes/' + code + '/redeem',
                                    json={"channel_id": str(ctx.channel.id)}, headers={'authorization': token}).text
                    delay = (time.time() - start_time)
                    try:
                        print(
                            Fore.LIGHTGREEN_EX + "[-] Sniped code: " + Fore.LIGHTRED_EX + code + Fore.RESET + " From " + ctx.author.name + "#" + ctx.author.discriminator + Fore.LIGHTMAGENTA_EX + " [" + ctx.guild.name + " > " + ctx.channel.name + "]" + Fore.RESET)
                    except:
                        print(
                            Fore.LIGHTGREEN_EX + "[-] Sniped code: " + Fore.LIGHTRED_EX + code + Fore.RESET + " From " + ctx.author.name + "#" + ctx.author.discriminator + Fore.RESET)

                    if 'This gift has been redeemed already.' in result:
                        print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                        print(Fore.LIGHTYELLOW_EX + "[-] Code has been already redeemed" + Fore.RESET,
                              end='')
                    elif 'nitro' in result:
                        print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                        print(Fore.GREEN + "[+] Code applied" + Fore.RESET, end='')
                    elif 'Unknown Gift Code' in result:
                        print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                        print(Fore.LIGHTRED_EX + "[-] Invalid Code" + Fore.RESET, end=' ')
                    print(" Delay:" + Fore.GREEN + " %.3fs" % delay + Fore.RESET)

        bot.run(token, bot=False)
    except:
        file = open("traceback.txt", "w")
        file.write(traceback.format_exc())
        file.close()
        exit(0)
